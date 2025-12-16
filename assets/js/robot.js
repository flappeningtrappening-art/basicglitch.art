/* robot.js — multi-robot randomizer + interactions + effects 
   ENHANCED VERSION WITH NEON GRID INTERACTIONS */

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

// ✅ ADD NEON GRID EFFECT STYLES
function addGridEffectStyles() {
  const style = document.createElement('style');
  style.textContent = `
    @keyframes gridIntensify {
      0% { 
        opacity: 0.7;
        filter: brightness(1);
      }
      50% { 
        opacity: 1;
        filter: brightness(1.3);
      }
      100% { 
        opacity: 0.7;
        filter: brightness(1);
      }
    }
    
    @keyframes gridGlitch {
      0% {
        background-position: 0px 0px, 0px 0px;
        filter: hue-rotate(0deg);
      }
      20% {
        background-position: 10px 10px, 10px 10px;
        filter: hue-rotate(90deg);
      }
      40% {
        background-position: -10px -10px, -10px -10px;
        filter: hue-rotate(180deg);
      }
      60% {
        background-position: 15px 15px, 15px 15px;
        filter: hue-rotate(270deg);
      }
      80% {
        background-position: -5px -5px, -5px -5px;
        filter: hue-rotate(360deg);
      }
      100% {
        background-position: 0px 0px, 0px 0px;
        filter: hue-rotate(0deg);
      }
    }
    
    @keyframes gridPulseWave {
      0% {
        --grid-wave-opacity: 0;
        --grid-wave-size: 0;
      }
      50% {
        --grid-wave-opacity: 0.5;
        --grid-wave-size: 50px;
      }
      100% {
        --grid-wave-opacity: 0;
        --grid-wave-size: 100px;
      }
    }
    
    .neon-grid-section.grid-effect-active::before {
      animation: 
        gridMove 30s linear infinite,
        gridIntensify 1.5s ease-in-out !important;
    }
    
    .neon-grid-section.grid-glitch-active::before {
      animation: 
        gridGlitch 0.8s steps(4) infinite,
        gridMove 30s linear infinite !important;
    }
    
    /* Robot click ripple effect */
    .robot-ripple {
      position: absolute;
      border-radius: 50%;
      background: radial-gradient(circle, var(--neon-mag) 0%, transparent 70%);
      pointer-events: none;
      z-index: -1;
      transform: translate(-50%, -50%);
      opacity: 0;
    }
    
    /* Enhanced visual effects that work with grid */
    .effect-neon-pulse-enhanced .hero-overlay {
      animation: neonPulse 0.9s ease-in-out;
    }
    
    @keyframes neonPulse {
      0%, 100% { opacity: 0.6; }
      50% { opacity: 0.3; }
    }
    
    .effect-glitch-burst-enhanced::before {
      content: '';
      position: absolute;
      inset: 0;
      background: linear-gradient(45deg, 
        transparent 45%, 
        var(--neon-mag) 50%, 
        transparent 55%
      );
      background-size: 200% 200%;
      animation: glitchScan 0.9s linear;
      pointer-events: none;
      z-index: 10;
      mix-blend-mode: screen;
    }
    
    @keyframes glitchScan {
      0% { background-position: 0% 0%; }
      100% { background-position: 100% 100%; }
    }
  `;
  document.head.appendChild(style);
}

// ✅ APPLY TO BOTH ROBOTS
document.addEventListener('DOMContentLoaded', ()=>{
  // Add grid effect styles first
  addGridEffectStyles();
  
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
    robotEl.title = `Click ${pick.id} for a surprise!`;

    if(randBool(ROBOT_ANIM_PROB)){
      robotEl.classList.add('animated');
    }

    // Enhanced click with ripple effect
    robotEl.addEventListener('click', (e)=> {
      triggerRobotAction(pick, e);
    });

    robotEl.addEventListener('touchstart', (e)=> {
      triggerRobotAction(pick, e);
    }, {passive:true});
  });
});

// ✅ ENHANCED SOUND + VISUAL FX WITH GRID INTERACTION
function triggerRobotAction(robot, event){
  const n = Math.floor(Math.random()*AUDIO_POOL_COUNT) + 1;
  const file = `${robot.audioPath}${robot.id}_${n}.mp3`;

  try{
    const a = new Audio(file);
    a.volume = 0.7;
    a.play().catch(err=>console.warn(err));

    // Create ripple effect at click position
    if (event) {
      createRippleEffect(event);
    }
    
    // Choose random effect that interacts with grid
    const effects = [
      'grid-intensify', 
      'grid-glitch', 
      'neon-pulse-enhanced', 
      'glitch-burst-enhanced'
    ];
    const pick = effects[Math.floor(Math.random()*effects.length)];
    applyEnhancedVisualEffect(pick, robot.id);

  }catch(e){
    console.warn('audio error', e);
  }
}

// ✅ CREATE RIPPLE EFFECT
function createRippleEffect(event) {
  const ripple = document.createElement('div');
  ripple.className = 'robot-ripple';
  
  // Position at click/touch
  const x = event.clientX || event.touches[0].clientX;
  const y = event.clientY || event.touches[0].clientY;
  
  ripple.style.left = `${x}px`;
  ripple.style.top = `${y}px`;
  ripple.style.width = '0px';
  ripple.style.height = '0px';
  
  document.body.appendChild(ripple);
  
  // Animate ripple
  ripple.animate([
    { width: '0px', height: '0px', opacity: 0.8 },
    { width: '300px', height: '300px', opacity: 0 }
  ], {
    duration: 1000,
    easing: 'cubic-bezier(0.215, 0.61, 0.355, 1)'
  });
  
  // Remove after animation
  setTimeout(() => {
    if (ripple.parentNode) {
      ripple.parentNode.removeChild(ripple);
    }
  }, 1000);
}

// ✅ ENHANCED APPLY FX TO HERO + BOTH ROBOTS + NEON GRIDS
function applyEnhancedVisualEffect(effectType, robotId){
  const hero = document.querySelector('.hero');
  const robots = document.querySelectorAll('#robot-foreground, #side-robot');
  const neonSections = document.querySelectorAll('.neon-grid-section');
  
  // Remove any existing effects first
  neonSections.forEach(section => {
    section.classList.remove('grid-effect-active', 'grid-glitch-active');
  });
  
  if(hero) hero.classList.remove('effect-neon-pulse-enhanced', 'effect-glitch-burst-enhanced');
  robots.forEach(r => r.classList.remove('effect-neon-pulse-enhanced', 'effect-glitch-burst-enhanced'));
  
  // Apply new effect based on type
  switch(effectType) {
    case 'grid-intensify':
      neonSections.forEach(section => {
        section.classList.add('grid-effect-active');
      });
      break;
      
    case 'grid-glitch':
      neonSections.forEach(section => {
        section.classList.add('grid-glitch-active');
      });
      break;
      
    case 'neon-pulse-enhanced':
      if(hero) hero.classList.add('effect-neon-pulse-enhanced');
      robots.forEach(r => r.classList.add('effect-neon-pulse-enhanced'));
      
      // Also pulse the grids slightly
      neonSections.forEach(section => {
        section.style.opacity = '0.9';
      });
      break;
      
    case 'glitch-burst-enhanced':
      if(hero) hero.classList.add('effect-glitch-burst-enhanced');
      robots.forEach(r => r.classList.add('effect-glitch-burst-enhanced'));
      break;
  }
  
  // Add robot-specific color tint to grid
  const gridColor = robotId === 'guitarbot' ? 'var(--neon-mag)' : 'var(--neon)';
  neonSections.forEach(section => {
    if (section.querySelector('::before')) {
      section.style.setProperty('--grid-tint-color', gridColor);
    }
  });

  // Remove effects after duration
  setTimeout(()=>{
    neonSections.forEach(section => {
      section.classList.remove('grid-effect-active', 'grid-glitch-active');
      section.style.opacity = '';
      section.style.setProperty('--grid-tint-color', '');
    });
    
    if(hero) hero.classList.remove('effect-neon-pulse-enhanced', 'effect-glitch-burst-enhanced');
    robots.forEach(r => r.classList.remove('effect-neon-pulse-enhanced', 'effect-glitch-burst-enhanced'));
  }, 1500);
}

// ✅ ENHANCED KEYBOARD TEST
document.addEventListener('keydown', (e)=>{
  if(e.key === 'r' || e.key === 'R'){
    const r = document.querySelector('#robot-foreground, #side-robot');
    if(r && r.dataset.robotId){
      // Simulate click at robot position
      const rect = r.getBoundingClientRect();
      const fakeEvent = {
        clientX: rect.left + rect.width / 2,
        clientY: rect.top + rect.height / 2,
        touches: [{ clientX: rect.left + rect.width / 2, clientY: rect.top + rect.height / 2 }]
      };
      
      triggerRobotAction({
        id: r.dataset.robotId,
        audioPath: `/assets/audio/${r.dataset.robotId}/`,
        src: r.src
      }, fakeEvent);
    }
  }
  
  // Bonus: 'G' key to trigger grid effect directly
  if(e.key === 'g' || e.key === 'G') {
    const neonSections = document.querySelectorAll('.neon-grid-section');
    neonSections.forEach(section => {
      section.classList.add('grid-effect-active');
      setTimeout(() => {
        section.classList.remove('grid-effect-active');
      }, 1500);
    });
  }
});

// ✅ ADD ROBOT HOVER EFFECTS
document.addEventListener('DOMContentLoaded', () => {
  // Add hover effect to robots
  const robots = document.querySelectorAll('#robot-foreground, #side-robot');
  
  robots.forEach(robot => {
    robot.addEventListener('mouseenter', () => {
      robot.style.filter = 'drop-shadow(0 0 10px var(--neon)) brightness(1.2)';
      robot.style.transition = 'filter 0.3s ease';
    });
    
    robot.addEventListener('mouseleave', () => {
      robot.style.filter = '';
    });
  });
  
  // Add subtle pulsing to robots when near neon grids
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      const robot = entry.target;
      if (entry.isIntersecting) {
        // Robot is visible and near a neon section
        if (!robot.classList.contains('animated')) {
          robot.style.animation = 'robotSubtlePulse 2s ease-in-out infinite';
        }
      } else {
        robot.style.animation = '';
      }
    });
  }, { threshold: 0.1 });
  
  robots.forEach(robot => observer.observe(robot));
});

// ✅ ADD SUBTLE PULSE ANIMATION FOR ROBOTS
const robotPulseStyle = document.createElement('style');
robotPulseStyle.textContent = `
  @keyframes robotSubtlePulse {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-5px); }
  }
  
  /* Enhance existing robot float animation */
  @keyframes robotFloat {
    0% { transform: translateY(0) rotate(0deg); }
    33% { transform: translateY(-16px) rotate(2deg); }
    66% { transform: translateY(-8px) rotate(-2deg); }
    100% { transform: translateY(0) rotate(0deg); }
  }
  
  .robot-foreground.animated {
    animation: robotFloat 4.8s ease-in-out infinite;
  }
`;
document.head.appendChild(robotPulseStyle);
