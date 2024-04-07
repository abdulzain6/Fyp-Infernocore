import firebase_admin
from firebase_admin import credentials, auth
import requests


cred = credentials.Certificate("/home/zain/Pictures/prj2/api/creds/infernocore-6721c-firebase-adminsdk-a4ti8-9dc65a5445.json")
firebase_admin.initialize_app(cred)

def login_with_email_and_password(email: str, password: str, api_key: str) -> str:
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"

    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        id_token = response.json().get("idToken")
        print("Login successful!")
        return id_token
    else:
        print("Login error:", response.json().get("error"))
        return None
    
def register_user(email, password):
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        print("User registered successfully!")
        return user
    except Exception as e:
        print("Registration error:", e)
        return None



email = "test@gmail.com"
password = "testpassword"

register_user(email, password)

if id_token := login_with_email_and_password(email, password, "AIzaSyDaDbc2I_1n2dwcm1qxtqfilq2IjFhhGok"):
    print("ID Token:", id_token)