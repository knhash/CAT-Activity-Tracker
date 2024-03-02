# data.py
import pandas as pd
from datetime import datetime

DATA_PATH = "dataset"
LEDGER_FILE = DATA_PATH+"/csvs/ledger.csv"
SCHEDULE_FILE = DATA_PATH+"/csvs/schedules.csv"
CABINET_FILE = DATA_PATH+"/csvs/cabinet.csv"

####################### Ledger #######################

def load_ledger_data():
    try:
        ledger_data = pd.read_csv(LEDGER_FILE)
        ledger_data.Date = pd.to_datetime(ledger_data.Date).dt.date
        # Remove the comma in the amount column
        ledger_data.Amount = ledger_data.Amount.str.replace(",", "")
        ledger_data.Amount = pd.to_numeric(ledger_data.Amount)
        ledger_data = ledger_data.sort_values(by="Date", ascending=False)
        return ledger_data
    except FileNotFoundError:
        return pd.DataFrame(columns=["Description", "Category", "Amount", "Date"])

def save_ledger_data(data):
    data.to_csv(LEDGER_FILE, index=False)

####################### Schedules #######################

def load_schedule_data():
    try:
        schedules = pd.read_csv(SCHEDULE_FILE)
        schedules["Date"] = pd.to_datetime(schedules["Date"]).dt.date
        schedules = schedules.sort_values(by="Date", ascending=True)
        return schedules
    except FileNotFoundError:
        return pd.DataFrame(columns=["Date", "Description", "Active"])
    except Exception as e:
        print(e)
        return pd.DataFrame(columns=["Date", "Description", "Active"])

def save_schedule_data(data):
    data.to_csv(SCHEDULE_FILE, index=False)

####################### Cabinet #######################
    
def load_cabinet_data():
    try:
        cabinet = pd.read_csv(CABINET_FILE)
        return cabinet
    except FileNotFoundError:
        return pd.DataFrame(columns=["Item", "Purpose", "Available"])
    except Exception as e:
        print(e)
        return pd.DataFrame(columns=["Item", "Purpose", "Available"])

def save_cabinet_data(data):
    data.to_csv(CABINET_FILE, index=False)


####################### Utilities #######################

def format_indian(number):
    number = str(number).split(".")[0]
    try:
        decimal = str(number).split(".")[1]
    except:
        decimal = "00"
    if len(number) <= 3:
        return number
    else:
        last_three = number[-3:]
        other_numbers = number[:-3]
        formatted = ','.join(other_numbers[i:i+2] for i in range(0, len(other_numbers), 2))
        return f'{formatted},{last_three}.{decimal}'
