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
if app_mode == "Mini Games Hub":
  st.header("🕹️ Arcade Game Hub")
  game_choice = st.selectbox(
      "Select a mini-game to play:", ["Snake", "2048", "Tetris"]
  )

  if game_choice == "Snake":
    st.subheader("🐍 Snake Game")
    # Native embedded HTML5 / JS Snake Game
    snake_html = """
        <div style="text-align: center;">
            <canvas id="gc" width="400" height="400" style="background-color: #111; border: 3px solid #4CAF50; border-radius: 8px;"></canvas>
            <p style="color: #888; font-family: sans-serif; font-size: 14px; margin-top: 8px;">Use Arrow Keys (← ↑ → ↓) to Control</p>
        </div>
        <script>
            window.onload = function() {
                canv = document.getElementById("gc");
                ctx = canv.getContext("2d");
                document.addEventListener("keydown", keyPush);
                setInterval(game, 1000/15);
            }
            px=py=10;
            gs=tc=20;
            ax=ay=15;
            xv=yv=0;
            trail=[];
            tail = 5;
            function game() {
                px+=xv;
                py+=yv;
                if(px<0) px=tc-1;
                if(px>tc-1) px=0;
                if(py<0) py=tc-1;
                if(py>tc-1) py=0;
                ctx.fillStyle="black";
                ctx.fillRect(0,0,canv.width,canv.height);
                ctx.fillStyle="lime";
                for(var i=0;i<trail.length;i++) {
                    ctx.fillRect(trail[i].x*gs,trail[i].y*gs,gs-2,gs-2);
                    if(trail[i].x==px && trail[i].y==py) tail = 5;
                }
                trail.push({x:px,y:py});
                while(trail.length>tail) { trail.shift(); }
                if(ax==px && ay==py) {
                    tail++;
                    ax=Math.floor(Math.random()*tc);
                    ay=Math.floor(Math.random()*tc);
                }
                ctx.fillStyle="red";
                ctx.fillRect(ax*gs,ay*gs,gs-2,gs-2);
            }
            function keyPush(evt) {
                switch(evt.keyCode) {
                    case 37: xv=-1;yv=0; break;
                    case 38: xv=0;yv=-1; break;
                    case 39: xv=1;yv=0; break;
                    case 40: xv=0;yv=1; break;
                }
            }
        </script>
        """
    st.components.v1.html(snake_html, height=480)

  elif game_choice == "2048":
    st.subheader("🎲 2048 Game")
    st.components.v1.iframe(
        "https://2048game.com/", height=600, scrolling=True
    )

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
