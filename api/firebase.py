import os
import firebase_admin

current_directory = os.path.dirname(os.path.abspath(__file__))
credentials_path = os.path.join(current_directory, 'creds', 'infernocore-6721c-firebase-adminsdk-a4ti8-9dc65a5445.json')

if not os.path.exists(credentials_path):
    raise FileNotFoundError(f"Credentials file not found at {credentials_path}")

cred = firebase_admin.credentials.Certificate(credentials_path)
default_app = firebase_admin.initialize_app(cred)