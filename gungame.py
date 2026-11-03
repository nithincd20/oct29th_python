
from flask import Flask, render_template_string

app = Flask(__name__)

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>SHADOW STRIKE | FPS</title>

<style>
*{box-sizing:border-box}
body{
 margin:0;overflow:hidden;background:#080c13;
 font-family:Arial,sans-serif;color:white
}
canvas{display:block}
#hud{
 position:fixed;inset:0;pointer-events:none;
 z-index:5
}
.top{
 display:flex;justify-content:space-between;
 padding:22px 28px;
 background:linear-gradient(#000a,transparent)
}
.panel{
 background:#101b2ccc;border:1px solid #52677c;
 padding:12px 18px;border-radius:8px;
 backdrop-filter:blur(8px)
}
.label{font-size:11px;color:#9eafc2;letter-spacing:2px}
.value{font-size:24px;font-weight:bold;margin-top:5px}
#crosshair{
 position:absolute;top:50%;left:50%;
 transform:translate(-50%,-50%);
 font-size:30px;color:#fff;
 text-shadow:0 0 8px #00eaff
}
#bottom{
 position:absolute;bottom:20px;left:50%;
 transform:translateX(-50%);
 display:flex;gap:12px;align-items:end
}
#weapon{min-width:180px}
#healthbar,#ammobar{
 height:8px;background:#344354;
 margin-top:8px;border-radius:10px;overflow:hidden
}
#healthfill{height:100%;width:100%;background:#28e68c}
#ammoFill{height:100%;width:100%;background:#00cfff}
#guns{
 position:absolute;right:25px;bottom:25px;
 display:flex;gap:8px
}
.gun{
 padding:10px 12px;background:#152235dd;
 border:1px solid #53677d;border-radius:5px;
 font-size:12px
}
.gun.active{border:1px solid #00eaff;color:#00eaff}
.gun.locked{opacity:.35}
#message{
 position:absolute;top:27%;width:100%;
 text-align:center;font-size:30px;
 font-weight:bold;color:#00eaff;
 text-shadow:0 0 15px #00cfff
}
#overlay{
 position:fixed;inset:0;z-index:20;
 background:radial-gradient(ellipse at center,#24394d,#070a11 75%);
 display:flex;align-items:center;justify-content:center;
 text-align:center
}
.menu{
 width:min(520px,90%);
 padding:35px;border:1px solid #50677d;
 background:#101a28ee;border-radius:15px;
 box-shadow:0 0 70px #000
}
h1{font-size:42px;letter-spacing:5px;margin:10px}
h1 span{color:#00dfff}
.subtitle{color:#9eb4ca;letter-spacing:3px;font-size:12px}
button{
 padding:15px 35px;background:#00c9ec;
 color:#06121c;border:0;border-radius:5px;
 font-weight:bold;font-size:15px;cursor:pointer;
 margin-top:20px
}
button:hover{background:white}
.instructions{color:#a9bbca;font-size:12px;line-height:2}
#damage{
 position:fixed;inset:0;pointer-events:none;
 z-index:4;opacity:0;
 background:radial-gradient(transparent 35%,#ff0000aa);
}
#hitmarker{
 position:absolute;top:50%;left:50%;
 transform:translate(-50%,-50%);
 font-size:34px;color:#ff5353;display:none
}
</style>

<script type="importmap">
{
 "imports":{
  "three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js",
  "three/addons/":"https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"
 }
}
</script>
</head>

<body>
<div id="hud">
 <div class="top">
  <div class="panel">
   <div class="label">MISSION</div>
   <div class="value" id="level">LEVEL 01</div>
  </div>
  <div class="panel">
   <div class="label">ELIMINATIONS</div>
   <div class="value" id="score">0</div>
  </div>
  <div class="panel">
   <div class="label">PLAYER HEALTH</div>
   <div class="value" id="healthText">100</div>
  </div>
 </div>

 <div id="crosshair">+</div>
 <div id="hitmarker">×</div>
 <div id="message"></div>
 <div id="damage"></div>

 <div id="bottom">
  <div class="panel" id="weapon">
   <div class="label">CURRENT WEAPON</div>
   <div class="value" id="weaponName">PISTOL</div>
   <div id="ammoText">12 / 48</div>
   <div id="ammobar"><div id="ammoFill"></div></div>
   <div class="label" style="margin-top:8px">HEALTH</div>
   <div id="healthbar"><div id="healthfill"></div></div>
  </div>
 </div>

 <div id="guns">
  <div class="gun active" id="g1">1 PISTOL</div>
  <div class="gun" id="g2">2 RIFLE</div>
  <div class="gun locked" id="g3">3 SHOTGUN</div>
  <div class="gun locked" id="g4">4 SNIPER</div>
 </div>
</div>

<div id="overlay">
 <div class="menu">
  <div class="subtitle">FIRST PERSON COMBAT EXPERIENCE</div>
  <h1>SHADOW <span>STRIKE</span></h1>
  <p style="color:#b4c8d9">Enter the battlefield. Survive three levels.</p>
  <p class="instructions">
   WASD - MOVE &nbsp; | &nbsp; MOUSE - AIM<br>
   LEFT CLICK - FIRE &nbsp; | &nbsp; R - RELOAD<br>
   1-4 - SWITCH WEAPONS &nbsp; | &nbsp; SHIFT - SPRINT
  </p>
  <button id="start">START MISSION</button>
  <p class="instructions" id="menuInfo">Defeat enemies to earn points and unlock weapons.</p>
 </div>
</div>

<script type="module">
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';

// ---------------- GAME CONFIG ----------------

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x9aaebe);
scene.fog = new THREE.Fog(0x9aaebe,35,100);

const camera = new THREE.PerspectiveCamera(
 75,innerWidth/innerHeight,0.1,150
);
camera.position.set(0,2,8);

const renderer = new THREE.WebGLRenderer({antialias:true});
renderer.setSize(innerWidth,innerHeight);
renderer.setPixelRatio(Math.min(devicePixelRatio,2));
renderer.shadowMap.enabled=true;
renderer.shadowMap.type=THREE.PCFSoftShadowMap;
renderer.outputColorSpace=THREE.SRGBColorSpace;
document.body.appendChild(renderer.domElement);

const ambient = new THREE.HemisphereLight(0xc8e4ff,0x26313d,2);
scene.add(ambient);

const sun = new THREE.DirectionalLight(0xffffff,2.5);
sun.position.set(-15,25,10);
sun.castShadow=true;
scene.add(sun);

const clock = new THREE.Clock();
const raycaster = new THREE.Raycaster();

let started=false;
let gameOver=false;
let score=0;
let level=1;
let health=100;
let enemies=[];
let keys={};
let spawnTimer=0;
let damageTimer=0;
let reloadTimer=0;
let shooting=false;
let lastShot=0;
let gunObjects=[];
let currentGun=1;
let recoil=0;

const weapons={
 1:{name:"PISTOL",damage:35,rate:350,mag:12,ammo:12,total:48,spread:0.015},
 2:{name:"ASSAULT RIFLE",damage:22,rate:110,mag:30,ammo:30,total:120,spread:0.035},
 3:{name:"SHOTGUN",damage:18,rate:800,mag:8,ammo:8,total:40,spread:0.12,pellets:7},
 4:{name:"SNIPER",damage:100,rate:1100,mag:5,ammo:5,total:25,spread:0.003}
};

const unlocked={1:true,2:true,3:false,4:false};

// ---------------- ENVIRONMENT ----------------

function makeBox(x,y,z,w,h,d,color){
 const m=new THREE.Mesh(
  new THREE.BoxGeometry(w,h,d),
  new THREE.MeshStandardMaterial({color,roughness:0.85})
 );
 m.position.set(x,y,z);
 m.castShadow=true;
 m.receiveShadow=true;
 scene.add(m);
 return m;
}

const floor=makeBox(0,-0.3,-25,100,0.5,110,0x52636d);
const grid=new THREE.GridHelper(100,60,0x718b9a,0x536574);
grid.position.y=-0.03;
scene.add(grid);

// Boundary walls
makeBox(-50,4,-25,2,8,110,0x354452);
makeBox(50,4,-25,2,8,110,0x354452);
makeBox(0,4,-80,100,8,2,0x354452);
makeBox(0,4,30,100,8,2,0x354452);

// Obstacles
for(let i=0;i<20;i++){
 const x=(Math.random()-.5)*75;
 const z=-10-Math.random()*60;
 makeBox(x,1,z,2+Math.random()*3,2,2+Math.random()*3,0x374a5c);
}

// Lights and industrial structures
for(let i=0;i<8;i++){
 const x=-35+i*10;
 makeBox(x,5,-45,0.5,10,0.5,0x273847);
 const light=new THREE.PointLight(0x00bfff,30,16);
 light.position.set(x,8,-45);
 scene.add(light);
}

// ---------------- PLAYER WEAPON MODEL ----------------

// Procedural weapon model. Replace with Blender GLB models below.
const weaponGroup=new THREE.Group();
camera.add(weaponGroup);
scene.add(camera);

function makeGun(color,scale=1){
 const group=new THREE.Group();
 const metal=new THREE.MeshStandardMaterial({
  color,metalness:.8,roughness:.3
 });
 const dark=new THREE.MeshStandardMaterial({
  color:0x18232b,metalness:.6,roughness:.5
 });

 function part(x,y,z,w,h,d,mat){
  const mesh=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),mat);
  mesh.position.set(x,y,z);
  group.add(mesh);
  return mesh;
 }

 part(0,0,0,0.18,0.18,0.55*scale,metal);
 part(0,-.13,.13,0.12,.22,.17,dark);
 part(0,.02,-.4*scale,.07,.07,.65*scale,dark);
 part(0,.12,-.12,.10,.07,.17,metal);
 return group;
}

function buildWeapons(){
 for(const g of gunObjects){
  weaponGroup.remove(g);
 }
 gunObjects=[];

 const colors=[0x8c9aa8,0x303d48,0x9d5c30,0x536c80];

 for(let i=1;i<=4;i++){
  const gun=makeGun(colors[i-1],i===4?1.5:1);
  gun.position.set(.35,-.32,-.65);
  gun.rotation.y=-.08;
  gun.visible=i===currentGun;
  weaponGroup.add(gun);
  gunObjects.push(gun);
 }
}
buildWeapons();

// OPTIONAL: load your Blender-exported GLB weapon.
// Export Blender models as GLB and put them in static/models.
// Example: loadModel("static/models/pistol.glb", 0);

function loadModel(path,index){
 const loader=new GLTFLoader();
 loader.load(path,(gltf)=>{
  const model=gltf.scene;
  model.scale.setScalar(.5);
  model.position.set(.35,-.32,-.65);
  weaponGroup.remove(gunObjects[index]);
  gunObjects[index]=model;
  weaponGroup.add(model);
  model.visible=index+1===currentGun;
 });
}

// ---------------- ENEMIES ----------------

function createEnemy(){
 const group=new THREE.Group();

 const color=level===1?0x647b5c:
             level===2?0x86513b:0x8a263d;

 const bodyMat=new THREE.MeshStandardMaterial({
  color,roughness:.8
 });
 const headMat=new THREE.MeshStandardMaterial({
  color:0xb6a18d,roughness:.8
 });

 const body=new THREE.Mesh(
  new THREE.BoxGeometry(.85,1.25,.48),bodyMat
 );
 body.position.y=1.25;
 body.castShadow=true;
 group.add(body);

 const head=new THREE.Mesh(
  new THREE.SphereGeometry(.35,12,12),headMat
 );
 head.position.y=2.15;
 head.castShadow=true;
 group.add(head);

 const eyeMat=new THREE.MeshBasicMaterial({color:0xff2020});
 for(let s of [-1,1]){
  const eye=new THREE.Mesh(
   new THREE.SphereGeometry(.055,8,8),eyeMat
  );
  eye.position.set(s*.13,2.2,-.29);
  group.add(eye);
 }

 for(let s of [-1,1]){
  const leg=new THREE.Mesh(
   new THREE.BoxGeometry(.25,.8,.3),bodyMat
  );
  leg.position.set(s*.23,.4,0);
  group.add(leg);
 }

 const hp=level===1?70:level===2?130:200;
 group.userData.hp=hp;
 group.userData.maxHp=hp;
 group.userData.speed=level===1?2.2:level===2?3:3.7;
 group.userData.attackCooldown=0;
 group.userData.isEnemy=true;

 const side=Math.random()<.5?-1:1;
 group.position.set(
  side*(18+Math.random()*20),
  0,
  -10-Math.random()*50
 );

 scene.add(group);
 enemies.push(group);
}

// ---------------- WEAPONS ----------------

function switchGun(number){
 if(!unlocked[number]||!weapons[number])return;
 currentGun=number;
 buildWeapons();
 updateHUD();
}

function updateHUD(){
 const w=weapons[currentGun];
 document.getElementById('weaponName').textContent=w.name;
 document.getElementById('ammoText').textContent=
  w.ammo+" / "+w.total;
 document.getElementById('ammoFill').style.width=
  (w.ammo/w.mag*100)+"%";

 document.getElementById('healthText').textContent=health;
 document.getElementById('healthfill').style.width=health+"%";

 document.getElementById('score').textContent=score;
 document.getElementById('level').textContent=
  "LEVEL 0"+level;

 for(let i=1;i<=4;i++){
  const el=document.getElementById('g'+i);
  el.classList.toggle('active',i===currentGun);
  el.classList.toggle('locked',!unlocked[i]);
 }
}

function reload(){
 const w=weapons[currentGun];
 if(reloadTimer>0||w.ammo===w.mag||w.total<=0)return;

 reloadTimer=1.3;
 document.getElementById('message').textContent="RELOADING...";
 setTimeout(()=>{
  if(gameOver)return;
  const amount=Math.min(w.mag-w.ammo,w.total);
  w.ammo+=amount;
  w.total-=amount;
  reloadTimer=0;
  document.getElementById('message').textContent="";
  updateHUD();
 },1300);
}

function shoot(){
 if(!started||gameOver||reloadTimer>0)return;

 const w=weapons[currentGun];
 const now=performance.now();

 if(now-lastShot<w.rate)return;
 if(w.ammo<=0){reload();return;}

 lastShot=now;
 w.ammo--;
 recoil=.08;

 const pellets=w.pellets||1;
 let hit=false;

 for(let i=0;i<pellets;i++){
  raycaster.setFromCamera(new THREE.Vector2(
   (Math.random()-.5)*w.spread,
   (Math.random()-.5)*w.spread
  ),camera);

  const targets=[];
  enemies.forEach(e=>{
   e.traverse(obj=>{
    if(obj.isMesh)targets.push(obj);
   });
  });

  const intersects=raycaster.intersectObjects(targets,false);
  if(intersects.length){
   let enemy=intersects[0].object;
   while(enemy&&!enemy.userData.isEnemy)enemy=enemy.parent;

   if(enemy){
    enemy.userData.hp-=w.damage;
    hit=true;
    if(enemy.userData.hp<=0)killEnemy(enemy);
   }
  }
 }

 if(hit){
  const marker=document.getElementById('hitmarker');
  marker.style.display='block';
  setTimeout(()=>marker.style.display='none',100);
 }

 updateHUD();
}

function killEnemy(enemy){
 if(!enemies.includes(enemy))return;
 scene.remove(enemy);
 enemies=enemies.filter(e=>e!==enemy);
 score+=10;
 updateHUD();
 checkLevel();
}

// ---------------- LEVEL SYSTEM ----------------

function checkLevel(){
 if(score>=250&&level===1){
  level=2;
  unlockWeapon(3);
  scene.background=new THREE.Color(0x716b65);
  scene.fog.color.set(0x716b65);
  document.getElementById('message').textContent=
   "LEVEL 2 - INDUSTRIAL ZONE";
  setTimeout(()=>document.getElementById('message').textContent="",2500);
 }
 if(score>=600&&level===2){
  level=3;
  unlockWeapon(4);
  scene.background=new THREE.Color(0x152331);
  scene.fog.color.set(0x152331);
  document.getElementById('message').textContent=
   "LEVEL 3 - ELITE BATTLEFIELD";
  setTimeout(()=>document.getElementById('message').textContent="",2500);
 }
 updateHUD();
}

function unlockWeapon(number){
 unlocked[number]=true;
 document.getElementById('message').textContent=
  weapons[number].name+" UNLOCKED!";
 setTimeout(()=>{
  document.getElementById('message').textContent="";
 },2500);
}

// ---------------- ENEMY AI ----------------

function updateEnemies(dt){
 for(const enemy of [...enemies]){
  const direction=new THREE.Vector3(
   camera.position.x-enemy.position.x,
   0,
   camera.position.z-enemy.position.z
  );

  const distance=direction.length();
  direction.normalize();

  enemy.lookAt(camera.position.x,enemy.position.y,camera.position.z);

  if(distance>1.6){
   enemy.position.addScaledVector(
    direction,enemy.userData.speed*dt
   );
  }else{
   enemy.userData.attackCooldown-=dt;

   if(enemy.userData.attackCooldown<=0){
    health-=10;
    enemy.userData.attackCooldown=1.2;

    document.getElementById('damage').style.opacity=.7;
    setTimeout(()=>{
     document.getElementById('damage').style.opacity=0;
    },150);

    updateHUD();
    if(health<=0)endGame();
   }
  }
 }
}

// ---------------- PLAYER MOVEMENT ----------------

let yaw=0,pitch=0;

document.addEventListener('mousemove',e=>{
 if(!started||document.pointerLockElement!==document.body)return;

 yaw-=e.movementX*.002;
 pitch-=e.movementY*.002;
 pitch=Math.max(-1.4,Math.min(1.4,pitch));
 camera.rotation.set(pitch,yaw,0,'YXZ');
});

document.addEventListener('keydown',e=>{
 keys[e.code]=true;

 if(e.code==='Digit1')switchGun(1);
 if(e.code==='Digit2')switchGun(2);
 if(e.code==='Digit3')switchGun(3);
 if(e.code==='Digit4')switchGun(4);
 if(e.code==='KeyR')reload();
});

document.addEventListener('keyup',e=>keys[e.code]=false);

document.addEventListener('mousedown',e=>{
 if(e.button===0&&started){
  if(document.pointerLockElement!==document.body){
   document.body.requestPointerLock();
  }else{
   shoot();
  }
 }
});

function movePlayer(dt){
 const speed=keys.ShiftLeft||keys.ShiftRight?12:7;
 const forward=new THREE.Vector3(
  -Math.sin(yaw),0,-Math.cos(yaw)
 );
 const right=new THREE.Vector3(
  Math.cos(yaw),0,-Math.sin(yaw)
 );

 if(keys.KeyW)camera.position.addScaledVector(forward,speed*dt);
 if(keys.KeyS)camera.position.addScaledVector(forward,-speed*dt);
 if(keys.KeyA)camera.position.addScaledVector(right,-speed*dt);
 if(keys.KeyD)camera.position.addScaledVector(right,speed*dt);

 camera.position.x=THREE.MathUtils.clamp(camera.position.x,-47,47);
 camera.position.z=THREE.MathUtils.clamp(camera.position.z,-77,27);
 camera.position.y=2;
}

// ---------------- GAME LOOP ----------------

function animate(){
 requestAnimationFrame(animate);

 const dt=Math.min(clock.getDelta(),.05);

 if(started&&!gameOver){
  movePlayer(dt);
  updateEnemies(dt);

  spawnTimer+=dt;
  const maxEnemies=level===1?6:level===2?9:12;
  const spawnDelay=level===1?2.4:level===2?1.8:1.3;

  if(spawnTimer>spawnDelay&&enemies.length<maxEnemies){
   createEnemy();
   spawnTimer=0;
  }

  recoil=Math.max(0,recoil-dt*.5);
  weaponGroup.position.z=recoil;
 }
 renderer.render(scene,camera);
}
animate();

// ---------------- START / END ----------------

function startGame(){
 started=true;
 gameOver=false;
 document.getElementById('overlay').style.display='none';
 document.body.requestPointerLock();

 if(enemies.length===0){
  for(let i=0;i<3;i++)createEnemy();
 }
}

function endGame(){
 gameOver=true;
 started=false;
 document.exitPointerLock();

 document.getElementById('overlay').style.display='flex';
 document.querySelector('h1').innerHTML='MISSION <span>FAILED</span>';
 document.getElementById('start').textContent='PLAY AGAIN';
 document.getElementById('menuInfo').textContent=
  "Final score: "+score+" | Eliminations: "+score/10;
}

function resetGame(){
 enemies.forEach(e=>scene.remove(e));
 enemies=[];
 score=0;
 level=1;
 health=100;
 currentGun=1;
 unlocked[1]=true;
 unlocked[2]=true;
 unlocked[3]=false;
 unlocked[4]=false;

 for(const [id,w] of Object.entries(weapons)){
  w.ammo=w.mag;
  w.total=id==='1'?48:id==='2'?120:id==='3'?40:25;
 }

 yaw=0;pitch=0;
 camera.position.set(0,2,8);
 camera.rotation.set(0,0,0);
 spawnTimer=0;
 reloadTimer=0;
 document.querySelector('h1').innerHTML='SHADOW <span>STRIKE</span>';
 document.getElementById('menuInfo').textContent=
  "Defeat enemies to earn points and unlock weapons.";
 updateHUD();
 startGame();
}

document.getElementById('start').addEventListener('click',()=>{
 if(gameOver)resetGame();
 else startGame();
});

document.addEventListener('pointerlockchange',()=>{
 if(document.pointerLockElement!==document.body&&started){
  started=false;
  document.getElementById('overlay').style.display='flex';
  document.querySelector('h1').innerHTML='GAME <span>PAUSED</span>';
  document.getElementById('start').textContent='RESUME';
  document.getElementById('menuInfo').textContent=
   'Click resume to continue your mission.';
 }
});

document.getElementById('start').addEventListener('click',()=>{
 if(!gameOver&&health>0&&score>0){
  started=true;
  document.getElementById('overlay').style.display='none';
  document.body.requestPointerLock();
 }
});

addEventListener('resize',()=>{
 camera.aspect=innerWidth/innerHeight;
 camera.updateProjectionMatrix();
 renderer.setSize(innerWidth,innerHeight);
});

updateHUD();
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
