import streamlit as st
from openai import OpenAI
import time

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set page config
st.set_page_config(
    page_title="Chat with mini",
    page_icon="💭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stTextInput>div>div>input {
        background-color: #f0f2f6;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar
with st.sidebar:
    st.title("Settings")
    temperature = st.slider("Temperature", min_value=0.1, max_value=1.0, value=0.80, step=0.1)
    max_tokens = st.slider("Max Tokens", min_value=50, max_value=4000, value=3192, step=50)
    theme = st.selectbox("Theme", ["Light", "Dark"])
    if theme == "Dark":
        st.markdown("""
        <style>
        .stApp {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        </style>
        """, unsafe_allow_html=True)

# Define callback functions
def clear_chat():
    st.session_state.messages = []

def save_chat():
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    st.session_state.chat_history.append((timestamp, st.session_state.messages))
    st.success(f"Chat saved at {timestamp}")

# Header with controls
col1, col2, col3 = st.columns([5, 1, 1])
with col1:
    st.title("Chat with mini")
with col2:
    st.button("Clear Chat", type="secondary", on_click=clear_chat)
with col3:
    st.button("Save Chat", type="primary", on_click=save_chat)

# Chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Get user input
prompt = st.chat_input("What's on your mind?")

if prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)

    # Show spinner while generating response
    with st.spinner("thinking..."):
        try:
            response = client.chat.completions.create(
                model="ft:gpt-4o-mini-2024-07-18:tradevf:twitter-me:AYW7WRY1",
                messages=[{
                    "role": "system",
                    "content": """you're a casual, thoughtful poster who engages in longer-form conversation while keeping it natural. you should:
- use all lowercase
- share deeper thoughts on learning/growth/tech
- maintain your humor while going into detail
- treat short questions as openings for broader thoughts
- draw connections between topics
- feel free to express complex ideas in simple terms

tone guideline:
- keep it conversational and genuine
- don't overdo the casualness - it should feel natural
- mix thoughtful observations with humor
- when discussing tech/gaming, be knowledgeable but approachable
- comfortable showing vulnerability while maintaining self-awareness

avoid:
- forced slang
- excessive emojis
- overly formal language
- pretentious takes on topics

remember to always write in lowercase and maintain a natural, conversational flow. treat each interaction as a chance to share interesting perspectives while staying relatable."""
                }] + st.session_state.messages,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=1.0,
                frequency_penalty=0.10,
                presence_penalty=0.10,
                response_format={"type": "text"}
            )

            assistant_response = response.choices[0].message.content.lower()
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            
            with st.chat_message("assistant"):
                st.write(assistant_response)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Display chat history
if st.session_state.chat_history:
    st.subheader("Chat History")
    for timestamp, chat in st.session_state.chat_history:
        if st.button(f"Load chat from {timestamp}"):
            st.session_state.messages = chat
            st.experimental_rerun()

