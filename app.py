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

# Private User Game Vault initialization (isolated per session/user)
if "user_game_vault" not in st.session_state:
  st.session_state.user_game_vault = []

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
      "Select Mode:",
      [
          "Chat & AI",
          "HD Image Generator",
          "Arcade Games",
          "✨ AI Game Creator & Vault",
      ],
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
          "🎲 2048 (Free Classic)",
          "🧩 Tetris (Free)",
          "🔻 Geometry Dash (Free Classic)",
          "🏎️ 3D Cyber Racer (👑 VIP)",
          "🧟 3D Zombie Survival (👑 VIP)",
          "🚀 3D Space Shooter (👑 VIP)",
      ],
  )

  # 1. SNAKE
  if "Snake" in game_choice:
    st.subheader("🐍 Snake (Free Classic)")
    snake_html = """
        <div style="text-align: center; background: #0b0f19; padding: 15px; border-radius: 12px; border: 2px solid #4CAF50;">
            <canvas id="gc" width="320" height="320" style="background-color: #111; border: 2px solid #4CAF50; border-radius: 8px;"></canvas>
            <p style="color: #888; font-family: sans-serif; font-size: 13px; margin: 8px 0;">PC: Arrow Keys | Mobile: Tap buttons below</p>
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

  # 2. 2048
  elif "2048" in game_choice:
    st.subheader("🎲 2048 (Free Classic)")
    st.markdown(
        '<div style="text-align: center; background: #bbada0; padding: 30px;'
        ' border-radius: 12px;"><h2 style="color: #776e65; margin-bottom:'
        ' 15px;">2048 Classic</h2><p style="color: #776e65; margin-bottom:'
        ' 20px;">Play the legendary puzzle game seamlessly:</p><a'
        ' href="https://play2048.co/" target="_blank" style="background:'
        ' #8f7a66; color: white; padding: 14px 28px; font-size: 18px; font-weight:'
        ' bold; border-radius: 8px; text-decoration: none; display:'
        ' inline-block;">🚀 Start 2048 Now</a></div>',
        unsafe_allow_html=True,
    )

  # 3. TETRIS (100% UNTOUCHED)
  elif "Tetris" in game_choice:
    st.subheader("🧩 Tetris (Free Classic)")
    st.components.v1.iframe(
        "https://tetris.com/play-tetris", height=620, scrolling=True
    )

  # 4. GEOMETRY DASH
  elif "Geometry Dash" in game_choice:
    st.subheader("🔻 Geometry Dash (Free Classic)")
    st.markdown(
        '<div style="text-align: center; background: #1e1b4b; padding: 30px;'
        ' border-radius: 12px; border: 2px solid #ec4899;"><h2'
        ' style="color: #00ffcc; margin-bottom: 15px;">Geometry Dash</h2><p'
        ' style="color: #fff; margin-bottom: 20px;">Jump over obstacles in'
        ' rhythm:</p><a href="https://geometrydash.io/" target="_blank"'
        ' style="background: #ec4899; color: white; padding: 14px 28px; font-size:'
        ' 18px; font-weight: bold; border-radius: 8px; text-decoration: none;'
        ' display: inline-block;">🚀 Play Geometry Dash</a></div>',
        unsafe_allow_html=True,
    )

  # 5. VIP: 3D CYBER RACER (100% UNTOUCHED)
  elif "3D Cyber Racer" in game_choice:
    if not st.session_state.is_premium:
      st.warning(
          "🔒 **3D Cyber Racer is reserved for VIP PRO members!**\n\nEnter VIP Key"
          " (`PRO2026`) in the sidebar to unlock."
      )
    else:
      st.subheader("🏎️ 3D Cyber Racer (👑 VIP Unlocked)")
      st.components.v1.iframe(
          "https://hexgl.bkcore.com/play/", height=550, scrolling=False
      )

  # 6. VIP: 3D ZOMBIE SURVIVAL
  elif "3D Zombie Survival" in game_choice:
    if not st.session_state.is_premium:
      st.warning(
          "🔒 **3D Zombie Survival is reserved for VIP PRO members!**\n\nEnter"
          " VIP Key (`PRO2026`) in the sidebar to unlock."
      )
    else:
      st.subheader("🧟 3D Zombie Survival (👑 VIP Unlocked)")
      st.markdown(
          '<div style="text-align: center; background: #111; padding: 30px;'
          ' border-radius: 12px; border: 2px solid #ef4444;"><h2'
          ' style="color: #ef4444; margin-bottom: 15px;">3D Zombie'
          ' Survival</h2><p style="color: #fff; margin-bottom: 20px;">Survive'
          ' the apocalypse:</p><a'
          ' href="https://www.crazygames.com/game/zombie-derby" target="_blank"'
          ' style="background: #ef4444; color: white; padding: 14px 28px; font-size:'
          ' 18px; font-weight: bold; border-radius: 8px; text-decoration: none;'
          ' display: inline-block;">🚀 Launch Zombie Game</a></div>',
          unsafe_allow_html=True,
      )

  # 7. VIP: 3D SPACE SHOOTER
  elif "3D Space Shooter" in game_choice:
    if not st.session_state.is_premium:
      st.warning(
          "🔒 **3D Space Shooter is reserved for VIP PRO members!**\n\nEnter VIP"
          " Key (`PRO2026`) in the sidebar to unlock."
      )
    else:
      st.subheader("🚀 3D Space Shooter (👑 VIP Unlocked)")
      st.markdown(
          '<div style="text-align: center; background: #020617; padding: 30px;'
          ' border-radius: 12px; border: 2px solid #8b5cf6;"><h2'
          ' style="color: #8b5cf6; margin-bottom: 15px;">3D Space'
          ' Shooter</h2><p style="color: #fff; margin-bottom: 20px;">Dominate'
          ' the galaxy:</p><a href="https://www.crazygames.com/game/space-wars"'
          ' target="_blank" style="background: #8b5cf6; color: white; padding:'
          ' 14px 28px; font-size: 18px; font-weight: bold; border-radius: 8px;'
          ' text-decoration: none; display: inline-block;">🚀 Launch Space'
          ' Shooter</a></div>',
          unsafe_allow_html=True,
      )

elif app_mode == "✨ AI Game Creator & Vault":
  st.header("✨ AI Game Generator & Private Vault")
  st.markdown(
      "Describe your dream game! The AI will cook up a fully functional, highly polished HTML5 canvas game "
      "with robust physics, immediate startup, beautiful custom vector graphics, and smooth controls, saved exclusively "
      "and **privately in your personal vault**."
  )

  # Input for new game prompt
  game_prompt = st.text_area(
      "Your Game Idea (e.g., 'A smooth arcade game where a cat catches falling mice'):",
      value="A smooth arcade game where a cat character catches falling mice.",
  )
  game_title_input = st.text_input("Game Title:", value="My Custom Arcade Game")

  if st.button("🚀 Generate Game & Save to Vault") and game_prompt:
    with st.spinner(
        "🤖 AI is cooking up your masterpiece (building robust HTML5 canvas"
        " loops & physics)..."
    ):
      try:
        client = Groq(api_key=api_key)
        # Master Chef System Prompt enforcing immediate self-starting loops and gorgeous vector graphics
        system_instructions = (
            "You are an elite, senior HTML5 game developer and master game designer. "
            "Write a complete, self-contained, fully working HTML5/JavaScript game based on the user's prompt. "
            "CRITICAL TECHNICAL REQUIREMENTS:\n"
            "1. The game MUST start immediately upon loading (auto-init or explicit start button inside the canvas UI, NO frozen screens).\n"
            "2. Implement a robust requestAnimationFrame game loop with clear update() and draw() functions.\n"
            "3. Use clean vector graphics, custom paths, gradients, and shapes via HTML5 Canvas API (ctx.arc, ctx.fillRect, ctx.beginPath) – DO NOT use emojis.\n"
            "4. Include interactive controls (keyboard Arrow keys / WASD and responsive on-screen buttons).\n"
            "5. Include a modern HUD (Score, Lives, Timer) and clean Game Over state with restart logic.\n"
            "6. CRITICAL: Return ONLY raw HTML code starting with <!DOCTYPE html> or <div> and ending with respective tags. "
            "Do NOT wrap the output in markdown code blocks like ```html ... ```, just output the exact raw HTML/JS code string."
        )

        completion = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": game_prompt},
            ],
            temperature=0.7,
        )
        generated_html = completion.choices[0].message.content.strip()

        # Clean markdown wrappers if returned accidentally
        if generated_html.startswith("```"):
          generated_html = generated_html.split("```")[1]
          if generated_html.startswith("html"):
            generated_html = generated_html[4:]

        # Save to private session user vault
        st.session_state.user_game_vault.append({
            "title": game_title_input,
            "prompt": game_prompt,
            "code": generated_html,
        })
        st.success(
            "🎉 Game successfully created and stored safely in your private"
            " vault!"
        )
      except Exception as e:
        st.error(f"⚠️ Generation error: {e}")

  st.markdown("---")
  st.subheader("🔒 Your Private Game Vault (Visible only to you)")

  if not st.session_state.user_game_vault:
    st.info(
        "Your vault is currently empty. Generate your first custom AI game"
        " above!"
    )
  else:
    # Select game from private vault
    vault_titles = [g["title"] for g in st.session_state.user_game_vault]
    selected_vault_game = st.selectbox(
        "Select a game from your Vault:", vault_titles
    )

    for g in st.session_state.user_game_vault:
      if g["title"] == selected_vault_game:
        st.markdown(f"**Idea:** _{g['prompt']}_")
        # Render user's private game safely
        st.components.v1.html(g["code"], height=520, scrolling=True)

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
