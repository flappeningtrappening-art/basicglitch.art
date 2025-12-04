// robot.js
(function(){
  // Config - file paths must match files you added to repo
  const bgChoices = [
    '/assets/images/mountains.png',
    '/assets/images/circuit-glitch.png'
  ]; // 50/50 between these two

  const robotChoices = [
    {id:'guitarbot', src: '/assets/images/guitarbot.png', audioPath: '/assets/audio/guitarbot/'},
    {id:'brobot', src: '/assets/images/broboticus_og.png', audioPath: '/assets/audio/broboticus/'}
  ]; // 50/50 robot pick

  // Helper: pick random item from array
  function pick(arr){ return arr[Math.floor(Math.random()*arr.length)]; }

  // Choose background location: header or hero (50/50)
  const placeHero = Math.random() < 0.5;
  const chosenBG = pick(bgChoices);

  const target = placeHero ? document.querySelector('.hero') : document.querySelector('.site-header');
  if(target){
    target.classList.add('glitch-bg');
    target.style.backgroundImage = `url("${chosenBG}")`;
    // add overlay element
    const ov = document.createElement('div');
    ov.className = 'circuit-overlay';
    // set overlay image path if available (you added circuit-overlay.png)
    ov.style.backgroundImage = `url('/assets/images/circuit-overlay.png')`;
    target.appendChild(ov);

    // subtle scroll transform
    window.addEventListener('scroll', ()=> {
      const y = window.scrollY * 0.04;
      ov.style.transform = `translateY(${ -4 - y }%)`;
    });
  }

  // Robot foreground: choose robot (50/50)
  const robotPick = pick(robotChoices);
  const showRobot = true; // if you want sometimes no robot, change to random test

  if(showRobot){
    const robotImg = document.getElementById('robot-foreground');
    robotImg.src = robotPick.src;
    robotImg.alt = robotPick.id;
    robotImg.style.display = 'block';
    // 50/50 animate
    if(Math.random() < 0.5){
      robotImg.classList.add('animated');
      robotImg.classList.add('robot-foreground');
    } else {
      robotImg.classList.add('robot-foreground');
    }

    // Preload audio list for this robot (assumes files broboticus_1.mp3 etc.)
    const audioList = [];
    for(let i=1;i<=6;i++){ // assume up to broboticus_1..6 or guitarbot_1..6
      const url = `${robotPick.audioPath}${robotPick.id}_${i}.mp3`;
      const a = new Audio(url);
      a.preload = 'auto';
      audioList.push(a);
    }

    // Click/tap handler -> play random audio & visual effect
    robotImg.addEventListener('click', (ev)=>{
      // choose a random audio that loaded (skip if not network-available)
      const playable = audioList.filter(x=>x && x.readyState >= 2);
      const audio = playable.length ? playable[Math.floor(Math.random()*playable.length)] : audioList[Math.floor(Math.random()*audioList.length)];
      if(audio){
        try{ audio.currentTime = 0; audio.play(); } catch(e){}
      }

      // random visual effect class
      const effects = ['effect-neonpulse','effect-glitchburst','effect-rgb','effect-ripple'];
      const chosen = effects[Math.floor(Math.random()*effects.length)];
      robotImg.classList.remove(...effects);
      void robotImg.offsetWidth; // force reflow
      robotImg.classList.add(chosen);
      // remove effect after timeout
      setTimeout(()=> robotImg.classList.remove(chosen), 900);
    }, {passive:true});

    // Optional: on hover, subtle glow increase
    robotImg.addEventListener('mouseenter', ()=> robotImg.style.transform = 'translateY(-4px) scale(1.02)');
    robotImg.addEventListener('mouseleave', ()=> robotImg.style.transform = '');
  } // end showRobot

  // If you want robots to be keyboard accessible
  document.addEventListener('keydown', (e)=>{
    if(e.key === 'r'){ // press "r" to trigger robot sound/effect for quick testing
      const robotImg = document.getElementById('robot-foreground');
      robotImg && robotImg.click();
    }
  });

  // Safety: hide robot image if file not found by setting display none (simple)
  const robotImgCheck = document.getElementById('robot-foreground');
  robotImgCheck.addEventListener('error', ()=> {
    robotImgCheck.style.display = 'none';
  });

})();
