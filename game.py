from flask import Flask, render_template_string

app = Flask(__name__)

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DINO // AFTER DARK</title>

<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800;900&family=Rajdhani:wght@400;600;700&display=swap');

:root {
    --cyan: #57f6ff;
    --green: #b8ff67;
    --pink: #ff4d9d;
    --bg: #060914;
}

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    background: var(--bg);
    color: white;
    font-family: 'Rajdhani', sans-serif;
    min-height: 100vh;
    overflow-x: hidden;
}

body::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    background:
        radial-gradient(ellipse at 50% 80%, #12334455, transparent 55%),
        radial-gradient(ellipse at 10% 10%, #30205244, transparent 40%);
    z-index: -2;
}

#stars {
    position: fixed;
    inset: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: -1;
}

.container {
    width: min(1100px, 94%);
    margin: auto;
    padding: 32px 0;
}

header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 20px;
    margin-bottom: 45px;
}

.logo {
    font-family: 'Orbitron', sans-serif;
    font-size: 17px;
    font-weight: 900;
    letter-spacing: 3px;
}

.logo span {
    color: var(--cyan);
}

.status {
    font-family: 'Orbitron', sans-serif;
    font-size: 10px;
    letter-spacing: 2px;
    color: var(--green);
    display: flex;
    align-items: center;
    gap: 9px;
}

.dot {
    height: 7px;
    width: 7px;
    background: var(--green);
    border-radius: 50%;
    box-shadow: 0 0 15px var(--green);
    animation: pulse 1.5s infinite;
}

@keyframes pulse {
    50% { opacity: .35; }
}

.hero {
    text-align: center;
    margin-bottom: 35px;
}

.eyebrow {
    color: var(--cyan);
    font-family: 'Orbitron', sans-serif;
    font-size: 10px;
    letter-spacing: 5px;
    margin-bottom: 15px;
}

h1 {
    font-family: 'Orbitron', sans-serif;
    font-size: clamp(35px, 7vw, 78px);
    font-weight: 900;
    letter-spacing: -3px;
    line-height: 1.12;
    text-shadow: 0 0 35px #57f6ff30;
}

h1 span {
    color: var(--cyan);
}

.subtitle {
    margin-top: 16px;
    color: #8493b2;
    font-size: 17px;
    letter-spacing: 2px;
}

.game-frame {
    position: relative;
    border: 1px solid #57f6ff55;
    background: #080d1b;
    box-shadow: 0 0 40px #00d9ff12, inset 0 0 45px #00d9ff08;
    overflow: hidden;
}

.frame-top {
    height: 44px;
    border-bottom: 1px solid #57f6ff25;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 20px;
    background: #ffffff04;
    font-family: 'Orbitron', sans-serif;
    font-size: 9px;
    letter-spacing: 2px;
    color: #8291b1;
}

.frame-top strong {
    color: var(--cyan);
    font-weight: 600;
}

#game {
    width: 100%;
    display: block;
    height: auto;
    touch-action: manipulation;
    cursor: pointer;
}

.game-footer {
    display: flex;
    justify-content: space-between;
    gap: 10px;
    padding: 15px 20px;
    border-top: 1px solid #57f6ff20;
    color: #74839f;
    font-family: 'Orbitron', sans-serif;
    font-size: 9px;
    letter-spacing: 1px;
}

.game-footer span {
    color: var(--cyan);
}

.info {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin-top: 25px;
}

.card {
    border: 1px solid #ffffff12;
    background: linear-gradient(135deg, #ffffff08, #ffffff02);
    padding: 20px;
}

.card-label {
    color: #8291b1;
    font-size: 11px;
    letter-spacing: 3px;
    margin-bottom: 8px;
}

.card-value {
    font-family: 'Orbitron', sans-serif;
    font-size: 21px;
    color: var(--green);
}

.instructions {
    text-align: center;
    margin-top: 35px;
    color: #8190aa;
    line-height: 2;
    font-size: 15px;
}

kbd {
    color: white;
    background: #151e32;
    border: 1px solid #34415a;
    padding: 4px 10px;
    font-family: 'Orbitron', sans-serif;
    font-size: 10px;
}

footer {
    text-align: center;
    padding: 35px 0 5px;
    color: #53617d;
    font-family: 'Orbitron', sans-serif;
    font-size: 9px;
    letter-spacing: 3px;
}

@media (max-width: 600px) {
    .container { padding-top: 22px; }
    header { margin-bottom: 35px; }
    .logo { font-size: 12px; }
    .status { font-size: 8px; letter-spacing: 1px; }
    h1 { letter-spacing: -2px; }
    .subtitle { font-size: 13px; }
    .info { gap: 7px; }
    .card { padding: 12px 8px; }
    .card-label { font-size: 8px; letter-spacing: 1px; }
    .card-value { font-size: 15px; }
    .frame-top { padding: 0 10px; font-size: 8px; }
    .game-footer { padding: 12px 8px; font-size: 7px; }
}
</style>
</head>

<body>
<canvas id="stars"></canvas>

<div class="container">

<header>
    <div class="logo">DINO <span>//</span> AFTER DARK</div>
    <div class="status"><i class="dot"></i> SYSTEM ONLINE</div>
</header>

<section class="hero">
    <div class="eyebrow">THE OFFLINE SURVIVAL PROTOCOL</div>
    <h1>RUN BEYOND<br><span>THE END.</span></h1>
    <p class="subtitle">ONE DINOSAUR. INFINITE NIGHT.</p>
</section>

<section class="game-frame">
    <div class="frame-top">
        <div>SECTOR 01 / DESERT</div>
        <div>MISSION: <strong id="mission">READY</strong></div>
    </div>

    <canvas id="game" width="1000" height="350"></canvas>

    <div class="game-footer">
        <div>ENGINE <span>RUNNER-X</span></div>
        <div>DIFFICULTY <span id="difficulty">01</span></div>
        <div>CONNECTION <span>NOT REQUIRED</span></div>
    </div>
</section>

<section class="info">
    <div class="card">
        <div class="card-label">DISTANCE</div>
        <div class="card-value" id="score">00000</div>
    </div>
    <div class="card">
        <div class="card-label">BEST RUN</div>
        <div class="card-value" id="best">00000</div>
    </div>
    <div class="card">
        <div class="card-label">SPEED LVL</div>
        <div class="card-value" id="level">01</div>
    </div>
</section>

<div class="instructions">
    <p>PRESS <kbd>SPACE</kbd> OR <kbd>↑</kbd> TO JUMP</p>
    <p>DOUBLE JUMP ENABLED &nbsp; // &nbsp; <kbd>R</kbd> RESTART</p>
    <p>OR TAP THE GAME AREA TO PLAY</p>
</div>

<footer>DESIGNED FOR THE DARKEST HOURS &nbsp; // &nbsp; DINO SYSTEMS © 2026</footer>
</div>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

const W = canvas.width;
const H = canvas.height;
const ground = 282;

let state = "ready";
let frame = 0;
let score = 0;
let best = 0;
let speed = 5;
let obstacles = [];
let particles = [];
let clouds = [];
let spawnTimer = 0;
let shake = 0;
let lastTime = 0;
let accumulator = 0;
const STEP = 1000 / 60;

try {
    best = Number(localStorage.getItem("dino_best") || 0);
} catch (e) {
    best = 0;
}

document.getElementById("best").textContent =
    String(best).padStart(5, "0");

// Stars background
const stars = document.getElementById("stars");
const sctx = stars.getContext("2d");
let starArray = [];

function resizeStars() {
    stars.width = innerWidth * devicePixelRatio;
    stars.height = innerHeight * devicePixelRatio;
    sctx.setTransform(devicePixelRatio, 0, 0, devicePixelRatio, 0, 0);

    starArray = Array.from({length: 110}, () => ({
        x: Math.random() * innerWidth,
        y: Math.random() * innerHeight,
        r: Math.random() * 1.5 + .2,
        a: Math.random() * .7 + .1
    }));
}

function drawStars() {
    sctx.clearRect(0, 0, innerWidth, innerHeight);

    for (const s of starArray) {
        sctx.fillStyle = `rgba(155,220,255,${s.a})`;
        sctx.fillRect(s.x, s.y, s.r, s.r);
    }
}

addEventListener("resize", resizeStars);
resizeStars();
drawStars();

// Generate background clouds
for (let i = 0; i < 7; i++) {
    clouds.push({
        x: Math.random() * W,
        y: 30 + Math.random() * 110,
        w: 35 + Math.random() * 70,
        speed: .25 + Math.random() * .5
    });
}

const dino = {
    x: 110,
    y: ground - 49,
    w: 43,
    h: 49,
    vy: 0,
    jumps: 0,
    duck: false
};

function groundY() {
    return ground;
}

function roundedRect(x, y, w, h, r, color) {
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.roundRect(x, y, w, h, r);
    ctx.fill();
}

function drawBackground() {
    const gradient = ctx.createLinearGradient(0, 0, 0, H);
    gradient.addColorStop(0, "#080e20");
    gradient.addColorStop(.7, "#10182a");
    gradient.addColorStop(1, "#151b2b");

    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, W, H);

    // Moon
    ctx.save();
    ctx.shadowColor = "#8af4ff";
    ctx.shadowBlur = 35;
    ctx.fillStyle = "#d5faff";
    ctx.beginPath();
    ctx.arc(810, 75, 29, 0, Math.PI * 2);
    ctx.fill();

    ctx.shadowBlur = 0;
    ctx.fillStyle = "#111a31";
    ctx.beginPath();
    ctx.arc(824, 65, 27, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();

    // Distant mountain silhouettes
    ctx.fillStyle = "#111c33";
    ctx.beginPath();
    ctx.moveTo(0, 245);

    for (let x = 0; x <= W; x += 100) {
        ctx.lineTo(x + 50, 180 + Math.sin(x * .02) * 22);
        ctx.lineTo(x + 100, 245);
    }

    ctx.lineTo(W, ground);
    ctx.lineTo(0, ground);
    ctx.fill();

    // Atmospheric clouds
    clouds.forEach(c => {
        ctx.fillStyle = "#a0d9ff10";
        ctx.fillRect(c.x, c.y, c.w, 2);
        ctx.fillRect(c.x + 10, c.y - 4, c.w * .5, 2);

        if (state === "playing") {
            c.x -= c.speed * (speed / 5);
            if (c.x + c.w < 0) {
                c.x = W + Math.random() * 100;
            }
        }
    });

    // Horizon glow
    const glow = ctx.createLinearGradient(0, ground - 40, 0, ground + 10);
    glow.addColorStop(0, "#57f6ff00");
    glow.addColorStop(1, "#57f6ff18");
    ctx.fillStyle = glow;
    ctx.fillRect(0, ground - 40, W, 50);

    // Ground
    ctx.strokeStyle = "#57f6ff";
    ctx.lineWidth = 2;
    ctx.shadowColor = "#57f6ff";
    ctx.shadowBlur = 12;

    ctx.beginPath();
    ctx.moveTo(0, ground);
    ctx.lineTo(W, ground);
    ctx.stroke();

    ctx.shadowBlur = 0;

    ctx.fillStyle = "#57f6ff";

    for (let i = 0; i < 50; i++) {
        let x = ((i * 43 - frame * speed) % (W + 43) + W + 43) % (W + 43);
        ctx.globalAlpha = .15 + (i % 3) * .1;
        ctx.fillRect(x, ground + 12 + (i % 3) * 8, 18, 1);
    }

    ctx.globalAlpha = 1;
}

function drawDino() {
    const ducking = dino.duck && dino.y >= ground - 35;
    const x = dino.x;
    const y = dino.y;

    ctx.save();

    ctx.shadowColor = "#b8ff67";
    ctx.shadowBlur = 18;
    ctx.fillStyle = "#b8ff67";

    if (ducking) {
        // Ducking dinosaur
        ctx.fillRect(x + 7, y + 17, 32, 18);
        ctx.fillRect(x + 28, y + 7, 18, 17);
        ctx.fillRect(x, y + 22, 12, 8);

        ctx.fillStyle = "#101629";
        ctx.fillRect(x + 38, y + 12, 3, 3);

        ctx.fillStyle = "#b8ff67";
        ctx.fillRect(x + 12, y + 32, 8, 6);
        ctx.fillRect(x + 30, y + 32, 8, 6);
    } else {
        // Tail
        ctx.fillRect(x, y + 23, 12, 7);
        ctx.fillRect(x - 5, y + 18, 9, 6);

        // Body
        ctx.fillRect(x + 8, y + 19, 28, 21);

        // Head
        ctx.fillRect(x + 21, y + 2, 23, 21);
        ctx.fillRect(x + 31, y + 15, 16, 7);

        // Eye
        ctx.fillStyle = "#0a1020";
        ctx.fillRect(x + 36, y + 7, 4, 4);

        // Tiny arm
        ctx.fillStyle = "#b8ff67";
        ctx.fillRect(x + 28, y + 24, 9, 4);

        // Animated legs
        const leg = Math.sin(frame * .35) * 5;

        if (state === "playing" && dino.y >= ground - dino.h - .5) {
            ctx.fillRect(x + 11, y + 37, 6, 12 + leg);
            ctx.fillRect(x + 28, y + 37, 6, 12 - leg);
        } else {
            ctx.fillRect(x + 11, y + 37, 6, 12);
            ctx.fillRect(x + 28, y + 37, 6, 12);
        }
    }

    ctx.restore();
}

function drawCactus(o) {
    ctx.save();

    ctx.shadowColor = "#ff4d9d";
    ctx.shadowBlur = 13;
    ctx.fillStyle = "#ff4d9d";

    const x = o.x;
    const y = ground - o.h;

    // Main stem
    ctx.fillRect(x + 12, y, 11, o.h);

    // Branches
    ctx.fillRect(x + 2, y + o.h * .35, 10, 6);
    ctx.fillRect(x + 2, y + o.h * .2, 6, o.h * .18);

    ctx.fillRect(x + 23, y + o.h * .52, 10, 6);
    ctx.fillRect(x + 27, y + o.h * .35, 6, o.h * .2);

    ctx.restore();
}

function drawBird(o) {
    const flap = Math.sin(frame * .18) * 7;

    ctx.save();
    ctx.shadowColor = "#57f6ff";
    ctx.shadowBlur = 12;
    ctx.fillStyle = "#57f6ff";

    ctx.fillRect(o.x, o.y, 27, 9);
    ctx.fillRect(o.x + 20, o.y + 2, 10, 5);

    ctx.beginPath();
    ctx.moveTo(o.x + 10, o.y + 4);
    ctx.lineTo(o.x + 5, o.y - flap);
    ctx.lineTo(o.x + 20, o.y + 4);
    ctx.fill();

    ctx.beginPath();
    ctx.moveTo(o.x + 12, o.y + 6);
    ctx.lineTo(o.x + 5, o.y + 11 + flap);
    ctx.lineTo(o.x + 23, o.y + 6);
    ctx.fill();

    ctx.restore();
}

function drawObstacles() {
    obstacles.forEach(o => {
        if (o.type === "bird") {
            drawBird(o);
        } else {
            drawCactus(o);
        }
    });
}

function burst(x, y) {
    for (let i = 0; i < 24; i++) {
        particles.push({
            x, y,
            vx: (Math.random() - .5) * 7,
            vy: (Math.random() - .7) * 7,
            life: 35 + Math.random() * 20,
            color: Math.random() > .5 ? "#b8ff67" : "#57f6ff"
        });
    }
}

function updateParticles() {
    particles.forEach(p => {
        p.x += p.vx;
        p.y += p.vy;
        p.vy += .15;
        p.life--;

        ctx.globalAlpha = Math.max(0, p.life / 50);
        ctx.fillStyle = p.color;
        ctx.fillRect(p.x, p.y, 3, 3);
    });

    ctx.globalAlpha = 1;
    particles = particles.filter(p => p.life > 0);
}

function spawnObstacle() {
    const birdChance = score > 250 && Math.random() < .28;

    if (birdChance) {
        obstacles.push({
            x: W + 30,
            y: ground - 55 - Math.random() * 55,
            w: 30,
            h: 16,
            type: "bird"
        });
    } else {
        const h = 30 + Math.random() * 27;

        obstacles.push({
            x: W + 30,
            y: ground - h,
            w: 35,
            h,
            type: "cactus"
        });
    }
}

function jump() {
    if (state === "ready") {
        state = "playing";
        document.getElementById("mission").textContent = "ACTIVE";
    }

    if (state === "over") return;

    if (dino.jumps < 2) {
        dino.vy = dino.jumps === 0 ? -12.8 : -11;
        dino.jumps++;
        burst(dino.x + 20, dino.y + dino.h);
    }
}

function reset() {
    state = "ready";
    score = 0;
    speed = 5;
    frame = 0;
    spawnTimer = 0;
    accumulator = 0;
    obstacles = [];
    particles = [];

    dino.y = ground - dino.h;
    dino.vy = 0;
    dino.jumps = 0;
    dino.duck = false;

    document.getElementById("mission").textContent = "READY";
    document.getElementById("score").textContent = "00000";
    document.getElementById("level").textContent = "01";
    document.getElementById("difficulty").textContent = "01";
}

function endGame() {
    if (state !== "playing") return;

    state = "over";
    shake = 10;
    burst(dino.x + 20, dino.y + 20);

    document.getElementById("mission").textContent = "FAILED";

    if (score > best) {
        best = score;

        try {
            localStorage.setItem("dino_best", best);
        } catch (e) {}

        document.getElementById("best").textContent =
            String(best).padStart(5, "0");
    }
}

function collide(a, b) {
    // Smaller hitboxes make gameplay fairer
    const ax = a.x + 8;
    const ay = a.y + 5;
    const aw = a.w - 15;
    const ah = a.h - 9;

    const bx = b.x + 4;
    const by = b.type === "bird" ? b.y + 2 : b.y + 4;
    const bw = b.w - 8;
    const bh = b.type === "bird" ? b.h - 4 : b.h - 4;

    return (
        ax < bx + bw &&
        ax + aw > bx &&
        ay < by + bh &&
        ay + ah > by
    );
}

function update() {
    frame++;

    if (state === "playing") {
        score += .12;
        speed = Math.min(5 + score / 100, 12);

        document.getElementById("score").textContent =
            String(Math.floor(score)).padStart(5, "0");

        const lvl = Math.floor(score / 100) + 1;

        document.getElementById("level").textContent =
            String(lvl).padStart(2, "0");

        document.getElementById("difficulty").textContent =
            String(lvl).padStart(2, "0");

        // Gravity
        dino.vy += .62;
        dino.y += dino.vy;

        if (dino.y >= ground - dino.h) {
            dino.y = ground - dino.h;
            dino.vy = 0;
            dino.jumps = 0;
        }

        // Spawn obstacles
        spawnTimer--;

        if (spawnTimer <= 0) {
            spawnObstacle();
            spawnTimer = Math.max(
                48,
                100 + Math.random() * 45 - speed * 3
            );
        }

        obstacles.forEach(o => {
            o.x -= speed;

            if (collide(dino, o)) {
                endGame();
            }
        });

        obstacles = obstacles.filter(o => o.x + o.w > -20);
    }

    if (shake > 0) shake *= .8;
}

function overlay(title, subtitle, action) {
    ctx.save();

    ctx.fillStyle = "#040816b8";
    ctx.fillRect(0, 0, W, H);

    ctx.textAlign = "center";
    ctx.shadowColor = "#57f6ff";
    ctx.shadowBlur = 22;

    ctx.font = "900 36px Orbitron, monospace";
    ctx.fillStyle = "#ffffff";
    ctx.fillText(title, W / 2, 130);

    ctx.shadowBlur = 0;
    ctx.font = "600 16px Rajdhani, sans-serif";
    ctx.fillStyle = "#57f6ff";
    ctx.fillText(subtitle, W / 2, 169);

    ctx.font = "600 14px Rajdhani, sans-serif";
    ctx.fillStyle = "#b8ff67";
    ctx.fillText(action, W / 2, 220);

    // Animated start indicator
    if (Math.floor(frame / 30) % 2 === 0) {
        ctx.fillStyle = "#ffffff";
        ctx.fillRect(W / 2 - 2, 250, 4, 4);
    }

    ctx.restore();
}

function render() {
    ctx.save();

    if (shake > .5) {
        ctx.translate(
            (Math.random() - .5) * shake,
            (Math.random() - .5) * shake
        );
    }

    drawBackground();
    drawObstacles();
    drawDino();
    updateParticles();

    if (state === "ready") {
        overlay(
            "READY TO RUN?",
            "THE NIGHT IS YOURS TO CONQUER",
            "PRESS SPACE OR TAP TO BEGIN"
        );
    }

    if (state === "over") {
        overlay(
            "MISSION FAILED",
            "DISTANCE: " + Math.floor(score) + " METERS",
            "PRESS R OR TAP TO RESTART"
        );
    }

    ctx.restore();
}

function loop(timestamp) {
    if (!lastTime) lastTime = timestamp;

    accumulator += Math.min(timestamp - lastTime, 100);
    lastTime = timestamp;

    while (accumulator >= STEP) {
        update();
        accumulator -= STEP;
    }

    render();
    requestAnimationFrame(loop);
}

addEventListener("keydown", e => {
    if (["Space", "ArrowUp", "ArrowDown"].includes(e.code)) {
        e.preventDefault();
    }

    if (e.repeat) return;

    if (e.code === "Space" || e.code === "ArrowUp") {
        if (state === "over") {
            reset();
            state = "playing";
            document.getElementById("mission").textContent = "ACTIVE";
        }

        jump();
    }

    if (e.code === "ArrowDown") {
        dino.duck = true;
    }

    if (e.code === "KeyR") {
        reset();
    }
});

addEventListener("keyup", e => {
    if (e.code === "ArrowDown") {
        dino.duck = false;
    }
});

canvas.addEventListener("pointerdown", () => {
    if (state === "over") {
        reset();
        state = "playing";
        document.getElementById("mission").textContent = "ACTIVE";
        return;
    }

    jump();
});

requestAnimationFrame(loop);
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)