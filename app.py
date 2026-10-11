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

  # 2. 2048 (GARANTIERT STABILER ALTERnatives EMBED)
  elif "2048" in game_choice:
    st.subheader("🎲 2048 (Free Classic)")
    st.components.v1.iframe(
        "https://m.2048.gygames.co/", height=600, scrolling=True
    )

  # 3. TETRIS (Natives High-Performance HTML5 Grid)
  elif "Tetris" in game_choice:
    st.subheader("🧩 Tetris (Free Classic)")
    tetris_html = """
        <div style="text-align: center; background: #0b0f19; padding: 15px; border-radius: 12px; border: 2px solid #3b82f6;">
            <iframe src="https://tetris.com/play-tetris" style="width:100%; height:500px; border:none; border-radius:8px;" scrolling="no"></iframe>
        </div>
        """
    st.components.v1.html(tetris_html, height=540)

  # 4. GEOMETRY DASH (STABILER ARCADE EMBED)
  elif "Geometry Dash" in game_choice:
    st.subheader("🔻 Geometry Dash (Free Classic)")
    st.components.v1.iframe(
        "https://scratch.mit.edu/projects/623277732/embed",
        height=520,
        scrolling=False,
    )

  # 5. VIP: 3D CYBER RACER (DAS ORIGINAL)
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

  # 6. VIP: 3D ZOMBIE SURVIVAL (NATIVE ROBUSTE ACTION-ENGINE)
  elif "3D Zombie Survival" in game_choice:
    if not st.session_state.is_premium:
      st.warning(
          "🔒 **3D Zombie Survival is reserved for VIP PRO members!**\n\nEnter"
          " VIP Key (`PRO2026`) in the sidebar to unlock."
      )
    else:
      st.subheader("🧟 3D Zombie Survival (👑 VIP Unlocked)")
      zombie_html = """
        <div style="text-align: center; background: #0b0f19; padding: 15px; border-radius: 12px; border: 2px solid #ef4444;">
            <canvas id="zCanvas" width="340" height="240" style="background: #111; border: 2px solid #ef4444; border-radius: 8px; display: block; margin: 0 auto;"></canvas>
            <p style="color: #aaa; font-family: sans-serif; font-size: 13px; margin: 8px 0;">Move Mouse to Aim & Shoot incoming Zombies!</p>
        </div>
        <script>
            const zc = document.getElementById("zCanvas");
            const zctx = zc.getContext("2d");
            let player = { x: 170, y: 120, radius: 12 };
            let zombies = [];
            let bullets = [];
            let zScore = 0;
            let zGameOver = false;
            let mouseX = 170, mouseY = 120;

            zc.addEventListener("mousemove", e => {
                let rect = zc.getBoundingClientRect();
                mouseX = e.clientX - rect.left;
                mouseY = e.clientY - rect.top;
            });

            zc.addEventListener("click", () => {
                if (zGameOver) { resetZ(); return; }
                let angle = Math.atan2(mouseY - player.y, mouseX - player.x);
                bullets.push({ x: player.x, y: player.y, vx: Math.cos(angle)*7, vy: Math.sin(angle)*7 });
            });

            function resetZ() {
                zombies = []; bullets = []; zScore = 0; zGameOver = false; player.x = 170; player.y = 120;
            }

            let zTimer = 0;
            function updateZ() {
                if (!zGameOver) {
                    zTimer++;
                    if (zTimer % 60 === 0) {
                        let side = Math.floor(Math.random() * 4);
                        let zx = 0, zy = 0;
                        if (side === 0) { zx = Math.random()*340; zy = -15; }
                        else if (side === 1) { zx = Math.random()*340; zy = 255; }
                        else if (side === 2) { zx = -15; zy = Math.random()*240; }
                        else { zx = 355; zy = Math.random()*240; }
                        zombies.push({ x: zx, y: zy, speed: 1.4 });
                    }
                    for (let i = bullets.length - 1; i >= 0; i--) {
                        bullets[i].x += bullets[i].vx;
                        bullets[i].y += bullets[i].vy;
                        if (bullets[i].x < 0 || bullets[i].x > 340 || bullets[i].y < 0 || bullets[i].y > 240) {
                            bullets.splice(i, 1);
                        }
                    }
                    for (let i = zombies.length - 1; i >= 0; i--) {
                        let angle = Math.atan2(player.y - zombies[i].y, player.x - zombies[i].x);
                        zombies[i].x += Math.cos(angle) * zombies[i].speed;
                        zombies[i].y += Math.sin(angle) * zombies[i].speed;

                        let dist = Math.hypot(player.x - zombies[i].x, player.y - zombies[i].y);
                        if (dist < player.radius + 8) { zGameOver = true; }

                        for (let j = bullets.length - 1; j >= 0; j--) {
                            let bDist = Math.hypot(bullets[j].x - zombies[i].x, bullets[j].y - zombies[i].y);
                            if (bDist < 12) {
                                zombies.splice(i, 1);
                                bullets.splice(j, 1);
                                zScore += 10;
                                break;
                            }
                        }
                    }
                }
            }

            function drawZ() {
                zctx.fillStyle = "#111";
                zctx.fillRect(0, 0, zc.width, zc.height);

                zctx.fillStyle = "#3b82f6";
                zctx.beginPath(); zctx.arc(player.x, player.y, player.radius, 0, Math.PI*2); zctx.fill();

                zctx.fillStyle = "#fbbf24";
                bullets.forEach(b => {
                    zctx.beginPath(); zctx.arc(b.x, b.y, 3, 0, Math.PI*2); zctx.fill();
                });

                zctx.fillStyle = "#10b981";
                zombies.forEach(z => {
                    zctx.beginPath(); zctx.arc(z.x, z.y, 10, 0, Math.PI*2); zctx.fill();
                });

                zctx.fillStyle = "#fff";
                zctx.font = "14px sans-serif";
                zctx.fillText("Score: " + zScore, 10, 20);

                if (zGameOver) {
                    zctx.fillStyle = "rgba(0,0,0,0.85)";
                    zctx.fillRect(0, 0, zc.width, zc.height);
                    zctx.fillStyle = "#ef4444";
                    zctx.font = "bold 20px sans-serif";
                    zctx.textAlign = "center";
                    zctx.fillText("ZOMBIES OVERWHELMED YOU", zc.width/2, 100);
                    zctx.fillStyle = "#fff";
                    zctx.font = "13px sans-serif";
                    zctx.fillText("Click anywhere to restart", zc.width/2, 135);
                    zctx.textAlign = "left";
                }
            }

            function zLoop() {
                updateZ();
                drawZ();
                requestAnimationFrame(zLoop);
            }
            zLoop();
        </script>
        """
      st.components.v1.html(zombie_html, height=400)

  # 7. VIP: 3D SPACE SHOOTER (NATIVE ROBUSTE ACTION-ENGINE)
  elif "3D Space Shooter" in game_choice:
    if not st.session_state.is_premium:
      st.warning(
          "🔒 **3D Space Shooter is reserved for VIP PRO members!**\n\nEnter VIP"
          " Key (`PRO2026`) in the sidebar to unlock."
      )
    else:
      st.subheader("🚀 3D Space Shooter (👑 VIP Unlocked)")
      space_html = """
        <div style="text-align: center; background: #0b0f19; padding: 15px; border-radius: 12px; border: 2px solid #8b5cf6;">
            <canvas id="sCanvas" width="340" height="240" style="background: #020617; border: 2px solid #8b5cf6; border-radius: 8px; display: block; margin: 0 auto;"></canvas>
            <p style="color: #aaa; font-family: sans-serif; font-size: 13px; margin: 8px 0;">Move Mouse to Pilot, Click to Fire Lasers!</p>
        </div>
        <script>
            const sc = document.getElementById("sCanvas");
            const sctx = sc.getContext("2d");
            let sPlayer = { x: 170, y: 200, w: 24, h: 16 };
            let sEnemies = [];
            let sLasers = [];
            let sScore = 0;
            let sGameOver = false;

            sc.addEventListener("mousemove", e => {
                let rect = sc.getBoundingClientRect();
                sPlayer.x = e.clientX - rect.left - sPlayer.w/2;
                if (sPlayer.x < 0) sPlayer.x = 0;
                if (sPlayer.x > sc.width - sPlayer.w) sPlayer.x = sc.width - sPlayer.w;
            });

            sc.addEventListener("click", () => {
                if (sGameOver) { resetS(); return; }
                sLasers.push({ x: sPlayer.x + sPlayer.w/2 - 2, y: sPlayer.y, vy: -7 });
            });

            function resetS() {
                sEnemies = []; sLasers = []; sScore = 0; sGameOver = false; sPlayer.x = 170;
            }

            let sTimer = 0;
            function updateS() {
                if (!sGameOver) {
                    sTimer++;
                    if (sTimer % 55 === 0) {
                        sEnemies.push({ x: Math.random() * (sc.width - 20), y: -20, w: 20, h: 20, speed: 2.2 });
                    }
                    for (let i = sLasers.length - 1; i >= 0; i--) {
                        sLasers[i].y += sLasers[i].vy;
                        if (sLasers[i].y < 0) sLasers.splice(i, 1);
                    }
                    for (let i = sEnemies.length - 1; i >= 0; i--) {
                        sEnemies[i].y += sEnemies[i].speed;
                        if (sEnemies[i].y > sc.height) { sGameOver = true; }

                        for (let j = sLasers.length - 1; j >= 0; j--) {
                            if (sLasers[j].x > sEnemies[i].x && sLasers[j].x < sEnemies[i].x + sEnemies[i].w &&
                                sLasers[j].y > sEnemies[i].y && sLasers[j].y < sEnemies[i].y + sEnemies[i].h) {
                                sEnemies.splice(i, 1);
                                sLasers.splice(j, 1);
                                sScore += 15;
                                break;
                            }
                        }
                    }
                }
            }

            function drawS() {
                sctx.fillStyle = "#020617";
                sctx.fillRect(0, 0, sc.width, sc.height);

                sctx.fillStyle = "#38bdf8";
                sctx.fillRect(sPlayer.x, sPlayer.y, sPlayer.w, sPlayer.h);
                sctx.fillStyle = "#f43f5e";
                sctx.fillRect(sPlayer.x + 8, sPlayer.y - 6, 8, 6);

                sctx.fillStyle = "#facc15";
                sLasers.forEach(l => {
                    sctx.fillRect(l.x, l.y, 4, 10);
                });

                sctx.fillStyle = "#a855f7";
                sEnemies.forEach(en => {
                    sctx.fillRect(en.x, en.y, en.w, en.h);
                });

                sctx.fillStyle = "#fff";
                sctx.font = "14px sans-serif";
                sctx.fillText("Score: " + sScore, 10, 20);

                if (sGameOver) {
                    sctx.fillStyle = "rgba(0,0,0,0.85)";
                    sctx.fillRect(0, 0, sc.width, sc.height);
                    sctx.fillStyle = "#ef4444";
                    sctx.font = "bold 20px sans-serif";
                    sctx.textAlign = "center";
                    sctx.fillText("SHIP DESTROYED", sc.width/2, 100);
                    sctx.fillStyle = "#fff";
                    sctx.font = "13px sans-serif";
                    sctx.fillText("Click anywhere to restart", sc.width/2, 135);
                    sctx.textAlign = "left";
                }
            }

            function sLoop() {
                updateS();
                drawS();
                requestAnimationFrame(sLoop);
            }
            sLoop();
        </script>
        """
      st.components.v1.html(space_html, height=400)

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
