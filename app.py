import time
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

# Virtual Balance & Cooldown for Gamble Station
if "arcade_coins" not in st.session_state:
  st.session_state.arcade_coins = 1000

if "last_bonus_time" not in st.session_state:
  st.session_state.last_bonus_time = 0.0

# Private User Game Vault initialization
if "user_game_vault" not in st.session_state:
  st.session_state.user_game_vault = []

st.title("⚡ Llama AI Hub & Arcade")

# Sidebar Navigation & Settings
with st.sidebar:
  st.header("🎮 Navigation & Status")

  # Virtual Wallet Display & Hourly Bonus Logic
  st.metric(
      label="🪙 Your Arcade Coins", value=f"{st.session_state.arcade_coins:,}"
  )

  current_time = time.time()
  cooldown_period = 3600  # 1 Hour in seconds
  time_passed = current_time - st.session_state.last_bonus_time

  if time_passed >= cooldown_period:
    if st.button("🎁 Claim Hourly Bonus (+500 Coins)"):
      st.session_state.arcade_coins += 500
      st.session_state.last_bonus_time = current_time
      st.success("Successfully claimed +500 Coins!")
      st.rerun()
  else:
    remaining_mins = int((cooldown_period - time_passed) // 60)
    st.info(
        f"⏳ Next bonus available in approx. {remaining_mins} minute(s)."
    )

  st.markdown("---")

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
          "🎰 Gamble Station (Free Coins)",
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

# GAMBLE STATION CATEGORY
elif app_mode == "🎰 Gamble Station (Free Coins)":
  st.header("🎰 Arcade Gamble Station")
  st.caption(
      "100% Free Virtual Minigames. No real money required. Play for highscores!"
  )

  gamble_game = st.selectbox(
      "Select Minigame:",
      [
          "💣 Mines (Grid Field)",
          "💥 TNT Crash Multiplier",
          "🪙 Coinflip Dual",
          "🎲 Lucky Dice",
      ],
  )

  st.markdown(
      f"**Current Balance:** 🪙 `{st.session_state.arcade_coins:,}` Arcade Coins"
  )

  if gamble_game == "💣 Mines (Grid Field)":
    st.subheader("💣 Mines Field")
    bet_amount = st.number_input(
        "Bet Amount:",
        min_value=10,
        max_value=st.session_state.arcade_coins
        if st.session_state.arcade_coins > 0
        else 10,
        value=50,
        step=10,
    )
    num_bombs = st.slider(
        "Number of Hidden Bombs:", min_value=1, max_value=10, value=3
    )

    # Callback mechanism to handle backend coin transactions safely
    col_w1, col_w2 = st.columns(2)
    with col_w1:
      if st.button("🔄 Reset / Deduct Initial Bet"):
        if st.session_state.arcade_coins >= bet_amount:
          st.session_state.arcade_coins -= bet_amount
          st.success(f"Bet of {bet_amount} placed! Good luck!")
          st.rerun()
        else:
          st.error("Not enough coins!")

    mines_html = f"""
        <div style="text-align:center; background:#111827; padding:20px; border-radius:12px; border:2px solid #10B981; font-family:sans-serif;">
            <h3 style="color:#10B981; margin-top:0;">Mines Arena</h3>
            <p style="color:#A1A1AA;">Active Bet: {bet_amount} Coins | Bombs: {num_bombs}</p>
            <div id="grid" style="display:grid; grid-template-columns:repeat(5,1fr); gap:8px; max-width:320px; margin:15px auto;"></div>
            <div style="margin-top:12px;">
                <button id="cashoutBtn" onclick="cashout()" style="background:#10B981; color:white; border:none; padding:12px 24px; font-size:16px; font-weight:bold; border-radius:8px; cursor:pointer; display:none; margin-right: 10px;">Take Winnings</button>
                <button id="restartBtn" onclick="resetGame()" style="background:#3B82F6; color:white; border:none; padding:12px 24px; font-size:16px; font-weight:bold; border-radius:8px; cursor:pointer; display:none;">🔄 Play Again</button>
            </div>
            <p id="statusMsg" style="color:#FFF; font-weight:bold; margin-top:10px;"></p>
        </div>
        <script>
            let totalCells = 25;
            let bombs = {num_bombs};
            let bet = {bet_amount};
            let bombPositions = [];
            let currentMultiplier = 1.0;
            let active = true;
            let revealed = 0;

            function initGame() {{
                bombPositions = [];
                currentMultiplier = 1.0;
                active = true;
                revealed = 0;
                document.getElementById("statusMsginnerHTML = "";
                document.getElementById("cashoutBtn").style.display = "none";
                document.getElementById("restartBtn").style.display = "none";
                
                while(bombPositions.length < bombs) {{
                    let r = Math.floor(Math.random() * totalCells);
                    if(!bombPositions.includes(r)) bombPositions.push(r);
                }}
                
                const grid = document.getElementById("grid");
                grid.innerHTML = "";
                for(let i=0; i<totalCells; i++) {{
                    let b = document.createElement("button");
                    b.style.height = "55px";
                    b.style.background = "#1F2937";
                    b.style.border = "2px solid #374151";
                    b.style.borderRadius = "8px";
                    b.style.fontSize = "20px";
                    b.style.cursor = "pointer";
                    b.style.color = "#FFF";
                    b.onclick = () => reveal(i, b);
                    grid.appendChild(b);
                }}
            }}

            function reveal(idx, btn) {{
                if(!active || btn.disabled) return;
                btn.disabled = true;
                if(bombPositions.includes(idx)) {{
                    btn.style.background = "#EF4444";
                    btn.innerHTML = "💣";
                    active = false;
                    document.getElementById("statusMsg").innerHTML = "💥 BOOM! You hit a bomb.";
                    document.getElementById("statusMsg").style.color = "#EF4444";
                    document.getElementById("cashoutBtn").style.display = "none";
                    document.getElementById("restartBtn").style.display = "inline-block";
                    revealAllBombs();
                }} else {{
                    btn.style.background = "#059669";
                    btn.innerHTML = "💎";
                    revealed++;
                    currentMultiplier = (currentMultiplier * 1.25).toFixed(2);
                    document.getElementById("cashoutBtn").style.display = "inline-block";
                    document.getElementById("cashoutBtn").innerText = "Cashout (" + Math.floor(bet * currentMultiplier) + " Coins)";
                }}
            }}

            function revealAllBombs() {{
                const buttons = document.getElementById("grid").children;
                for(let i=0; i<buttons.length; i++) {{
                    if(bombPositions.includes(i)) {{
                        buttons[i].style.background = "#EF4444";
                        buttons[i].innerHTML = "💣";
                    }}
                    buttons[i].disabled = true;
                }}
            }}

            function cashout() {{
                if(!active) return;
                active = false;
                let profit = Math.floor(bet * currentMultiplier);
                document.getElementById("statusMsg").innerHTML = "🎉 CASHED OUT! Won " + profit + " coins (" + currentMultiplier + "x)!";
                document.getElementById("statusMsg").style.color = "#10B981";
                document.getElementById("cashoutBtn").style.display = "none";
                document.getElementById("restartBtn").style.display = "inline-block";
                revealAllBombs();
            }}

            function resetGame() {{
                initGame();
            }}

            initGame();
        </script>
        """
    st.components.v1.html(mines_html, height=500)

  elif gamble_game == "💥 TNT Crash Multiplier":
    st.subheader("💥 TNT Crash Multiplier")
    bet_crash = st.number_input(
        "Bet Amount:",
        min_value=10,
        max_value=st.session_state.arcade_coins
        if st.session_state.arcade_coins > 0
        else 10,
        value=50,
        step=10,
        key="crash_bet",
    )

    crash_html = f"""
        <div style="text-align:center; background:#0F172A; padding:25px; border-radius:12px; border:2px solid #F59E0B; font-family:sans-serif;">
            <h2 id="mult" style="color:#F59E0B; font-size:48px; margin:10px 0;">1.00x</h2>
            <div>
                <button id="startBtn" onclick="startCrash()" style="background:#F59E0B; color:black; border:none; padding:12px 28px; font-size:18px; font-weight:bold; border-radius:8px; cursor:pointer; margin-right:10px;">🚀 START RUN</button>
                <button id="outBtn" onclick="eject()" style="background:#10B981; color:white; border:none; padding:12px 28px; font-size:18px; font-weight:bold; border-radius:8px; cursor:pointer; display:none; margin-right:10px;">💰 CASH OUT</button>
                <button id="crashResetBtn" onclick="resetCrash()" style="background:#3B82F6; color:white; border:none; padding:12px 28px; font-size:18px; font-weight:bold; border-radius:8px; cursor:pointer; display:none;">🔄 Play Again</button>
            </div>
            <p id="cMsg" style="color:#FFF; margin-top:15px; font-weight:bold;"></p>
        </div>
        <script>
            let mult = 1.00;
            let timer = null;
            let crashPoint = (1.1 + Math.random() * 4.5).toFixed(2);
            let activeRun = false;
            let bet = {bet_crash};

            function resetCrash() {{
                mult = 1.00;
                crashPoint = (1.1 + Math.random() * 4.5).toFixed(2);
                activeRun = false;
                document.getElementById("mult").innerText = "1.00x";
                document.getElementById("mult").style.color = "#F59E0B";
                document.getElementById("startBtn").style.display = "inline-block";
                document.getElementById("outBtn").style.display = "none";
                document.getElementById("crashResetBtn").style.display = "none";
                document.getElementById("cMsg").innerText = "";
            }}

            function startCrash() {{
                document.getElementById("startBtn").style.display = "none";
                document.getElementById("outBtn").style.display = "inline-block";
                activeRun = true;
                timer = setInterval(() => {{
                    mult += 0.04;
                    document.getElementById("mult").innerText = mult.toFixed(2) + "x";
                    if(mult >= crashPoint) {{
                        clearInterval(timer);
                        activeRun = false;
                        document.getElementById("outBtn").style.display = "none";
                        document.getElementById("crashResetBtn").style.display = "inline-block";
                        document.getElementById("mult").style.color = "#EF4444";
                        document.getElementById("mult").innerText = "💥 CRASHED AT " + mult.toFixed(2) + "x";
                        document.getElementById("cMsg").innerText = "Round crashed!";
                        document.getElementById("cMsg").style.color = "#EF4444";
                    }}
                }}, 100);
            }}

            function eject() {{
                if(!activeRun) return;
                clearInterval(timer);
                activeRun = false;
                document.getElementById("outBtn").style.display = "none";
                document.getElementById("crashResetBtn").style.display = "inline-block";
                let win = Math.floor(bet * mult);
                document.getElementById("cMsg").innerText = "🎉 Cashout Successful! You won " + win + " coins!";
                document.getElementById("cMsg").style.color = "#10B981";
            }}
        </script>
        """
    st.components.v1.html(crash_html, height=300)

  elif gamble_game == "🪙 Coinflip Dual":
    st.subheader("🪙 Coinflip Dual")
    col1, col2 = st.columns(2)
    with col1:
      choice = st.radio("Choose Side:", ["HEADS 🪙", "TAILS 🪙"])
    with col2:
      cf_bet = st.number_input(
          "Bet:",
          min_value=10,
          max_value=st.session_state.arcade_coins,
          value=50,
          key="cf_bet",
      )

    if st.button("🚀 Flip Coin!"):
      import random

      outcome = random.choice(["HEADS 🪙", "TAILS 🪙"])
      if choice == outcome:
        st.session_state.arcade_coins += cf_bet
        st.balloons()
        st.success(
            f"🎉 Result: {outcome}! You WON {cf_bet * 2} Coins! (New Balance:"
            f" {st.session_state.arcade_coins})"
        )
      else:
        st.session_state.arcade_coins -= cf_bet
        st.error(
            f"💥 Result: {outcome}! You LOST {cf_bet} Coins. (New Balance:"
            f" {st.session_state.arcade_coins})"
        )

  elif gamble_game == "🎲 Lucky Dice":
    st.subheader("🎲 Lucky Dice (Roll Over 50)")
    dice_bet = st.number_input(
        "Bet Amount:",
        min_value=10,
        max_value=st.session_state.arcade_coins,
        value=50,
        key="dice_bet",
    )

    if st.button("🎲 Roll Dice"):
      import random

      roll = random.randint(1, 100)
      if roll > 50:
        st.session_state.arcade_coins += dice_bet
        st.success(
            f"🎉 Rolled **{roll}** (> 50)! You won {dice_bet * 2} Coins! (New"
            f" Balance: {st.session_state.arcade_coins})"
        )
      else:
        st.session_state.arcade_coins -= dice_bet
        st.error(
            f"💥 Rolled **{roll}** (<= 50)! You lost {dice_bet} Coins. (New"
            f" Balance: {st.session_state.arcade_coins})"
        )

elif app_mode == "✨ AI Game Creator & Vault":
  st.header("✨ AI Game Generator & Private Vault")
  st.markdown(
      "Describe your dream game! The AI will cook up a fully functional HTML5 game "
      "with clean graphics, saved exclusively and **privately in your personal vault**."
  )

  game_prompt = st.text_area(
      "Your Game Idea:",
      value="A smooth arcade game where a cat character catches falling mice.",
  )
  game_title_input = st.text_input("Game Title:", value="My Custom Arcade Game")

  if st.button("🚀 Generate Game & Save to Vault") and game_prompt:
    with st.spinner("🤖 AI is cooking up your game..."):
      try:
        client = Groq(api_key=api_key)
        system_instructions = (
            "You are an elite HTML5 game developer. Write a complete, self-contained HTML5/JavaScript game. "
            "Return ONLY raw HTML code without markdown code blocks."
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

        if generated_html.startswith("```"):
          generated_html = generated_html.split("```")[1]
          if generated_html.startswith("html"):
            generated_html = generated_html[4:]

        st.session_state.user_game_vault.append({
            "title": game_title_input,
            "prompt": game_prompt,
            "code": generated_html,
        })
        st.success("🎉 Game stored safely in your private vault!")
      except Exception as e:
        st.error(f"⚠️ Generation error: {e}")

  st.markdown("---")
  st.subheader("🔒 Your Private Game Vault")

  if st.session_state.user_game_vault:
    vault_titles = [g["title"] for g in st.session_state.user_game_vault]
    selected_vault_game = st.selectbox(
        "Select a game from your Vault:", vault_titles
    )

    for g in st.session_state.user_game_vault:
      if g["title"] == selected_vault_game:
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
