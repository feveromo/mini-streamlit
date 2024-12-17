import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set page config
st.set_page_config(
    page_title="Chat with mini",
    page_icon="💭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Define callback function
def clear_chat():
    st.session_state.messages = []

# Simple header with controls
col1, col2 = st.columns([7, 1])
with col1:
    st.title("Chat with mini")
with col2:
    st.button("clear chat", type="secondary", on_click=clear_chat)

# Chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Get user input
if prompt := st.chat_input("What's on your mind?"):
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
- maintain your dry humor while going into detail
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
                temperature=0.7,
                max_tokens=3192,
                top_p=1.0,
                frequency_penalty=0.35,
                presence_penalty=0.40,
                response_format={"type": "text"}
            )

            assistant_response = response.choices[0].message.content.lower()
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            
            with st.chat_message("assistant"):
                st.write(assistant_response)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}") 