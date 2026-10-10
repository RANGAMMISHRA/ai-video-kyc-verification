Video KYC Project-AI

A full-stack Video KYC (Know Your Customer) system that enables secure, real-time identity verification using document OCR, face matching, liveness detection, and AI-powered speech transcription.
Features

    Verifier Login — Org-code + employee-code + password authentication with OTP-based password reset
    Customer OTP Verification — OTP sent via SMS (Fast2SMS) and Email (Gmail SMTP)
    Document OCR — Extracts Aadhaar and PAN fields using Tesseract OCR
    Face Match & Liveness — Compares document photo to live KYC video; detects blinks and smiles using dlib + face_recognition
    Re-KYC Check — Looks up existing KYC records and enforces expiry based on risk category (Low/Medium/High)
    Speech Transcription — Uploads KYC audio to AWS S3 and transcribes using AWS Transcribe
    LLM Answer Extraction — Uses OpenAI GPT to extract structured Q&A answers from transcript
    Customer Profiler — Generates a Word document (.docx) profiler using LLM-generated overview
    PDF Report — Generates a one-page KYC verification report
    Email Report — Sends the PDF report to the customer via Gmail
    Audit Logging — Saves all KYC sessions to CSV logs and SQLite (kyc_records + kyc_history tables)
    Admin Dashboard — View, filter, and download KYC logs and Q&A data

Tech Stack
Layer 	Technology
Frontend 	Python, Streamlit
Backend 	Python, Flask, Flask-CORS
OCR 	Tesseract, OpenCV
Face & Liveness 	face_recognition, dlib, OpenCV
Speech-to-Text 	AWS Transcribe, AWS S3
LLM 	OpenAI GPT (transcript parsing, profiler)
Auth 	bcrypt (password hashing), OTP via Fast2SMS + Gmail
Storage 	SQLite, CSV, local filesystem
Document Generation 	python-docx (profiler), fpdf (PDF report)
Project Structure

video-kyc-project/
├── backend/
│   ├── app.py                     # Flask entry point
│   ├── verify_api.py              # KYC upload, verify, finalize endpoints
│   ├── log_api.py                 # Log save/fetch endpoints
│   ├── ocr_api.py                 # Standalone OCR endpoint
│   ├── report_api.py              # PDF report generation endpoint
│   ├── parse_transcript.py        # LLM-based Q&A extraction from transcript
│   ├── database/
│   │   ├── kyc_records.db         # KYC records + history (gitignored)
│   │   └── verifier_system.db     # Verifier/org authentication DB (gitignored)
│   └── utils/
│       ├── verification_utils.py  # Face match + liveness detection
│       ├── ocr_utils.py           # Tesseract OCR extraction
│       ├── db_utils.py            # SQLite helpers (save/get KYC records & history)
│       ├── log_utils.py           # CSV log helpers
│       ├── report_utils.py        # PDF report generation (fpdf)
│       ├── profiler_utils.py      # Word doc profiler generation (python-docx)
│       ├── audio_extraction.py    # Extract audio from video (ffmpeg/moviepy)
│       ├── aws_transcribe_utils.py# AWS S3 upload + Transcribe job
│       ├── sms_utils.py           # Fast2SMS OTP sender
│       └── add_employees.py       # Script to seed employee data
│
├── frontend/
│   ├── app.py                     # Main Streamlit KYC app (customer + verifier flow)
│   ├── app_admin.py               # Admin Streamlit app (same flow, standalone entry)
│   ├── api_client.py              # HTTP client for backend API calls
│   └── utils/
│       └── helper.py              # Validation and formatting utilities
│
├── assets/
│   └── shape_predictor_68_face_landmarks.dat   # dlib model (download separately — see below)
│
├── app_verifier.py                # Verifier auth logic (login, OTP, password reset)
├── verifier_db.py                 # Script to initialize verifier/org database
├── verifier_manage_ui.py          # Streamlit UI to manage verifier records
├── verifier_organisation_ui_db.py # Streamlit UI to manage org records + download templates
├── verifier_admin_portal.py       # Streamlit admin portal (combined verifier management)
│
├── .env.example                   # Environment variable template
├── requirements.txt
└── README.md

Prerequisites
1. Python Environment

Recommended: Anaconda with Python 3.10+

conda create -n vkycenv python=3.10
conda activate vkycenv
pip install -r requirements.txt

    If dlib or face_recognition fails to install (common on Windows), install dlib through conda first, then retry:

    conda install -c conda-forge dlib
    pip install face_recognition

2. Download the dlib Face Landmark Model

The face liveness detection requires a 96 MB model file that is not included in the repository.

Download shape_predictor_68_face_landmarks.dat from the official dlib repository and place it in the assets/ folder:

assets/shape_predictor_68_face_landmarks.dat

    Download link: http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
    Extract with: bunzip2 shape_predictor_68_face_landmarks.dat.bz2 (Linux/Mac) or 7-Zip / WinRAR (Windows)

The backend will not start if this file is missing.
3. Install Tesseract OCR

    Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki and add to PATH
    Linux/Mac: sudo apt install tesseract-ocr / brew install tesseract

4. Install ffmpeg

Required for audio extraction from KYC video.

    Windows: Download from https://ffmpeg.org/download.html and add bin/ to PATH
    Linux/Mac: sudo apt install ffmpeg / brew install ffmpeg

Setup
1. Configure Environment Variables

Copy .env.example to .env and fill in your values:

cp .env.example .env

BACKEND_PORT=5000

AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key

OPENAI_API_KEY=your_openai_api_key

FAST2SMS_API_KEY=your_fast2sms_api_key

GMAIL_USER=your_gmail@gmail.com
GMAIL_APP_PASSWORD=your_gmail_app_password

    For Gmail, use an App Password (not your account password). Enable 2FA on your Google account, then generate one at: Google Account → Security → App Passwords.

2. Initialize the Verifier Database

Run this once to create the verifier_system.db with the organizations and employees tables:

python verifier_db.py

To add verifiers and organizations via UI:

streamlit run verifier_admin_portal.py

3. Set Up AWS (S3 + Transcribe)

Speech transcription needs an S3 bucket and an IAM user with least-privilege access (upload/read to one bucket, start/check Transcribe jobs only — nothing else).

See docs/AWS_SETUP.md for step-by-step bucket creation, the IAM policy, and commands to test the setup.
Running the App
Start the Backend (Flask API)

cd backend
python app.py

Backend runs at http://localhost:5000
Start the Frontend (Streamlit)

In a separate terminal:

cd frontend
streamlit run app.py

Frontend runs at http://localhost:8501

    Both backend and frontend must be running simultaneously for the app to work.

API Endpoints

All backend routes are prefixed as shown below:
Method 	Endpoint 	Description
POST 	/verify/upload_files 	Upload Aadhaar, PAN, and KYC video
POST 	/verify/verify_kyc 	Run OCR + face match + liveness
POST 	/verify/finalize_kyc 	Save KYC decision, generate PDF, log to DB
GET 	/verify/download_report/<kyc_id> 	Download PDF report
POST 	/verify/check_existing_kyc 	Check if KYC exists and validity
POST 	/verify/simulate_otp 	Simulate OTP (for testing)
GET 	/verify/download_kyc_log_csv 	Download KYC log as CSV
GET 	/verify/download_kyc_log_xlsx 	Download KYC log as Excel
POST 	/log/save 	Save a KYC log entry
GET 	/log/all 	Get all KYC log entries
POST 	/ocr/extract 	Extract fields from uploaded image
POST 	/report/generate 	Generate PDF report from KYC data
KYC Workflow

Customer Approaches
        ↓
Verifier Login (Org Code + Employee Code + Password)
        ↓
Enter Customer Details (Name, Aadhaar, PAN, Mobile, Email)
        ↓
Send OTP to Customer → Verify OTP
        ↓
Check Existing KYC (risk category, expiry)
        ↓
Upload / Capture Aadhaar + PAN + KYC Video
        ↓
OCR Extraction → Validate against input
        ↓
Face Match (document photo vs video) + Liveness (blinks, smile)
        ↓
Speech Transcription (AWS Transcribe) → LLM Q&A Extraction
        ↓
Verifier Reviews Results → Approve or Reject
        ↓
Generate PDF Report + Customer Profiler (.docx)
        ↓
Email Report to Customer + Save to DB + Audit Log

Risk-Based KYC Expiry
Risk Category 	KYC Valid For
Low 	365 days
Medium 	180 days
High 	90 days
Data Storage
Data 	Location
KYC records (latest per customer) 	backend/database/kyc_records.db → kyc_records table
Full KYC history (every session) 	backend/database/kyc_records.db → kyc_history table
Verifier / org authentication 	backend/database/verifier_system.db
KYC session log 	frontend/uploads/logs/kyc_log.csv
Q&A log 	frontend/uploads/logs/kyc_qa.csv
Integrated log 	frontend/uploads/logs/kyc_integrated.csv
PDF reports 	frontend/uploads/reports/
Customer profilers 	frontend/uploads/profilers/
KYC documents 	backend/uploads/kyc_docs/
KYC videos 	backend/uploads/videos/

    All upload folders, databases, and logs are gitignored to protect customer PII.

Verifier Management
Script 	Purpose
verifier_db.py 	Initialize verifier/org SQLite database
verifier_manage_ui.py 	Streamlit UI to add/edit verifier records
verifier_organisation_ui_db.py 	Streamlit UI to manage orgs + download templates
verifier_admin_portal.py 	Combined Streamlit admin portal
Troubleshooting
Problem 	Fix
Port 5000 or 8501 already in use (Windows) 	netstat -ano | findstr :8501 then taskkill /PID <PID> /F
Backend fails at startup with a dlib error 	Check that assets/shape_predictor_68_face_landmarks.dat exists
dlib / face_recognition install fails 	conda install -c conda-forge dlib, then pip install face_recognition
UnicodeEncodeError on Windows 	Run set PYTHONIOENCODING=utf-8 before starting the app
tesseract or ffmpeg not found 	Make sure each tool's install folder is added to your PATH, then restart the terminal
AWS Transcribe returns poor results 	Convert audio to mono, 16 kHz WAV: ffmpeg -i input.mp3 -ac 1 -ar 16000 output.wav
License

MIT License
Contributing

Pull requests and issues are welcome!