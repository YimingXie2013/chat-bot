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


def extract_and_display_response(text):
  """Parses [IMAGE: ...] tags from the response and renders images inline."""
  image_match = re.search(r"\[IMAGE:\s*(.*?)\]", text, re.IGNORECASE)

  if image_match:
    prompt = image_match.group(1).strip()
    clean_text = re.sub(r"\[IMAGE:\s*.*?\]", "", text, flags=re.IGNORECASE).strip()

    if clean_text:
      st.markdown(clean_text)

    encoded_prompt = urllib.parse.quote(prompt)
    image_url = f"https://pollinations.ai/p/{encoded_prompt}?width=1024&height=1024&seed=42"

    with st.spinner("🎨 Generating image..."):
      st.image(image_url, caption=f"Prompt: {prompt}")
  else:
    st.markdown(text)


# Display chat history
for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    extract_and_display_response(message["content"])

# User input field
if user_input := st.chat_input("Schreibe deine Nachricht hier..."):
  st.session_state.messages.append({"role": "user", "content": user_input})
  with st.chat_message("user"):
    st.markdown(user_input)

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

      # Request completion using Llama 3.3 70B
      completion = client.chat.completions.create(
          model="llama-3.1-8b-instant",
          messages=groq_messages,
          temperature=0.7,
      )

      response_text = completion.choices[0].message.content
      message_placeholder.empty()

      extract_and_display_response(response_text)

      st.session_state.messages.append(
          {"role": "assistant", "content": response_text}
      )
    except Exception as e:
      message_placeholder.markdown(f"⚠️ **Error:** {e}")
