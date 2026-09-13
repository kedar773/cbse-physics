/**
 * CBSE Physics Notebook - Kedar Krishna Educator Contact Modal
 * Features:
 * - Teacher credentials & specialization (Senior STEM & Physics Specialist)
 * - Academic centers in Bhubaneswar (Arundhati Vihar & Jagannath Vihar)
 * - Interactive mailto and consultation inquiries
 */

(function() {
  'use strict';

  function createContactModal() {
    if (document.getElementById('contactModalOverlay')) return;

    const modal = document.createElement('div');
    modal.id = 'contactModalOverlay';
    modal.className = 'contact-modal-overlay';
    modal.style.display = 'none';
    modal.innerHTML = `
      <div class="contact-modal-dialog">
        <button class="contact-modal-close" id="closeContactModal" title="Close Modal">✕</button>
        <div class="contact-modal-hero">
          <div class="contact-avatar-badge">👨‍🏫</div>
          <div class="contact-hero-info">
            <h3 class="contact-name">Kedar Krishna</h3>
            <div class="contact-title">Senior STEM &amp; Chemistry Educator • CBSE &amp; JEE Specialist</div>
            <div class="contact-tagline">Academic Mentor &amp; Chemistry Educator</div>
          </div>
        </div>

        <div class="contact-modal-body">
          <div class="contact-section">
            <div class="contact-section-title">📍 Teaching Centers (Bhubaneswar, Odisha)</div>
            <div class="contact-location-list">
              <div class="location-item">
                <span class="loc-pin">🏢</span>
                <div>
                  <strong>Arundhati Vihar Center:</strong>
                  <div class="loc-sub">Plot 104, Arundhati Vihar, Near Silicon Hills, Bhubaneswar</div>
                </div>
              </div>
              <div class="location-item">
                <span class="loc-pin">🏫</span>
                <div>
                  <strong>Jagannath Vihar Center:</strong>
                  <div class="loc-sub">Lane 3, Jagannath Vihar, Baramunda, Bhubaneswar</div>
                </div>
              </div>
            </div>
          </div>

          <div class="contact-section">
            <div class="contact-section-title">📬 Direct Academic Inquiries</div>
            <div class="contact-methods">
              <a href="mailto:chemistrykedar@gmail.com?subject=CBSE%20Physics%20Notebook%20Inquiry" class="contact-btn email">
                <span>✉️ Email:</span> <strong>chemistrykedar@gmail.com</strong>
              </a>
            </div>
          </div>

          <div class="contact-section">
            <div class="contact-section-title">🎯 Academic Pedagogy &amp; Engine Mission</div>
            <p class="contact-bio">
              Dedicated to conceptual mastery, first-principles derivation, and rigorous step-marking rubrics.
              This Physics Engine synthesizes NCERT line-by-line rigor with 2020–2025 CBSE Board PYQs,
              interactive HTML5 physics simulations, and intuitive ELI5 analogies to empower CBSE Class 11 &amp; 12 students.
            </p>
          </div>
        </div>

        <div class="contact-modal-footer">
          <span>Powered by Kedar's Academy</span>
          <button class="doodle-tag tag-blue" id="closeContactModalBtn" style="cursor: pointer; border: none; padding: 0.4rem 1rem;">Close</button>
        </div>
      </div>
    `;

    document.body.appendChild(modal);

    const closeBtn = modal.querySelector('#closeContactModal');
    const closeBtn2 = modal.querySelector('#closeContactModalBtn');

    function openModal() {
      modal.style.display = 'flex';
      modal.classList.add('open');
      modal.classList.add('active');
      document.body.style.overflow = 'hidden';
    }

    function closeModal() {
      modal.classList.remove('open');
      modal.classList.remove('active');
      modal.style.display = 'none';
      document.body.style.overflow = '';
    }

    closeBtn.addEventListener('click', closeModal);
    closeBtn2.addEventListener('click', closeModal);
    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeModal();
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && (modal.classList.contains('open') || modal.style.display === 'flex')) {
        closeModal();
      }
    });

    document.querySelectorAll('.open-contact-trigger, #footerContactBtn, #headerContactBtn, a[href="#contact"]').forEach(el => {
      el.addEventListener('click', (e) => {
        e.preventDefault();
        openModal();
      });
    });

    window.ContactModal = {
      open: openModal,
      close: closeModal
    };
  }

  document.addEventListener('DOMContentLoaded', () => {
    createContactModal();
  });
})();

