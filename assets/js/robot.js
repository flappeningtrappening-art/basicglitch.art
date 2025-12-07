/* robot.js — multi-robot randomizer + interactions + effects */

// Config
const ROBOT_IMAGES = [
  { src: '/assets/images/guitarbot.png', id: 'guitarbot', audioPath: '/assets/audio/guitarbot/' },
  { src: '/assets/images/broboticus_og.png', id: 'broboticus', audioPath: '/assets/audio/broboticus/' }
];

const ROBOT_PROBABILITY = 0.75; // chance to show robots
const ROBOT_ANIM_PROB = 0.75;
const AUDIO_POOL_COUNT = 3;

// utility
function randBool(p){ return Math.random() < p; }

// ✅ APPLY TO BOTH ROBOTS
document.addEventListener('DOMContentLoaded', ()=>{
  const robots = document.querySelectorAll('#robot-foreground, #side-robot');
  if(!robots.length) return;

  robots.forEach(robotEl => {
    if(!randBool(ROBOT_PROBABILITY)){
      robotEl.style.display = 'none';
      return;
    }

    const pick = ROBOT_IMAGES[Math.floor(Math.random()*ROBOT_IMAGES.length)];
    robotEl.src = pick.src;
    robotEl.dataset.robotId = pick.id;
    robotEl.style.display = 'block';
    robotEl.style.cursor = 'pointer';

    if(randBool(ROBOT_ANIM_PROB)){
      robotEl.classList.add('animated');
    }

    robotEl.addEventListener('click', ()=> {
      triggerRobotAction(pick);
    });

    robotEl.addEventListener('touchstart', ()=> {
      triggerRobotAction(pick);
    }, {passive:true});
  });
});

// ✅ SOUND + VISUAL FX
function triggerRobotAction(robot){
  const n = Math.floor(Math.random()*AUDIO_POOL_COUNT) + 1;
  const file = `${robot.audioPath}${robot.id}_${n}.mp3`;

  try{
    const a = new Audio(file);
    a.volume = 0.7;
    a.play().catch(err=>console.warn(err));

    const effects = ['effect-neon-pulse','effect-glitch-burst','effect-rgb-split','effect-ripple'];
    const pick = effects[Math.floor(Math.random()*effects.length)];
    applyVisualEffect(pick);

  }catch(e){
    console.warn('audio error', e);
  }
}

// ✅ APPLY FX TO HERO + BOTH ROBOTS
function applyVisualEffect(cls){
  const hero = document.querySelector('.hero');
  const robots = document.querySelectorAll('#robot-foreground, #side-robot');

  if(hero) hero.classList.add(cls);
  robots.forEach(r => r.classList.add(cls));

  setTimeout(()=>{
    if(hero) hero.classList.remove(cls);
    robots.forEach(r => r.classList.remove(cls));
  }, 900);
}

// ✅ KEYBOARD TEST
document.addEventListener('keydown', (e)=>{
  if(e.key === 'r'){
    const r = document.querySelector('#robot-foreground, #side-robot');
    if(r && r.dataset.robotId){
      triggerRobotAction({
        id:r.dataset.robotId,
        audioPath:`/assets/audio/${r.dataset.robotId}/`,
        src:r.src
      });
    }
  }
});
