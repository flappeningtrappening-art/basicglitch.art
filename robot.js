/* robot.js — robot foreground randomizer + interactions + small effects */

// Config
const ROBOT_IMAGES = [
  { src: '/assets/images/guitarbot.png', id: 'guitarbot', audioPath: '/assets/audio/guitarbot/' },
  { src: '/assets/images/broboticus_og.png', id: 'broboticus', audioPath: '/assets/audio/broboticus/' }
];
const ROBOT_PROBABILITY = 0.5; // 50% chance to show foreground on page load
const ROBOT_ANIM_PROB = 0.67; // if shown, 67% chance to animate (float)
const AUDIO_POOL_COUNT = 3; // expects files named broboticus_1.mp3 ... broboticus_3.mp3

// utility
function randBool(p){ return Math.random() < p; }

// create or attach robot element
document.addEventListener('DOMContentLoaded', ()=>{
  const show = randBool(ROBOT_PROBABILITY);
  const robotEl = document.getElementById('robot-foreground');
  if(!robotEl) return;

  if(!show){
    robotEl.style.display = 'none';
    return;
  }

  // choose a robot at random (50/50)
  const pick = ROBOT_IMAGES[Math.floor(Math.random()*ROBOT_IMAGES.length)];
  robotEl.src = pick.src;
  robotEl.dataset.robotId = pick.id;
  robotEl.style.display = 'block';

  // decide if animated float
  if(randBool(ROBOT_ANIM_PROB)) robotEl.classList.add('animated');

  // pointer interaction: click to trigger sound + effect
  robotEl.style.cursor = 'pointer';
  robotEl.addEventListener('click', ()=> {
    triggerRobotAction(pick);
  });

  // mobile tap also handled by click; optionally add touchstart
  robotEl.addEventListener('touchstart', ()=> {
    triggerRobotAction(pick);
  }, {passive:true});
});

// Plays a random sound from robot audio folder and triggers a visual effect.
function triggerRobotAction(robot){
  // sound selection
  // expect files named e.g. guitarbot_1.mp3 .. guitarbot_3.mp3 (adjust AUDIO_POOL_COUNT)
  const max = AUDIO_POOL_COUNT;
  const n = Math.floor(Math.random()*max) + 1;
  const file = `${robot.audioPath}${robot.id}_${n}.mp3`;

  // create audio element and play
  try{
    const a = new Audio(file);
    a.volume = 0.7;
    a.play().catch(err=>{ console.warn('audio play failed', err); });

    // choose a visual effect randomly
    const effects = ['effect-neon-pulse','effect-glitch-burst','effect-rgb-split','effect-ripple'];
    const pick = effects[Math.floor(Math.random()*effects.length)];
    applyVisualEffect(pick);
  }catch(e){
    console.warn('audio error', e);
  }
}

function applyVisualEffect(cls){
  // apply to hero and robot to keep consistent visual
  const hero = document.querySelector('.hero');
  const robotEl = document.getElementById('robot-foreground');
  if(hero) hero.classList.add(cls);
  if(robotEl) robotEl.classList.add(cls);

  setTimeout(()=>{
    if(hero) hero.classList.remove(cls);
    if(robotEl) robotEl.classList.remove(cls);
  }, 900);
}

/* Optional: keyboard shortcut to audition robots (for testing) */
document.addEventListener('keydown', (e)=>{
  if(e.key === 'r'){ // press 'r' to trigger robot action if present
    const robotEl = document.getElementById('robot-foreground');
    if(robotEl && robotEl.dataset.robotId){
      triggerRobotAction({ id: robotEl.dataset.robotId, audioPath: `/assets/audio/${robotEl.dataset.robotId}/`, src: robotEl.src });
    }
  }
});
