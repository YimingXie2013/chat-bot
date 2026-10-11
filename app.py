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
    page_title="Llama AI Ultimate Hub", page_icon="⚡", layout="centered"
)

# Session State Initializations
if "messages" not in st.session_state:
  st.session_state.messages = []

if "is_premium" not in st.session_state:
  st.session_state.is_premium = False

st.title("⚡ Llama AI Hub & Arcade")

# Sidebar Navigation & Settings
with st.sidebar:
  st.header("🎮 Navigation & Status")

  # Premium Badge Status
  if st.session_state.is_premium:
    st.success("👑 VIP PRO Status: ACTIVE")
  else:
    st.info("🔓 Free Version (3D Games Locked)")

  app_mode = st.radio(
      "Select Mode:", ["Chat & AI", "HD Image Generator", "Arcade Games"]
  )

  # VIP Unlock Code Section
  st.markdown("---")
  st.subheader("🔑 Redeem VIP Key")
  promo_code = st.text_input(
      "Enter VIP Code:", type="password", key="vip_input"
  )
  if st.button("Unlock Code"):
    if promo_code == "PRO2026":  # Master VIP Key
      st.session_state.is_premium = True
      st.success("🎉 VIP Status Successfully Activated!")
      st.rerun()
    else:
      st.error("❌ Invalid VIP Code!")

  if app_mode == "HD Image Generator":
    st.markdown("---")
    st.subheader("🎨 Flux HD Image Generator")
    image_prompt_input = st.text_input("What do you want to generate?")

    if st.button("Generate Image") and image_prompt_input:
      with st.spinner("🎨 AI is generating your HD image..."):
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
        st.success("Image ready! Switch to the 'Chat & AI' tab to view it.")

# Main Rendering Logic
if app_mode == "Arcade Games":
  st.header("🕹️ Arcade Game Hub")

  game_choice = st.selectbox(
      "Choose a game:",
      [
          "🐍 Snake (Free)",
          "🎲 2048 (Free)",
          "🧩 Tetris (Free)",
          "🏎️ 3D Cyber Racer (👑 VIP High-Quality)",
      ],
  )

  # FREE GAME 1: Snake (Mobile Touch + PC Controls)
  if "Snake" in game_choice:
    st.subheader("🐍 Snake (Free Classic)")
    snake_html = """
        <div style="text-align: center; background: #0b0f19; padding: 15px; border-radius: 12px; border: 2px solid #4CAF50;">
            <canvas id="gc" width="320" height="320" style="background-color: #111; border: 2px solid #4CAF50; border-radius: 8px;"></canvas>
            <p style="color: #888; font-family: sans-serif; font-size: 13px; margin: 8px 0;">PC: Arrow Keys | Mobile: Tap controls below</p>
            
            <!-- Mobile Touch Controls -->
            <div style="display: flex; flex-direction: column; align-items: center; gap: 5px; margin-top: 10px;">
                <button onclick="changeDir(38)" style="background: #1f2937; color: white; border: 2px solid #4CAF50; padding: 10px 25px; font-size: 18px; border-radius: 8px; cursor: pointer;">⬆️ UP</button>
                <div style="display: flex; gap: 10px;">
                    <button onclick="changeDir(37)" style="background: #1f2937; color: white; border: 2px solid #4CAF50; padding: 10px 20px; font-size: 18px; border-radius: 8px; cursor: pointer;">⬅️ LEFT</button>
                    <button onclick="changeDir(40)" style="background: #1f2937; color: white; border: 2px solid #4CAF50; padding: 10px 20px; font-size: 18px; border-radius: 8px; cursor: pointer;">⬇️ DOWN</button>
                    <button onclick="changeDir(39)" style="background: #1f2937; color: white; border: 2px solid #4CAF50; padding: 10px 20px; font-size: 18px; border-radius: 8px; cursor: pointer;">RIGHT ➡️</button>
                </div>
            </div>
        </div>
        <script>
            window.onload = function() {
                canv = document.getElementById("gc");
                ctx = canv.getContext("2d");
                document.addEventListener("keydown", keyPush);
                setInterval(game, 1000/12);
            }
            px=py=10; gs=tc=16; ax=ay=12; xv=yv=0; trail=[]; tail = 5;
            function game() {
                px+=xv; py+=yv;
                if(px<0) px=tc-1; if(px>tc-1) px=0;
                if(py<0) py=tc-1; if(py>tc-1) py=0;
                ctx.fillStyle="#111"; ctx.fillRect(0,0,canv.width,canv.height);
                ctx.fillStyle="lime";
                for(var i=0;i<trail.length;i++) {
                    ctx.fillRect(trail[i].x*gs,trail[i].y*gs,gs-2,gs-2);
                    if(trail[i].x==px && trail[i].y==py) tail = 5;
                }
                trail.push({x:px,y:py});
                while(trail.length>tail) { trail.shift(); }
                if(ax==px && ay==py) {
                    tail++;
                    ax=Math.floor(Math.random()*tc); ay=Math.floor(Math.random()*tc);
                }
                ctx.fillStyle="red"; ctx.fillRect(ax*gs,ay*gs,gs-2,gs-2);
            }
            function changeDir(keyCode) {
                switch(keyCode) {
                    case 37: if(xv!=1){xv=-1;yv=0;} break;
                    case 38: if(yv!=1){xv=0;yv=-1;} break;
                    case 39: if(xv!=-1){xv=1;yv=0;} break;
                    case 40: if(yv!=-1){xv=0;yv=1;} break;
                }
            }
            function keyPush(evt) { changeDir(evt.keyCode); }
        </script>
        """
    st.components.v1.html(snake_html, height=560)

  # FREE GAME 2: 2048 (Native Swipe Touch Support)
  elif "2048" in game_choice:
    st.subheader("🎲 2048 (Free Classic)")
    st.components.v1.iframe(
        "https://2048game.com/", height=600, scrolling=True
    )

  # FREE GAME 3: English Mobile Tetris
  elif "Tetris" in game_choice:
    st.subheader("🧩 Tetris (Free Classic)")
    st.components.v1.iframe(
        "https://austin-nguyen.github.io/tetris/", height=620, scrolling=False
    )

  # VIP HIGH QUALITY GAME: 3D Cyber Racer with Touch Pad & Fullscreen Options
  elif "3D Cyber Racer" in game_choice:
    if not st.session_state.is_premium:
      st.warning(
          "🔒 **3D Cyber Racer is an exclusive VIP High-Quality game!**\n\n"
          "This premium 3D game is reserved for PRO members.\n"
          "Enter your VIP Key (`PRO2026`) in the sidebar to unlock it!"
      )
    else:
      st.subheader("🏎️ 3D Cyber Racer (👑 VIP Unlocked)")
      st.info(
          "🕹️ **Controls:** Use WASD / Arrow keys on PC, or use the touch"
          " buttons below on Mobile!"
      )

      st.markdown(
          '<a href="https://hexgl.bkcore.com/play/" target="_blank"'
          ' style="display: inline-block; background-color: #00ffcc; color:'
          ' #0b0f19; padding: 10px 20px; font-weight: bold; border-radius:'
          ' 6px; text-decoration: none; margin-bottom: 12px;">🚀 Launch Game'
          ' in New Fullscreen Tab</a>',
          unsafe_allow_html=True,
      )

      cyber_racer_html = """
            <div style="text-align: center; background: #0b0f19; padding: 10px; border-radius: 12px; border: 2px solid #00ffcc;">
                <iframe src="https://hexgl.bkcore.com/play/" width="100%" height="450px" style="border:none; border-radius: 8px;" allowfullscreen="true"></iframe>
                
                <p style="color: #00ffcc; font-family: sans-serif; font-size: 13px; margin: 10px 0 5px 0; font-weight: bold;">📱 Mobile Touch Controls</p>
                <div style="display: flex; justify-content: center; gap: 8px; flex-wrap: wrap;">
                    <button onclick="sendKey(37)" style="background: #1f2937; color: white; border: 2px solid #00ffcc; padding: 10px 18px; font-size: 16px; border-radius: 8px; cursor: pointer; font-weight: bold;">⬅️ Left</button>
                    <button onclick="sendKey(38)" style="background: #1f2937; color: white; border: 2px solid #00ffcc; padding: 10px 18px; font-size: 16px; border-radius: 8px; cursor: pointer; font-weight: bold;">🚀 Gas</button>
                    <button onclick="sendKey(39)" style="background: #1f2937; color: white; border: 2px solid #00ffcc; padding: 10px 18px; font-size: 16px; border-radius: 8px; cursor: pointer; font-weight: bold;">Right ➡️</button>
                    <button onclick="sendKey(40)" style="background: #1f2937; color: white; border: 2px solid #ff4444; padding: 10px 18px; font-size: 16px; border-radius: 8px; cursor: pointer; font-weight: bold;">🛑 Brake</button>
                </div>
            </div>
            <script>
                function sendKey(keyCode) {
                    var iframe = document.querySelector('iframe');
                    if (iframe && iframe.contentWindow) {
                        iframe.contentWindow.dispatchEvent(new KeyboardEvent('keydown', {'keyCode': keyCode, 'which': keyCode}));
                        setTimeout(function() {
                            iframe.contentWindow.dispatchEvent(new KeyboardEvent('keyup', {'keyCode': keyCode, 'which': keyCode}));
                        }, 100);
                    }
                }
            </script>
            """
      st.components.v1.html(cyber_racer_html, height=580)

elif app_mode == "Chat & AI":
  # Render Chat History
  for message in st.session_state.messages:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])
      if "image_url" in message and message["image_url"]:
        st.image(message["image_url"])

  # Main Chat Input
  if user_input := st.chat_input("Type a message..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
      st.markdown(user_input)

    with st.chat_message("assistant"):
      message_placeholder = st.empty()
      message_placeholder.markdown("*AI is thinking...*")

      try:
        client = Groq(api_key=api_key)
        groq_messages = [
            {"role": msg["role"], "content": msg["content"]}
            for msg in st.session_state.messages
            if "role" in msg and "content" in msg
        ]

        completion = client.chat.completions.create(
            model="openai/gpt-oss-20b", messages=groq_messages, temperature=0.7
        )

        response_text = completion.choices[0].message.content
        message_placeholder.markdown(response_text)
        st.session_state.messages.append(
            {"role": "assistant", "content": response_text}
        )

      except Exception as api_error:
        message_placeholder.markdown(f"⚠️ **Error:** {api_error}")
