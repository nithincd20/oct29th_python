from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SUPERCAR | Ultimate Racing</title>

<style>
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    background: #05070b;
    color: white;
    font-family: Arial, sans-serif;
    overflow: hidden;
}

#game {
    position: fixed;
    inset: 0;
}

canvas {
    display: block;
}

#hud {
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 2;
}

.topbar {
    position: absolute;
    top: 22px;
    left: 25px;
    right: 25px;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
}

.brand {
    font-size: 22px;
    font-weight: 900;
    letter-spacing: 4px;
}

.brand span {
    color: #00e5ff;
}

.subtitle {
    font-size: 10px;
    letter-spacing: 3px;
    color: #a0b4c5;
    margin-top: 7px;
}

.level-box {
    background: rgba(3, 10, 20, 0.75);
    border: 1px solid rgba(0, 229, 255, 0.45);
    padding: 13px 20px;
    text-align: right;
    backdrop-filter: blur(10px);
}

.level-box small {
    display: block;
    color: #00e5ff;
    font-size: 10px;
    letter-spacing: 2px;
    margin-bottom: 5px;
}

.level-box strong {
    font-size: 17px;
    letter-spacing: 2px;
}

.bottom {
    position: absolute;
    bottom: 24px;
    left: 25px;
    right: 25px;
    display: flex;
    justify-content: space-between;
    align-items: end;
    gap: 20px;
}

.speed-panel {
    display: flex;
    align-items: end;
    gap: 10px;
    background: rgba(3, 10, 20, 0.78);
    padding: 15px 22px;
    border-left: 3px solid #00e5ff;
}

#speed {
    font-size: 53px;
    font-weight: 900;
    line-height: 1;
    font-variant-numeric: tabular-nums;
}

.unit {
    color: #00e5ff;
    font-size: 11px;
    letter-spacing: 2px;
    padding-bottom: 5px;
}

.stats {
    text-align: center;
    background: rgba(3, 10, 20, 0.72);
    padding: 13px 22px;
    min-width: 130px;
}

.stats small {
    color: #8ba4ba;
    font-size: 10px;
    letter-spacing: 2px;
}

.stats strong {
    display: block;
    font-size: 20px;
    margin-top: 7px;
}

.controls {
    text-align: right;
    color: #b9cad8;
    font-size: 11px;
    line-height: 2;
}

kbd {
    background: #142332;
    padding: 4px 7px;
    border: 1px solid #304b60;
    border-radius: 3px;
    color: white;
}

.progress-wrap {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: rgba(255,255,255,.12);
}

#progress {
    width: 0;
    height: 100%;
    background: #00e5ff;
    box-shadow: 0 0 15px #00e5ff;
}

#overlay {
    position: fixed;
    inset: 0;
    z-index: 5;
    display: flex;
    align-items: center;
    justify-content: center;
    background:
        radial-gradient(ellipse at center, rgba(0,25,40,.35), rgba(0,0,0,.88));
}

.card {
    width: min(520px, 92vw);
    padding: 36px;
    background: rgba(4, 10, 19, .92);
    border: 1px solid rgba(0,229,255,.45);
    box-shadow: 0 0 70px rgba(0,229,255,.12);
    text-align: center;
    backdrop-filter: blur(15px);
}

.tag {
    color: #00e5ff;
    font-size: 11px;
    letter-spacing: 5px;
    margin-bottom: 20px;
}

h1 {
    font-size: clamp(36px, 7vw, 60px);
    line-height: .95;
    font-weight: 900;
    letter-spacing: -2px;
}

h1 span {
    color: #00e5ff;
}

.description {
    color: #a7b8c8;
    font-size: 13px;
    line-height: 1.8;
    margin: 22px 0;
}

#start {
    border: 0;
    width: 100%;
    padding: 17px;
    background: #00e5ff;
    color: #001019;
    font-weight: 900;
    font-size: 14px;
    letter-spacing: 3px;
    cursor: pointer;
    transition: .2s;
}

#start:hover {
    background: white;
    transform: translateY(-2px);
}

.cars {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin: 22px 0;
}

.car-chip {
    border: 1px solid #263a4b;
    padding: 10px;
    flex: 1;
    color: #c3d5e4;
    font-size: 10px;
    letter-spacing: 1px;
}

.car-chip.active {
    border-color: #00e5ff;
    color: #00e5ff;
}

#toast {
    position: absolute;
    top: 30%;
    width: 100%;
    text-align: center;
    font-size: clamp(24px, 5vw, 42px);
    font-weight: 900;
    letter-spacing: 4px;
    color: #fff;
    text-shadow: 0 0 25px #00e5ff;
    opacity: 0;
    transition: opacity .4s;
}

@media (max-width: 650px) {
    .topbar {
        top: 12px;
        left: 12px;
        right: 12px;
    }

    .brand {
        font-size: 16px;
        letter-spacing: 2px;
    }

    .level-box {
        padding: 10px;
    }

    .level-box strong {
        font-size: 12px;
    }

    .bottom {
        bottom: 18px;
        left: 12px;
        right: 12px;
        flex-wrap: wrap;
    }

    #speed {
        font-size: 38px;
    }

    .speed-panel {
        padding: 12px;
    }

    .stats {
        padding: 10px;
        min-width: 90px;
    }

    .controls {
        display: none;
    }

    .card {
        padding: 24px;
    }
}
</style>
</head>

<body>

<div id="game"></div>

<div id="hud">

    <div class="topbar">
        <div>
            <div class="brand">SUPER<span>CAR</span></div>
            <div class="subtitle">ULTIMATE RACING EXPERIENCE</div>
        </div>

        <div class="level-box">
            <small id="levelLabel">LEVEL 01 / 03</small>
            <strong id="environment">SNOW MOUNTAIN</strong>
        </div>
    </div>

    <div id="toast">LEVEL UNLOCKED</div>

    <div class="bottom">

        <div class="speed-panel">
            <div id="speed">000</div>
            <div class="unit">KM/H</div>
        </div>

        <div class="stats">
            <small>DISTANCE</small>
            <strong id="distance">0 m</strong>
        </div>

        <div class="stats">
            <small>SUPER CAR</small>
            <strong id="carName">FROST GT</strong>
        </div>

        <div class="controls">
            <kbd>W</kbd> ACCELERATE
            <kbd>S</kbd> BRAKE<br>
            <kbd>A</kbd> <kbd>D</kbd> STEER
            <kbd>SPACE</kbd> BRAKE
        </div>

    </div>

    <div class="progress-wrap">
        <div id="progress"></div>
    </div>

</div>

<div id="overlay">
    <div class="card">
        <div class="tag">THREE WORLDS. THREE SUPERCARS.</div>

        <h1>DRIVE<br><span>BEYOND.</span></h1>

        <p class="description">
            Conquer frozen mountain roads, survive muddy terrain,
            and dominate the ultimate highway.<br>
            Every level unlocks a faster supercar.
        </p>

        <div class="cars">
            <div class="car-chip active">01<br>FROST GT</div>
            <div class="car-chip">02<br>STORM X</div>
            <div class="car-chip">03<br>APEX V12</div>
        </div>

        <button id="start">START YOUR ENGINE →</button>

        <p class="description">
            W / ↑ Accelerate &nbsp; A / D Steer<br>
            S / ↓ / SPACE Brake &nbsp; ESC Pause
        </p>
    </div>
</div>

<script type="importmap">
{
  "imports": {
    "three": "https://cdn.jsdelivr.net/npm/three@0.180.0/build/three.module.js"
  }
}
</script>

<script type="module">
import * as THREE from 'three';

// ======================================================
// SUPERCAR 3D RACING GAME
// ======================================================

const root = document.getElementById('game');

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x9bc5df);
scene.fog = new THREE.Fog(0x9bc5df, 45, 230);

const camera = new THREE.PerspectiveCamera(
    65,
    innerWidth / innerHeight,
    0.1,
    600
);

camera.position.set(0, 5, 10);

const renderer = new THREE.WebGLRenderer({
    antialias: true,
    powerPreference: 'high-performance'
});

renderer.setSize(innerWidth, innerHeight);
renderer.setPixelRatio(Math.min(devicePixelRatio, 1.75));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.15;

root.appendChild(renderer.domElement);

// ------------------------------------------------------
// LIGHTING
// ------------------------------------------------------

scene.add(new THREE.HemisphereLight(0xd7edff, 0x333344, 2));

const sun = new THREE.DirectionalLight(0xffffff, 3);
sun.position.set(-12, 24, 8);
sun.castShadow = true;
sun.shadow.mapSize.set(1024, 1024);
scene.add(sun);

// ------------------------------------------------------
// MATERIALS
// ------------------------------------------------------

const mat = (color, metalness=0, roughness=0.55) =>
    new THREE.MeshStandardMaterial({
        color,
        metalness,
        roughness
    });

const materials = {
    body1: mat(0xc7f1ff, 0.7, 0.23),
    body2: mat(0xff4b20, 0.65, 0.25),
    body3: mat(0x161d2b, 0.85, 0.2),
    glass: mat(0x102b43, 0.75, 0.16),
    tire: mat(0x101114, 0.1, 0.8),
    rim: mat(0xbac7d1, 0.9, 0.2),
    black: mat(0x11151a, 0.2, 0.4),
    light: new THREE.MeshBasicMaterial({color: 0x9ffaff}),
    red: new THREE.MeshBasicMaterial({color: 0xff163b}),
    snow: mat(0xe9f5ff, 0.05, 0.95),
    mud: mat(0x65432b, 0, 1),
    asphalt: mat(0x272d35, 0.1, 0.9),
    highway: mat(0x30343b, 0.2, 0.8),
    white: mat(0xffffff, 0, 0.8)
};

// ------------------------------------------------------
// PROCEDURAL SUPERCAR
// ------------------------------------------------------

function makeCar(bodyMaterial) {
    const car = new THREE.Group();

    function box(parent, w, h, d, material, x, y, z) {
        const mesh = new THREE.Mesh(
            new THREE.BoxGeometry(w, h, d),
            material
        );

        mesh.position.set(x, y, z);
        mesh.castShadow = true;
        mesh.receiveShadow = true;
        parent.add(mesh);
        return mesh;
    }

    // Low, wide supercar chassis
    box(car, 1.85, 0.38, 3.7, bodyMaterial, 0, 0.65, 0);

    // Front hood
    box(car, 1.7, 0.18, 1.0, bodyMaterial, 0, 0.86, -1.15);

    // Rear deck
    box(car, 1.65, 0.20, 0.85, bodyMaterial, 0, 0.86, 1.2);

    // Sloping windshield
    const windshield = box(
        car, 1.38, 0.58, 1.05, materials.glass, 0, 1.05, -0.12
    );

    windshield.rotation.x = -0.12;

    // Rear window
    box(car, 1.25, 0.36, 0.5, materials.glass, 0, 1.06, 0.7);

    // Aerodynamic front splitter
    box(car, 2.0, 0.09, 0.38, materials.black, 0, 0.43, -1.85);

    // Rear spoiler
    box(car, 1.8, 0.10, 0.38, materials.black, 0, 1.25, 1.72);
    box(car, 0.12, 0.32, 0.12, materials.black, -0.55, 1.08, 1.65);
    box(car, 0.12, 0.32, 0.12, materials.black, 0.55, 1.08, 1.65);

    // Headlights and tail lights
    box(car, 0.47, 0.10, 0.06, materials.light, -0.57, 0.83, -1.72);
    box(car, 0.47, 0.10, 0.06, materials.light,  0.57, 0.83, -1.72);

    box(car, 0.48, 0.10, 0.06, materials.red, -0.55, 0.83, 1.85);
    box(car, 0.48, 0.10, 0.06, materials.red,  0.55, 0.83, 1.85);

    // Exhausts
    box(car, 0.22, 0.12, 0.15, materials.rim, -0.48, 0.47, 1.91);
    box(car, 0.22, 0.12, 0.15, materials.rim,  0.48, 0.47, 1.91);

    // Four wheels
    const wheels = [];

    for (const x of [-0.99, 0.99]) {
        for (const z of [-1.15, 1.15]) {
            const wheel = new THREE.Group();

            const tire = new THREE.Mesh(
                new THREE.CylinderGeometry(0.39, 0.39, 0.24, 24),
                materials.tire
            );

            tire.rotation.z = Math.PI / 2;
            tire.castShadow = true;
            wheel.add(tire);

            const rim = new THREE.Mesh(
                new THREE.CylinderGeometry(0.23, 0.23, 0.255, 12),
                materials.rim
            );

            rim.rotation.z = Math.PI / 2;
            wheel.add(rim);

            wheel.position.set(x, 0.40, z);
            car.add(wheel);
            wheels.push(wheel);
        }
    }

    car.userData.wheels = wheels;

    // Soft contact shadow
    const shadow = new THREE.Mesh(
        new THREE.CircleGeometry(1.45, 32),
        new THREE.MeshBasicMaterial({
            color: 0x000000,
            transparent: true,
            opacity: 0.25
        })
    );

    shadow.rotation.x = -Math.PI / 2;
    shadow.scale.set(1, 1.6, 1);
    shadow.position.y = 0.04;
    car.add(shadow);

    return car;
}

// ------------------------------------------------------
// CAR UPGRADES / LEVELS
// ------------------------------------------------------

const levels = [
    {
        name: 'SNOW MOUNTAIN',
        car: 'FROST GT',
        body: materials.body1,
        speed: 39,
        acceleration: 23,
        color: 0xe9f5ff,
        sky: 0x9bc5df,
        fog: 0xbad4e7,
        ground: 0xe8f3fb,
        road: 0x5b6978,
        type: 'snow'
    },
    {
        name: 'MUD STORM',
        car: 'STORM X',
        body: materials.body2,
        speed: 52,
        acceleration: 29,
        color: 0x65432b,
        sky: 0x9e8b76,
        fog: 0xb9a58b,
        ground: 0x513b29,
        road: 0x40332a,
        type: 'mud'
    },
    {
        name: 'HIGHWAY LEGENDS',
        car: 'APEX V12',
        body: materials.body3,
        speed: 68,
        acceleration: 35,
        color: 0x171d29,
        sky: 0x182b46,
        fog: 0x33465e,
        ground: 0x202b35,
        road: 0x24272e,
        type: 'highway'
    }
];

let currentLevel = 0;
let gameStarted = false;
let paused = false;
let gameOver = false;

let distance = 0;
let speed = 0;
let lateral = 0;
let steer = 0;
let travel = 0;

let car = makeCar(levels[0].body);
scene.add(car);

// ------------------------------------------------------
// ROAD AND WORLD
// ------------------------------------------------------

const roadGroup = new THREE.Group();
scene.add(roadGroup);

const scenery = new THREE.Group();
scene.add(scenery);

const obstacles = [];

function clearGroup(group) {
    while (group.children.length) {
        const child = group.children[0];
        group.remove(child);

        child.traverse?.(obj => {
            if (obj.geometry) obj.geometry.dispose();
        });
    }
}

function addBox(group, w, h, d, material, x, y, z) {
    const mesh = new THREE.Mesh(
        new THREE.BoxGeometry(w, h, d),
        material
    );

    mesh.position.set(x, y, z);
    mesh.receiveShadow = true;
    mesh.castShadow = true;
    group.add(mesh);
    return mesh;
}

function createMountain(x, z, size, color) {
    const mountain = new THREE.Mesh(
        new THREE.ConeGeometry(size, size * 1.6, 5),
        mat(color, 0, 1)
    );

    mountain.position.set(x, size * 0.65, z);
    mountain.rotation.y = Math.random() * 1.5;
    mountain.castShadow = true;
    scenery.add(mountain);

    if (currentLevel === 0) {
        const cap = new THREE.Mesh(
            new THREE.ConeGeometry(size * 0.35, size * 0.45, 5),
            materials.snow
        );

        cap.position.set(x, size * 1.35, z);
        scenery.add(cap);
    }
}

function createTree(x, z) {
    const group = new THREE.Group();

    const trunk = new THREE.Mesh(
        new THREE.CylinderGeometry(0.12, 0.2, 1.4, 7),
        mat(0x493324)
    );

    trunk.position.y = 0.7;
    group.add(trunk);

    for (let i = 0; i < 3; i++) {
        const foliage = new THREE.Mesh(
            new THREE.ConeGeometry(0.8 - i * 0.12, 1.25, 7),
            mat(currentLevel === 0 ? 0xd9edfa : 0x244a38)
        );

        foliage.position.y = 1.4 + i * 0.5;
        group.add(foliage);
    }

    group.position.set(x, 0, z);
    scenery.add(group);
}

function createWorld() {
    clearGroup(roadGroup);
    clearGroup(scenery);

    obstacles.length = 0;

    const L = levels[currentLevel];

    scene.background.setHex(L.sky);
    scene.fog.color.setHex(L.fog);

    const groundMaterial = mat(L.ground, 0, 0.95);
    const roadMaterial = mat(L.road, 0.15, 0.85);

    // Long ground plane
    addBox(scenery, 500, 0.2, 600, groundMaterial, 0, -0.25, -170);

    // Main road
    addBox(roadGroup, 13, 0.15, 650, roadMaterial, 0, 0, -280);

    // Road shoulders
    addBox(roadGroup, 1.2, 0.16, 650, groundMaterial, -7.1, 0.01, -280);
    addBox(roadGroup, 1.2, 0.16, 650, groundMaterial, 7.1, 0.01, -280);

    // Dashed lane markings
    for (let z = 20; z > -600; z -= 12) {
        addBox(
            roadGroup, 0.13, 0.025, 4.3,
            materials.white, 0, 0.095, z
        );
    }

    // Highway crash barriers
    if (currentLevel === 2) {
        for (let z = 20; z > -600; z -= 8) {
            addBox(
                roadGroup, 0.18, 0.7, 8,
                materials.rim, -7.2, 0.35, z
            );

            addBox(
                roadGroup, 0.18, 0.7, 8,
                materials.rim, 7.2, 0.35, z
            );
        }

        // Tall stylized highway buildings
        for (let i = 0; i < 45; i++) {
            const z = 20 - i * 13;
            const side = i % 2 ? 1 : -1;
            const height = 7 + Math.random() * 22;

            addBox(
                scenery,
                5 + Math.random() * 7,
                height,
                7 + Math.random() * 8,
                mat(
                    [0x28384c, 0x36465a, 0x202e40][i % 3],
                    0.35, 0.6
                ),
                side * (17 + Math.random() * 18),
                height / 2 - 0.2,
                z
            );
        }
    } else {
        // Mountain scenery
        for (let i = 0; i < 65; i++) {
            const z = 20 - i * 9;
            const side = i % 2 ? 1 : -1;

            createMountain(
                side * (17 + Math.random() * 24),
                z,
                5 + Math.random() * 12,
                currentLevel === 0
                    ? [0x9bb4c7, 0xc3d6e5, 0x879faf][i % 3]
                    : [0x544337, 0x70563e, 0x3d3a31][i % 3]
            );

            if (currentLevel === 0 && i % 2 === 0) {
                createTree(side * 13, z - 4);
            }
        }
    }

    // Obstacles
    for (let i = 0; i < 28; i++) {
        const z = -28 - i * 17 - Math.random() * 5;
        const x = [-4, 0, 4][Math.floor(Math.random() * 3)];

        const obstacle = new THREE.Group();

        if (currentLevel === 0) {
            // Snow boulders
            const rock = new THREE.Mesh(
                new THREE.DodecahedronGeometry(0.9, 0),
                mat(0xb8cbd8, 0, 0.9)
            );

            rock.position.y = 0.65;
            rock.castShadow = true;
            obstacle.add(rock);

        } else if (currentLevel === 1) {
            // Mud road rock formations
            const rock = new THREE.Mesh(
                new THREE.DodecahedronGeometry(1.0, 0),
                mat(0x62513d, 0, 1)
            );

            rock.position.y = 0.7;
            rock.castShadow = true;
            obstacle.add(rock);

        } else {
            // Highway traffic vehicles
            const trafficBody = new THREE.Mesh(
                new THREE.BoxGeometry(1.7, 1.0, 3.2),
                mat([0x3a88aa, 0xb2b9c0, 0x7d3140][i % 3], 0.5, 0.35)
            );

            trafficBody.position.y = 0.75;
            trafficBody.castShadow = true;
            obstacle.add(trafficBody);

            const cabin = new THREE.Mesh(
                new THREE.BoxGeometry(1.3, 0.65, 1.35),
                materials.glass
            );

            cabin.position.set(0, 1.5, 0.1);
            obstacle.add(cabin);
        }

        obstacle.position.set(x, 0, z);
        scenery.add(obstacle);

        obstacles.push(obstacle);
    }
}

// ------------------------------------------------------
// LEVEL SYSTEM
// ------------------------------------------------------

function updateLevel(levelIndex) {
    currentLevel = levelIndex;

    const L = levels[currentLevel];

    scene.remove(car);

    car = makeCar(L.body);
    car.position.set(lateral, 0, 0);

    scene.add(car);

    speed = 0;
    steer = 0;

    document.getElementById('levelLabel').textContent =
        `LEVEL 0${currentLevel + 1} / 03`;

    document.getElementById('environment').textContent = L.name;
    document.getElementById('carName').textContent = L.car;

    document.querySelectorAll('.car-chip').forEach((chip, i) => {
        chip.classList.toggle('active', i === currentLevel);
    });

    createWorld();

    scene.fog.near = 45;
    scene.fog.far = currentLevel === 2 ? 260 : 210;

    showToast(currentLevel === 0
        ? 'LEVEL 01 — BEGIN'
        : currentLevel === 1
            ? 'LEVEL 02 — STORM X UNLOCKED'
            : 'LEVEL 03 — APEX V12 UNLOCKED'
    );
}

let toastTimeout;

function showToast(message) {
    const toast = document.getElementById('toast');

    toast.textContent = message;
    toast.style.opacity = '1';

    clearTimeout(toastTimeout);

    toastTimeout = setTimeout(() => {
        toast.style.opacity = '0';
    }, 2500);
}

// ------------------------------------------------------
// CONTROLS
// ------------------------------------------------------

const keys = {};

addEventListener('keydown', e => {
    keys[e.key.toLowerCase()] = true;

    if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', ' '].includes(e.key)) {
        e.preventDefault();
    }

    if (e.key === 'Escape' && gameStarted && !gameOver) {
        paused = !paused;
        showToast(paused ? 'PAUSED' : 'RACE RESUMED');
    }
});

addEventListener('keyup', e => {
    keys[e.key.toLowerCase()] = false;
});

document.getElementById('start').addEventListener('click', () => {
    gameStarted = true;
    paused = false;
    gameOver = false;

    document.getElementById('overlay').style.display = 'none';

    updateLevel(0);
});

// ------------------------------------------------------
// MOVEMENT AND COLLISION
// ------------------------------------------------------

function updateGame(dt) {
    if (!gameStarted || paused || gameOver) return;

    const L = levels[currentLevel];

    const accelerating = keys['w'] || keys['arrowup'];
    const braking = keys['s'] || keys['arrowdown'] || keys[' '];

    if (accelerating) {
        speed += L.acceleration * dt;
    } else {
        speed -= 8 * dt;
    }

    if (braking) {
        speed -= 48 * dt;
    }

    speed = THREE.MathUtils.clamp(speed, 0, L.speed);

    const steeringLeft = keys['a'] || keys['arrowleft'];
    const steeringRight = keys['d'] || keys['arrowright'];

    steer = (steeringLeft ? 1 : 0) - (steeringRight ? 1 : 0);

    // Steering sensitivity increases with speed
    lateral += steer * dt * (2.4 + speed * 0.095);

    lateral = THREE.MathUtils.clamp(lateral, -5.2, 5.2);

    car.position.x = THREE.MathUtils.damp(
        car.position.x, lateral, 9, dt
    );

    car.rotation.z = THREE.MathUtils.damp(
        car.rotation.z, -steer * 0.12, 6, dt
    );

    car.rotation.y = THREE.MathUtils.damp(
        car.rotation.y, -steer * 0.09, 5, dt
    );

    car.userData.wheels.forEach(wheel => {
        wheel.rotation.x -= speed * dt * 0.8;
    });

    // World travels toward the player
    const worldSpeed = speed * 0.19;

    travel += worldSpeed;
    distance += worldSpeed;

    scenery.position.z += worldSpeed;
    roadGroup.position.z += worldSpeed;

    // Recycle obstacles to keep the race going
    for (const obstacle of obstacles) {
        if (obstacle.position.z > 12) {
            obstacle.position.z -= 470;
            obstacle.position.x = [-4, 0, 4][
                Math.floor(Math.random() * 3)
            ];
        }

        const dz = Math.abs(obstacle.position.z);
        const dx = Math.abs(obstacle.position.x - car.position.x);

        if (dz < 1.9 && dx < 1.35) {
            speed *= 0.94;
        }
    }

    // Recycle scenery and road groups for continuous driving
    if (scenery.position.z > 450) {
        scenery.position.z -= 500;
    }

    if (roadGroup.position.z > 450) {
        roadGroup.position.z -= 500;
    }

    // Level progression
    const levelDistance = 450;

    if (distance >= (currentLevel + 1) * levelDistance) {
        if (currentLevel < 2) {
            updateLevel(currentLevel + 1);
        } else {
            distance = 0;
            showToast('CHAMPION — RACE AGAIN!');
            updateLevel(0);
        }
    }

    document.getElementById('speed').textContent =
        String(Math.round(speed * 3.6)).padStart(3, '0');

    document.getElementById('distance').textContent =
        Math.floor(distance) + ' m';

    const stageProgress =
        (distance % levelDistance) / levelDistance;

    document.getElementById('progress').style.width =
        (stageProgress * 100) + '%';
}

// ------------------------------------------------------
// CINEMATIC CHASE CAMERA
// ------------------------------------------------------

const cameraTarget = new THREE.Vector3();
const desiredCamera = new THREE.Vector3();

function updateCamera(dt) {
    desiredCamera.set(
        car.position.x * 0.55,
        4.4 + speed * 0.008,
        8.5
    );

    camera.position.lerp(
        desiredCamera,
        1 - Math.exp(-3.5 * dt)
    );

    cameraTarget.set(
        car.position.x * 0.65,
        0.9,
        -8
    );

    camera.lookAt(cameraTarget);
}

// ------------------------------------------------------
// RENDER LOOP
// ------------------------------------------------------

let lastTime = performance.now();

function animate(now) {
    requestAnimationFrame(animate);

    const dt = Math.min((now - lastTime) / 1000, 0.04);
    lastTime = now;

    updateGame(dt);
    updateCamera(dt);

    renderer.render(scene, camera);
}

updateLevel(0);

requestAnimationFrame(animate);

// Responsive window
addEventListener('resize', () => {
    camera.aspect = innerWidth / innerHeight;
    camera.updateProjectionMatrix();

    renderer.setSize(innerWidth, innerHeight);
    renderer.setPixelRatio(Math.min(devicePixelRatio, 1.75));
});

</script>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/api/status")
def status():
    return jsonify({
        "game": "SUPERCAR",
        "levels": [
            "Snow Mountain",
            "Mud Storm",
            "Highway Legends"
        ],
        "engine": "Three.js",
        "backend": "Flask",
        "status": "running"
    })


if __name__ == "__main__":
    print("=" * 48)
    print(" SUPERCAR 3D RACING GAME")
    print(" Open: http://127.0.0.1:5000")
    print("=" * 48)

    app.run(host="127.0.0.1", port=5000, debug=True)