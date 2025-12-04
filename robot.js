// robot.js - Mobile Responsive Version
(function() {
  'use strict';

  // ===== MOBILE CONFIGURATION =====
  const MOBILE_CONFIG = {
    phone: 480,    // Small phones
    tablet: 768,   // Tablets & large phones
    desktop: 1024  // Desktops & laptops
  };

  // Robot scale factors for different screen sizes
  const SCALE_FACTORS = {
    phone: 0.4,
    tablet: 0.6,
    desktop: 0.8,
    largeDesktop: 1.0
  };

  // Audio volume based on device (quieter on mobile)
  const AUDIO_VOLUME = {
    phone: 0.3,
    tablet: 0.5,
    desktop: 0.7,
    largeDesktop: 0.8
  };

  // ===== ASSET PATHS =====
  const bgChoices = [
    '/assets/images/mountains.png',
    '/assets/images/circuit-glitch.png'
  ];

  const robotChoices = [
    {
      id: 'guitarbot',
      src: '/assets/images/guitarbot.png',
      audioPath: '/assets/audio/guitarbot/',
      mobileSrc: '/assets/images/guitarbot-mobile.png' // Optional: smaller version
    },
    {
      id: 'brobot',
      src: '/assets/images/broboticus_og.png',
      audioPath: '/assets/audio/broboticus/',
      mobileSrc: '/assets/images/broboticus-mobile.png' // Optional: smaller version
    }
  ];

  // ===== HELPER FUNCTIONS =====
  function pick(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
  }

  function getDeviceType() {
    const width = window.innerWidth;
    if (width <= MOBILE_CONFIG.phone) return 'phone';
    if (width <= MOBILE_CONFIG.tablet) return 'tablet';
    if (width <= MOBILE_CONFIG.desktop) return 'desktop';
    return 'largeDesktop';
  }

  function getRobotScale() {
    const device = getDeviceType();
    return SCALE_FACTORS[device] || 1.0;
  }

  function getAudioVolume() {
    const device = getDeviceType();
    return AUDIO_VOLUME[device] || 0.7;
  }

  function isTouchDevice() {
    return ('ontouchstart' in window) || 
           (navigator.maxTouchPoints > 0) || 
           (navigator.msMaxTouchPoints > 0);
  }

  // ===== MOBILE-OPTIMIZED BACKGROUND SETUP =====
  function setupBackground() {
    // On mobile, always use hero section for better visibility
    const isMobile = window.innerWidth <= MOBILE_CONFIG.tablet;
    const placeHero = isMobile ? true : Math.random() < 0.5;
    const chosenBG = pick(bgChoices);
    
    const target = placeHero ? document.querySelector('.hero') : document.querySelector('.site-header');
    
    if (!target) return;

    // Only add background effect if image loads successfully
    const bgImage = new Image();
    bgImage.onload = function() {
      target.classList.add('glitch-bg');
      target.style.backgroundImage = `url("${chosenBG}")`;
      target.style.backgroundSize = isMobile ? 'cover' : '120%';
      target.style.backgroundPosition = 'center';
      target.style.backgroundAttachment = isMobile ? 'scroll' : 'fixed';
      
      // Add overlay element
      const overlay = document.createElement('div');
      overlay.className = 'circuit-overlay';
      overlay.setAttribute('aria-hidden', 'true');
      
      // Use CSS variable for mobile optimization
      overlay.style.cssText = `
        position: absolute;
        inset: 0;
        background-image: url('/assets/images/circuit-overlay.png');
        background-size: ${isMobile ? '200%' : '120%'};
        background-repeat: repeat;
        opacity: 0.1;
        mix-blend-mode: lighten;
        pointer-events: none;
        transition: transform 0.25s ease;
      `;
      
      target.style.position = 'relative';
      target.appendChild(overlay);

      // Optimized scroll effect (throttled for performance)
      let scrollTimeout;
      window.addEventListener('scroll', function() {
        if (scrollTimeout) return;
        
        scrollTimeout = setTimeout(function() {
          const y = window.scrollY * 0.02; // Reduced effect on mobile
          overlay.style.transform = `translateY(${-2 - y}%)`;
          scrollTimeout = null;
        }, 16); // ~60fps
      }, { passive: true });
    };
    
    bgImage.onerror = function() {
      console.warn('Background image failed to load:', chosenBG);
    };
    
    bgImage.src = chosenBG;
  }

  // ===== MOBILE-OPTIMIZED ROBOT SETUP =====
  function setupRobot() {
    const robotPick = pick(robotChoices);
    const showRobot = true;
    
    if (!showRobot) return;

    const robotImg = document.getElementById('robot-foreground');
    if (!robotImg) return;

    // Choose appropriate image source based on device
    const isMobile = window.innerWidth <= MOBILE_CONFIG.tablet;
    const robotSrc = (isMobile && robotPick.mobileSrc) ? robotPick.mobileSrc : robotPick.src;
    
    // Set robot attributes
    robotImg.src = robotSrc;
    robotImg.alt = `${robotPick.id} - Interactive character`;
    robotImg.loading = 'lazy';
    
    // Apply mobile-responsive styles
    robotImg.style.cssText = `
      position: fixed;
      z-index: 9999;
      pointer-events: auto;
      filter: drop-shadow(0 0 14px rgba(0, 255, 247, 0.9));
      opacity: 0.98;
      transition: transform 0.25s ease, opacity 0.3s ease;
      max-width: min(200px, 25vw);
      height: auto;
      user-select: none;
      -webkit-tap-highlight-color: transparent;
    `;

    // Position robot based on screen size
    function positionRobot() {
      const device = getDeviceType();
      const scale = getRobotScale();
      
      switch(device) {
        case 'phone':
          robotImg.style.bottom = '10px';
          robotImg.style.right = '10px';
          robotImg.style.width = '80px';
          break;
        case 'tablet':
          robotImg.style.bottom = '20px';
          robotImg.style.right = '20px';
          robotImg.style.width = '120px';
          break;
        default:
          robotImg.style.bottom = '40px';
          robotImg.style.right = '20px';
          robotImg.style.width = 'clamp(160px, 22vw, 320px)';
      }
      
      // Apply scale via CSS variable
      document.documentElement.style.setProperty('--robot-scale', scale);
      
      // Show robot after positioning
      robotImg.style.display = 'block';
      robotImg.style.opacity = '1';
    }

    // Initialize position
    positionRobot();

    // Add animation randomly (but less frequently on mobile for performance)
    const isTouch = isTouchDevice();
    const shouldAnimate = Math.random() < (isTouch ? 0.3 : 0.5);
    
    if (shouldAnimate) {
      robotImg.classList.add('animated');
    }
    
    robotImg.classList.add('robot-foreground');

    // ===== MOBILE-OPTIMIZED AUDIO =====
    const audioList = [];
    const maxAudioFiles = isMobile ? 3 : 6; // Load fewer on mobile
    
    function preloadAudio() {
      for (let i = 1; i <= maxAudioFiles; i++) {
        const url = `${robotPick.audioPath}${robotPick.id}_${i}.mp3`;
        const audio = new Audio();
        audio.src = url;
        audio.preload = 'auto';
        audio.volume = getAudioVolume();
        
        // Store for later use
        audioList.push({
          element: audio,
          url: url,
          loaded: false
        });
        
        // Mark as loaded when ready
        audio.addEventListener('canplaythrough', function() {
          const audioObj = audioList.find(a => a.element === this);
          if (audioObj) audioObj.loaded = true;
        }, { once: true });
        
        // Handle errors
        audio.addEventListener('error', function() {
          console.warn(`Audio failed to load: ${url}`);
        });
      }
    }

    // Preload audio on user interaction (for autoplay policies)
    function loadAudioOnInteraction() {
      preloadAudio();
      document.removeEventListener('click', loadAudioOnInteraction);
      document.removeEventListener('touchstart', loadAudioOnInteraction);
    }

    // Wait for user interaction before preloading audio
    if (isTouch) {
      document.addEventListener('touchstart', loadAudioOnInteraction, { once: true });
    } else {
      document.addEventListener('click', loadAudioOnInteraction, { once: true });
    }

    // ===== INTERACTION HANDLERS =====
    function playRandomAudio() {
      const loadedAudios = audioList.filter(a => a.loaded);
      const volume = getAudioVolume();
      
      if (loadedAudios.length > 0) {
        const randomAudio = loadedAudios[Math.floor(Math.random() * loadedAudios.length)];
        randomAudio.element.volume = volume;
        randomAudio.element.currentTime = 0;
        
        // Handle autoplay restrictions
        const playPromise = randomAudio.element.play();
        if (playPromise !== undefined) {
          playPromise.catch(error => {
            console.log('Audio play failed:', error);
            // Fallback: vibrate on mobile if audio fails
            if (isTouch && navigator.vibrate) {
              navigator.vibrate(100);
            }
          });
        }
      } else {
        // Fallback vibration for mobile
        if (isTouch && navigator.vibrate) {
          navigator.vibrate(50);
        }
      }
    }

    function triggerVisualEffect() {
      const effects = ['effect-neonpulse', 'effect-glitchburst', 'effect-rgb', 'effect-ripple'];
      const chosenEffect = effects[Math.floor(Math.random() * effects.length)];
      
      // Remove all effects first
      robotImg.classList.remove(...effects);
      
      // Force reflow
      void robotImg.offsetWidth;
      
      // Add new effect
      robotImg.classList.add(chosenEffect);
      
      // Remove effect after animation completes
      setTimeout(() => {
        robotImg.classList.remove(chosenEffect);
      }, 900);
    }

    // ===== EVENT HANDLERS =====
    function handleRobotInteraction(event) {
      event.preventDefault();
      
      playRandomAudio();
      triggerVisualEffect();
      
      // Add subtle interaction feedback
      robotImg.style.transform = 'scale(0.95)';
      setTimeout(() => {
        robotImg.style.transform = '';
      }, 150);
    }

    // Touch/click event with better mobile support
    const eventType = isTouchDevice() ? 'touchstart' : 'click';
    
    robotImg.addEventListener(eventType, handleRobotInteraction, { 
      passive: false 
    });
    
    // Add keyboard support
    robotImg.setAttribute('tabindex', '0');
    robotImg.setAttribute('role', 'button');
    robotImg.setAttribute('aria-label', `Interact with ${robotPick.id}. Press Enter or Space to activate.`);
    
    robotImg.addEventListener('keydown', function(event) {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        handleRobotInteraction(event);
      }
    });

    // Hover effects only for non-touch devices
    if (!isTouch) {
      robotImg.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-4px) scale(1.02)';
        this.style.cursor = 'pointer';
      });
      
      robotImg.addEventListener('mouseleave', function() {
        this.style.transform = '';
      });
    }

    // ===== RESPONSIVE UPDATES =====
    let resizeTimeout;
    window.addEventListener('resize', function() {
      clearTimeout(resizeTimeout);
      resizeTimeout = setTimeout(positionRobot, 250);
    }, { passive: true });

    // Handle image loading errors
    robotImg.addEventListener('error', function() {
      console.warn(`Robot image failed to load: ${robotSrc}`);
      this.style.opacity = '0';
      this.style.pointerEvents = 'none';
      
      // Try fallback to original source if mobile src failed
      if (robotSrc !== robotPick.src) {
        this.src = robotPick.src;
      }
    });

    // Handle successful image load
    robotImg.addEventListener('load', function() {
      this.style.opacity = '1';
    });
  }

  // ===== CANVAS EFFECTS (MOBILE OPTIMIZED) =====
  function setupCanvasEffects() {
    const canvas = document.getElementById('robot-effect-canvas');
    if (!canvas) return;
    
    // Set canvas size responsively
    function resizeCanvas() {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
      canvas.style.width = '100vw';
      canvas.style.height = '100vh';
    }
    
    resizeCanvas();
    
    // Initial setup
    canvas.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      pointer-events: none;
      z-index: 1;
      opacity: 0.3;
    `;
    
    // Throttled resize handler
    let resizeThrottle;
    window.addEventListener('resize', function() {
      if (resizeThrottle) return;
      resizeThrottle = setTimeout(function() {
        resizeCanvas();
        resizeThrottle = null;
      }, 100);
    }, { passive: true });
    
    // Only run animations on non-mobile for performance
    if (window.innerWidth > MOBILE_CONFIG.tablet) {
      requestAnimationFrame(animateCanvas);
    }
    
    function animateCanvas() {
      // Simple particle effect for desktop only
      const ctx = canvas.getContext('2d');
      if (!ctx) return;
      
      // Clear with slight trail effect
      ctx.fillStyle = 'rgba(5, 5, 5, 0.05)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      // Request next frame (only if visible)
      if (document.visibilityState === 'visible') {
        requestAnimationFrame(animateCanvas);
      }
    }
  }

  // ===== GLOBAL KEYBOARD SHORTCUTS =====
  function setupKeyboardShortcuts() {
    document.addEventListener('keydown', function(event) {
      // Press "R" to trigger robot (development helper)
      if (event.key === 'r' || event.key === 'R') {
        const robotImg = document.getElementById('robot-foreground');
        if (robotImg && robotImg.style.display !== 'none') {
          robotImg.click();
        }
      }
      
      // Press "Escape" to hide robot temporarily
      if (event.key === 'Escape') {
        const robotImg = document.getElementById('robot-foreground');
        if (robotImg) {
          robotImg.style.opacity = robotImg.style.opacity === '0.3' ? '1' : '0.3';
        }
      }
    });
  }

  // ===== INITIALIZATION =====
  function init() {
    // Set loading class for CSS
    document.body.classList.add('js-loading');
    
    // Initialize components with delay for better performance
    setTimeout(() => {
      setupBackground();
      setupRobot();
      setupCanvasEffects();
      setupKeyboardShortcuts();
      
      // Remove loading class
      setTimeout(() => {
        document.body.classList.remove('js-loading');
      }, 300);
    }, 100);
  }

  // ===== ENTRY POINT =====
  // Wait for DOM to be ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // ===== PUBLIC API (for debugging) =====
  window.RobotDebug = {
    reloadRobot: function() {
      const robotImg = document.getElementById('robot-foreground');
      if (robotImg) {
        robotImg.style.opacity = '0';
        setTimeout(() => {
          robotImg.src = robotImg.src; // Trigger reload
          robotImg.style.opacity = '1';
        }, 300);
      }
    },
    getScaleFactor: getRobotScale,
    getDeviceType: getDeviceType
  };

})();
