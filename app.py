import os
import gradio as gr
from groq import Groq

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

demo.launch()
