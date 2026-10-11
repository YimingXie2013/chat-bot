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
      "⚠️ Please enter your GROQ_API_KEY in Streamlit Secrets (Settings >"
      " Secrets)."
  )

# Page configuration
st.set_page_config(
    page_title="Llama AI Assistant & Hub", page_icon="✨", layout="centered"
)

st.title("✨ Llama AI Chat, Image & Game Hub")

# Initialize chat history in session state
if "messages" not in st.session_state:
  st.session_state.messages = []

# Sidebar for Mode Selection, Image Generator & Games
with st.sidebar:
  st.header("🎮 Navigation & Hub")
  app_mode = st.radio(
      "Choose Mode:", ["Chat & AI", "HD Image Generator", "Mini Games Hub"]
  )

  if app_mode == "HD Image Generator":
    st.markdown("---")
    st.subheader("🎨 Flux HD Image Generator")
    image_prompt_input = st.text_input("What would you like to generate?")

    if st.button("Generate Image") and image_prompt_input:
      with st.spinner("🎨 Translating & generating HD image..."):
        try:
          client = Groq(api_key=api_key)
          translation_response = client.chat.completions.create(
              model="openai/gpt-oss-20b",
              messages=[{
                  "role": "user",
                  "content": (
                      "Translate and expand this image prompt into detailed,"
                      " high-quality English for an AI image generator (only"
                      f" return the translated prompt text): {image_prompt_input}"
                  ),
              }],
          )
          english_prompt = translation_response.choices[0].message.content.strip()
        except Exception:
          english_prompt = image_prompt_input

        encoded = urllib.parse.quote(english_prompt)
        img_url = (
            f"https://image.pollinations.ai/prompt/{encoded}?model=flux&width=1024&height=1024&nologo=true"
        )

        st.session_state.messages.append({
            "role": "assistant",
            "content": f"Here is your HD image for: *{image_prompt_input}*",
            "image_url": img_url,
        })
        st.success("Image generated! Switch to 'Chat & AI' to view it.")

# Render content based on selected mode
if "app_mode" in locals() and app_mode == "Mini Games Hub":
  st.header("🕹️ Arcade Game Hub")
  game_choice = st.selectbox(
      "Select a mini-game to play:", ["Snake", "2048", "Tetris"]
  )

  if game_choice == "Snake":
    st.subheader("🐍 Snake Game")
    st.components.v1.iframe("https://playsnake.org/", height=500, scrolling=True)
  elif game_choice == "2048":
    st.subheader("🎲 2048 Game")
    st.components.v1.iframe("https://play2048.co/", height=500, scrolling=True)
  elif game_choice == "Tetris":
    st.subheader("🧩 Tetris Game")
    st.components.v1.iframe(
        "https://chvin.github.io/react-tetris/", height=600, scrolling=False
    )

else:
  # Display chat history safely
  for message in st.session_state.messages:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])
      if "image_url" in message and message["image_url"]:
        st.image(message["image_url"])

  # Main Chat Input
  if user_input := st.chat_input("Type your message here..."):
    # Append user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
      st.markdown(user_input)

    # Generate assistant response via Groq
    with st.chat_message("assistant"):
      message_placeholder = st.empty()
      message_placeholder.markdown("*AI is thinking...*")

      try:
        client = Groq(api_key=api_key)

        groq_messages = []
        for msg in st.session_state.messages:
          if "role" in msg and "content" in msg:
            groq_messages.append({"role": msg["role"], "content": msg["content"]})

        completion = client.chat.completions.create(
            model="openai/gpt-oss-20b", messages=groq_messages, temperature=0.7
        )

        response_text = completion.choices[0].message.content
        message_placeholder.markdown(response_text)

        # Save assistant response to history
        st.session_state.messages.append(
            {"role": "assistant", "content": response_text}
        )

      except Exception as api_error:
        message_placeholder.markdown(f"⚠️ **Error:** {api_error}")
