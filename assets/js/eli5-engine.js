/**
 * CBSE Physics Notebook - ELI5 (Explain Like I'm 5) Intuition Engine
 * Toggles between rigorous academic physics & intuitive real-world analogies
 */

(function() {
  'use strict';

  function initEli5Toggles() {
    const toggles = document.querySelectorAll('.eli5-toggle-btn, .eli5-switch input');
    
    toggles.forEach(toggle => {
      toggle.addEventListener('change', function(e) {
        const card = this.closest('.eli5-card');
        if (!card) return;
        
        const isEli5 = this.checked;
        const standardPane = card.querySelector('.eli5-standard-view');
        const intuitivePane = card.querySelector('.eli5-intuitive-view');
        const badge = card.querySelector('.eli5-status-badge');
        
        if (isEli5) {
          card.classList.add('eli5-active');
          if (standardPane) standardPane.style.display = 'none';
          if (intuitivePane) {
            intuitivePane.style.display = 'block';
            intuitivePane.classList.add('animate-pop-in');
          }
          if (badge) {
            badge.textContent = '🎈 ELI5 Mode Active';
            badge.classList.add('active');
          }
          
          // Trigger a micro spark / confetti if available
          if (window.NotebookAnimations && typeof window.NotebookAnimations.spawnConfetti === 'function') {
            const rect = card.getBoundingClientRect();
            window.NotebookAnimations.spawnConfetti(rect.left + rect.width / 2, rect.top + 30);
          }
          if (window.NotebookAnimations && typeof window.NotebookAnimations.showToast === 'function') {
            window.NotebookAnimations.showToast('💡 Intuitive Analogy Unlocked!', 'success');
          }
        } else {
          card.classList.remove('eli5-active');
          if (standardPane) {
            standardPane.style.display = 'block';
            standardPane.classList.add('animate-pop-in');
          }
          if (intuitivePane) intuitivePane.style.display = 'none';
          if (badge) {
            badge.textContent = '📐 Rigorous Academic Mode';
            badge.classList.remove('active');
          }
        }
      });
    });
  }

  // Also expose global toggle function for button clicks
  window.toggleEli5Mode = function(cardId) {
    const card = document.getElementById(cardId);
    if (!card) return;
    const checkbox = card.querySelector('.eli5-switch input');
    if (checkbox) {
      checkbox.checked = !checkbox.checked;
      checkbox.dispatchEvent(new Event('change'));
    }
  };

  document.addEventListener('DOMContentLoaded', initEli5Toggles);
  window.initEli5Toggles = initEli5Toggles;
})();
