/* UTM Tracking for BasicGlitch Marketing */
(function() {
  'use strict';
  
  // Capture UTMs from URL on page load
  function captureUTMs() {
    const urlParams = new URLSearchParams(window.location.search);
    const utmParams = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'];
    const utms = {};
    
    utmParams.forEach(param => {
      const value = urlParams.get(param);
      if (value) {
        utms[param] = value;
      }
    });
    
    // Store in sessionStorage for this session
    if (Object.keys(utms).length > 0) {
      sessionStorage.setItem('basicglitch_utms', JSON.stringify(utms));
    }
  }
  
  // Get stored UTMs
  function getStoredUTMs() {
    try {
      const stored = sessionStorage.getItem('basicglitch_utms');
      return stored ? JSON.parse(stored) : {};
    } catch (e) {
      return {};
    }
  }
  
  // Append UTMs to external links (Gumroad, etc.)
  function appendUTMsToLinks() {
    const utms = getStoredUTMs();
    if (Object.keys(utms).length === 0) return;
    
    const links = document.querySelectorAll('a[href*="gumroad.com"]');
    links.forEach(link => {
      try {
        const url = new URL(link.href);
        // Don't override existing UTMs
        Object.keys(utms).forEach(key => {
          if (!url.searchParams.has(key)) {
            url.searchParams.set(key, utms[key]);
          }
        });
        link.href = url.toString();
      } catch (e) {
        // Skip invalid URLs
      }
    });
  }
  
  // Initialize
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      captureUTMs();
      appendUTMsToLinks();
    });
  } else {
    captureUTMs();
    appendUTMsToLinks();
  }
})();
