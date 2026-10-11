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
    st.components.v1.iframe(
        "https://play2048.co/", height=600, scrolling=True
    )

  # 3. TETRIS (Native Optimized Canvas)
  elif "Tetris" in game_choice:
    st.subheader("🧩 Tetris (Free Classic)")
    tetris_html = """
        <div style="text-align: center; background: #0b0f19; padding: 15px; border-radius: 12px; border: 2px solid #3b82f6;">
            <canvas id="tetris" width="200" height="350" style="background-color: #000; border: 2px solid #3b82f6; border-radius: 8px; display: block; margin: 0 auto;"></canvas>
            <p style="color: #888; font-family: sans-serif; font-size: 13px; margin: 8px 0;">Controls: Arrow Keys to Move/Rotate, Down to Drop</p>
            <div style="display: flex; justify-content: center; gap: 8px; margin-top: 10px;">
                <button onclick="playerMove(-1)" style="background: #1f2937; color: white; border: 1px solid #3b82f6; padding: 8px 14px; border-radius: 6px; cursor: pointer;">⬅️</button>
                <button onclick="playerRotate()" style="background: #1f2937; color: white; border: 1px solid #3b82f6; padding: 8px 14px; border-radius: 6px; cursor: pointer;">🔄</button>
                <button onclick="playerDrop()" style="background: #1f2937; color: white; border: 1px solid #3b82f6; padding: 8px 14px; border-radius: 6px; cursor: pointer;">⬇️</button>
                <button onclick="playerMove(1)" style="background: #1f2937; color: white; border: 1px solid #3b82f6; padding: 8px 14px; border-radius: 6px; cursor: pointer;">➡️</button>
            </div>
        </div>
        <script>
            const canvas = document.getElementById('tetris');
            const context = canvas.getContext('2d');
            context.scale(20, 20);
            function arenaSweep() {
                let rowCount = 1;
                outer: for (let y = arena.length - 1; y > 0; --y) {
                    for (let x = 0; x < arena[y].length; ++x) { if (arena[y][x] === 0) continue outer; }
                    const row = arena.splice(y, 1)[0].fill(0);
                    arena.unshift(row); ++y;
                }
            }
            function collide(arena, player) {
                const [m, o] = [player.matrix, player.pos];
                for (let y = 0; y < m.length; ++y) {
                    for (let x = 0; x < m[y].length; ++x) {
                        if (m[y][x] !== 0 && (arena[y + o.y] && arena[y + o.y][x + o.x]) !== 0) return true;
                    }
                }
                return false;
            }
            function createMatrix(w, h) {
                const matrix = [];
                while (h--) matrix.push(new Array(w).fill(0));
                return matrix;
            }
            function createPiece(type) {
                if (type === 'T') return [[0, 1, 0], [1, 1, 1], [0, 0, 0]];
                else if (type === 'O') return [[2, 2], [2, 2]];
                else if (type === 'L') return [[0, 0, 3], [3, 3, 3], [0, 0, 0]];
                else if (type === 'J') return [[4, 0, 0], [4, 4, 4], [0, 0, 0]];
                else if (type === 'I') return [[0, 5, 0, 0], [0, 5, 0, 0], [0, 5, 0, 0], [0, 5, 0, 0]];
                else if (type === 'S') return [[0, 6, 6], [6, 6, 0], [0, 0, 0]];
                else if (type === 'Z') return [[7, 7, 0], [0, 7, 7], [0, 0, 0]];
            }
            function drawMatrix(matrix, offset) {
                matrix.forEach((row, y) => {
                    row.forEach((value, x) => {
                        if (value !== 0) { context.fillStyle = colors[value]; context.fillRect(x + offset.x, y + offset.y, 1, 1); }
                    });
                });
            }
            function draw() {
                context.fillStyle = '#000'; context.fillRect(0, 0, canvas.width, canvas.height);
                drawMatrix(arena, {x: 0, y: 0}); drawMatrix(player.matrix, player.pos);
            }
            function merge(arena, player) {
                player.matrix.forEach((row, y) => {
                    row.forEach((value, x) => { if (value !== 0) arena[y + player.pos.y][x + player.pos.x] = value; });
                });
            }
            function playerDrop() {
                player.pos.y++;
                if (collide(arena, player)) { player.pos.y--; merge(arena, player); playerReset(); arenaSweep(); }
                dropCounter = 0;
            }
            function playerMove(dir) {
                player.pos.x += dir;
                if (collide(arena, player)) player.pos.x -= dir;
            }
            function playerReset() {
                const pieces = 'TJLOSZI';
                player.matrix = createPiece(pieces[(pieces.length * Math.random()) | 0]);
                player.pos.y = 0;
                player.pos.x = (arena[0].length / 2 | 0) - (player.matrix[0].length / 2 | 0);
                if (collide(arena, player)) arena.forEach(row => row.fill(0));
            }
            function playerRotate() {
                const posX = player.pos.x; let offset = 1;
                rotate(player.matrix);
                while (collide(arena, player)) {
                    player.pos.x += offset; offset = -(offset + (offset > 0 ? 1 : -1));
                    if (offset > player.matrix[0].length) { rotate(player.matrix); player.pos.x = posX; return; }
                }
            }
            function rotate(matrix) {
                for (let y = 0; y < matrix.length; ++y) {
                    for (let x = 0; x < y; ++x) { [matrix[x][y], matrix[y][x]] = [matrix[y][x], matrix[x][y]]; }
                }
                matrix.forEach(row => row.reverse());
            }
            let dropCounter = 0, dropInterval = 1000, lastTime = 0;
            function update(time = 0) {
                const deltaTime = time - lastTime; lastTime = time;
                dropCounter += deltaTime;
                if (dropCounter > dropInterval) playerDrop();
                draw();
                requestAnimationFrame(update);
            }
            const colors = [null, '#FF0D72', '#0DC2FF', '#0DFF72', '#F538FF', '#FF8E0D', '#FFE138', '#3877FF'];
            const arena = createMatrix(10, 17);
            const player = {pos: {x: 0, y: 0}, matrix: null};
            document.addEventListener('keydown', event => {
                if (event.keyCode === 37) playerMove(-1);
                else if (event.keyCode === 39) playerMove(1);
                else if (event.keyCode === 40) playerDrop();
                else if (event.keyCode === 38) playerRotate();
            });
            playerReset(); update();
        </script>
        """
    st.components.v1.html(tetris_html, height=520)

  # 4. GEOMETRY DASH (Native Arcade Runner)
  elif "Geometry Dash" in game_choice:
    st.subheader("🔻 Geometry Dash (Free Classic)")
    gd_html = """
        <div style="text-align: center; background: #0b0f19; padding: 15px; border-radius: 12px; border: 2px solid #ec4899;">
            <canvas id="gdCanvas" width="340" height="200" style="background: linear-gradient(to bottom, #1e1b4b, #311042); border: 2px solid #ec4899; border-radius: 8px; display: block; margin: 0 auto; cursor: pointer;"></canvas>
            <p style="color: #aaa; font-family: sans-serif; font-size: 13px; margin: 10px 0;">Tap screen or press Spacebar to Jump over spikes!</p>
            <button onclick="jump()" style="background: #ec4899; color: white; border: none; padding: 10px 30px; font-size: 16px; font-weight: bold; border-radius: 8px; cursor: pointer;">JUMP 🚀</button>
        </div>
        <script>
            const canvas = document.getElementById("gdCanvas");
            const ctx = canvas.getContext("2d");
            let cube = { x: 50, y: 140, size: 25, vy: 0, gravity: 0.8, jumpForce: -11, grounded: true };
            let obstacles = [];
            let score = 0;
            let gameOver = false;
            let frameCount = 0;

            function jump() {
                if (cube.grounded && !gameOver) {
                    cube.vy = cube.jumpForce;
                    cube.grounded = false;
                } else if (gameOver) {
                    resetGame();
                }
            }

            document.addEventListener("keydown", e => {
                if (e.code === "Space" || e.code === "ArrowUp") {
                    e.preventDefault();
                    jump();
                }
            });

            canvas.addEventListener("click", () => jump());

            function resetGame() {
                cube.y = 140; cube.vy = 0; cube.grounded = true;
                obstacles = []; score = 0; gameOver = false;
            }

            function update() {
                if (!gameOver) {
                    frameCount++;
                    cube.vy += cube.gravity;
                    cube.y += cube.vy;
                    if (cube.y >= 140) {
                        cube.y = 140; cube.vy = 0; cube.grounded = true;
                    }
                    if (frameCount % 90 === 0) {
                        obstacles.push({ x: 340, y: 145, w: 20, speed: 4.5 });
                    }
                    for (let i = obstacles.length - 1; i >= 0; i--) {
                        obstacles[i].x -= obstacles[i].speed;
                        // Collision check
                        if (cube.x < obstacles[i].x + obstacles[i].w &&
                            cube.x + cube.size > obstacles[i].x &&
                            cube.y < obstacles[i].y + 20 &&
                            cube.y + cube.size > obstacles[i].y) {
                            gameOver = true;
                        }
                        if (obstacles[i].x + obstacles[i].w < 0) {
                            obstacles.splice(i, 1);
                            score += 10;
                        }
                    }
                }
            }

            function draw() {
                ctx.fillStyle = "#1e1b4b";
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                
                // Ground line
                ctx.strokeStyle = "#ec4899";
                ctx.lineWidth = 3;
                ctx.beginPath();
                ctx.moveTo(0, 165);
                ctx.lineTo(340, 165);
                ctx.stroke();

                // Draw Cube
                ctx.fillStyle = "#00ffcc";
                ctx.fillRect(cube.x, cube.y, cube.size, cube.size);
                ctx.strokeStyle = "#fff";
                ctx.lineWidth = 2;
                ctx.strokeRect(cube.x, cube.y, cube.size, cube.size);

                // Draw Obstacles (Spikes)
                ctx.fillStyle = "#f43f5e";
                obstacles.forEach(obs => {
                    ctx.beginPath();
                    ctx.moveTo(obs.x, obs.y + 20);
                    ctx.lineTo(obs.x + obs.w / 2, obs.y);
                    ctx.lineTo(obs.x + obs.w, obs.y + 20);
                    ctx.fill();
                });

                // Score
                ctx.fillStyle = "#ffffff";
                ctx.font = "16px sans-serif";
                ctx.fillText("Score: " + score, 15, 25);

                if (gameOver) {
                    ctx.fillStyle = "rgba(0, 0, 0, 0.75)";
                    ctx.fillRect(0, 0, canvas.width, canvas.height);
                    ctx.fillStyle = "#ff4444";
                    ctx.font = "bold 22px sans-serif";
                    ctx.textAlign = "center";
                    ctx.fillText("GAME OVER", canvas.width / 2, 80);
                    ctx.fillStyle = "#ffffff";
                    ctx.font = "14px sans-serif";
                    ctx.fillText("Click or Press Space to Restart", canvas.width / 2, 115);
                    ctx.textAlign = "left";
                }
            }

            function loop() {
                update();
                draw();
                requestAnimationFrame(loop);
            }
            loop();
        </script>
        """
    st.components.v1.html(gd_html, height=360)

  # 5. VIP: 3D CYBER RACER
  elif "3D Cyber Racer" in game_choice:
    if not st.session_state.is_premium:
      st.warning(
          "🔒 **3D Cyber Racer is reserved for VIP PRO members!**\n\nEnter VIP Key"
          " (`PRO2026`) in the sidebar to unlock."
      )
    else:
      st.subheader("🏎️ 3D Cyber Racer (👑 VIP Unlocked)")
      st.markdown(
          '<a href="https://hexgl.bkcore.com/play/" target="_blank"'
          ' style="display: inline-block; background-color: #00ffcc; color:'
          ' #0b0f19; padding: 10px 20px; font-weight: bold; border-radius:'
          ' 6px; text-decoration: none; margin-bottom: 12px;">🚀 Launch Fullscreen'
          ' Mode</a>',
          unsafe_allow_html=True,
      )
      st.components.v1.iframe(
          "https://hexgl.bkcore.com/play/", height=550, scrolling=False
      )

  # 6. VIP: 3D ZOMBIE SURVIVAL (Native Canvas Action)
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
            <canvas id="zCanvas" width="340" height="220" style="background: #111; border: 2px solid #ef4444; border-radius: 8px; display: block; margin: 0 auto;"></canvas>
            <p style="color: #aaa; font-family: sans-serif; font-size: 13px; margin: 8px 0;">Move Mouse to Aim, Click to Shoot Zombies!</p>
        </div>
        <script>
            const zc = document.getElementById("zCanvas");
            const zctx = zc.getContext("2d");
            let player = { x: 170, y: 110, radius: 12 };
            let zombies = [];
            let bullets = [];
            let zScore = 0;
            let zGameOver = false;
            let mouseX = 170, mouseY = 110;

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
                zombies = []; bullets = []; zScore = 0; zGameOver = false; player.x = 170; player.y = 110;
            }

            let zTimer = 0;
            function updateZ() {
                if (!zGameOver) {
                    zTimer++;
                    if (zTimer % 70 === 0) {
                        let side = Math.floor(Math.random() * 4);
                        let zx = 0, zy = 0;
                        if (side === 0) { zx = Math.random()*340; zy = -15; }
                        else if (side === 1) { zx = Math.random()*340; zy = 235; }
                        else if (side === 2) { zx = -15; zy = Math.random()*220; }
                        else { zx = 355; zy = Math.random()*220; }
                        zombies.push({ x: zx, y: zy, speed: 1.2 });
                    }
                    // Bullet update
                    for (let i = bullets.length - 1; i >= 0; i--) {
                        bullets[i].x += bullets[i].vx;
                        bullets[i].y += bullets[i].vy;
                        if (bullets[i].x < 0 || bullets[i].x > 340 || bullets[i].y < 0 || bullets[i].y > 220) {
                            bullets.splice(i, 1);
                        }
                    }
                    // Zombie update
                    for (let i = zombies.length - 1; i >= 0; i--) {
                        let angle = Math.atan2(player.y - zombies[i].y, player.x - zombies[i].x);
                        zombies[i].x += Math.cos(angle) * zombies[i].speed;
                        zombies[i].y += Math.sin(angle) * zombies[i].speed;

                        // Check collision with player
                        let dist = Math.hypot(player.x - zombies[i].x, player.y - zombies[i].y);
                        if (dist < player.radius + 8) { zGameOver = true; }

                        // Check bullet collision
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

                // Player
                zctx.fillStyle = "#3b82f6";
                zctx.beginPath(); zctx.arc(player.x, player.y, player.radius, 0, Math.PI*2); zctx.fill();

                // Bullets
                zctx.fillStyle = "#fbbf24";
                bullets.forEach(b => {
                    zctx.beginPath(); zctx.arc(b.x, b.y, 3, 0, Math.PI*2); zctx.fill();
                });

                // Zombies
                zctx.fillStyle = "#10b981";
                zombies.forEach(z => {
                    zctx.beginPath(); zctx.arc(z.x, z.y, 10, 0, Math.PI*2); zctx.fill();
                });

                zctx.fillStyle = "#fff";
                zctx.font = "14px sans-serif";
                zctx.fillText("Score: " + zScore, 10, 20);

                if (zGameOver) {
                    zctx.fillStyle = "rgba(0,0,0,0.8)";
                    zctx.fillRect(0, 0, zc.width, zc.height);
                    zctx.fillStyle = "#ef4444";
                    zctx.font = "bold 20px sans-serif";
                    zctx.textAlign = "center";
                    zctx.fillText("ZOMBIES GOT YOU!", zc.width/2, 90);
                    zctx.fillStyle = "#fff";
                    zctx.font = "13px sans-serif";
                    zctx.fillText("Click anywhere to restart", zc.width/2, 125);
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
      st.components.v1.html(zombie_html, height=380)

  # 7. VIP: 3D SPACE SHOOTER (Native Canvas Arcade)
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
            <canvas id="sCanvas" width="340" height="220" style="background: #020617; border: 2px solid #8b5cf6; border-radius: 8px; display: block; margin: 0 auto;"></canvas>
            <p style="color: #aaa; font-family: sans-serif; font-size: 13px; margin: 8px 0;">Move Mouse to Pilot Ship, Click to Fire Lasers!</p>
        </div>
        <script>
            const sc = document.getElementById("sCanvas");
            const sctx = sc.getContext("2d");
            let sPlayer = { x: 170, y: 180, w: 24, h: 16 };
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
                sLasers.push({ x: sPlayer.x + sPlayer.w/2 - 2, y: sPlayer.y, vy: -6 });
            });

            function resetS() {
                sEnemies = []; sLasers = []; sScore = 0; sGameOver = false; sPlayer.x = 170;
            }

            let sTimer = 0;
            function updateS() {
                if (!sGameOver) {
                    sTimer++;
                    if (sTimer % 60 === 0) {
                        sEnemies.push({ x: Math.random() * (sc.width - 20), y: -20, w: 20, h: 20, speed: 2 });
                    }
                    for (let i = sLasers.length - 1; i >= 0; i--) {
                        sLasers[i].y += sLasers[i].vy;
                        if (sLasers[i].y < 0) sLasers.splice(i, 1);
                    }
                    for (let i = sEnemies.length - 1; i >= 0; i--) {
                        sEnemies[i].y += sEnemies[i].speed;
                        if (sEnemies[i].y > sc.height) { sGameOver = true; }

                        // Laser collision
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

                // Player Ship
                sctx.fillStyle = "#38bdf8";
                sctx.fillRect(sPlayer.x, sPlayer.y, sPlayer.w, sPlayer.h);
                sctx.fillStyle = "#f43f5e";
                sctx.fillRect(sPlayer.x + 8, sPlayer.y - 6, 8, 6);

                // Lasers
                sctx.fillStyle = "#facc15";
                sLasers.forEach(l => {
                    sctx.fillRect(l.x, l.y, 4, 10);
                });

                // Enemies
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
                    sctx.fillText("SHIP DESTROYED", sc.width/2, 90);
                    sctx.fillStyle = "#fff";
                    sctx.font = "13px sans-serif";
                    sctx.fillText("Click anywhere to restart", sc.width/2, 125);
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
      st.components.v1.html(space_html, height=380)

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
