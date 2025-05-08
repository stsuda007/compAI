import streamlit as st
import requests
import os

# Configure API keys
# For local development, you can set these as environment variables before running the app
# For deployment, you'll configure these in the platform (Streamlit Cloud, AWS, etc.)
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
FINETUNED_MODEL_ID = os.getenv("FINETUNED_MODEL_ID", "")

# Alternative: For local development only (not recommended for production)
# Uncomment and set these directly if needed (but don't commit with real keys!)
# ANTHROPIC_API_KEY = "your_anthropic_key_here"
# OPENAI_API_KEY = "your_openai_key_here"
# FINETUNED_MODEL_ID = "your_finetuned_model_id_here"

# Password protection function
def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        # Get password from Streamlit secrets or use a fallback for local development
        correct_password = st.secrets.get("password", "default_password_change_me")
        
        if st.session_state["password"] == correct_password:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state
