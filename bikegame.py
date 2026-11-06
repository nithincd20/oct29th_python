
from flask import Flask, render_template_string

app = Flask(__name__)

PAGE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Ultimate Highway Racing 3D</title>

<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#050914;color:white;font-family:Arial;overflow:hidden}
#game{position:fixed;inset:0}
canvas{display:block}

.panel{
 position:absolute;z-index:5;background:rgba(5,12,25,.78);
 border:1px solid rgba(255,255,255,.15);
 border-radius:12px;padding:12px;
 backdrop-filter:blur(10px)
}
#top{top:12px;left:12px;right:12px;display:flex;
 justify-content:space-between;align-items:center;gap:10px}
#stats{top:85px;left:12px;line-height:2}
#speed{position:absolute;bottom:20px;left:20px;z-index:5;
 font-size:35px;font-weight:bold;text-shadow:0 2px 10px black}
#speed small{font-size:13px;color:#bbb}
#nitroBox{position:absolute;bottom:25px;right:20px;width:160px;z-index:5}
.bar{height:10px;background:#222;border-radius:10px;overflow:hidden;margin-top:6px}
.fill{height:100%;width:100%;background:#00cfff}
button{background:#00a9e8;border:0;color:white;padding:11px 16px;
 border-radius:8px;font-weight:bold;cursor:pointer;margin:3px}
button:hover{background:#007da9}
#overlay{position:absolute;inset:0;z-index:10;
 display:flex;justify-content:center;align-items:center;
 background:linear-gradient(135deg,rgba(2,7,20,.94),rgba(0,30,55,.83))}
.card{width:min(500px,92vw);padding:30px;text-align:center;
 background:rgba(9,20,39,.96);border:1px solid #168fc3;
 border-radius:18px;box-shadow:0 0 45px #0076aa55}
.card h1{font-size:32px;color:#20caff;margin-bottom:12px}
.card p{color:#c4d3e0;line-height:1.7;margin:12px 0}
.card button{font-size:15px;margin-top:10px}
.hidden{display:none!important}
#mobile{position:absolute;bottom:100px;left:0;right:0;
 display:none;justify-content:space-between;padding:20px;z-index:6}
#mobile button{width:65px;height:60px;font-size:22px;opacity:.8}
#mobile .group{display:flex;gap:8px}
#rank{color:#ffdb67}
@media(max-width:700px){
 #mobile{display:flex}
 #stats{font-size:12px;top:76px}
 #top{font-size:12px}
 #speed{bottom:15px;font-size:25px}
 #nitroBox{bottom:18px;width:115px;font-size:12px}
}
</style>
</head>

<body>
<div id="game"></div>

<div id="top" class="panel">
 <b>🏁 ULTIMATE RACING 3D</b>
 <span id="levelName">LEVEL 1</span>
 <div>
 <button onclick="pauseGame()">Ⅱ PAUSE</button>
 </div>
</div>

<div id="stats" class="panel">
 <div>🏆 Position: <b id="position">1 / 6</b></div>
 <div>📏 Distance: <b id="distance">0</b> m</div>
 <div>🚦 Opponents: <b id="opponents">5</b></div>
 <div>⚡ Nitro: <b id="nitroText">100%</b></div>
 <div>🏍 Vehicle: <b id="vehicleName">Aero V1</b></div>
</div>

<div id="speed">0 <small>KM/H</small></div>

<div id="nitroBox">
 <b>NITRO BOOST</b>
 <div class="bar"><div class="fill" id="nitroFill"></div></div>
</div>

<div id="mobile">
 <div class="group">
  <button id="leftBtn">◀</button>
  <button id="rightBtn">▶</button>
 </div>
 <div class="group">
  <button id="brakeBtn">▼</button>
  <button id="nitroBtn">⚡</button>
  <button id="gasBtn">▲</button>
 </div>
</div>

<div id="overlay">
 <div class="card" id="menu">
  <h1>ULTIMATE RACING</h1>
  <p>Experience high-speed 3D highway racing.</p>
  <p>3 Levels • 5 AI Racers • Nitro • Vehicle Upgrades</p>
  <p>LEVEL 1 — AERO SUPERBIKE</p>
  <button onclick="startGame()">START RACING</button>
  <p style="font-size:12px">W/↑ Accelerate | S/↓ Brake | A/D Steering | SPACE Nitro</p>
 </div>
 <div class="card hidden" id="pause">
  <h1>GAME PAUSED</h1>
  <button onclick="resumeGame()">RESUME</button>
  <button onclick="restartGame()">RESTART</button>
 </div>
 <div class="card hidden" id="complete">
  <h1>LEVEL COMPLETED!</h1>
  <p id="upgradeText"></p>
  <button onclick="nextLevel()">NEXT LEVEL</button>
 </div>
 <div class="card hidden" id="over">
  <h1>RACE OVER</h1>
  <p id="overText">Your race has ended.</p>
  <button onclick="restartGame()">TRY AGAIN</button>
 </div>
</div>

<script type="module">
import * as THREE from
'https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js';

// --------------------------------
// GAME CONFIGURATION
// --------------------------------

const levels = [
 {
  name:"BEGINNER",
  vehicle:"AERO SUPERBIKE",
  max:190, acceleration:75, handling:7,
  goal:1200, traffic:5, color:0xff2020,
  sky:0x87b8df, road:0x292d34
 },
 {
  name:"PROFESSIONAL",
  vehicle:"M POWER SUPERBIKE",
  max:260, acceleration:105, handling:9,
  goal:1800, traffic:7, color:0x147aff,
  sky:0x637a9a, road:0x222831
 },
 {
  name:"ULTIMATE",
  vehicle:"HYPER GT",
  max:340, acceleration:145, handling:11,
  goal:2400, traffic:9, color:0xffd21a,
  sky:0x15213a, road:0x171a21
 }
];

let level=0, speed=0, distance=0, nitro=100;
let playerX=0, steering=0;
let running=false, paused=false, gameOver=false;
let nitroActive=false;
let opponents=[], scenery=[], roadMarks=[];
let elapsed=0, lastTime=0;
let score=0, collisionCooldown=0;

const keys={};
const lanePositions=[-4,0,4];
const clock=new THREE.Clock();

const scene=new THREE.Scene();
scene.background=new THREE.Color(0x87b8df);
scene.fog=new THREE.Fog(0x87b8df,45,230);

const camera=new THREE.PerspectiveCamera(
 65,window.innerWidth/window.innerHeight,.1,500
);
camera.position.set(0,5.5,10);

const renderer=new THREE.WebGLRenderer({antialias:true});
renderer.setSize(window.innerWidth,window.innerHeight);
renderer.setPixelRatio(Math.min(devicePixelRatio,2));
renderer.shadowMap.enabled=true;
renderer.shadowMap.type=THREE.PCFSoftShadowMap;
renderer.toneMapping=THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure=1.15;
document.getElementById("game").appendChild(renderer.domElement);

// --------------------------------
// LIGHTING
// --------------------------------

const ambient=new THREE.HemisphereLight(0xffffff,0x303b4d,2);
scene.add(ambient);

const sun=new THREE.DirectionalLight(0xffffff,2.5);
sun.position.set(-25,40,20);
sun.castShadow=true;
sun.shadow.mapSize.set(2048,2048);
scene.add(sun);

// --------------------------------
// MATERIALS
// --------------------------------

function material(color,roughness=.65,metalness=.1){
 return new THREE.MeshStandardMaterial({
  color,roughness,metalness
 });
}

const roadMat=material(0x292d34,.9);
const lineMat=material(0xffffff);
const grassMat=material(0x244a2b);
const tireMat=material(0x090a0c);
const metalMat=material(0x8d9aa7,.3,.8);

// --------------------------------
// ROAD
// --------------------------------

const road=new THREE.Mesh(
 new THREE.PlaneGeometry(16,500),
 roadMat
);
road.rotation.x=-Math.PI/2;
road.position.z=-190;
road.receiveShadow=true;
scene.add(road);

const ground=new THREE.Mesh(
 new THREE.PlaneGeometry(500,500),
 grassMat
);
ground.rotation.x=-Math.PI/2;
ground.position.y=-.12;
ground.position.z=-180;
scene.add(ground);

function createRoadMark(x,z){
 const mark=new THREE.Mesh(
  new THREE.BoxGeometry(.13,.025,5),
  lineMat
 );
 mark.position.set(x,.025,z);
 scene.add(mark);
 roadMarks.push(mark);
}

for(let z=-250;z<15;z+=12){
 createRoadMark(-2.65,z);
 createRoadMark(2.65,z);
}

for(const x of [-8.1,8.1]){
 const rail=new THREE.Mesh(
  new THREE.BoxGeometry(.35,.6,500),
  metalMat
 );
 rail.position.set(x,.35,-190);
 scene.add(rail);
}

// --------------------------------
// ENVIRONMENT
// --------------------------------

function createTree(x,z){
 const group=new THREE.Group();

 const trunk=new THREE.Mesh(
  new THREE.CylinderGeometry(.15,.22,2,8),
  material(0x65402a)
 );
 trunk.position.y=1;
 group.add(trunk);

 const leaves=new THREE.Mesh(
  new THREE.ConeGeometry(1.1,3,8),
  material(0x17652c)
 );
 leaves.position.y=3;
 group.add(leaves);

 group.position.set(x,0,z);
 scene.add(group);
 scenery.push(group);
}

function createBuilding(x,z){
 const group=new THREE.Group();
 const h=5+Math.random()*17;
 const w=4+Math.random()*5;

 const building=new THREE.Mesh(
  new THREE.BoxGeometry(w,h,5),
  material(
   [0x596778,0x777e8c,0x3c4c61,0x8a929c]
   [Math.floor(Math.random()*4)]
  )
 );
 building.position.y=h/2;
 group.add(building);

 for(let y=2;y<h;y+=2.5){
  for(let xx=-w/2+.8;xx<w/2;xx+=1.5){
   const win=new THREE.Mesh(
    new THREE.BoxGeometry(.7,.9,.05),
    material(0xffd98a,.25)
   );
   win.position.set(xx,y,2.53);
   group.add(win);
  }
 }

 group.position.set(x,0,z);
 scene.add(group);
 scenery.push(group);
}

function createStreetLight(x,z){
 const g=new THREE.Group();
 const pole=new THREE.Mesh(
  new THREE.CylinderGeometry(.07,.09,6,8),
  metalMat
 );
 pole.position.y=3;
 g.add(pole);

 const arm=new THREE.Mesh(
  new THREE.BoxGeometry(2,.09,.1),
  metalMat
 );
 arm.position.set(x<0?1:-1,5.9,0);
 g.add(arm);

 const bulb=new THREE.Mesh(
  new THREE.SphereGeometry(.2,8,8),
  material(0xfff0b0,.2)
 );
 bulb.position.set(x<0?2:-2,5.8,0);
 g.add(bulb);

 g.position.set(x,0,z);
 scene.add(g);
 scenery.push(g);
}

function populateEnvironment(){
 for(let z=-20;z>-250;z-=20){
  createTree(-12-Math.random()*5,z);
  createTree(12+Math.random()*5,z-8);

  if(Math.random()>.35){
   createBuilding(-27,z-10);
   createBuilding(27,z-5);
  }
  createStreetLight(-9,z);
  createStreetLight(9,z-10);
 }
}

// --------------------------------
// PROCEDURAL 3D VEHICLES
// --------------------------------

function createWheel(radius=.48,width=.3){
 const wheel=new THREE.Mesh(
  new THREE.CylinderGeometry(radius,radius,width,24),
  tireMat
 );
 wheel.rotation.z=Math.PI/2;
 wheel.castShadow=true;
 return wheel;
}

function createBike(color=0xff2020){
 const g=new THREE.Group();
 const paint=material(color,.27,.65);
 const dark=material(0x10151c,.4,.4);
 const chrome=material(0xaab6c1,.22,.8);

 // Main frame
 const body=new THREE.Mesh(
  new THREE.BoxGeometry(.75,.5,1.7),paint
 );
 body.position.y=1.05;
 g.add(body);

 // Fuel tank
 const tank=new THREE.Mesh(
  new THREE.SphereGeometry(.53,20,16),
  paint
 );
 tank.scale.set(.8,.65,1.15);
 tank.position.set(0,1.42,-.1);
 g.add(tank);

 // Front fairing
 const front=new THREE.Mesh(
  new THREE.SphereGeometry(.46,20,16),
  paint
 );
 front.scale.set(.85,.8,.75);
 front.position.set(0,1.48,-1.05);
 g.add(front);

 // Seat
 const seat=new THREE.Mesh(
  new THREE.BoxGeometry(.65,.17,.85),dark
 );
 seat.position.set(0,1.5,.75);
 g.add(seat);

 // Wheels
 const frontWheel=createWheel();
 frontWheel.position.set(0,.49,-1.45);
 g.add(frontWheel);

 const backWheel=createWheel();
 backWheel.position.set(0,.49,1.25);
 g.add(backWheel);

 // Wheel rims
 for(const z of [-1.45,1.25]){
  const rim=new THREE.Mesh(
   new THREE.TorusGeometry(.31,.035,8,24),
   chrome
  );
  rim.rotation.y=Math.PI/2;
  rim.position.set(0,.49,z);
  g.add(rim);
 }

 // Forks
 for(const x of [-.22,.22]){
  const fork=new THREE.Mesh(
   new THREE.CylinderGeometry(.055,.055,1.05,10),
   chrome
  );
  fork.position.set(x,.95,-1.35);
  g.add(fork);
 }

 // Handlebars
 const handle=new THREE.Mesh(
  new THREE.BoxGeometry(1.15,.08,.1),chrome
 );
 handle.position.set(0,1.95,-1.25);
 g.add(handle);

 // Headlight
 const light=new THREE.Mesh(
  new THREE.BoxGeometry(.42,.23,.12),
  material(0xeaffff,.1)
 );
 light.position.set(0,1.55,-1.45);
 g.add(light);

 const headlamp=new THREE.SpotLight(0xe5f5ff,20,50,.5);
 headlamp.position.set(0,1.55,-1.5);
 headlamp.target.position.set(0,0,-20);
 g.add(headlamp);
 g.add(headlamp.target);

 // Exhaust
 const exhaust=new THREE.Mesh(
  new THREE.CylinderGeometry(.11,.16,.9,12),
  chrome
 );
 exhaust.rotation.x=Math.PI/2;
 exhaust.position.set(.45,.85,.85);
 g.add(exhaust);

 // Rear light
 const tail=new THREE.Mesh(
  new THREE.BoxGeometry(.3,.13,.1),
  material(0xff1010)
 );
 tail.position.set(0,1.2,1.5);
 g.add(tail);

 g.traverse(o=>{
  if(o.isMesh)o.castShadow=true;
 });
 return g;
}

// Hypercar for level 3
function createHypercar(color=0xffd21a){
 const g=new THREE.Group();
 const paint=material(color,.25,.65);
 const dark=material(0x101318);
 const glass=material(0x152a3c,.15,.6);

 const body=new THREE.Mesh(
  new THREE.BoxGeometry(2.1,.75,4.2),paint
 );
 body.position.y=.75;
 g.add(body);

 const cabin=new THREE.Mesh(
  new THREE.BoxGeometry(1.65,.85,1.9),glass
 );
 cabin.position.set(0,1.45,.1);
 g.add(cabin);

 const hood=new THREE.Mesh(
  new THREE.BoxGeometry(1.8,.22,1.3),paint
 );
 hood.position.set(0,1.05,-1.3);
 g.add(hood);

 for(const x of [-1,1]){
  for(const z of [-1.35,1.35]){
   const wheel=new THREE.Mesh(
    new THREE.CylinderGeometry(.48,.48,.3,24),
    tireMat
   );
   wheel.rotation.z=Math.PI/2;
   wheel.position.set(x, .48,z);
   g.add(wheel);
  }
 }

 const lamp=new THREE.Mesh(
  new THREE.BoxGeometry(1.2,.12,.1),
  material(0xeafaff)
 );
 lamp.position.set(0,.95,-2.1);
 g.add(lamp);

 g.traverse(o=>{if(o.isMesh)o.castShadow=true});
 return g;
}

let player;

function createPlayer(){
 if(player)scene.remove(player);

 player=level===2
  ?createHypercar(levels[level].color)
  :createBike(levels[level].color);

 player.position.set(0,0,0);
 scene.add(player);
}

// --------------------------------
// AI RACERS
// --------------------------------

function createOpponent(i){
 const bike=createBike([
  0x00aaff,0xff9900,0x8a45ff,
  0x00ff9d,0xffee00
 ][i%5]);

 bike.scale.setScalar(.9);
 bike.position.set(lanePositions[i%3],0,-25-i*22);
 scene.add(bike);

 return {
  mesh:bike,
  speed:85+Math.random()*85+i*7,
  targetLane:lanePositions[i%3],
  changeTimer:2+Math.random()*5,
  passed:false,
  skill:Math.random()
 };
}

function createOpponents(){
 opponents.forEach(o=>scene.remove(o.mesh));
 opponents=[];
 for(let i=0;i<5;i++){
  opponents.push(createOpponent(i));
 }
}

// --------------------------------
// GAME START
// --------------------------------

function showOnly(id){
 ["menu","pause","complete","over"].forEach(x=>
  document.getElementById(x).classList.add("hidden")
 );
 document.getElementById(id).classList.remove("hidden");
}

function startGame(){
 level=0;
 resetLevel();
 running=true;
 paused=false;
 gameOver=false;
 document.getElementById("overlay").classList.add("hidden");
 clock.start();
}

function resetLevel(){
 speed=0;
 distance=0;
 nitro=100;
 score=0;
 playerX=0;
 elapsed=0;
 collisionCooldown=0;
 createPlayer();
 createOpponents();
 updateUI();
}

function pauseGame(){
 if(!running||paused)return;
 paused=true;
 showOnly("pause");
 document.getElementById("overlay").classList.remove("hidden");
}

function resumeGame(){
 paused=false;
 document.getElementById("overlay").classList.add("hidden");
 lastTime=performance.now();
}

function restartGame(){
 resetLevel();
 running=true;
 paused=false;
 gameOver=false;
 document.getElementById("overlay").classList.add("hidden");
 lastTime=performance.now();
}

function nextLevel(){
 level++;
 if(level>=3){
  showOnly("over");
  document.querySelector("#over h1").textContent="CHAMPION!";
  document.getElementById("overText").textContent=
   "Congratulations! You completed all three racing levels.";
  document.getElementById("overlay").classList.remove("hidden");
  running=false;
  return;
 }

 resetLevel();
 running=true;
 paused=false;
 document.getElementById("overlay").classList.add("hidden");
}

// --------------------------------
// KEYBOARD CONTROLS
// --------------------------------

window.addEventListener("keydown",e=>{
 keys[e.code]=true;
 if(["ArrowUp","ArrowDown","ArrowLeft","ArrowRight","Space"].includes(e.code))
 e.preventDefault();
});
window.addEventListener("keyup",e=>keys[e.code]=false);

function bindHold(id,key){
 const el=document.getElementById(id);
 el.addEventListener("pointerdown",e=>{
  e.preventDefault();keys[key]=true;
 });
 ["pointerup","pointerleave","pointercancel"].forEach(event=>{
  el.addEventListener(event,()=>keys[key]=false);
 });
}
bindHold("leftBtn","ArrowLeft");
bindHold("rightBtn","ArrowRight");
bindHold("gasBtn","ArrowUp");
bindHold("brakeBtn","ArrowDown");
bindHold("nitroBtn","Space");

// --------------------------------
// GAME PHYSICS
// --------------------------------

function updateGame(dt){
 const cfg=levels[level];
 elapsed+=dt;
 collisionCooldown=Math.max(0,collisionCooldown-dt);

 const gas=keys.KeyW||keys.ArrowUp;
 const brake=keys.KeyS||keys.ArrowDown;
 const left=keys.KeyA||keys.ArrowLeft;
 const right=keys.KeyD||keys.ArrowRight;
 nitroActive=(keys.Space||false)&&nitro>0;

 let maxSpeed=cfg.max;

 if(nitroActive){
  maxSpeed*=1.35;
  nitro=Math.max(0,nitro-28*dt);
 }else{
  nitro=Math.min(100,nitro+9*dt);
 }

 if(gas)speed+=cfg.acceleration*dt;
 else speed-=12*dt;

 if(brake)speed-=cfg.acceleration*1.7*dt;

 speed=THREE.MathUtils.clamp(speed,0,maxSpeed);

 const steer=(right?1:0)-(left?1:0);
 steering=THREE.MathUtils.damp(steering,steer,7,dt);

 playerX+=steering*cfg.handling*dt*(.5+speed/cfg.max);
 playerX=THREE.MathUtils.clamp(playerX,-5.8,5.8);

 player.position.x=THREE.MathUtils.damp(
  player.position.x,playerX,10,dt
 );
 player.rotation.z=-steering*.12;
 player.rotation.x=steering*.035;

 const movement=speed*dt*.15;
 distance+=speed*dt/3.6;

 // Road markings
 roadMarks.forEach(m=>{
  m.position.z+=movement;
  if(m.position.z>15)m.position.z-=264;
 });

 // Environment scrolling
 scenery.forEach(s=>{
  s.position.z+=movement;
  if(s.position.z>25)s.position.z-=270;
 });

 // Opponents
 opponents.forEach((o,i)=>{
  o.changeTimer-=dt;

  if(o.changeTimer<=0){
   o.targetLane=lanePositions[
    Math.floor(Math.random()*3)
   ];
   o.changeTimer=2+Math.random()*4;
  }

  const laneX=THREE.MathUtils.damp(
   o.mesh.position.x,o.targetLane,1.6,dt
  );

  o.mesh.position.x=laneX;

  // Relative forward movement
  o.mesh.position.z+=(speed-o.speed)*dt*.15;

  // Slight opponent movement animation
  o.mesh.rotation.z=(o.targetLane-o.mesh.position.x)*.05;

  // Opponent respawn after falling behind
  if(o.mesh.position.z>15){
   o.mesh.position.z=-140-Math.random()*70;
   o.mesh.position.x=lanePositions[
    Math.floor(Math.random()*3)
   ];
   o.speed=85+Math.random()*115+level*15;
   score+=100;
  }

  // Recycle opponents far ahead
  if(o.mesh.position.z < -220){
   o.mesh.position.z=-100-Math.random()*60;
  }

  // Collision detection
  const dx=Math.abs(o.mesh.position.x-player.position.x);
  const dz=Math.abs(o.mesh.position.z);

  if(dx<1.15&&dz<2.0&&collisionCooldown<=0){
   collisionCooldown=1.3;
   speed*=.45;
   score=Math.max(0,score-50);
   player.position.x+=player.position.x>o.mesh.position.x? .8:-.8;
   o.mesh.position.z+=4;
  }
 });

 // Camera follow
 const camX=player.position.x*.65;
 camera.position.x=THREE.MathUtils.damp(
  camera.position.x,camX,3,dt
 );
 camera.position.y=THREE.MathUtils.damp(
  camera.position.y,level===2?6.2:5.5,2,dt
 );
 camera.lookAt(player.position.x*.3,1,-9);

 // Bike wheel rotation
 player.traverse(o=>{
  if(o.isMesh&&o.geometry.type==="CylinderGeometry"){
   o.rotation.x+=movement*.3;
  }
 });

 if(distance>=cfg.goal){
  completeLevel();
 }

 if(speed<0)speed=0;
 updateUI();
}

// --------------------------------
// UI
// --------------------------------

function updateUI(){
 const cfg=levels[level];
 document.getElementById("levelName").textContent=
  "LEVEL "+(level+1)+" — "+cfg.name;
 document.getElementById("vehicleName").textContent=cfg.vehicle;
 document.getElementById("speed").innerHTML=
  Math.round(speed)+" <small>KM/H</small>";
 document.getElementById("distance").textContent=
  Math.floor(distance)+" / "+cfg.goal+" m";
 document.getElementById("nitroText").textContent=
  Math.floor(nitro)+"%";
 document.getElementById("nitroFill").style.width=nitro+"%";

 const position=1+opponents.filter(o=>
  o.mesh.position.z < 0
 ).length;

 document.getElementById("position").textContent=
  Math.min(position,6)+" / 6";

 document.getElementById("opponents").textContent=
  opponents.length;
}

// --------------------------------
// LEVEL COMPLETION
// --------------------------------

function completeLevel(){
 running=false;
 speed=0;

 const next=level+1;
 let message;

 if(next<3){
  message="You unlocked: "+levels[next].vehicle+
   ". Your engine, acceleration, speed and handling have improved!";
 }else{
  message="Final vehicle unlocked: "+levels[2].vehicle+
   ". Complete this final challenge to become champion!";
 }

 document.getElementById("upgradeText").textContent=message;
 showOnly("complete");
 document.getElementById("overlay").classList.remove("hidden");
}

// --------------------------------
// ANIMATION
// --------------------------------

function animate(now){
 requestAnimationFrame(animate);

 let dt=Math.min((now-lastTime)/1000,.04);
 lastTime=now;

 if(running&&!paused&&!gameOver){
  updateGame(dt);
 }

 renderer.render(scene,camera);
}

// --------------------------------
// INITIALIZATION
// --------------------------------

function changeLevelEnvironment(){
 scene.background=new THREE.Color(levels[level].sky);
 scene.fog.color.set(levels[level].sky);
 roadMat.color.set(levels[level].road);
}

populateEnvironment();
createPlayer();
createOpponents();

const originalReset=resetLevel;
resetLevel=function(){
 originalReset();
 changeLevelEnvironment();
};

window.addEventListener("resize",()=>{
 camera.aspect=window.innerWidth/window.innerHeight;
 camera.updateProjectionMatrix();
 renderer.setSize(window.innerWidth,window.innerHeight);
});

lastTime=performance.now();
requestAnimationFrame(animate);

</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(PAGE)

if __name__ == "__main__":
    print("Ultimate 3D Racing Game")
    print("Open http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)
