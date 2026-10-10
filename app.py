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

# Initialize chat history in session state
if "messages" not in st.session_state:
  st.session_state.messages = []

# Sidebar for direct image generation option
with st.sidebar:
  st.header("🎨 Bildgenerator")
  image_prompt_input = st.text_input("Was möchtest du generieren?")
  if st.button("Bild direkt erstellen") and image_prompt_input:
    encoded = urllib.parse.quote(image_prompt_input)
    img_url = f"https://pollinations.ai/p/{encoded}?width=1024&height=1024"
    st.session_state.messages.append({
        "role": "assistant",
        "content": f"Hier ist dein generiertes Bild für: *{image_prompt_input}*",
        "image_url": img_url,
    })
    st.rerun()

# Display chat history safely
for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])
    if "image_url" in message and message["image_url"]:
      st.image(message["image_url"])

# Main Chat Input
if user_input := st.chat_input("Schreibe deine Nachricht hier..."):
  # User message
  st.session_state.messages.append({"role": "user", "content": user_input})
  with st.chat_message("user"):
    st.markdown(user_input)

  # Assistant response via Groq
  with st.chat_message("assistant"):
    message_placeholder = st.empty()
    message_placeholder.markdown("*AI is thinking...*")

    try:
      client = Groq(api_key=api_key)

      groq_messages = []
      for msg in st.session_state.messages:
        # Nur Textnachrichten an Groq übergeben
        if "role" in msg and "content" in msg:
          groq_messages.append({"role": msg["role"], "content": msg["content"]})

      completion = client.chat.completions.create(
          model="openai/gpt-oss-20b", messages=groq_messages, temperature=0.7
      )

      response_text = completion.choices[0].message.content
      message_placeholder.markdown(response_text)

      # Save to history
      st.session_state.messages.append(
          {"role": "assistant", "content": response_text}
      )

    except Exception as e:
      message_placeholder.markdown(f"⚠️ **Error:** {e}")
