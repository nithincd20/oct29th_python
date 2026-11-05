

from flask import Flask, render_template_string

app = Flask(__name__)

PAGE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Superbike Rush 3D</title>

<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#030711;color:white;font-family:Arial;overflow:hidden}
canvas{display:block}
#hud{
 position:fixed;top:15px;left:15px;right:15px;
 display:flex;justify-content:space-between;
 gap:8px;z-index:5;pointer-events:none
}
.info{
 background:#071a2ddd;border:1px solid #00d9ff;
 padding:10px 14px;border-radius:9px;
 box-shadow:0 0 12px #00cfff33
}
.info small{color:#00eaff;font-size:11px}
.info div{font-size:19px;font-weight:bold;margin-top:5px}
#overlay{
 position:fixed;inset:0;z-index:10;
 display:flex;align-items:center;justify-content:center;
 background:linear-gradient(135deg,#020817ed,#092c43dd);
 text-align:center;padding:15px
}
.card{
 width:min(500px,95%);padding:35px 22px;
 background:#061525;border:1px solid #00cfff;
 border-radius:18px;box-shadow:0 0 35px #008cff55
}
h1{font-size:clamp(32px,7vw,55px);color:#00eaff}
.card p{line-height:1.8;color:#d5eaf4;margin:20px 0}
button{
 border:0;border-radius:9px;padding:14px 23px;
 background:linear-gradient(90deg,#008cff,#00eaff);
 font-weight:bold;font-size:16px;cursor:pointer;color:#00121e
}
button:active{transform:scale(.96)}
#message{
 position:fixed;top:27%;left:0;right:0;
 text-align:center;font-size:30px;font-weight:bold;
 color:#00eaff;text-shadow:0 0 15px #00cfff;
 opacity:0;z-index:6;pointer-events:none
}
#controls{
 position:fixed;bottom:18px;left:0;right:0;
 display:flex;justify-content:center;gap:15px;
 z-index:5;pointer-events:none
}
#controls button{
 width:65px;height:58px;padding:0;
 font-size:23px;pointer-events:auto;
 touch-action:none
}
#nitro{
 position:fixed;right:15px;bottom:90px;
 z-index:5;background:#ff8c00;color:white;
 pointer-events:auto
}
#instructions{
 position:fixed;bottom:5px;left:0;right:0;
 text-align:center;font-size:11px;color:#bcd7e9;
 pointer-events:none
}
</style>
</head>
<body>

<div id="hud">
 <div class="info"><small>RACE LEVEL</small><div id="level">1</div></div>
 <div class="info"><small>SCORE</small><div id="score">0</div></div>
 <div class="info"><small>SPEED</small><div id="speed">0 KM/H</div></div>
 <div class="info"><small>DISTANCE</small><div id="distance">0 M</div></div>
</div>

<div id="message"></div>

<div id="overlay">
 <div class="card">
  <h1>SUPERBIKE<br>RUSH 3D</h1>
  <p>
   Experience the ultimate superbike racing challenge.<br>
   LEVEL 1: SNOW<br>
   LEVEL 2: MUD<br>
   LEVEL 3: NIGHT HIGHWAY
  </p>
  <button id="start">START RACE</button>
  <p style="font-size:12px">
   W / UP = Accelerate<br>
   A / LEFT = Steer left<br>
   D / RIGHT = Steer right<br>
   S / DOWN = Brake · SHIFT = Nitro
  </p>
 </div>
</div>

<button id="nitro">NITRO ⚡</button>

<div id="controls">
 <button id="left">◀</button>
 <button id="right">▶</button>
</div>
<div id="instructions">Avoid traffic • Collect distance • Unlock upgraded superbikes</div>

<script type="module">
import * as THREE from
'https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js';

import { GLTFLoader } from
'https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/loaders/GLTFLoader.js';

// ---------------- SCENE ----------------

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x9ccbea);
scene.fog = new THREE.Fog(0x9ccbea,35,160);

const camera = new THREE.PerspectiveCamera(
 65,innerWidth/innerHeight,.1,500
);
camera.position.set(0,5,12);

const renderer = new THREE.WebGLRenderer({antialias:true});
renderer.setSize(innerWidth,innerHeight);
renderer.setPixelRatio(Math.min(devicePixelRatio,2));
renderer.shadowMap.enabled=true;
renderer.shadowMap.type=THREE.PCFSoftShadowMap;
renderer.toneMapping=THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure=1.15;
document.body.appendChild(renderer.domElement);

scene.add(new THREE.HemisphereLight(0xffffff,0x526071,2));

const sun=new THREE.DirectionalLight(0xffffff,2.5);
sun.position.set(-15,25,12);
sun.castShadow=true;
scene.add(sun);

// ---------------- MATERIALS ----------------

function material(color,metalness=0,roughness=.5){
 return new THREE.MeshStandardMaterial({
  color,metalness,roughness
 });
}

const colors=[0xe51b35,0xffa000,0x00eaff];

const roadMaterials=[
 material(0xe2edf4),
 material(0x513a29),
 material(0x20242d,.25)
];

const bikeNames=[
 'BMW S1000RR',
 'DUCATI PANIGALE V4',
 'KAWASAKI NINJA H2R'
];

// ---------------- GAME STATE ----------------

let running=false;
let gameOver=false;
let score=0;
let distance=0;
let speed=0;
let level=1;
let lane=0;
let nitro=100;
let spawnTime=0;
let environment=-1;

const keys={};
const obstacles=[];
const decorations=[];
const marks=[];

let bike=new THREE.Group();
let bikeBody=new THREE.Group();
scene.add(bike);

let importedModel=null;

// ---------------- HELPERS ----------------

function addBox(parent,w,h,d,mat,x,y,z){
 const m=new THREE.Mesh(
  new THREE.BoxGeometry(w,h,d),mat
 );
 m.position.set(x,y,z);
 m.castShadow=true;
 m.receiveShadow=true;
 parent.add(m);
 return m;
}

// ---------------- SUPERBIKE MODEL ----------------

function buildBike(index){

 bike.remove(bikeBody);
 bikeBody=new THREE.Group();

 if(importedModel){
  bikeBody.add(importedModel.clone());
 }else{

  const paint=material(colors[index],.65,.25);
  const black=material(0x090d13,.25,.3);
  const metal=material(0x9daebc,.85,.2);
  const glass=material(0x17405b,.6,.15);

  // Fuel tank and frame
  addBox(bikeBody,.8,.48,1.1,paint,0,1,-.05);
  addBox(bikeBody,.55,.32,.8,black,0,.75,.65);

  // Front fairing
  const front=addBox(
   bikeBody,.85,.72,.65,paint,0,1.3,-.85
  );
  front.rotation.x=-.12;

  // Windshield
  const screen=addBox(
   bikeBody,.52,.48,.08,glass,0,1.75,-.98
  );
  screen.rotation.x=-.35;

  // Rear body
  addBox(bikeBody,.58,.3,.9,black,0,1.12,.95);
  addBox(bikeBody,.55,.32,.65,paint,0,1.32,1.25);

  // Handlebar
  addBox(bikeBody,1.25,.07,.12,metal,0,1.52,-.5);

  // Wheels
  function wheel(z){
   const tire=new THREE.Mesh(
    new THREE.TorusGeometry(.48,.13,12,32),
    black
   );
   tire.rotation.y=Math.PI/2;
   tire.position.set(0,.52,z);
   bikeBody.add(tire);

   const rim=new THREE.Mesh(
    new THREE.TorusGeometry(.29,.035,8,24),
    material(0xc0d0db,.8,.2)
   );
   rim.rotation.y=Math.PI/2;
   rim.position.set(0,.52,z);
   bikeBody.add(rim);
  }

  wheel(-1.12);
  wheel(1.15);

  // Front forks
  for(const x of [-.22,.22]){
   const fork=new THREE.Mesh(
    new THREE.CylinderGeometry(.045,.045,.9,12),
    metal
   );
   fork.position.set(x,.88,-.85);
   bikeBody.add(fork);
  }

  // Exhaust
  const exhaust=new THREE.Mesh(
   new THREE.CylinderGeometry(.1,.15,.75,12),
   metal
  );
  exhaust.rotation.x=Math.PI/2;
  exhaust.position.set(.45,.7,.65);
  bikeBody.add(exhaust);

  // Headlight
  addBox(
   bikeBody,.4,.17,.06,
   material(0x9ff7ff,.1,.1),0,1.35,-1.22
  );

  // Mirrors
  for(const x of [-.65,.65]){
   addBox(bikeBody,.17,.12,.1,black,x,1.68,-.5);
  }
 }

 bike.add(bikeBody);
 bike.position.set(0,0,4);
}

// Optional Blender GLB model
const gltfLoader=new GLTFLoader();
gltfLoader.load(
 '/static/bike.glb',
 gltf=>{
  importedModel=gltf.scene;
  importedModel.scale.set(.8,.8,.8);
  buildBike(level-1);
 },
 undefined,
 ()=>console.log('No Blender model found. Using built-in bike.')
);

buildBike(0);

// ---------------- ROAD ----------------

const road=new THREE.Mesh(
 new THREE.PlaneGeometry(16,450),
 roadMaterials[0]
);
road.rotation.x=-Math.PI/2;
road.position.set(0,0,-180);
road.receiveShadow=true;
scene.add(road);

// Road boundaries
for(const x of [-8,8]){
 const edge=addBox(
  scene,.35,.25,450,
  material(0xe7edf3),x,.1,-180
 );
}

// Road lane markings
for(let i=0;i<40;i++){
 const mark=addBox(
  scene,.13,.025,3,
  material(0xffffff),0,.025,10-i*11
 );
 marks.push(mark);
}

// ---------------- ENVIRONMENT ----------------

function clearDecorations(){
 for(const d of decorations) scene.remove(d);
 decorations.length=0;
}

function makeEnvironment(){

 clearDecorations();

 for(let i=0;i<42;i++){

  const side=Math.random()>.5?1:-1;
  const group=new THREE.Group();

  if(level===1){

   // Snow trees
   const trunk=new THREE.Mesh(
    new THREE.CylinderGeometry(.16,.25,2,8),
    material(0x5b4937)
   );
   trunk.position.y=1;
   group.add(trunk);

   const leaves=new THREE.Mesh(
    new THREE.ConeGeometry(1.25,3,8),
    material(0xf0f8ff)
   );
   leaves.position.y=3;
   group.add(leaves);

  }else if(level===2){

   // Mud rocks and bushes
   const rock=new THREE.Mesh(
    new THREE.DodecahedronGeometry(.8+Math.random(),1),
    material(0x59402c)
   );
   rock.position.y=.5;
   group.add(rock);

   const bush=new THREE.Mesh(
    new THREE.SphereGeometry(.65,8,8),
    material(0x354b2b)
   );
   bush.position.set(.6,.45,.2);
   group.add(bush);

  }else{

   // Highway streetlights
   const pole=new THREE.Mesh(
    new THREE.CylinderGeometry(.07,.12,7,8),
    material(0x606b78,.7)
   );
   pole.position.y=3.5;
   group.add(pole);

   const arm=addBox(
    group,1.4,.12,.12,
    material(0x606b78),side>0?-.5:.5,6.8,0
   );

   const lamp=addBox(
    group,.6,.13,.5,
    material(0xffe29b,0,.15),
    side>0?-1:.5,6.65,0
   );
  }

  group.position.set(
   side*(11+Math.random()*3),
   0,
   -Math.random()*430
  );

  scene.add(group);
  decorations.push(group);
 }
}

function changeEnvironment(){
 const env=level-1;
 if(env===environment)return;

 environment=env;
 road.material=roadMaterials[env];

 if(level===1){
  scene.background.set(0x9ccbea);
  scene.fog.color.set(0xc8e4f5);
  scene.fog.near=35;
 }else if(level===2){
  scene.background.set(0x98785e);
  scene.fog.color.set(0x98785e);
  scene.fog.near=30;
 }else{
  scene.background.set(0x101c37);
  scene.fog.color.set(0x101c37);
  scene.fog.near=35;
 }

 makeEnvironment();

 showMessage(
  'LEVEL '+level+'<br><small>'+bikeNames[level-1]+'</small>'
 );
}

// ---------------- TRAFFIC ----------------

function createTraffic(){

 const group=new THREE.Group();

 const paint=material(
  [0xff2929,0xffbb00,0x18caff,0xffffff][
   Math.floor(Math.random()*4)
  ],.3,.35
 );

 addBox(group,1.8,1,3,paint,0,.8,0);
 addBox(
  group,1.3,.6,1.5,
  material(0x192a3a,.4,.2),0,1.55,0
 );

 for(const x of [-.7,.7]){
  for(const z of [-1,1]){
   const w=new THREE.Mesh(
    new THREE.CylinderGeometry(.25,.25,.2,12),
    material(0x080808)
   );
   w.rotation.z=Math.PI/2;
   w.position.set(x,.3,z);
   group.add(w);
  }
 }

 const lanes=[-4,0,4];
 group.position.set(
  lanes[Math.floor(Math.random()*3)],
  0,-100-Math.random()*20
 );

 scene.add(group);
 obstacles.push(group);
}

// ---------------- INPUT ----------------

function setKey(key,value){
 keys[key]=value;
}

document.addEventListener('keydown',e=>{
 const k=e.key.toLowerCase();
 setKey(k,true);

 if(['arrowleft','arrowright','arrowup','arrowdown',' '].includes(k)){
  e.preventDefault();
 }
});

document.addEventListener('keyup',e=>{
 setKey(e.key.toLowerCase(),false);
});

function bindButton(id,key){
 const b=document.getElementById(id);

 b.addEventListener('pointerdown',e=>{
  e.preventDefault();
  setKey(key,true);
  b.setPointerCapture(e.pointerId);
 });

 ['pointerup','pointercancel','lostpointercapture'].forEach(ev=>{
  b.addEventListener(ev,()=>setKey(key,false));
 });
}

bindButton('left','a');
bindButton('right','d');
bindButton('nitro','shift');

// ---------------- HUD ----------------

function updateHUD(){
 document.getElementById('level').textContent=level;
 document.getElementById('score').textContent=Math.floor(score);
 document.getElementById('speed').textContent=
  Math.floor(speed*8)+' KM/H';
 document.getElementById('distance').textContent=
  Math.floor(distance)+' M';
}

function showMessage(text){
 const m=document.getElementById('message');
 m.innerHTML=text;
 m.style.opacity=1;
 clearTimeout(showMessage.timer);
 showMessage.timer=setTimeout(()=>m.style.opacity=0,2200);
}

// ---------------- START / END ----------------

function resetGame(){

 for(const o of obstacles)scene.remove(o);
 obstacles.length=0;

 score=0;
 distance=0;
 speed=0;
 nitro=100;
 lane=0;
 spawnTime=0;
 level=1;
 environment=-1;
 gameOver=false;
 running=true;

 bike.position.set(0,0,4);
 bike.rotation.set(0,0,0);

 for(const k in keys)keys[k]=false;

 changeEnvironment();
 buildBike(0);
 updateHUD();

 document.getElementById('overlay').style.display='none';
}

function endGame(){
 if(gameOver)return;

 gameOver=true;
 running=false;

 document.getElementById('overlay').style.display='flex';
 document.querySelector('.card').innerHTML=`
  <h1>RACE OVER</h1>
  <p>
   Final score: ${Math.floor(score)}<br>
   Distance: ${Math.floor(distance)} m<br>
   Level reached: ${level}
  </p>
  <button id="restart">RESTART RACE</button>
 `;
 document.getElementById('restart').onclick=resetGame;
}

document.getElementById('start').onclick=resetGame;

// ---------------- MAIN GAME LOOP ----------------

const clock=new THREE.Clock();

function animate(){

 requestAnimationFrame(animate);

 const dt=Math.min(clock.getDelta(),.04);

 if(running){

  // Acceleration and braking
  const accelerating=keys['w']||keys['arrowup'];
  const braking=keys['s']||keys['arrowdown'];
  const boosting=keys['shift'];

  if(accelerating)speed+=dt*18;
  else speed-=dt*4;

  if(braking)speed-=dt*25;

  if(boosting&&nitro>0&&!braking){
   speed+=dt*25;
   nitro-=dt*24;
  }else{
   nitro=Math.min(100,nitro+dt*8);
  }

  speed=THREE.MathUtils.clamp(speed,0,55);

  distance+=speed*dt*.55;
  score+=speed*dt*.18;

  // Level progression
  const newLevel=distance<350?1:
                 distance<800?2:3;

  if(newLevel!==level){
   level=newLevel;
   buildBike(level-1);
   changeEnvironment();
  }

  // Steering
  if(keys['a']||keys['arrowleft'])lane-=dt*8;
  if(keys['d']||keys['arrowright'])lane+=dt*8;

  lane=THREE.MathUtils.clamp(lane,-5,5);

  bike.position.x=THREE.MathUtils.lerp(
   bike.position.x,lane,.13
  );

  // Bike lean
  const steering=keys['a']||keys['arrowleft']?-1:
                 keys['d']||keys['arrowright']?1:0;

  bike.rotation.z=THREE.MathUtils.lerp(
   bike.rotation.z,-steering*.3,.12
  );

  // Road movement
  for(const mark of marks){
   mark.position.z+=speed*dt;
   if(mark.position.z>15)mark.position.z-=440;
  }

  // Scenery movement
  for(const obj of decorations){
   obj.position.z+=speed*dt;

   if(obj.position.z>18){
    obj.position.z=-420-Math.random()*20;
   }
  }

  // Traffic spawning
  spawnTime+=dt;

  if(spawnTime>Math.max(.55,1.6-level*.25)){
   createTraffic();
   spawnTime=0;
  }

  // Traffic and collision
  for(let i=obstacles.length-1;i>=0;i--){

   const o=obstacles[i];
   o.position.z+=speed*dt;

   const closeZ=Math.abs(o.position.z-bike.position.z)<2.2;
   const closeX=Math.abs(o.position.x-bike.position.x)<1.45;

   if(closeZ&&closeX){
    endGame();
    break;
   }

   if(o.position.z>15){
    scene.remove(o);
    obstacles.splice(i,1);
    score+=100;
   }
  }

  // Camera follows player
  camera.position.x=THREE.MathUtils.lerp(
   camera.position.x,bike.position.x*.4,.06
  );

  camera.position.y=THREE.MathUtils.lerp(
   camera.position.y,5,.06
  );

  camera.lookAt(bike.position.x*.3,1,-9);

  updateHUD();
 }

 renderer.render(scene,camera);
}

animate();

// ---------------- RESIZE ----------------

window.addEventListener('resize',()=>{
 camera.aspect=innerWidth/innerHeight;
 camera.updateProjectionMatrix();
 renderer.setSize(innerWidth,innerHeight);
});
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(PAGE)

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
