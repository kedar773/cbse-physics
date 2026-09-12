/**
 * CBSE Physics Notebook - Chapter Engine
 * Manages:
 * - 5-Tab marker tray switching
 * - Smart auto-hiding scroll header with floating #headerTogglePill
 * - KaTeX on-demand rendering per tab
 * - 2020-2025 PYQ multi-criteria filtering (Year, Marks)
 * - LocalStorage mastery tracking with step checklists & confetti milestones
 */

(function() {
  'use strict';

  let lastScrollY = window.scrollY;
  let isHeaderForcedVisible = false;

  function initTabs() {
    const tabButtons = document.querySelectorAll('.tab-marker-btn');
    const tabPanes = document.querySelectorAll('.notebook-tab-pane');

    function switchTab(targetTabId) {
      tabButtons.forEach(btn => {
        if (btn.getAttribute('data-tab') === targetTabId) {
          btn.classList.add('active');
        } else {
          btn.classList.remove('active');
        }
      });

      tabPanes.forEach(pane => {
        if (pane.id === targetTabId) {
          pane.classList.add('active');
          // Trigger KaTeX rendering on the newly active pane if needed
          renderMathInPane(pane);
        } else {
          pane.classList.remove('active');
        }
      });

      // Update URL hash without jumping
      if (history.replaceState) {
        history.replaceState(null, null, '#' + targetTabId);
      }
    }

    tabButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        const tabId = btn.getAttribute('data-tab');
        switchTab(tabId);
      });
    });

    // Handle initial hash in URL
    const initialHash = window.location.hash.replace('#', '');
    if (initialHash && document.getElementById(initialHash)) {
      switchTab(initialHash);
    }
  }

  function renderMathInPane(pane) {
    if (typeof renderMathInElement === 'function') {
      try {
        renderMathInElement(pane, {
          delimiters: [
            { left: '$$', right: '$$', display: true },
            { left: '\\[', right: '\\]', display: true },
            { left: '$', right: '$', display: false },
            { left: '\\(', right: '\\)', display: false }
          ],
          throwOnError: false,
          ignoredTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']
        });
      } catch (err) {
        console.warn('KaTeX render warning:', err);
      }
    }
  }

  function initSmartHeader() {
    const header = document.querySelector('.chapter-top-bar');
    const togglePill = document.getElementById('headerTogglePill');
    if (!header) return;

    let ticking = false;

    window.addEventListener('scroll', () => {
      if (!ticking) {
        window.requestAnimationFrame(() => {
          const currentScrollY = window.scrollY;
          
          if (!isHeaderForcedVisible) {
            if (currentScrollY > 120 && currentScrollY > lastScrollY + 5) {
              // Scrolling down -> hide header
              header.classList.add('header-hidden');
              header.classList.remove('header-visible');
              if (togglePill) togglePill.classList.add('pill-visible');
            } else if (currentScrollY < lastScrollY - 10 || currentScrollY <= 80) {
              // Scrolling up -> show header
              header.classList.remove('header-hidden');
              header.classList.add('header-visible');
              if (togglePill && currentScrollY <= 80) {
                togglePill.classList.remove('pill-visible');
              }
            }
          }

          lastScrollY = currentScrollY;
          ticking = false;
        });
        ticking = true;
      }
    }, { passive: true });

    if (togglePill) {
      togglePill.addEventListener('click', () => {
        if (header.classList.contains('header-hidden')) {
          header.classList.remove('header-hidden');
          header.classList.add('header-visible');
          togglePill.textContent = '▲ Hide Header';
          isHeaderForcedVisible = true;
        } else {
          header.classList.add('header-hidden');
          header.classList.remove('header-visible');
          togglePill.textContent = '▼ Show Tabs / Header';
          isHeaderForcedVisible = false;
        }
      });
    }
  }

  function initPyqFilters() {
    const yearFilters = document.querySelectorAll('.pyq-filter-year');
    const markFilters = document.querySelectorAll('.pyq-filter-mark');
    const qCards = document.querySelectorAll('.question-card');

    let activeYear = 'all';
    let activeMark = 'all';

    function applyFilters() {
      let visibleCount = 0;
      qCards.forEach(card => {
        const cardYear = (card.getAttribute('data-year') || '').toLowerCase();
        const cardMarks = (card.getAttribute('data-marks') || '').toLowerCase();

        let yearMatch = activeYear === 'all';
        if (!yearMatch) {
          if (activeYear === 'case') yearMatch = cardYear.includes('case');
          else if (activeYear === 'exemplar') yearMatch = cardYear.includes('exemplar');
          else if (activeYear === 'hots') yearMatch = cardYear.includes('hots');
          else yearMatch = cardYear.includes(activeYear);
        }

        let markMatch = activeMark === 'all';
        if (!markMatch) {
          markMatch = cardMarks === activeMark;
        }

        if (yearMatch && markMatch) {
          card.style.display = 'block';
          visibleCount++;
        } else {
          card.style.display = 'none';
        }
      });

      const countBadge = document.getElementById('pyqVisibleCount');
      if (countBadge) {
        countBadge.textContent = `${visibleCount} Questions Displayed`;
      }
    }

    yearFilters.forEach(btn => {
      btn.addEventListener('click', () => {
        yearFilters.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        activeYear = btn.getAttribute('data-val').toLowerCase();
        applyFilters();
      });
    });

    markFilters.forEach(btn => {
      btn.addEventListener('click', () => {
        markFilters.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        activeMark = btn.getAttribute('data-val').toLowerCase();
        applyFilters();
      });
    });
  }

  function initMasteryTracker() {
    const chapterSlug = document.body.getAttribute('data-chapter-slug') || 'current';
    const storageKey = `physics_mastery_${chapterSlug}`;
    let masteredIds = [];

    try {
      masteredIds = JSON.parse(localStorage.getItem(storageKey) || '[]');
    } catch (e) {
      masteredIds = [];
    }

    const checkboxes = document.querySelectorAll('.step-checkbox');
    const totalQuestions = checkboxes.length;
    const progressFill = document.getElementById('masteryProgressFill');
    const progressText = document.getElementById('masteryProgressText');

    function updateMasteryUI() {
      const count = masteredIds.length;
      const pct = totalQuestions > 0 ? Math.round((count / totalQuestions) * 100) : 0;
      
      if (progressFill) progressFill.style.width = `${pct}%`;
      if (progressText) progressText.textContent = `${count} of ${totalQuestions} Completed (${pct}%)`;

      if (pct === 100 && totalQuestions > 0) {
        if (window.NotebookAnimations && typeof window.NotebookAnimations.spawnConfetti === 'function') {
          window.NotebookAnimations.spawnConfetti(window.innerWidth / 2, 200);
        }
        if (window.NotebookAnimations && typeof window.NotebookAnimations.showToast === 'function') {
          window.NotebookAnimations.showToast('🏆 100% Chapter Mastery Achieved! Excellent work!', 'success');
        }
      }
    }

    checkboxes.forEach(cb => {
      const card = cb.closest('.question-card');
      if (!card) return;
      const qId = card.id;

      if (masteredIds.includes(qId)) {
        cb.checked = true;
        card.classList.add('mastered');
      }

      cb.addEventListener('change', () => {
        if (cb.checked) {
          if (!masteredIds.includes(qId)) masteredIds.push(qId);
          card.classList.add('mastered');
          if (window.NotebookAnimations && typeof window.NotebookAnimations.showToast === 'function') {
            window.NotebookAnimations.showToast('✓ Step Checked & Mastered!', 'success');
          }
        } else {
          masteredIds = masteredIds.filter(id => id !== qId);
          card.classList.remove('mastered');
        }
        localStorage.setItem(storageKey, JSON.stringify(masteredIds));
        updateMasteryUI();
      });
    });

    updateMasteryUI();
  }

  function initSubtopicNavigator() {
    const toggleAllBtn = document.getElementById('toggleAllModulesBtn');
    if (toggleAllBtn) {
      toggleAllBtn.addEventListener('click', () => {
        const sheets = document.querySelectorAll('.notebook-module-sheet');
        const isAnyOpen = Array.from(sheets).some(s => !s.classList.contains('collapsed'));
        sheets.forEach(s => {
          if (isAnyOpen) {
            s.classList.add('collapsed');
          } else {
            s.classList.remove('collapsed');
          }
        });
        toggleAllBtn.textContent = isAnyOpen ? '⊞ Expand All Notes' : '⊟ Collapse All Notes';
      });
    }

    // When clicking a topic chip, ensure the target module is un-collapsed and smoothly scroll
    document.querySelectorAll('.topic-chip').forEach(chip => {
      chip.addEventListener('click', (e) => {
        const href = chip.getAttribute('href');
        if (href && href.startsWith('#')) {
          const target = document.querySelector(href);
          if (target && target.classList.contains('notebook-module-sheet')) {
            target.classList.remove('collapsed');
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            e.preventDefault();
          }
        }
      });
    });
  }

  document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    initSmartHeader();
    initPyqFilters();
    initMasteryTracker();
    initSubtopicNavigator();

    // Initial KaTeX pass on entire page
    if (typeof renderMathInElement === 'function') {
      try {
        renderMathInElement(document.body, {
          delimiters: [
            { left: '$$', right: '$$', display: true },
            { left: '\\[', right: '\\]', display: true },
            { left: '$', right: '$', display: false },
            { left: '\\(', right: '\\)', display: false }
          ],
          throwOnError: false,
          ignoredTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']
        });
      } catch (e) {
        console.warn('Initial KaTeX error:', e);
      }
    }
  });

  window.ChapterEngine = {
    initTabs,
    initSmartHeader,
    initPyqFilters,
    initMasteryTracker,
    initSubtopicNavigator
  };
})();
