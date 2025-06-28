import firebase_admin
from firebase_admin import credentials, auth
from firebase_admin import firestore
from fastapi import HTTPException
import os
from dotenv import load_dotenv

load_dotenv()

FIREBASE_KEY_PATH = os.getenv("FIREBASE_KEY_PATH", "firebase_service_account.json")

if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_KEY_PATH)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def verify_firebase_token(token: str):
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid authentication token")

def store_user_result(user_id: str, result: dict):
    doc_ref = db.collection("results").document(user_id)
    doc_ref.set(result)
    return True

def store_user_feedback(user_id: str, feedback: str):
    doc_ref = db.collection("feedback").document(user_id)
    doc_ref.set({"feedback": feedback})
    return True 