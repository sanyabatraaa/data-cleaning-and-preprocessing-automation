import os
import pandas as pd
from dotenv import load_dotenv
import google.generativeai as genai
from langgraph.graph import StateGraph, END
from pydantic import BaseModel
import logging
logging.basicConfig(level=logging.DEBUG)

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("Gemini API key is missing. Set it in environment variables.")

genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel("gemini-1.5-pro-latest")

class CleaningState(BaseModel):
    input_text: str
    structured_response: str = ""

class AIAgent:
    def __init__(self):
        self.graph = self.create_graph()

    def create_graph(self):
        graph = StateGraph(CleaningState)

        def agent_logic(state: CleaningState) -> CleaningState:
            response = model.generate_content(state.input_text)
            logging.debug(f"Response from model: {response}")
            reply = response.text.strip()
            return CleaningState(input_text=state.input_text, structured_response=reply)

        graph.add_node("cleaning_agent", agent_logic)
        graph.set_entry_point("cleaning_agent")
        graph.set_finish_point("cleaning_agent")
        return graph.compile()

    def process_data(self, df, batch_size=20):
        cleaned_csv_responses = []
        for i in range(0, len(df), batch_size):
            df_batch = df.iloc[i:i + batch_size]

            prompt = f"""
You are a data cleaning assistant.

Clean the following data:
{df_batch.to_csv(index=False)}

Steps to follow:
1. Handle missing values using mean (numerical), mode (categorical).
2. Remove duplicate rows.
3. Fix data types and capitalize text fields.
4. Return ONLY the cleaned data as a valid CSV — no markdown, no explanations, no triple backticks.
"""

            state = CleaningState(input_text=prompt)
            response = self.graph.invoke(state)
            if isinstance(response, dict):
                response = CleaningState(**response)
            cleaned_csv_responses.append(response.structured_response.strip())

        final_csv = "\n".join(cleaned_csv_responses)
        return final_csv  # return raw CSV text
