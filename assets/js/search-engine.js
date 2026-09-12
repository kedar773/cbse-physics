/**
 * CBSE Physics Notebook - Global Search Engine
 * Handles Ctrl+K modal, instant client-side full text search across all 25 chapters,
 * formulas, questions, and competitive advanced modules.
 */

(function() {
  'use strict';

  let searchIndex = [];
  let isIndexLoaded = false;

  function getBaseRelativePath() {
    // If in class-11/xx or class-12/xx, base path is ../../
    const path = window.location.pathname.replace(/\\/g, '/');
    if (path.includes('/class-11/') || path.includes('/class-12/')) {
      return '../../';
    }
    return './';
  }

  async function loadSearchIndex() {
    if (isIndexLoaded) return;
    try {
      const basePath = getBaseRelativePath();
      const res = await fetch(`${basePath}assets/data/search_index.json`);
      if (res.ok) {
        searchIndex = await res.json();
        isIndexLoaded = true;
      }
    } catch (err) {
      console.warn('Could not load search_index.json:', err);
    }
  }

  function createSearchModal() {
    if (document.getElementById('searchModalOverlay')) return;

    const modal = document.createElement('div');
    modal.id = 'searchModalOverlay';
    modal.className = 'search-modal-overlay';
    modal.style.display = 'none';
    modal.innerHTML = `
      <div class="search-modal-dialog">
        <div class="search-modal-header">
          <span class="search-icon">🔍</span>
          <input type="text" id="globalSearchInput" class="search-modal-input" placeholder="Search topics, laws, formulas, derivations, or PYQs... (Press Esc to close)" autocomplete="off">
          <button class="search-close-btn" id="closeSearchModal">✕</button>
        </div>
        <div class="search-quick-tags">
          <span class="quick-tag" data-query="Gauss Law">⚡ Gauss's Law</span>
          <span class="quick-tag" data-query="Bernoulli">🌊 Bernoulli's Eq</span>
          <span class="quick-tag" data-query="Lens Maker">🔬 Lens Maker</span>
          <span class="quick-tag" data-query="Carnot">🔥 Carnot Cycle</span>
          <span class="quick-tag" data-query="Doppler">🔊 Doppler Effect</span>
          <span class="quick-tag" data-query="Photoelectric">☀️ Photoelectric</span>
        </div>
        <div class="search-results-tray" id="searchResultsTray">
          <div class="search-empty-state">Start typing to search 25 CBSE Physics Chapters...</div>
        </div>
      </div>
    `;

    document.body.appendChild(modal);

    const input = modal.querySelector('#globalSearchInput');
    const closeBtn = modal.querySelector('#closeSearchModal');
    const resultsTray = modal.querySelector('#searchResultsTray');
    const quickTags = modal.querySelectorAll('.quick-tag');

    function openModal() {
      modal.style.display = 'flex';
      modal.classList.add('open');
      modal.classList.add('active');
      document.body.style.overflow = 'hidden';
      input.focus();
      loadSearchIndex();
    }

    function closeModal() {
      modal.classList.remove('open');
      modal.classList.remove('active');
      modal.style.display = 'none';
      document.body.style.overflow = '';
      input.value = '';
      resultsTray.innerHTML = '<div class="search-empty-state">Start typing to search 25 CBSE Physics Chapters...</div>';
    }

    closeBtn.addEventListener('click', closeModal);
    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeModal();
    });

    document.addEventListener('keydown', (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        openModal();
      } else if (e.key === 'Escape' && (modal.classList.contains('open') || modal.style.display === 'flex')) {
        closeModal();
      }
    });

    // Attach to triggers on page
    document.querySelectorAll('.open-search-trigger, #headerSearchBtn, .portal-search-box').forEach(el => {
      el.addEventListener('click', (e) => {
        e.preventDefault();
        openModal();
      });
    });

    quickTags.forEach(tag => {
      tag.addEventListener('click', () => {
        input.value = tag.getAttribute('data-query');
        performSearch(input.value, resultsTray);
      });
    });

    input.addEventListener('input', () => {
      performSearch(input.value.trim(), resultsTray);
    });
  }

  function performSearch(query, tray) {
    if (!query || query.length < 2) {
      tray.innerHTML = '<div class="search-empty-state">Type at least 2 characters to search...</div>';
      return;
    }

    const q = query.toLowerCase();
    const basePath = getBaseRelativePath();

    const matches = searchIndex.filter(item => {
      return (
        item.title.toLowerCase().includes(q) ||
        (item.snippet && item.snippet.toLowerCase().includes(q)) ||
        (item.chapter && item.chapter.toLowerCase().includes(q)) ||
        (item.keywords && item.keywords.some(k => k.toLowerCase().includes(q)))
      );
    }).slice(0, 20);

    if (matches.length === 0) {
      tray.innerHTML = `<div class="search-empty-state">No matching physics concepts or PYQs found for "<strong>${query}</strong>"</div>`;
      return;
    }

    let html = '';
    matches.forEach(m => {
      const linkUrl = `${basePath}${m.url}`;
      html += `
        <a href="${linkUrl}" class="search-result-item">
          <div class="result-top">
            <span class="result-chapter">${m.class ? 'Class ' + m.class + ' • ' : ''}${m.chapter || 'Physics'}</span>
            <span class="result-badge ${m.type || 'core'}">${m.badge || m.type || 'Concept'}</span>
          </div>
          <div class="result-title">${highlightText(m.title, q)}</div>
          ${m.snippet ? `<div class="result-snippet">${highlightText(m.snippet, q)}</div>` : ''}
        </a>
      `;
    });

    tray.innerHTML = html;
  }

  function highlightText(text, q) {
    if (!text) return '';
    const safeText = text.replace(/</g, '&lt;').replace(/>/g, '&gt;');
    const regex = new RegExp(`(${q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
    return safeText.replace(regex, '<mark class="search-highlight">$1</mark>');
  }

  document.addEventListener('DOMContentLoaded', () => {
    createSearchModal();
  });

  window.SearchEngine = {
    loadSearchIndex,
    open: () => {
      const modal = document.getElementById('searchModalOverlay');
      if (modal) {
        modal.classList.add('open');
        const input = modal.querySelector('#globalSearchInput');
        if (input) input.focus();
        loadSearchIndex();
      }
    }
  };
})();
