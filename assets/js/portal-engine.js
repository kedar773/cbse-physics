/**
 * CBSE Physics Notebook - Portal Engine
 * Controls landing page interactions:
 * - Class 11 vs Class 12 tab switcher
 * - Domain filter chips (Mechanics, Thermodynamics, Electromagnetism, Optics, Modern Physics)
 * - Curriculum stats counter animation
 */

(function() {
  'use strict';

  function initPortalFilters() {
    const classBtns = document.querySelectorAll('.portal-class-tab');
    const domainChips = document.querySelectorAll('.portal-domain-chip');
    const chapterCards = document.querySelectorAll('.notebook-chapter-card');

    let currentClass = 'all';
    let currentDomain = 'all';

    function filterCards() {
      let count = 0;
      chapterCards.forEach(card => {
        const cardClass = card.getAttribute('data-class'); // '11' or '12'
        const cardDomain = (card.getAttribute('data-domain') || '').toLowerCase();

        const classMatch = (currentClass === 'all' || cardClass === currentClass);
        const domainMatch = (currentDomain === 'all' || cardDomain.includes(currentDomain));

        if (classMatch && domainMatch) {
          card.style.display = 'flex';
          card.classList.add('animate-pop-in');
          count++;
        } else {
          card.style.display = 'none';
        }
      });

      const countDisplay = document.getElementById('portalVisibleChapterCount');
      if (countDisplay) {
        countDisplay.textContent = `${count} Chapters Displayed`;
      }
    }

    classBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        classBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentClass = btn.getAttribute('data-class');
        filterCards();
      });
    });

    domainChips.forEach(chip => {
      chip.addEventListener('click', () => {
        domainChips.forEach(c => c.classList.remove('active'));
        chip.classList.add('active');
        currentDomain = chip.getAttribute('data-domain').toLowerCase();
        filterCards();
      });
    });
  }

  function initStatsAnimation() {
    const statElements = document.querySelectorAll('.portal-stat-num');
    statElements.forEach(el => {
      const target = parseInt(el.getAttribute('data-count') || el.textContent, 10);
      if (isNaN(target)) return;

      let current = 0;
      const step = Math.max(1, Math.ceil(target / 40));
      const interval = setInterval(() => {
        current += step;
        if (current >= target) {
          current = target;
          clearInterval(interval);
        }
        el.textContent = current + (el.getAttribute('data-suffix') || '');
      }, 25);
    });
  }

  function renderPortalMath() {
    if (typeof renderMathInElement === 'function') {
      try {
        renderMathInElement(document.body, {
          delimiters: [
            { left: '$$', right: '$$', display: true },
            { left: '$', right: '$', display: false },
            { left: '\\(', right: '\\)', display: false },
            { left: '\\[', right: '\\]', display: true }
          ],
          ignoredTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code'],
          throwOnError: false
        });
      } catch (e) {
        console.warn('Portal math render error:', e);
      }
    } else {
      setTimeout(renderPortalMath, 150);
    }
  }

  document.addEventListener('DOMContentLoaded', () => {
    initPortalFilters();
    initStatsAnimation();
    renderPortalMath();
  });

  window.addEventListener('load', () => {
    renderPortalMath();
  });

  window.PortalEngine = {
    initPortalFilters,
    initStatsAnimation,
    renderPortalMath
  };
})();
