/**
 * Physics Notebook Micro-Animations & Interaction Suite
 * Confetti bursts, toast notifications, and tactile feedback.
 */
(function () {
  'use strict';

  const WhiteboardAnimations = {
    showToast: function (msg, duration = 3000) {
      let toast = document.getElementById('whiteboardToast');
      if (!toast) {
        toast = document.createElement('div');
        toast.id = 'whiteboardToast';
        document.body.appendChild(toast);
      }
      toast.innerHTML = '<span>⚡</span> <span>' + msg + '</span>';
      toast.classList.add('show');
      clearTimeout(this._toastTimer);
      this._toastTimer = setTimeout(() => {
        toast.classList.remove('show');
      }, duration);
    },

    triggerConfetti: function (originX, originY) {
      let canvas = document.getElementById('confettiCanvas');
      if (!canvas) {
        canvas = document.createElement('canvas');
        canvas.id = 'confettiCanvas';
        document.body.appendChild(canvas);
      }
      const ctx = canvas.getContext('2d');
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;

      const particles = [];
      const colors = ['#1d4ed8', '#dc2626', '#16a34a', '#d97706', '#9333ea', '#2563eb', '#f59e0b'];
      const x = originX || window.innerWidth / 2;
      const y = originY || window.innerHeight / 2;

      for (let i = 0; i < 70; i++) {
        const angle = Math.random() * Math.PI * 2;
        const speed = Math.random() * 8 + 3;
        particles.push({
          x: x,
          y: y,
          vx: Math.cos(angle) * speed,
          vy: Math.sin(angle) * speed - 2,
          size: Math.random() * 7 + 4,
          color: colors[Math.floor(Math.random() * colors.length)],
          rotation: Math.random() * 360,
          rotationSpeed: Math.random() * 10 - 5,
          alpha: 1
        });
      }

      function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        let active = false;
        particles.forEach(p => {
          p.x += p.vx;
          p.y += p.vy;
          p.vy += 0.22; // gravity
          p.rotation += p.rotationSpeed;
          p.alpha -= 0.014;

          if (p.alpha > 0) {
            active = true;
            ctx.save();
            ctx.translate(p.x, p.y);
            ctx.rotate((p.rotation * Math.PI) / 180);
            ctx.globalAlpha = Math.max(0, p.alpha);
            ctx.fillStyle = p.color;
            ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size * 0.6);
            ctx.restore();
          }
        });

        if (active) {
          requestAnimationFrame(animate);
        } else {
          ctx.clearRect(0, 0, canvas.width, canvas.height);
        }
      }
      requestAnimationFrame(animate);
    }
  };

  window.WhiteboardAnimations = WhiteboardAnimations;
})();
