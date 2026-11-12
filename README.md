
# AI-Powered Resume Parser & Multi-Channel 2FA Onboarding Pipeline

## Project Overview
A FastAPI-based application that extracts information from PDF and DOCX resumes and provides secure user registration with multi-channel two-factor authentication (2FA).

## Features
- Upload and parse PDF and DOCX resumes.
- Extract name, email, phone number, and skills.
- Store resume information in PostgreSQL.
- Register users with Pydantic validation.
- Secure password hashing using Argon2.
- Generate and verify email OTPs.
- WhatsApp OTP integration through Twilio.
- Browser-based TOTP authentication.
- Store OTPs as hashes with expiry.
- Generate JWT access tokens after verification.
- View and update user profiles.
- Access a protected dashboard.

## Technologies Used
- Python
- FastAPI
- PostgreSQL
- SQLAlchemy (Async)
- Pydantic
- PyJWT
- Argon2
- PyOTP
- Twilio API
- pdfplumber
- python-docx

## Project Structure
```text
AI-Resume-Parser-2FA/
├── app/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── config.py
│   ├── database.py
│   └── main.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:
   ```bash
   git clone YOUR_GITHUB_REPOSITORY_URL
   ```

2. Navigate into the project:
   ```bash
   cd AI-Resume-Parser-2FA
   ```

3. Create a virtual environment:
   ```bash
   py -m venv venv
   ```

4. Activate the virtual environment:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

6. Create a `.env` file with your PostgreSQL database URL and secure secret key. Configure SMTP and Twilio settings if using real email and WhatsApp delivery. Never commit this file.

7. Start the application:
   ```bash
   py -m uvicorn app.main:app --reload
   ```

## API Documentation
Open the interactive API documentation:

http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/v1/resume/parse` | Parse uploaded resumes |
| POST | `/api/v1/auth/register` | Register users |
| POST | `/api/v1/auth/send-otp` | Generate email OTP |
| POST | `/api/v1/auth/send-whatsapp-otp` | Generate WhatsApp OTP |
| POST | `/api/v1/auth/verify-2fa` | Verify email or WhatsApp OTP |
| POST | `/api/v1/auth/totp/setup/{user_id}` | Set up browser TOTP |
| POST | `/api/v1/auth/totp/verify` | Verify browser TOTP |
| GET | `/api/v1/profile/` | View profile |
| PATCH | `/api/v1/profile/` | Update profile |
| GET | `/api/v1/dashboard/student` | Access protected dashboard |

## Implementation Notes
- Email and WhatsApp OTP endpoints support development mode when provider credentials are not configured.
- Real email delivery requires SMTP configuration.
- Real WhatsApp delivery requires valid Twilio credentials and WhatsApp sender configuration.
- Browser TOTP setup and verification endpoints are implemented.
- Resume extraction currently uses rule-based parsing.

## Security
- Passwords are hashed using Argon2.
- OTP values are stored as hashes with expiry.
- JWT authentication protects profile and dashboard endpoints.
- Environment secrets are excluded from Git using `.gitignore`.

## Author
Likitha
