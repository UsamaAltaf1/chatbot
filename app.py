import os
import gradio as gr
from flask import Flask, request
from groq import Groq

# Initialize Flask app
app = Flask(__name__)

# Secure API key access
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Chatbot function with memory
def chat_with_bot(message, history):
    # Convert chat history to the required format
    messages = [{"role": "system", "content": "You are a helpful AI assistant."}]
    
    for user_msg, bot_msg in history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": bot_msg})

    # Add latest user input
    messages.append({"role": "user", "content": message})

    # Get response from Groq LLM API
    response = client.chat.completions.create(
        messages=messages, model="llama-3.3-70b-versatile"
    )

    bot_reply = response.choices[0].message.content

    return bot_reply

# Create Gradio UI with chat history
with gr.Blocks(theme="soft") as demo:
    gr.Markdown("<h1 style='text-align: center; color: #4A90E2;'>💬 Smart AI Chatbot</h1>")
    gr.Markdown("<p style='text-align: center;'>Talk to the AI about anything!</p>")

    chat_interface = gr.ChatInterface(chat_with_bot, chatbot=gr.Chatbot(height=400))

# Define a route for Flask to serve Gradio
@app.route("/")
def index():
    return demo.launch(share=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
