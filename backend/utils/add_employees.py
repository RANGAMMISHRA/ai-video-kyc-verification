# add_employees.py
# Adds sample verifiers to the verifier system database with hashed passwords.
import sqlite3
from pathlib import Path
import bcrypt

DB_PATH = Path(__file__).resolve().parents[1] / "database" / "verifier_system.db"

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

# Sample employees (dummy data, default password: "password")
new_employees = [
    {
        "emp_code": "EMP003",
        "password": "password",
        "verifier_name": "RAJESH KUMAR",
        "org_code": "BANK001",
        "department": "Verification",
        "designation": "KYC Officer",
        "mobile": "9000000001",
        "email": "employee1@example.com",
    },
    {
        "emp_code": "EMP004",
        "password": "password",
        "verifier_name": "abhishek kumar",
        "org_code": "BANK001",
        "department": "Verification",
        "designation": "Verifier",
        "mobile": "9000000002",
        "email": "employee2@example.com",
    },
]

with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.cursor()
    for emp in new_employees:
        cursor.execute("""
            INSERT OR IGNORE INTO employees (
                emp_code, password_hash, verifier_name, org_code,
                department, designation, mobile, email
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            emp["emp_code"], hash_password(emp["password"]), emp["verifier_name"],
            emp["org_code"], emp["department"], emp["designation"],
            emp["mobile"], emp["email"],
        ))
    conn.commit()
    print("✅ New employees added successfully!")