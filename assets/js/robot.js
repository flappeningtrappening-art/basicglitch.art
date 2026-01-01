/* robot.js — Section Guardian interactions 
   ENHANCED VERSION: Monumental static anchors with glitch effects */

// Config
const ROBOT_ASSETS = {
  'guitarbot': { audioPath: '/assets/audio/guitarbot/', color: 'var(--neon-mag)' },
  'broboticus': { audioPath: '/assets/audio/broboticus/', color: 'var(--neon)' }
};

const AUDIO_POOL_COUNT = 3;

// ✅ ADD ENHANCED GUARDIAN STYLES
function addGuardianStyles() {
  const style = document.createElement('style');
  style.textContent = `
    .section-guardian {
      transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
      filter: saturate(0.4) brightness(0.8);
    }
    
    .section-guardian:hover {
      filter: saturate(1.2) brightness(1.2) drop-shadow(0 0 20px var(--neon-glow));
      transform: scale(1.02);
    }

    .guardian-active {
      animation: guardianGlitchBurst 0.6s steps(3);
    }

    @keyframes guardianGlitchBurst {
      0% { transform: translate(0) scale(1.02); filter: hue-rotate(0deg) brightness(2); }
      33% { transform: translate(-10px, 5px) scale(1.05); filter: hue-rotate(90deg) brightness(3); }
      66% { transform: translate(10px, -5px) scale(1.03); filter: hue-rotate(180deg) brightness(2); }
      100% { transform: translate(0) scale(1.02); filter: hue-rotate(0deg) brightness(1.2); }
    }

    @keyframes gridIntensify {
      0%, 100% { opacity: 0.7; filter: brightness(1); }
      50% { opacity: 1; filter: brightness(1.4); }
    }
    
    @keyframes gridGlitch {
      0% { background-position: 0px 0px; filter: hue-rotate(0deg); }
      25% { background-position: 5px 5px; filter: hue-rotate(90deg); }
      50% { background-position: -5px -5px; filter: hue-rotate(180deg); }
      75% { background-position: 2px 2px; filter: hue-rotate(270deg); }
      100% { background-position: 0px 0px; filter: hue-rotate(0deg); }
    }

    .neon-grid-section.grid-effect-active::before {
      animation: gridMove 30s linear infinite, gridIntensify 0.8s ease-in-out !important;
    }
    
    .neon-grid-section.grid-glitch-active::before {
      animation: gridGlitch 0.4s steps(4) infinite, gridMove 30s linear infinite !important;
    }
    
    .robot-ripple {
      position: absolute;
      border-radius: 50%;
      background: radial-gradient(circle, var(--neon-mag) 0%, transparent 70%);
      pointer-events: none;
      z-index: 1000;
      transform: translate(-50%, -50%);
      opacity: 0;
    }
  `;
  document.head.appendChild(style);
}

document.addEventListener('DOMContentLoaded', () => {
  addGuardianStyles();
  
  const guardians = document.querySelectorAll('.section-guardian');
  
  guardians.forEach(guardian => {
    const robotId = guardian.dataset.robotId;
    const config = ROBOT_ASSETS[robotId];

    // Interaction logic
    guardian.addEventListener('click', (e) => {
      triggerGuardianAction(robotId, config, e);
      
      // Visual feedback on the robot itself
      guardian.classList.add('guardian-active');
      setTimeout(() => guardian.classList.remove('guardian-active'), 600);
    });

    // Keyboard support
    document.addEventListener('keydown', (e) => {
      if ((e.key === 'r' || e.key === 'R') && isElementInViewport(guardian)) {
        triggerGuardianAction(robotId, config);
        guardian.classList.add('guardian-active');
        setTimeout(() => guardian.classList.remove('guardian-active'), 600);
      }
    });
  });
});

function triggerGuardianAction(robotId, config, event) {
  // Audio
  const n = Math.floor(Math.random() * AUDIO_POOL_COUNT) + 1;
  const file = `${config.audioPath}${robotId}_${n}.mp3`;
  try {
    const a = new Audio(file);
    a.volume = 0.6;
    a.play().catch(err => console.warn('Audio play blocked/failed', err));
  } catch(e) { console.warn(e); }

  // Ripple
  if (event) createRippleEffect(event, config.color);

  // Site-wide Glitch
  const effects = ['grid-intensify', 'grid-glitch'];
  const pick = effects[Math.floor(Math.random() * effects.length)];
  applyGridEffect(pick, config.color);
}

function createRippleEffect(event, color) {
  const ripple = document.createElement('div');
  ripple.className = 'robot-ripple';
  ripple.style.background = `radial-gradient(circle, ${color} 0%, transparent 70%)`;
  
  const x = event.clientX || (event.touches && event.touches[0].clientX);
  const y = event.clientY || (event.touches && event.touches[0].clientY);
  
  ripple.style.left = `${x}px`;
  ripple.style.top = `${y}px`;
  
  document.body.appendChild(ripple);
  
  ripple.animate([
    { width: '0px', height: '0px', opacity: 0.8 },
    { width: '500px', height: '500px', opacity: 0 }
  ], {
    duration: 800,
    easing: 'ease-out'
  });
  
  setTimeout(() => ripple.remove(), 800);
}

function applyGridEffect(type, color) {
  const neonSections = document.querySelectorAll('.neon-grid-section');
  const className = type === 'grid-intensify' ? 'grid-effect-active' : 'grid-glitch-active';
  
  neonSections.forEach(section => {
    section.classList.add(className);
    section.style.setProperty('--neon-glow', color);
  });

  setTimeout(() => {
    neonSections.forEach(section => {
      section.classList.remove(className);
      section.style.setProperty('--neon-glow', '');
    });
  }, 1000);
}

function isElementInViewport(el) {
  const rect = el.getBoundingClientRect();
  return (
    rect.top >= 0 &&
    rect.left >= 0 &&
    rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
    rect.right <= (window.innerWidth || document.documentElement.clientWidth)
  );
}