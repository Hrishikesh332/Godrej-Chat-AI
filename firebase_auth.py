import firebase_admin
from firebase_admin import credentials, auth, db
import streamlit as st
import os
from dotenv import load_dotenv

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

            user_data = db.reference(f'users/{user.uid}').get()
            if user_data:
                st.session_state.user_data = user_data
                st.success("Logged in successfully!")
                return True
            else:
                st.error("User data not found")
        except auth.UserNotFoundError:
            st.error("Invalid email or password")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
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
                "skills": skills.split(',')
            }
            db.reference(f'users/{user.uid}').set(user_data)
            st.session_state.user_data = user_data
            st.success("Account created successfully!")
            return True
        except auth.EmailAlreadyExistsError:
            st.error("Email already exists")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    return False

def logout():
    if st.sidebar.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.success("Logged out successfully!")
        st.rerun()