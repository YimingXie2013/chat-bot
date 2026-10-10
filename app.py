import re
import urllib.parse
from google import genai
import streamlit as st

# Safe API key loading: Tries Streamlit Secrets first, local fallback is empty
try:
  api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
  api_key = ""

if not api_key:
  st.error(
      "⚠️ Bitte trage deinen API-Key in den Streamlit Secrets (unter Settings >"
      " Secrets) oder im Code ein."
  )

# Page configuration
st.set_page_config(
    page_title="Gemini AI Assistant", page_icon="✨", layout="centered"
)

st.title("✨ Gemini AI Chat & Image Assistant")
st.markdown(
    "Chatte mit der KI in jeder Sprache oder lass dir direkt Bilder im Chat"
    " generieren!"
)

# Initialize chat history
if "messages" not in st.session_state:
  st.session_state.messages = []

# System instructions
system_instruction = (
    "You are a helpful, multilingual AI assistant. When the user asks to draw,"
    " create, or generate an image, you must include a special tag in your"
    " response formatted strictly as: [IMAGE: detailed english description of"
    " the image]. Keep your conversational text brief when an image is"
    " requested."
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
if user_input := st.chat_input(
    "Schreibe deine Nachricht hier (z.B. 'Hallo' oder 'Zeichne eine futuristische"
    " Stadt')..."
):
  st.session_state.messages.append({"role": "user", "content": user_input})
  with st.chat_message("user"):
    st.markdown(user_input)

  # Generate assistant response
  with st.chat_message("assistant"):
    message_placeholder = st.empty()
    message_placeholder.markdown("*AI is thinking...*")

    try:
      # Frischen Client und Chat pro Anfrage erstellen, um geschlossene Verbindungen zu verhindern
      client = genai.Client(api_key=api_key)
      chat = client.chats.create(
          model="gemini-2.5-flash",
          config=dict(system_instruction=system_instruction),
      )

      response = chat.send_message(user_input)
      message_placeholder.empty()

      extract_and_display_response(response.text)

      st.session_state.messages.append(
          {"role": "assistant", "content": response.text}
      )
    except Exception as e:
      message_placeholder.markdown(
          "⚠️ **Error:** Rate limit reached or connection issue. Please wait a"
          f" moment. (Details: {e})"
      )
