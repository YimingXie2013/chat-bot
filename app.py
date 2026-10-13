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

if "last_bonus_time" not in st.session_state:
  st.session_state.last_bonus_time = 0.0

# Private User Game Vault initialization
if "user_game_vault" not in st.session_state:
  st.session_state.user_game_vault = []

st.title("⚡ Llama AI Hub & Arcade")

# Sidebar Navigation & Settings
with st.sidebar:
  st.header("🎮 Navigation & Status")

  # Visible Live Countdown for Hourly Bonus
  st.markdown("🎁 **Hourly Coin Bonus**")
  bonus_widget_html = """
    <div style="background:#1e293b; padding:10px; border-radius:8px; text-align:center; border:1px solid #334155; margin-bottom: 10px;">
        <p style="color:#94a3b8; font-size:12px; margin:0 0 5px 0;">Status / Countdown:</p>
        <div id="bonusTimer" style="color:#f59e0b; font-weight:bold; font-size:14px;">Loading...</div>
        <button onclick="claimBonus()" style="background:#10b981; color:white; border:none; padding:8px 14px; font-size:13px; font-weight:bold; border-radius:6px; cursor:pointer; margin-top:8px; width:100%;">Claim +500 Coins</button>
    </div>
    <script>
        function updateTimer() {
            let lastClaim = parseInt(localStorage.getItem('last_bonus_timestamp') || '0');
            let now = Date.now();
            let cooldown = 3600000; // 1 hour in ms
            let elapsed = now - lastClaim;
            let timerEl = document.getElementById("bonusTimer");
            
            if (elapsed >= cooldown) {
                timerEl.innerHTML = "✅ Ready to Claim!";
                timerEl.style.color = "#10b981";
            } else {
                let remaining = cooldown - elapsed;
                let mins = Math.floor(remaining / 60000);
                let secs = Math.floor((remaining % 60000) / 1000);
                timerEl.innerHTML = "⏳ " + mins + "m " + secs + "s remaining";
                timerEl.style.color = "#f59e0b";
            }
        }
        setInterval(updateTimer, 1000);
        updateTimer();

        function claimBonus() {
            let lastClaim = parseInt(localStorage.getItem('last_bonus_timestamp') || '0');
            let now = Date.now();
            let cooldown = 3600000;
            if (now - lastClaim < cooldown) {
                alert("⏳ Cooldown active! Please wait for the timer to finish.");
            } else {
                localStorage.setItem('last_bonus_timestamp', now);
                let coins = parseInt(localStorage.getItem('arcade_coins') || '1000');
                coins += 500;
                localStorage.setItem('arcade_coins', coins);
                window.parent.location.reload();
            }
        }
    </script>
    """
  st.components.v1.html(bonus_widget_html, height=130)

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
          "🎰 Gamble Station (High-End)",
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

# GAMBLE STATION CATEGORY (HIGH-END DARK THEME + HOUSE EDGE + ANIMATED PLINKO & JACKPOT)
elif app_mode == "🎰 Gamble Station (High-End)":
  st.header("🎰 Gamble Station Originals")
  st.caption(
      "Play provably fair virtual games with smooth animations & house edge."
  )

  gamble_game = st.selectbox(
      "Select Original Game:",
      [
          "💣 Mines (Grid Field)",
          "💥 TNT Crash Multiplier",
          "🪙 Coinflip Dual (Animated)",
          "🎲 Lucky Dice (Adjustable Roll-Over)",
          "🔻 Plinko (Physics Animation)",
          "🎡 Wheel of Fortune (Jackpot Wheel)",
      ],
  )

  if gamble_game == "💣 Mines (Grid Field)":
    st.subheader("💣 Mines Field")
    bet_amount = st.number_input(
        "Bet Amount:", min_value=10, max_value=100000, value=50, step=10
    )
    num_bombs = st.slider(
        "Number of Hidden Bombs:", min_value=1, max_value=10, value=3
    )

    mines_html = (
        """
        <div style="text-align:center; background:linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); padding:25px; border-radius:16px; border:2px solid #10b981; font-family:sans-serif; box-shadow: 0 10px 25px rgba(0,0,0,0.5);">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px; background: rgba(0,0,0,0.3); padding: 10px 15px; border-radius: 10px;">
                <h3 style="color:#10b981; margin:0; font-size: 18px;">💎 MINES ARENA</h3>
                <span style="background:#111827; color:#f59e0b; padding:6px 14px; border-radius:8px; font-weight:bold; border:1px solid #374151;">🪙 <span id="coinDisplay">1,000</span> Coins</span>
            </div>
            <p style="color:#94a3b8; margin:8px 0; font-size: 14px;">Active Bet: """
        + str(bet_amount)
        + """ | Bombs: """
        + str(num_bombs)
        + """</p>
            <div id="grid" style="display:grid; grid-template-columns:repeat(5,1fr); gap:10px; max-width:340px; margin:20px auto;"></div>
            <div style="margin-top:15px;">
                <button id="cashoutBtn" onclick="cashout()" style="background:#10b981; color:white; border:none; padding:12px 26px; font-size:16px; font-weight:bold; border-radius:10px; cursor:pointer; display:none; margin-right: 10px;">Take Winnings</button>
                <button id="restartBtn" onclick="resetGame()" style="background:#3b82f6; color:white; border:none; padding:12px 26px; font-size:16px; font-weight:bold; border-radius:10px; cursor:pointer; display:none;">🔄 Play Again</button>
            </div>
            <p id="statusMsg" style="color:#fff; font-weight:bold; margin-top:12px; font-size: 15px;"></p>
        </div>
        <script>
            let totalCells = 25;
            let bombs = """
        + str(num_bombs)
        + """;
            let bet = """
        + str(bet_amount)
        + """;
            let bombPositions = [];
            let currentMultiplier = 1.0;
            let active = false;

            function getCoins() { return parseInt(localStorage.getItem('arcade_coins') || '1000'); }
            function setCoins(val) { localStorage.setItem('arcade_coins', val); document.getElementById("coinDisplay").innerText = val.toLocaleString(); }

            function initGame() {
                let coins = getCoins();
                setCoins(coins);
                if(coins < bet) {
                    document.getElementById("statusMsg").innerHTML = "⚠️ Not enough coins!";
                    document.getElementById("statusMsg").style.color = "#ef4444";
                    return;
                }
                setCoins(coins - bet);
                bombPositions = [];
                currentMultiplier = 1.0;
                active = true;
                document.getElementById("statusMsg").innerHTML = "Game started! Pick safe tiles.";
                document.getElementById("statusMsg").style.color = "#10b981";
                document.getElementById("cashoutBtn").style.display = "none";
                document.getElementById("restartBtn").style.display = "none";
                
                while(bombPositions.length < bombs) {
                    let r = Math.floor(Math.random() * totalCells);
                    if(!bombPositions.includes(r)) bombPositions.push(r);
                }
                
                const grid = document.getElementById("grid");
                grid.innerHTML = "";
                for(let i=0; i<totalCells; i++) {
                    let b = document.createElement("button");
                    b.style.height = "60px";
                    b.style.background = "#1e293b";
                    b.style.border = "2px solid #334155";
                    b.style.borderRadius = "10px";
                    b.style.fontSize = "22px";
                    b.style.cursor = "pointer";
                    b.style.color = "#fff";
                    b.onclick = () => reveal(i, b);
                    grid.appendChild(b);
                }
            }

            function reveal(idx, btn) {
                if(!active) { initGame(); return; }
                if(btn.disabled) return;
                btn.disabled = true;
                
                if(bombPositions.includes(idx)) {
                    btn.style.background = "#ef4444";
                    btn.innerHTML = "💣";
                    active = false;
                    document.getElementById("statusMsg").innerHTML = "💥 BOOM! You lost " + bet + " coins.";
                    document.getElementById("statusMsg").style.color = "#ef4444";
                    document.getElementById("cashoutBtn").style.display = "none";
                    document.getElementById("restartBtn").style.display = "inline-block";
                    revealAllBombs();
                } else {
                    btn.style.background = "#059669";
                    btn.innerHTML = "💎";
                    currentMultiplier = (currentMultiplier * 1.22).toFixed(2);
                    let currentWin = Math.floor(bet * currentMultiplier);
                    document.getElementById("cashoutBtn").style.display = "inline-block";
                    document.getElementById("cashoutBtn").innerText = "Cashout (" + currentWin + " Coins)";
                }
            }

            function revealAllBombs() {
                const buttons = document.getElementById("grid").children;
                for(let i=0; i<buttons.length; i++) {
                    if(bombPositions.includes(i)) {
                        buttons[i].style.background = "#ef4444";
                        buttons[i].innerHTML = "💣";
                    }
                    buttons[i].disabled = true;
                }
            }

            function cashout() {
                if(!active) return;
                active = false;
                let profit = Math.floor(bet * currentMultiplier);
                let coins = getCoins() + profit;
                setCoins(coins);
                
                document.getElementById("statusMsg").innerHTML = "🎉 CASHED OUT! Won " + profit + " coins (" + currentMultiplier + "x)!";
                document.getElementById("statusMsg").style.color = "#10b981";
                document.getElementById("cashoutBtn").style.display = "none";
                document.getElementById("restartBtn").style.display = "inline-block";
                revealAllBombs();
            }

            function resetGame() { initGame(); }

            setCoins(getCoins());
            const grid = document.getElementById("grid");
            for(let i=0; i<totalCells; i++) {
                let b = document.createElement("button");
                b.style.height = "60px";
                b.style.background = "#1e293b";
                b.style.border = "2px solid #334155";
                b.style.borderRadius = "10px";
                b.style.fontSize = "16px";
                b.style.cursor = "pointer";
                b.style.color = "#fff";
                b.innerHTML = "▶️";
                b.onclick = () => initGame();
                grid.appendChild(b);
            }
            document.getElementById("statusMsg").innerHTML = "Click any tile above to place bet & play!";
        </script>
        """
    )
    st.components.v1.html(mines_html, height=540)

  elif gamble_game == "💥 TNT Crash Multiplier":
    st.subheader("💥 TNT Crash Multiplier")
    bet_crash = st.number_input(
        "Bet Amount:", min_value=10, max_value=100000, value=50, step=10, key="cb"
    )

    crash_html = (
        """
        <div style="text-align:center; background:linear-gradient(135deg, #090d16 0%, #171f33 100%); padding:30px; border-radius:16px; border:2px solid #f59e0b; font-family:sans-serif; box-shadow: 0 10px 25px rgba(0,0,0,0.5);">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px; background: rgba(0,0,0,0.3); padding: 10px 15px; border-radius: 10px;">
                <h3 style="color:#f59e0b; margin:0; font-size: 18px;">🧨 TNT CRASH</h3>
                <span style="background:#111827; color:#f59e0b; padding:6px 14px; border-radius:8px; font-weight:bold; border:1px solid #374151;">🪙 <span id="coinDisplay">1,000</span> Coins</span>
            </div>
            <h2 id="mult" style="color:#f59e0b; font-size:56px; margin:15px 0; font-weight: 900;">1.00x</h2>
            <div style="margin-top: 15px;">
                <button id="startBtn" onclick="startCrash()" style="background:#f59e0b; color:#000; border:none; padding:14px 32px; font-size:18px; font-weight:bold; border-radius:10px; cursor:pointer; margin-right:10px;">🚀 START RUN</button>
                <button id="outBtn" onclick="eject()" style="background:#10b981; color:white; border:none; padding:14px 32px; font-size:18px; font-weight:bold; border-radius:10px; cursor:pointer; display:none; margin-right:10px;">💰 CASH OUT</button>
                <button id="crashResetBtn" onclick="resetCrash()" style="background:#3b82f6; color:white; border:none; padding:14px 32px; font-size:18px; font-weight:bold; border-radius:10px; cursor:pointer; display:none;">🔄 Play Again</button>
            </div>
            <p id="cMsg" style="color:#fff; margin-top:18px; font-weight:bold; font-size: 15px;"></p>
        </div>
        <script>
            let mult = 1.00;
            let timer = null;
            let crashPoint = (1.0 + Math.random() * 4.2).toFixed(2);
            let activeRun = false;
            let bet = """
        + str(bet_crash)
        + """;

            function getCoins() { return parseInt(localStorage.getItem('arcade_coins') || '1000'); }
            function setCoins(val) { localStorage.setItem('arcade_coins', val); document.getElementById("coinDisplay").innerText = val.toLocaleString(); }
            setCoins(getCoins());

            function resetCrash() {
                mult = 1.00;
                crashPoint = (1.0 + Math.random() * 4.2).toFixed(2);
                activeRun = false;
                document.getElementById("mult").innerText = "1.00x";
                document.getElementById("mult").style.color = "#f59e0b";
                document.getElementById("startBtn").style.display = "inline-block";
                document.getElementById("outBtn").style.display = "none";
                document.getElementById("crashResetBtn").style.display = "none";
                document.getElementById("cMsg").innerText = "";
            }

            function startCrash() {
                let coins = getCoins();
                if(coins < bet) {
                    document.getElementById("cMsg").innerText = "⚠️ Not enough coins!";
                    document.getElementById("cMsg").style.color = "#ef4444";
                    return;
                }
                setCoins(coins - bet);
                document.getElementById("startBtn").style.display = "none";
                document.getElementById("outBtn").style.display = "inline-block";
                document.getElementById("cMsg").innerText = "";
                activeRun = true;
                
                timer = setInterval(() => {
                    mult += 0.04;
                    document.getElementById("mult").innerText = mult.toFixed(2) + "x";
                    if(mult >= crashPoint) {
                        clearInterval(timer);
                        activeRun = false;
                        document.getElementById("outBtn").style.display = "none";
                        document.getElementById("crashResetBtn").style.display = "inline-block";
                        document.getElementById("mult").style.color = "#ef4444";
                        document.getElementById("mult").innerText = "💥 CRASHED AT " + mult.toFixed(2) + "x";
                        document.getElementById("cMsg").innerText = "Lost " + bet + " coins!";
                        document.getElementById("cMsg").style.color = "#ef4444";
                    }
                }, 100);
            }

            function eject() {
                if(!activeRun) return;
                clearInterval(timer);
                activeRun = false;
                document.getElementById("outBtn").style.display = "none";
                document.getElementById("crashResetBtn").style.display = "inline-block";
                let win = Math.floor(bet * mult);
                setCoins(getCoins() + win);
                document.getElementById("cMsg").innerText = "🎉 Cashout Successful! Won " + win + " coins!";
                document.getElementById("cMsg").style.color = "#10b981";
            }
        </script>
        """
    )
    st.components.v1.html(crash_html, height=340)

  elif gamble_game == "🪙 Coinflip Dual (Animated)":
    st.subheader("🪙 Coinflip Dual (Animated)")
    cf_bet = st.number_input(
        "Bet Amount:", min_value=10, max_value=100000, value=50, step=10, key="cfb"
    )

    coin_html = (
        """
        <div style="text-align:center; background:linear-gradient(135deg, #100f24 0%, #291d4e 100%); padding:30px; border-radius:16px; border:2px solid #8b5cf6; font-family:sans-serif; box-shadow: 0 10px 25px rgba(0,0,0,0.5);">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px; background: rgba(0,0,0,0.3); padding: 10px 15px; border-radius: 10px;">
                <h3 style="color:#c084fc; margin:0; font-size: 18px;">🪙 COINFLIP (1.95x)</h3>
                <span style="background:#111827; color:#f59e0b; padding:6px 14px; border-radius:8px; font-weight:bold; border:1px solid #374151;">🪙 <span id="coinDisplay">1,000</span> Coins</span>
            </div>
            
            <div style="margin:25px auto; perspective: 1000px; width: 100px; height: 100px;">
                <div id="coin" style="width: 100%; height: 100%; position: relative; transform-style: preserve-3d; transition: transform 1.5s cubic-bezier(0.15, 0.85, 0.35, 1.2); border-radius: 50%;">
                    <div style="position: absolute; width: 100%; height: 100%; backface-visibility: hidden; border-radius: 50%; background: linear-gradient(135deg, #f59e0b, #b45309); display: flex; align-items: center; justify-content: center; font-size: 32px; font-weight: bold; color: #fff; border: 4px solid #fde68a;">H</div>
                    <div style="position: absolute; width: 100%; height: 100%; backface-visibility: hidden; border-radius: 50%; background: linear-gradient(135deg, #94a3b8, #475569); display: flex; align-items: center; justify-content: center; font-size: 32px; font-weight: bold; color: #fff; border: 4px solid #cbd5e1; transform: rotateY(180deg);">T</div>
                </div>
            </div>

            <div style="margin-bottom: 20px;">
                <button onclick="flip('HEADS')" style="background:#334155; color:white; border:2px solid #a855f7; padding:12px 26px; font-weight:bold; border-radius:10px; cursor:pointer; margin-right:12px;">👑 HEADS (H)</button>
                <button onclick="flip('TAILS')" style="background:#334155; color:white; border:2px solid #a855f7; padding:12px 26px; font-weight:bold; border-radius:10px; cursor:pointer;">🛡️ TAILS (T)</button>
            </div>
            <p id="cfMsg" style="color:#fff; font-weight:bold; margin:0; font-size: 15px;"></p>
        </div>
        <script>
            let bet = """
        + str(cf_bet)
        + """;
            function getCoins() { return parseInt(localStorage.getItem('arcade_coins') || '1000'); }
            function setCoins(val) { localStorage.setItem('arcade_coins', val); document.getElementById("coinDisplay").innerText = val.toLocaleString(); }
            setCoins(getCoins());

            function flip(choice) {
                let coins = getCoins();
                if(coins < bet) {
                    document.getElementById("cfMsg").innerText = "⚠️ Not enough coins!";
                    document.getElementById("cfMsg").style.color = "#ef4444";
                    return;
                }
                setCoins(coins - bet);
                document.getElementById("cfMsg").innerText = " Flipping coin...";
                document.getElementById("cfMsg").style.color = "#f59e0b";

                let coin = document.getElementById("coin");
                let outcome = Math.random() < 0.5 ? "HEADS" : "TAILS";
                
                let turns = (Math.floor(Math.random() * 3) + 4) * 360;
                let extra = outcome === "HEADS" ? 0 : 180;
                coin.style.transform = "rotateY(" + (turns + extra) + "deg)";

                setTimeout(() => {
                    if(choice === outcome) {
                        let win = Math.floor(bet * 1.95);
                        setCoins(getCoins() + win);
                        document.getElementById("cfMsg").innerText = "🎉 Result: " + outcome + "! You WON " + win + " coins!";
                        document.getElementById("cfMsg").style.color = "#10b981";
                    } else {
                        document.getElementById("cfMsg").innerText = "💥 Result: " + outcome + "! You LOST " + bet + " coins.";
                        document.getElementById("cfMsg").style.color = "#ef4444";
                    }
                }, 1500);
            }
        </script>
        """
    )
    st.components.v1.html(coin_html, height=360)

  elif gamble_game == "🎲 Lucky Dice (Adjustable Roll-Over)":
    st.subheader("🎲 Lucky Dice (Adjustable Roll-Over)")
    dice_bet = st.number_input(
        "Bet Amount:", min_value=10, max_value=100000, value=50, step=10, key="db"
    )
    roll_target = st.slider(
        "Roll Over Target:", min_value=10, max_value=90, value=50, step=1
    )

    dice_html = (
        """
        <div style="text-align:center; background:linear-gradient(135deg, #1b0f1e 0%, #4a1c38 100%); padding:30px; border-radius:16px; border:2px solid #ec4899; font-family:sans-serif; box-shadow: 0 10px 25px rgba(0,0,0,0.5);">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px; background: rgba(0,0,0,0.3); padding: 10px 15px; border-radius: 10px;">
                <h3 style="color:#f472b6; margin:0; font-size: 18px;">🎲 LUCKY DICE (Roll Over """
        + str(roll_target)
        + """)</h3>
                <span style="background:#111827; color:#f59e0b; padding:6px 14px; border-radius:8px; font-weight:bold; border:1px solid #374151;">🪙 <span id="coinDisplay">1,000</span> Coins</span>
            </div>
            
            <div id="diceBox" style="width:90px; height:90px; background:#1e293b; border:3px solid #ec4899; border-radius:16px; display:flex; align-items:center; justify-content:center; font-size:36px; color:#fff; margin:20px auto;">🎲</div>

            <button onclick="rollDice()" style="background:#ec4899; color:white; border:none; padding:14px 32px; font-size:16px; font-weight:bold; border-radius:10px; cursor:pointer;">🎲 ROLL DICE (> """
        + str(roll_target)
        + """)</button>
            <p id="dMsg" style="color:#fff; font-weight:bold; margin-top:18px; font-size: 15px;"></p>
        </div>
        <script>
            let bet = """
        + str(dice_bet)
        + """;
            let target = """
        + str(roll_target)
        + """;
            function getCoins() { return parseInt(localStorage.getItem('arcade_coins') || '1000'); }
            function setCoins(val) { localStorage.setItem('arcade_coins', val); document.getElementById("coinDisplay").innerText = val.toLocaleString(); }
            setCoins(getCoins());

            function rollDice() {
                let coins = getCoins();
                if(coins < bet) {
                    document.getElementById("dMsg").innerText = "⚠️ Not enough coins!";
                    document.getElementById("dMsg").style.color = "#ef4444";
                    return;
                }
                setCoins(coins - bet);
                document.getElementById("dMsg").innerText = "Rolling dice...";
                document.getElementById("dMsg").style.color = "#ec4899";
                
                let diceBox = document.getElementById("diceBox");
                let rollInterval = setInterval(() => {
                    diceBox.innerText = Math.floor(Math.random() * 100) + 1;
                }, 80);

                setTimeout(() => {
                    clearInterval(rollInterval);
                    let finalRoll = Math.floor(Math.random() * 100) + 1;
                    diceBox.innerText = finalRoll;

                    if(finalRoll > target) {
                        let winChance = (100 - target - 2) / 100; // House edge included
                        let mult = winChance > 0 ? (0.98 / (1 - (target/100))).toFixed(2) : 2.0;
                        let win = Math.floor(bet * mult);
                        setCoins(getCoins() + win);
                        document.getElementById("dMsg").innerText = "🎉 Rolled " + finalRoll + " (">" + target + ")! Won " + win + " coins (" + mult + "x)!";
                        document.getElementById("dMsg").style.color = "#10b981";
                    } else {
                        document.getElementById("dMsg").innerText = "💥 Rolled " + finalRoll + " (<= " + target + ")! Lost " + bet + " coins.";
                        document.getElementById("dMsg").style.color = "#ef4444";
                    }
                }, 1200);
            }
        </script>
        """
    )
    st.components.v1.html(dice_html, height=360)

  elif gamble_game == "🔻 Plinko (Physics Animation)":
    st.subheader("🔻 Plinko (Physics Animation)")
    plinko_bet = st.number_input(
        "Bet Amount:", min_value=10, max_value=100000, value=50, step=10, key="pb"
    )

    plinko_html = (
        """
        <div style="text-align:center; background:linear-gradient(135deg, #022330 0%, #083344 100%); padding:20px; border-radius:16px; border:2px solid #06b6d4; font-family:sans-serif; box-shadow: 0 10px 25px rgba(0,0,0,0.5);">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; background: rgba(0,0,0,0.3); padding: 8px 12px; border-radius: 10px;">
                <h3 style="color:#22d3ee; margin:0; font-size: 16px;">🔻 PLINKO ARENA</h3>
                <span style="background:#111827; color:#f59e0b; padding:4px 10px; border-radius:8px; font-weight:bold; border:1px solid #374151;">🪙 <span id="coinDisplay">1,000</span> Coins</span>
            </div>
            
            <canvas id="plinkoCanvas" width="340" height="240" style="background:#030712; border-radius:10px; border:2px solid #0e7490; display:block; margin: 10px auto;"></canvas>

            <button onclick="dropPlinkoBall()" style="background:#06b6d4; color:#000; border:none; padding:12px 28px; font-size:15px; font-weight:bold; border-radius:10px; cursor:pointer;">🔻 DROP BALL</button>
            <p id="pMsg" style="color:#fff; font-weight:bold; margin-top:10px; font-size: 14px;"></p>
        </div>
        <script>
            let bet = """
        + str(plinko_bet)
        + """;
            function getCoins() { return parseInt(localStorage.getItem('arcade_coins') || '1000'); }
            function setCoins(val) { localStorage.setItem('arcade_coins', val); document.getElementById("coinDisplay").innerText = val.toLocaleString(); }
            setCoins(getCoins());

            const canvas = document.getElementById("plinkoCanvas");
            const ctx = canvas.getContext("2d");

            function drawBoard(ballX = -10, ballY = -10) {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                // Draw Pins
                ctx.fillStyle = "#38bdf8";
                let rows = 5;
                for(let r=0; r<rows; r++) {
                    let pinsInRow = r + 3;
                    let spacingX = 45;
                    let startX = (canvas.width - (pinsInRow - 1) * spacingX) / 2;
                    for(let p=0; p<pinsInRow; p++) {
                        let px = startX + p * spacingX;
                        let py = 40 + r * 35;
                        ctx.beginPath();
                        ctx.arc(px, py, 4, 0, Math.PI * 2);
                        ctx.fill();
                    }
                }
                // Draw Ball if active
                if(ballX >= 0 && ballY >= 0) {
                    ctx.fillStyle = "#f59e0b";
                    ctx.beginPath();
                    ctx.arc(ballX, ballY, 7, 0, Math.PI * 2);
                    ctx.fill();
                }
            }
            drawBoard();

            function dropPlinkoBall() {
                let coins = getCoins();
                if(coins < bet) {
                    document.getElementById("pMsg").innerText = "⚠️ Not enough coins!";
                    document.getElementById("pMsg").style.color = "#ef4444";
                    return;
                }
                setCoins(coins - bet);
                document.getElementById("pMsg").innerText = "Ball dropping...";
                document.getElementById("pMsg").style.color = "#22d3ee";

                let bx = canvas.width / 2 + (Math.random() * 20 - 10);
                let by = 10;
                let vx = (Math.random() - 0.5) * 4;
                let vy = 2;

                let anim = setInterval(() => {
                    by += vy;
                    bx += vx;
                    vy += 0.2; // gravity

                    // Bounce off walls
                    if(bx < 15 || bx > canvas.width - 15) vx *= -0.8;

                    drawBoard(bx, by);

                    if(by >= 210) {
                        clearInterval(anim);
                        // Determine slot multiplier (5 slots)
                        let slotWidth = canvas.width / 5;
                        let slot = Math.floor(bx / slotWidth);
                        slot = Math.max(0, Math.min(4, slot));
                        let multipliers = [0.2, 0.8, 1.5, 3.0, 10.0];
                        let mult = multipliers[slot];
                        let win = Math.floor(bet * mult);
                        setCoins(getCoins() + win);

                        drawBoard();
                        if(mult >= 1.0) {
                            document.getElementById("pMsg").innerText = "🎯 Landed on " + mult + "x! Won " + win + " coins!";
                            document.getElementById("pMsg").style.color = "#10b981";
                        } else {
                            document.getElementById("pMsg").innerText = "💥 Landed on " + mult + "x. Returned " + win + " coins.";
                            document.getElementById("pMsg").style.color = "#ef4444";
                        }
                    }
                }, 30);
            }
        </script>
        """
    )
    st.components.v1.html(plinko_html, height=420)

  elif gamble_game == "🎡 Wheel of Fortune (Jackpot Wheel)":
    st.subheader("🎡 Wheel of Fortune (Jackpot Wheel)")
    wheel_bet = st.number_input(
        "Bet Amount:", min_value=10, max_value=100000, value=50, step=10, key="wb"
    )

    wheel_html = (
        """
        <div style="text-align:center; background:linear-gradient(135deg, #3b0764 0%, #581c87 100%); padding:25px; border-radius:16px; border:2px solid #d946ef; font-family:sans-serif; box-shadow: 0 10px 25px rgba(0,0,0,0.5);">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; background: rgba(0,0,0,0.3); padding: 8px 12px; border-radius: 10px;">
                <h3 style="color:#e879f9; margin:0; font-size: 16px;">🎡 JACKPOT WHEEL</h3>
                <span style="background:#111827; color:#f59e0b; padding:4px 10px; border-radius:8px; font-weight:bold; border:1px solid #374151;">🪙 <span id="coinDisplay">1,000</span> Coins</span>
            </div>
            
            <div style="position: relative; width: 140px; height: 140px; margin: 15px auto;">
                <div id="wheel" style="width: 100%; height: 100%; border-radius: 50%; background: conic-gradient(#ef4444 0deg 60deg, #f59e0b 60deg 120deg, #10b981 120deg 180deg, #06b6d4 180deg 240deg, #8b5cf6 240deg 300deg, #ec4899 300deg 360deg); border: 4px solid #fbcfe8; transition: transform 2.5s cubic-bezier(0.15, 0.85, 0.35, 1); display: flex; align-items: center; justify-content: center; box-shadow: 0 0 20px rgba(217,70,239,0.5);">
                    <div style="background: #111827; width: 35px; height: 35px; border-radius: 50%; border: 2px solid #fff;"></div>
                </div>
                <div style="position: absolute; top: -10px; left: 50%; transform: translateX(-50%); width: 0; height: 0; border-left: 8px solid transparent; border-right: 8px solid transparent; border-top: 15px solid #fff;"></div>
            </div>

            <button onclick="spinJackpot()" style="background:#d946ef; color:white; border:none; padding:12px 28px; font-size:15px; font-weight:bold; border-radius:10px; cursor:pointer;">🎡 SPIN WHEEL</button>
            <p id="wMsg" style="color:#fff; font-weight:bold; margin-top:12px; font-size: 14px;"></p>
        </div>
        <script>
            let bet = """
        + str(wheel_bet)
        + """;
            function getCoins() { return parseInt(localStorage.getItem('arcade_coins') || '1000'); }
            function setCoins(val) { localStorage.setItem('arcade_coins', val); document.getElementById("coinDisplay").innerText = val.toLocaleString(); }
            setCoins(getCoins());

            let currentRotation = 0;

            function spinJackpot() {
                let coins = getCoins();
                if(coins < bet) {
                    document.getElementById("wMsg").innerText = "⚠️ Not enough coins!";
                    document.getElementById("wMsg").style.color = "#ef4444";
                    return;
                }
                setCoins(coins - bet);
                document.getElementById("wMsg").innerText = "Spinning wheel...";
                document.getElementById("wMsg").style.color = "#e879f9";

                let wheel = document.getElementById("wheel");
                
                // 6 segments: 0x (60deg), 0.5x, 1.0x, 1.5x, 3.0x, 10x
                let segmentAngles = [30, 90, 150, 210, 270, 330];
                let weights = [0.38, 0.30, 0.18, 0.09, 0.04, 0.01]; // House edge
                let rand = Math.random();
                let cumulative = 0;
                let chosenIdx = 0;
                for(let i=0; i<weights.length; i++) {
                    cumulative += weights[i];
                    if(rand <= cumulative) { chosenIdx = i; break; }
                }

                let targetAngle = 360 - segmentAngles[chosenIdx];
                let spins = (Math.floor(Math.random() * 3) + 5) * 360;
                currentRotation = spins + targetAngle;
                wheel.style.transform = "rotate(" + currentRotation + "deg)";

                setTimeout(() => {
                    let multipliers = [0, 0.5, 1.0, 1.5, 3.0, 10.0];
                    let mult = multipliers[chosenIdx];
                    let win = Math.floor(bet * mult);
                    setCoins(getCoins() + win);

                    if(mult >= 1.0) {
                        document.getElementById("wMsg").innerText = "🎉 Jackpot! Hit " + mult + "x! Won " + win + " coins!";
                        document.getElementById("wMsg").style.color = "#10b981";
                    } else {
                        document.getElementById("wMsg").innerText = "💥 Hit " + mult + "x. Returned " + win + " coins.";
                        document.getElementById("wMsg").style.color = "#ef4444";
                    }
                }, 2500);
            }
        </script>
        """
    )
    st.components.v1.html(wheel_html, height=420)

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
