from App.models import StudentRecord
from App.database import db

def get_all_records():
    records = StudentRecord.getRecords()
    if not records:
        return {"error": "No records found."}
    return records