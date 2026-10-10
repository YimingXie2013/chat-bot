import re
import urllib.parse
from groq import Groq
import streamlit as st

# Safe API key loading from Streamlit Secrets
try:
  api_key = st.secrets["GROQ_API_KEY"]
except Exception:
  api_key = ""

if not api_key:
  st.error(
      "⚠️ Bitte trage deinen GROQ_API_KEY in den Streamlit Secrets (unter"
      " Settings > Secrets) ein."
  )

# Page configuration
st.set_page_config(
    page_title="Llama AI Assistant", page_icon="✨", layout="centered"
)

st.title("✨ Llama AI Chat & Image Assistant (Groq)")
st.markdown(
    "Chatte ultraschnell mit der KI oder lass dir direkt Bilder im Chat"
    " generieren!"
)

# Initialize chat history
if "messages" not in st.session_state:
  st.session_state.messages = []

# System instruction
system_prompt = (
    "You are a helpful, multilingual AI assistant powered by Groq. When the user"
    " asks to draw, create, or generate an image, you must include a special tag"
    " in your response formatted strictly as: [IMAGE: detailed english"
    " description of the image]. Keep your conversational text brief when an"
    " image is requested."
)


def render_message(msg):
  """Renders user and assistant messages, including image generation."""
  with st.chat_message(msg["role"]):
    text = msg["content"]
    image_url = msg.get("image_url")
    image_prompt = msg.get("image_prompt")

    if text:
      st.markdown(text)

    if image_url:
      st.image(image_url, caption=f"Prompt: {image_prompt}")


# Display all previous messages from session history
for message in st.session_state.messages:
  render_message(message)

# User input field
if user_input := st.chat_input("Schreibe deine Nachricht hier..."):
  # Append user message
  user_msg = {"role": "user", "content": user_input}
  st.session_state.messages.append(user_msg)
  render_message(user_msg)

  # Generate assistant response
  with st.chat_message("assistant"):
    message_placeholder = st.empty()
    message_placeholder.markdown("*AI is thinking...*")

    try:
      client = Groq(api_key=api_key)

      # Build message list for Groq API including system prompt
      groq_messages = [{"role": "system", "content": system_prompt}]
      for msg in st.session_state.messages:
        groq_messages.append({"role": msg["role"], "content": msg["content"]})

      completion = client.chat.completions.create(
          model="openai/gpt-oss-20b",
          messages=groq_messages,
          temperature=0.7,
      )

      response_text = completion.choices[0].message.content
      message_placeholder.empty()

      # Check for [IMAGE: ...] prompt in AI response
      image_match = re.search(r"\[IMAGE:\s*(.*?)\]", response_text, re.IGNORECASE)

      if image_match:
        prompt = image_match.group(1).strip()
        clean_text = re.sub(
            r"\[IMAGE:\s*.*?\]", "", response_text, flags=re.IGNORECASE
        ).strip()
        encoded_prompt = urllib.parse.quote(prompt)
        image_url = f"https://pollinations.ai/p/{encoded_prompt}?width=1024&height=1024&seed=42"

        assistant_msg = {
            "role": "assistant",
            "content": clean_text,
            "image_url": image_url,
            "image_prompt": prompt,
        }
      else:
        assistant_msg = {"role": "assistant", "content": response_text}

      # Save message to session state & display
      st.session_state.messages.append(assistant_msg)
      render_message(assistant_msg)

    except Exception as e:
      message_placeholder.markdown(f"⚠️ **Error:** {e}")
