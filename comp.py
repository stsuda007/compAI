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
        if not ANTHROPIC_API_KEY:
            return "Error: Anthropic API key not configured"
            
        headers = {
            "x-api-key": ANTHROPIC_API_KEY,
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
        if not OPENAI_API_KEY:
            return "Error: OpenAI API key not configured"
            
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
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
        if not OPENAI_API_KEY or not FINETUNED_MODEL_ID:
            return "Error: OpenAI API key or fine-tuned model ID not configured"
            
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": FINETUNED_MODEL_ID,
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

# Run the app with password protection
if __name__ == "__main__":
    # For Streamlit Cloud, uncomment this to use secrets:
    # if not st.secrets.get("password"):
    #     st.error("Password not configured in secrets")
    #     st.stop()
    
    # Check password first
    if check_password():
        main()
    else:
        st.info("Please enter the password to access the application.")
        st.markdown("*Note: This is a basic password protection. For production use, implement proper authentication.*")
