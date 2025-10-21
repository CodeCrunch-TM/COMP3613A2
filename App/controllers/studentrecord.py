from models import StudentRecord
from App.database import db

def get_all_records():
    records = StudentRecord.getRecords()
    if not records:
        return {"error": "No records found."}
    return [record.to_json() for record in records] # supposed to make the records easier to read - convert back to str(record) if needed