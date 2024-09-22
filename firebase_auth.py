import firebase_admin
from firebase_admin import credentials, auth, db
import streamlit as st
import os
from dotenv import load_dotenv
import datetime
import json

load_dotenv()

def get_firebase_credentials():

    creds = {
            "type": "service_account",
            "project_id": os.getenv("FIREBASE_PROJECT_ID"),
            "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
            "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace('\\n', '\n'),
            "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
            "client_id": os.getenv("FIREBASE_CLIENT_ID"),
            "auth_uri": os.getenv("FIREBASE_AUTH_URI"),
            "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
            "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_X509_CERT_URL"),
            "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL"),
            "database_url": os.getenv("FIREBASE_DATABASE_URL")
            
        }
    
    
    return creds

# Initialize Firebase only if it hasn't been initialized yet
if not firebase_admin._apps:
    firebase_cred = get_firebase_credentials()
    cred = credentials.Certificate(firebase_cred)

    firebase_admin.initialize_app(cred, {
        'databaseURL': os.getenv("FIREBASE_DATABASE_URL")
    })

def login():
    st.title("Login")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")
    
    if st.button("Login", key="login_button"):
        try:
            user = auth.get_user_by_email(email)
            user_data = db.reference(f'users/{user.uid}/info').get()
            if user_data:
                st.session_state.user_data = user_data
                st.success("Logged in successfully!")
                log_to_firebase(user.uid, email, "success")
                return True
            else:
                st.error("User data not found")
        except auth.UserNotFoundError:
            st.error("Invalid email or password")
            # log_to_firebase(None, email, "failure", "Invalid email or password")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            # log_to_firebase(None, email, "failure", str(e))
    return False

def signup():
    st.title("Sign Up")
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_password")
    department = st.text_input("Department", key="signup_department")
    interests = st.text_input("Interests (comma-separated)", key="signup_interests")
    skills = st.text_input("Skills (comma-separated)", key="signup_skills")
    
    if st.button("Sign Up", key="signup_button"):
        try:
            user = auth.create_user(
                email=email,
                password=password
            )

            user_data = {
                "department": department,
                "interests": interests.split(','),
                "skills": skills.split(','),
                "uid": user.uid
            }
            db.reference(f'users/{user.uid}/info').set(user_data)
            st.session_state.user_data = user_data
            st.success("Account created successfully!")
            return True
        except auth.EmailAlreadyExistsError:
            st.error("Email already exists")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    return False

def log_to_firebase(uid, email, status, error_message=None):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H%M%S")
    log_data = {
        "email": email,
        "status": status,
        "error_message": error_message,
        "timestamp": timestamp
    }
    db.reference(f'users/{uid}/log/{timestamp}').set(log_data)





def data_to_firebase(question, response, title):
    if 'user_data' in st.session_state and st.session_state['user_data']:
        user_data = st.session_state['user_data']
        timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H%M%S")
        log_data = {
            "question": question,
            "response": response,
            "title": title
        }

        if 'uid' in user_data:
            uid = user_data['uid']
            db.reference(f'users/{uid}/chat/{timestamp}').set(log_data)
            st.success("Data logged successfully.")
        else:
            st.warning("User ID not found. Data not logged.")
    else:
        st.warning("User not logged in. Data not logged.")

def get_conversation_titles():
    if 'user_data' in st.session_state and st.session_state['user_data']:
        user_data = st.session_state['user_data']
        uid = user_data['uid']
        user_chat = db.reference(f'users/{uid}/chat').get()
        
        if user_chat:
            titles = [entry.get('title', 'Untitled') for entry in user_chat.values()]
            return list(set(titles))
        
    return []


def get_recent_questions():
    if 'user_data' in st.session_state and st.session_state['user_data']:
        user_data = st.session_state['user_data']
        uid = user_data['uid']
        user_chat = db.reference(f'users/{uid}/chat').get()
        
        if user_chat:
            questions = [entry.get('question', '') for entry in user_chat.values()]
            return questions[-10:] 
        
    return []

def convert_chat_log(log_content):
    
    # data = json.loads(log_content)

    result = [
        {
            "question": entry["question"],
            "response": entry["response"]
        }
        for entry in log_content.values()
    ]
    
    return result


def get_conversation_data(uid):
    user_chat = db.reference(f'users/{uid}/chat').get()
    if user_chat:
        conversations = {}
        for timestamp, data in user_chat.items():
            title = data.get('title', 'Untitled')
            if title not in conversations:
                conversations[title] = []
            conversations[title].append({
                "role": "user",
                "content": data.get('question', '')
            })
            conversations[title].append({
                "role": "assistant",
                "content": data.get('response', '')
            })
        return conversations
    return {}

def logout():
    if st.sidebar.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.success("Logged out successfully!")
        st.rerun()


