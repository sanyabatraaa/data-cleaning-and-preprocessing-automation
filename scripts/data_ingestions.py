import os
import pandas as pd
import requests
from sqlalchemy import create_engine

DATA_DIR= os.path.join(os.path.dirname(os.path.abspath(__file__)),"../data")

class DataIngestion:
    def __init__(self,db_url=None):
        self.engine = create_engine(db_url) if db_url else None

    def load_csv(self,file_name):
        file_path = os.path.join(DATA_DIR,file_name)
        try:
            df = pd.read_csv(file_path)
            print(f"CSV loaded successfully{file_path}" )
            return df
        except Exception as e:
            print("error")
            return None
        
    def load_excel(self, file_name):
        file_path = os.path.join(DATA_DIR, file_name)
        try:
            df = pd.read_excel(file_path)
            print(f"Excel file loaded successfully: {file_path}")
            return df
        except Exception as e:
            print(f"Error loading Excel file: {e}")
            return None

    def connect_database(self,db_url):
        try:
            self.engine = create_engine(db_url)
            print("DB connection successful")
        except Exception as e:
            print("Error connecting to db")

    def load_database(self, query):
        if self.engine is None:
            print("Database connection not established.")
            return None
        try:
            df = pd.read_sql(query, self.engine)
            print("Data loaded from database successfully.")
            return df
        except Exception as e:
            print(f"Error loading data from database: {e}")
            return None

    def fetch_from_api(self,api_url,params=None):
        try:
            response = requests.get(api_url,params=params)
            if response.status_code==200:
                data = response.json()
                df= pd.DataFrame(data)
                print("Data fetched from API successfully")
                return df
            else:
                print(f"API request failed {response.status_code}")
                return None
        except Exception as e:
            print("Error fetching data from api")
            return None