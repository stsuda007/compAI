import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables for API keys
load_dotenv()

# Password protection function
def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        if not st.session_state["password_correct"]:
            st.error("😕 Password incorrect")
    return False

# API functions
def get_anthropic_response(prompt):
    try:
        headers = {
            "x-api-key": os.getenv("ANTHROPIC_API_KEY"),
            "content-type": "application/json"
        }
        data = {
            "model": "claude-3-opus-20240229",
            "max_tokens": 1000,
            "messages": [{"role": "user", "content": prompt}]
        }
        response = requests.post("https://api.anthropic.com/v1/messages", json=data, headers=headers)
        response.raise_for_status()
        return response.json()["content"][0]["text"]
    except Exception as e:
        return f"Error with Anthropic API: {str(e)}"

def get_openai_response(prompt):
    try:
        headers = {
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-4-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1000
        }
        response = requests.post("https://api.openai.com/v1/chat/completions", json=data, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error with OpenAI API: {str(e)}"

def get_finetuned_openai_response(prompt):
    try:
        headers = {
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
            "Content-Type": "application/json"
        }
        # Replace with your fine-tuned model ID
        data = {
            "model": os.getenv("FINETUNED_MODEL_ID"),
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1000
        }
        response = requests.post("https://api.openai.com/v1/chat/completions", json=data, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error with Fine-tuned OpenAI API: {str(e)}"

# Main app
def main():
    st.set_page_config(page_title="LLM Comparison Tool", layout="wide")
    
    st.title("LLM Comparison Tool")
    st.markdown("Compare responses from multiple language models side-by-side")
    
    # Create a text input for the user's prompt
    user_input = st.text_area("Enter your prompt:", height=150)
    
    # Create columns for the model responses
    col1, col2, col3 = st.columns(3)
    
    # Display loading spinners and responses when the user clicks the button
    if st.button("Generate Responses"):
        if user_input:
            with st.spinner("Generating responses..."):
                # Get responses from all three models
                anthropic_response = get_anthropic_response(user_input)
                openai_response = get_openai_response(user_input)
                finetuned_response = get_finetuned_openai_response(user_input)
                
                # Display the responses
                with col1:
                    st.subheader("Claude (Anthropic)")
                    st.markdown(anthropic_response)
                
                with col2:
                    st.subheader("GPT-4 (OpenAI)")
                    st.markdown(openai_response)
                
                with col3:
                    st.subheader("Fine-tuned OpenAI")
                    st.markdown(finetuned_response)

# Create secrets.toml file content guide
secrets_guide = """
Create a file named .streamlit/secrets.toml with:

password = "your_password_here"
"""

# Run the app with password protection
if __name__ == "__main__":
    # Check password first
    if check_password():
        main()
    else:
        st.info("Please enter the password to access the application.")
        st.markdown("*Note: This is a basic password protection. For production use, implement proper authentication.*")
