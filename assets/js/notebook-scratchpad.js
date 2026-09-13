/**
 * Interactive Whiteboard Scratchpad Engine
 * Provides a responsive HTML5 canvas for scribbling, solving physics equations and FBDs by hand,
 * and practicing CBSE derivations directly inside the browser.
 * Faithfully matches Kedar's Mathematics Whiteboard scratchpad experience.
 */

(function () {
  'use strict';

  let canvas, ctx;
  let isDrawing = false;
  let currentTool = 'pen'; // 'pen' | 'highlighter' | 'eraser'
  let currentColor = '#1e293b';
  let currentLineWidth = 3;
  let undoStack = [];
  const MAX_UNDO = 20;

  function initScratchpad() {
    const modal = document.getElementById('scratchpadModal');
    const toggleBtn = document.getElementById('scratchpadToggleBtn');
    const topBarBtn = document.getElementById('openScratchpadBtn');
    const quickNavBtn = document.getElementById('quickNavScratchpadBtn');
    const closeBtn = document.getElementById('scratchpadCloseBtn');
    const clearBtn = document.getElementById('scratchpadClearBtn');
    const undoBtn = document.getElementById('scratchpadUndoBtn');
    const toolPen = document.getElementById('toolPen');
    const toolHighlighter = document.getElementById('toolHighlighter');
    const toolEraser = document.getElementById('toolEraser');
    const sizeSlider = document.getElementById('scratchpadSize');
    const colorDots = document.querySelectorAll('.scratchpad-toolbar .color-dot');

    canvas = document.getElementById('scratchpadCanvas');
    if (!canvas || !modal) return;

    ctx = canvas.getContext('2d', { willReadFrequently: true });

    function resizeCanvas() {
      const rect = canvas.getBoundingClientRect();
      const dpr = window.devicePixelRatio || 1;

      // Save content before resize
      let imgData = null;
      if (canvas.width > 0 && canvas.height > 0) {
        try {
          imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        } catch (e) {
          // ignore potential context read errors
        }
      }

      canvas.width = rect.width * dpr;
      canvas.height = rect.height * dpr;
      ctx.scale(dpr, dpr);
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';

      if (imgData) {
        try {
          ctx.putImageData(imgData, 0, 0);
        } catch (e) {
          // ignore
        }
      }
    }

    function saveState() {
      if (undoStack.length >= MAX_UNDO) undoStack.shift();
      try {
        undoStack.push(ctx.getImageData(0, 0, canvas.width, canvas.height));
      } catch (e) {}
    }

    function openModal() {
      if (!modal.classList.contains('open')) {
        modal.classList.add('open');
        resizeCanvas();
        if (undoStack.length === 0) saveState();
      }
    }

    function closeModal() {
      modal.classList.remove('open');
    }

    function toggleModal(e) {
      if (e) e.preventDefault();
      const isOpen = modal.classList.toggle('open');
      if (isOpen) {
        resizeCanvas();
        if (undoStack.length === 0) saveState();
      }
    }

    // Toggle Modal Triggers
    if (toggleBtn) toggleBtn.addEventListener('click', toggleModal);
    if (topBarBtn) topBarBtn.addEventListener('click', toggleModal);
    if (quickNavBtn) quickNavBtn.addEventListener('click', toggleModal);

    // Fallback for any quick-nav button with title "Scratchpad"
    document.querySelectorAll('.quick-nav-btn[title="Scratchpad"]').forEach(btn => {
      btn.addEventListener('click', toggleModal);
    });

    // Any contextual open trigger
    document.querySelectorAll('.open-scratchpad-trigger').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        openModal();
      });
    });

    if (closeBtn) {
      closeBtn.addEventListener('click', (e) => {
        e.preventDefault();
        closeModal();
      });
    }

    // ESC key closes scratchpad
    window.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && modal.classList.contains('open')) {
        closeModal();
      }
    });

    // Tools & Colors
    if (toolPen) {
      toolPen.addEventListener('click', () => {
        currentTool = 'pen';
        ctx.globalCompositeOperation = 'source-over';
        ctx.globalAlpha = 1.0;
        updateActiveTool(toolPen);
      });
    }

    if (toolHighlighter) {
      toolHighlighter.addEventListener('click', () => {
        currentTool = 'highlighter';
        ctx.globalCompositeOperation = 'multiply';
        ctx.globalAlpha = 0.35;
        updateActiveTool(toolHighlighter);
      });
    }

    if (toolEraser) {
      toolEraser.addEventListener('click', () => {
        currentTool = 'eraser';
        ctx.globalCompositeOperation = 'destination-out';
        ctx.globalAlpha = 1.0;
        updateActiveTool(toolEraser);
      });
    }

    function updateActiveTool(activeBtn) {
      [toolPen, toolHighlighter, toolEraser].forEach(b => b && b.classList.remove('active'));
      if (activeBtn) activeBtn.classList.add('active');
    }

    colorDots.forEach(dot => {
      dot.addEventListener('click', () => {
        colorDots.forEach(d => d.classList.remove('active'));
        dot.classList.add('active');
        currentColor = dot.getAttribute('data-color') || '#1e293b';
        if (currentTool === 'eraser') {
          toolPen && toolPen.click();
        }
      });
    });

    if (sizeSlider) {
      sizeSlider.addEventListener('input', (e) => {
        currentLineWidth = parseInt(e.target.value, 10) || 3;
      });
    }

    if (undoBtn) {
      undoBtn.addEventListener('click', () => {
        if (undoStack.length > 1) {
          undoStack.pop(); // remove current
          const prev = undoStack[undoStack.length - 1];
          ctx.putImageData(prev, 0, 0);
        } else if (undoStack.length === 1) {
          ctx.clearRect(0, 0, canvas.width, canvas.height);
          undoStack = [];
          saveState();
        }
      });
    }

    if (clearBtn) {
      clearBtn.addEventListener('click', () => {
        saveState();
        ctx.clearRect(0, 0, canvas.width, canvas.height);
      });
    }

    // Pointer Events for Stylus, Mouse, and Touch
    let lastX = 0, lastY = 0;

    function getCoords(e) {
      const rect = canvas.getBoundingClientRect();
      const clientX = e.touches ? e.touches[0].clientX : e.clientX;
      const clientY = e.touches ? e.touches[0].clientY : e.clientY;
      return {
        x: clientX - rect.left,
        y: clientY - rect.top
      };
    }

    function startDraw(e) {
      isDrawing = true;
      const coords = getCoords(e);
      lastX = coords.x;
      lastY = coords.y;
      draw(e);
    }

    function draw(e) {
      if (!isDrawing) return;
      if (e.cancelable && e.type.startsWith('touch')) e.preventDefault();

      const coords = getCoords(e);

      ctx.beginPath();
      ctx.moveTo(lastX, lastY);
      ctx.lineTo(coords.x, coords.y);

      ctx.strokeStyle = currentColor;
      ctx.lineWidth = currentTool === 'highlighter' ? currentLineWidth * 3.5 : (currentTool === 'eraser' ? currentLineWidth * 4.5 : currentLineWidth);
      ctx.stroke();

      lastX = coords.x;
      lastY = coords.y;
    }

    function stopDraw() {
      if (isDrawing) {
        isDrawing = false;
        saveState();
      }
    }

    canvas.addEventListener('mousedown', startDraw);
    canvas.addEventListener('mousemove', draw);
    window.addEventListener('mouseup', stopDraw);

    canvas.addEventListener('touchstart', startDraw, { passive: false });
    canvas.addEventListener('touchmove', draw, { passive: false });
    window.addEventListener('touchend', stopDraw);

    window.addEventListener('resize', () => {
      if (modal.classList.contains('open')) {
        resizeCanvas();
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initScratchpad);
  } else {
    initScratchpad();
  }
})();
