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
          "🧩 Tetris (Free Local)",
          "🔻 Geometry Dash (Free Classic)",
          "🏎️ 3D Cyber Racer (👑 VIP)",
          "🧟 3D Zombie Survival (👑 VIP)",
          "🚀 3D Space Shooter (👑 VIP)",
      ],
  )

  # FREE GAME 1: Snake (Embedded HTML5)
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

  # FREE GAME 2: 2048
  elif "2048" in game_choice:
    st.subheader("🎲 2048 (Free Classic)")
    st.components.v1.iframe(
        "https://play2048.co/", height=600, scrolling=True
    )

  # FREE GAME 3: Tetris (Local HTML5 Canvas - No 404 Errors)
  elif "Tetris" in game_choice:
    st.subheader("🧩 Tetris (Free Local Classic)")
    tetris_html = """
        <div style="text-align: center; background: #0b0f19; padding: 15px; border-radius: 12px; border: 2px solid #3b82f6;">
            <canvas id="tetris" width="240" height="400" style="background-color: #000; border: 2px solid #3b82f6; border-radius: 8px; display: block; margin: 0 auto;"></canvas>
            <p style="color: #888; font-family: sans-serif; font-size: 13px; margin: 10px 0;">Controls: Arrow Left/Right to Move, Arrow Up to Rotate, Down to Drop</p>
            <div style="display: flex; justify-content: center; gap: 10px; margin-top: 10px;">
                <button onclick="playerMove(-1)" style="background: #1f2937; color: white; border: 1px solid #3b82f6; padding: 10px 15px; border-radius: 6px; cursor: pointer;">⬅️</button>
                <button onclick="playerRotate()" style="background: #1f2937; color: white; border: 1px solid #3b82f6; padding: 10px 15px; border-radius: 6px; cursor: pointer;">🔄</button>
                <button onclick="playerDrop()" style="background: #1f2937; color: white; border: 1px solid #3b82f6; padding: 10px 15px; border-radius: 6px; cursor: pointer;">⬇️</button>
                <button onclick="playerMove(1)" style="background: #1f2937; color: white; border: 1px solid #3b82f6; padding: 10px 15px; border-radius: 6px; cursor: pointer;">➡️</button>
            </div>
        </div>
        <script>
            const canvas = document.getElementById('tetris');
            const context = canvas.getContext('2d');
            context.scale(20, 20);

            function arenaSweep() {
                let rowCount = 1;
                outer: for (let y = arena.length - 1; y > 0; --y) {
                    for (let x = 0; x < arena[y].length; ++x) {
                        if (arena[y][x] === 0) {
                            continue outer;
                        }
                    }
                    const row = arena.splice(y, 1)[0].fill(0);
                    arena.unshift(row);
                    ++y;
                }
            }

            function collide(arena, player) {
                const [m, o] = [player.matrix, player.pos];
                for (let y = 0; y < m.length; ++y) {
                    for (let x = 0; x < m[y].length; ++x) {
                        if (m[y][x] !== 0 && (arena[y + o.y] && arena[y + o.y][x + o.x]) !== 0) {
                            return true;
                        }
                    }
                }
                return false;
            }

            function createMatrix(w, h) {
                const matrix = [];
                while (h--) {
                    matrix.push(new Array(w).fill(0));
                }
                return matrix;
            }

            function createPiece(type) {
                if (type === 'T') {
                    return [[0, 1, 0], [1, 1, 1], [0, 0, 0]];
                } else if (type === 'O') {
                    return [[2, 2], [2, 2]];
                } else if (type === 'L') {
                    return [[0, 0, 3], [3, 3, 3], [0, 0, 0]];
                } else if (type === 'J') {
                    return [[4, 0, 0], [4, 4, 4], [0, 0, 0]];
                } else if (type === 'I') {
                    return [[0, 5, 0, 0], [0, 5, 0, 0], [0, 5, 0, 0], [0, 5, 0, 0]];
                } else if (type === 'S') {
                    return [[0, 6, 6], [6, 6, 0], [0, 0, 0]];
                } else if (type === 'Z') {
                    return [[7, 7, 0], [0, 7, 7], [0, 0, 0]];
                }
            }

            function drawMatrix(matrix, offset) {
                matrix.forEach((row, y) => {
                    row.forEach((value, x) => {
                        if (value !== 0) {
                            context.fillStyle = colors[value];
                            context.fillRect(x + offset.x, y + offset.y, 1, 1);
                        }
                    });
                });
            }

            function draw() {
                context.fillStyle = '#000';
                context.fillRect(0, 0, canvas.width, canvas.height);
                drawMatrix(arena, {x: 0, y: 0});
                drawMatrix(player.matrix, player.pos);
            }

            function merge(arena, player) {
                player.matrix.forEach((row, y) => {
                    row.forEach((value, x) => {
                        if (value !== 0) {
                            arena[y + player.pos.y][x + player.pos.x] = value;
                        }
                    });
                });
            }

            function playerDrop() {
                player.pos.y++;
                if (collide(arena, player)) {
                    player.pos.y--;
                    merge(arena, player);
                    playerReset();
                    arenaSweep();
                }
                dropCounter = 0;
            }

            function playerMove(dir) {
                player.pos.x += dir;
                if (collide(arena, player)) {
                    player.pos.x -= dir;
                }
            }

            function playerReset() {
                const pieces = 'TJLOSZI';
                player.matrix = createPiece(pieces[(pieces.length * Math.random()) | 0]);
                player.pos.y = 0;
                player.pos.x = (arena[0].length / 2 | 0) - (player.matrix[0].length / 2 | 0);
                if (collide(arena, player)) {
                    arena.forEach(row => row.fill(0));
                }
            }

            function playerRotate() {
                const posX = player.pos.x;
                let offset = 1;
                rotate(player.matrix);
                while (collide(arena, player)) {
                    player.pos.x += offset;
                    offset = -(offset + (offset > 0 ? 1 : -1));
                    if (offset > player.matrix[0].length) {
                        rotate(player.matrix);
                        player.pos.x = posX;
                        return;
                    }
                }
            }

            function rotate(matrix) {
                for (let y = 0; y < matrix.length; ++y) {
                    for (let x = 0; x < y; ++x) {
                        matrix[x][y] = matrix[y][x];
                        matrix[y][x] = matrix[x][y];
                    }
                }
                matrix.forEach(row => row.reverse());
            }

            let dropCounter = 0;
            let dropInterval = 1000;
            let lastTime = 0;

            function update(time = 0) {
                const deltaTime = time - lastTime;
                lastTime = time;
                dropCounter += deltaTime;
                if (dropCounter > dropInterval) {
                    playerDrop();
                }
                draw();
                requestAnimationFrame(update);
            }

            const colors = [null, '#FF0D72', '#0DC2FF', '#0DFF72', '#F538FF', '#FF8E0D', '#FFE138', '#3877FF'];
            const arena = createMatrix(12, 20);
            const player = {pos: {x: 0, y: 0}, matrix: null};

            document.addEventListener('keydown', event => {
                if (event.keyCode === 37) playerMove(-1);
                else if (event.keyCode === 39) playerMove(1);
                else if (event.keyCode === 40) playerDrop();
                else if (event.keyCode === 38) playerRotate();
            });

            playerReset();
            update();
        </script>
        """
    st.components.v1.html(tetris_html, height=540)

  # FREE GAME 4: Geometry Dash
  elif "Geometry Dash" in game_choice:
    st.subheader("🔻 Geometry Dash (Free Classic)")
    st.info("🕹️ **Controls:** Tap screen or use Spacebar / Up Arrow to jump!")
    st.components.v1.iframe(
        "https://scratch.mit.edu/projects/623277732/embed",
        height=520,
        scrolling=False,
    )

  # VIP GAME 1: 3D Cyber Racer
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

  # VIP GAME 2: 3D Zombie Survival
  elif "3D Zombie Survival" in game_choice:
    if not st.session_state.is_premium:
      st.warning(
          "🔒 **3D Zombie Survival is reserved for VIP PRO members!**\n\nEnter"
          " VIP Key (`PRO2026`) in the sidebar to unlock."
      )
    else:
      st.subheader("🧟 3D Zombie Survival (👑 VIP Unlocked)")
      st.components.v1.iframe(
          "https://www.crazygames.com/embed/zombie-derby",
          height=600,
          scrolling=False,
      )

  # VIP GAME 3: 3D Space Shooter
  elif "3D Space Shooter" in game_choice:
    if not st.session_state.is_premium:
      st.warning(
          "🔒 **3D Space Shooter is reserved for VIP PRO members!**\n\nEnter VIP"
          " Key (`PRO2026`) in the sidebar to unlock."
      )
    else:
      st.subheader("🚀 3D Space Shooter (👑 VIP Unlocked)")
      st.components.v1.iframe(
          "https://www.crazygames.com/embed/space-wars",
          height=600,
          scrolling=False,
      )

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
