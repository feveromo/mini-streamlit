# Chat with Mini

A streamlit app that uses a fine-tuned GPT model to engage in casual, thoughtful conversations.

## Setup

1. Clone this repository
2. Install the required packages:
   ```bash
   pip install streamlit openai
   ```

3. Set up environment:
   - Create a `.streamlit/secrets.toml` file
   - Add OpenAI API key:
     ```toml
     OPENAI_API_KEY = "api-key-here"
     ```

## Running the App

Launch the application with: 
```bash
streamlit run app.py
```