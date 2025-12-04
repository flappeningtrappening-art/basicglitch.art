/* robot.js — robot foreground randomizer + interactivity + light effects
   Place at /robot.js and index.html includes <script src="robot.js" defer></script>
*/

(function () {
  const ROOT = window;
  const doc = document;
  const robotImg = doc.getElementById('robot-foreground');
  const canvas = doc.getElementById('robot-effect-canvas');
  const ctx = canvas && canvas.getContext ? canvas.getContext('2d') : null;

  /* -----------------------------
     Config — adjust paths & weights
     ----------------------------- */
  const bgChoices = [
    {src: '/assets/images/mountains.png', weight: 0.5},
    {src: '/assets/images/circuit-glitch.png', weight: 0.5}
  ];
  // foreground robots (50/50)
  const robots = [
    {id: 'guitarbot', src: '/assets/images/guitarbot.png', audioPath: '/assets/audio/guitarbot/', files: ['guitarbot_1.mp3','guitarbot_2.mp3','guitarbot_3.mp3']},
    {id: 'brobot', src: '/assets/images/broboticus_og.png', audioPath: '/assets/audio/broboticus/', files: ['broboticus_1.mp3','broboticus_2.mp3','broboticus_3.mp3']}
  ];

  // effect names used by CSS classes and canvas
  const EFFECTS = ['neonPulse','glitchBurst','rgbSplit','ripple'];

  /* -----------------------------
     Utility helpers
     ----------------------------- */
  function weightedPick(list){
    const sum = list.reduce((s,i)=>s+i.weight,0);
    let r = Math.random()*sum;
    for(const it of list){
      if(r < it.weight) return it;
      r -= it.weight;
    }
    return list[0];
  }
  function pickRandom(arr){ return arr[Math.floor(Math.random()*arr.length)]; }

  /* -----------------------------
     Canvas init & responsive sizing
     ----------------------------- */
  function fitCanvas(){
    if(!canvas) return;
    canvas.width = window.innerWidth * devicePixelRatio;
    canvas.height = window.innerHeight * devicePixelRatio;
    canvas.style.width = window.innerWidth + 'px';
    canvas.style.height = window.innerHeight + 'px';
    if(ctx) ctx.scale(devicePixelRatio, devicePixelRatio);
  }
  fitCanvas();
  window.addEventListener('resize', () => {
    fitCanvas();
  });

  /* -----------------------------
     Background placer
     Only mountains & circuit-glitch are used as bg
     ----------------------------- */
  function placeBackground(){
    const chosen = weightedPick(bgChoices);
    // 60% hero, 40% header (you said 50/50 earlier but requested 60/40 previously; keep hero-preferred)
    const placeInHero = Math.random() < 0.6;
    const target = placeInHero ? doc.querySelector('.hero') : doc.querySelector('.site-header');
    if(!target) return;
    target.classList.add('glitch-bg');
    target.style.backgroundImage = `url("${chosen.src}")`;
    // add subtle overlay
    let ov = target.querySelector('.circuit-overlay');
    if(!ov){
      ov = doc.createElement('div');
      ov.className = 'circuit-overlay';
      ov.style.backgroundImage = 'url("/assets/images/circuit-overlay.png")';
      target.appendChild(ov);
    }
  }

  /* -----------------------------
     Robot placement (front page only)
     50% chance to appear (user requested 50/50 for everything). If appears,
     pick robot at 50/50 and decide whether it's animated (50/50).
     ----------------------------- */
  function setupRobot(){
    // 50% chance to show robot at all on page load
    const show = Math.random() < 0.5;
    if(!show){
      robotImg.style.display = 'none';
      return;
    }
    // pick robot 50/50
    const robot = pickRandom(robots);
    robotImg.src = robot.src;
    robotImg.alt = robot.id === 'guitarbot' ? 'Guitarbot (foreground)' : 'Broboticus (foreground)';
    robotImg.dataset.robotId = robot.id;
    robotImg.dataset.audioPath = robot.audioPath;
    robotImg.dataset.audioFiles = JSON.stringify(robot.files);
    robotImg.style.display = '';
    // 50% chance animate
    const animate = Math.random() < 0.5;
    if(animate) robotImg.classList.add('animated');
    else robotImg.classList.remove('animated');

    // show with small entrance effect
    robotImg.style.opacity = '0';
    robotImg.style.transform = 'translateY(10px) scale(0.995)';
    requestAnimationFrame(()=> {
      robotImg.style.transition = 'opacity .28s ease, transform .28s ease';
      robotImg.style.opacity = '1';
      robotImg.style.transform = 'translateY(0) scale(1)';
    });

    // Add click & keyboard interaction
    robotImg.setAttribute('tabindex','0');
    robotImg.style.cursor = 'pointer';
    robotImg.addEventListener('click', onRobotInteract);
    robotImg.addEventListener('keydown', (ev) => { if(ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); onRobotInteract(); }});
  }

  /* -----------------------------
     Audio playback (simple, one-shot)
     ----------------------------- */
  function playRobotAudio(robotId, audioPath, files){
    if(!files || !files.length) return;
    const file = pickRandom(files);
    const full = audioPath + file;
    const a = new Audio(full);
    a.volume = 0.9;
    a.play().catch(()=>{ /* fail silently */ });
  }

  /* -----------------------------
     Visual effect triggers
     - adds CSS classes to robotImg and draws lightweight overlay on canvas
     ----------------------------- */
  function triggerEffect(effectName){
    if(!robotImg) return;
    // Map effectName to class and optional canvas draw
    switch(effectName){
      case 'neonPulse':
        robotImg.classList.add('effect-neon-pulse');
        setTimeout(()=> robotImg.classList.remove('effect-neon-pulse'), 700);
        drawPulseOnCanvas();
        break;
      case 'glitchBurst':
        robotImg.classList.add('effect-glitch-burst');
        setTimeout(()=> robotImg.classList.remove('effect-glitch-burst'), 420);
        drawGlitchOnCanvas();
        break;
      case 'rgbSplit':
        robotImg.classList.add('effect-rgb-split');
        setTimeout(()=> robotImg.classList.remove('effect-rgb-split'), 520);
        drawRGBOnCanvas();
        break;
      case 'ripple':
        robotImg.classList.add('effect-ripple');
        setTimeout(()=> robotImg.classList.remove('effect-ripple'), 720);
        drawRippleOnCanvas();
        break;
      default: break;
    }
  }

  /* -----------------------------
     Canvas drawing helpers — lightweight, mobile-friendly
     These draw brief noise/scanline bursts near robot center.
     ----------------------------- */
  function clearCanvas(){ if(!ctx) return; ctx.clearRect(0,0,canvas.width,canvas.height); }

  function drawPulseOnCanvas(){
    if(!ctx) return;
    const w = canvas.width / devicePixelRatio;
    const h = canvas.height / devicePixelRatio;
    // brief radial glow around robot position
    const rect = robotImg.getBoundingClientRect();
    const cx = rect.left + rect.width/2;
    const cy = rect.top + rect.height/2;
    clearCanvas();
    const grad = ctx.createRadialGradient(cx,cy,0,cx,cy, Math.max(rect.width,rect.height)*2);
    grad.addColorStop(0, 'rgba(0,255,247,0.35)');
    grad.addColorStop(0.5,'rgba(0,255,247,0.08)');
    grad.addColorStop(1,'rgba(0,0,0,0)');
    ctx.fillStyle = grad;
    ctx.fillRect(0,0,w,h);
    // fade quickly
    setTimeout(()=> clearCanvas(), 250);
  }

  function drawGlitchOnCanvas(){
    if(!ctx) return;
    const w = canvas.width / devicePixelRatio;
    const h = canvas.height / devicePixelRatio;
    const rect = robotImg.getBoundingClientRect();
    const lines = 6;
    clearCanvas();
    for(let i=0;i<lines;i++){
      const y = rect.top + Math.random()*rect.height;
      ctx.fillStyle = `rgba(0,255,247,${0.08 + Math.random()*0.12})`;
      ctx.fillRect(rect.left - 8 + Math.random()*20, y, rect.width + 16, 2 + Math.random()*6);
    }
    setTimeout(()=> clearCanvas(), 240);
  }

  function drawRGBOnCanvas(){
    if(!ctx) return;
    const rect = robotImg.getBoundingClientRect();
    // draw 3 offset colored silhouettes
    clearCanvas();
    ctx.globalCompositeOperation = 'lighter';
    ctx.fillStyle = 'rgba(255,0,80,0.18)';
    ctx.fillRect(rect.left+6, rect.top, rect.width, rect.height);
    ctx.fillStyle = 'rgba(0,200,255,0.14)';
    ctx.fillRect(rect.left-6, rect.top, rect.width, rect.height);
    setTimeout(()=>{ ctx.globalCompositeOperation='source-over'; clearCanvas(); }, 360);
  }

  function drawRippleOnCanvas(){
    if(!ctx) return;
    const rect = robotImg.getBoundingClientRect();
    clearCanvas();
    const cx = rect.left + rect.width/2;
    const cy = rect.top + rect.height/2;
    ctx.beginPath();
    ctx.strokeStyle = 'rgba(0,255,247,0.16)';
    ctx.lineWidth = 2;
    ctx.arc(cx,cy,rect.width * 0.9,0,Math.PI*2);
    ctx.stroke();
    setTimeout(()=> clearCanvas(), 420);
  }

  /* -----------------------------
     Robot click handler — picks audio + effect
     ----------------------------- */
  function onRobotInteract(ev){
    const robotId = robotImg.dataset.robotId;
    const audioPath = robotImg.dataset.audioPath;
    const audioFiles = JSON.parse(robotImg.dataset.audioFiles || '[]');
    if(!robotId) return;

    // play sound (random from that robot)
    playRobotAudio(robotId, audioPath, audioFiles);

    // choose random effect (equal chance)
    const fx = pickRandom(EFFECTS);
    triggerEffect(fx);

    // small visual bounce
    robotImg.animate([{transform:'scale(1)'},{transform:'scale(1.05)'},{transform:'scale(1)'}], {duration:260, easing:'ease-out'});
  }

  /* -----------------------------
     Init on DOM ready
     ----------------------------- */
  function init(){
    placeBackground();
    setupRobot();
    // canvas prepared
    fitCanvas();
    // accessibility: ensure robot will be focusable if present
    if(robotImg) robotImg.setAttribute('tabindex','0');
  }
  if (doc.readyState === 'loading') doc.addEventListener('DOMContentLoaded', init); else init();

  // Expose for debugging
  ROOT.__basicGlitch = {placeBackground, setupRobot, triggerEffect};
})();
