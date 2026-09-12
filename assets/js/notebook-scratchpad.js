/**
 * Physics Notebook Scribble & Scratchpad Drawer
 * Allows students to solve rough equations, sketch physics free-body diagrams, and scribble calculations.
 */
(function () {
  'use strict';

  function initScratchpad() {
    const modal = document.getElementById('scratchpadModal');
    const toggleBtn = document.getElementById('scratchpadToggleBtn');
    const closeBtn = document.getElementById('scratchpadCloseBtn');
    const canvas = document.getElementById('scratchpadCanvas');
    if (!modal || !canvas) return;

    const ctx = canvas.getContext('2d');
    let isDrawing = false;
    let currentColor = '#1e293b';
    let currentTool = 'pen'; // 'pen', 'highlighter', 'eraser'
    let strokeSize = 3;
    const history = [];

    function resizeCanvas() {
      const rect = canvas.parentElement.getBoundingClientRect();
      const temp = ctx.getImageData(0, 0, canvas.width, canvas.height);
      canvas.width = rect.width;
      canvas.height = rect.height;
      if (temp.width > 0 && temp.height > 0) {
        ctx.putImageData(temp, 0, 0);
      }
    }

    function openScratchpad() {
      modal.classList.add('open');
      setTimeout(resizeCanvas, 50);
    }

    function closeScratchpad() {
      modal.classList.remove('open');
    }

    if (toggleBtn) toggleBtn.addEventListener('click', openScratchpad);
    if (closeBtn) closeBtn.addEventListener('click', closeScratchpad);

    function getCoords(e) {
      const rect = canvas.getBoundingClientRect();
      if (e.touches && e.touches.length > 0) {
        return {
          x: e.touches[0].clientX - rect.left,
          y: e.touches[0].clientY - rect.top
        };
      }
      return {
        x: e.clientX - rect.left,
        y: e.clientY - rect.top
      };
    }

    function startDrawing(e) {
      isDrawing = true;
      const { x, y } = getCoords(e);
      ctx.beginPath();
      ctx.moveTo(x, y);
      saveState();
    }

    function draw(e) {
      if (!isDrawing) return;
      e.preventDefault();
      const { x, y } = getCoords(e);

      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';

      if (currentTool === 'eraser') {
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = strokeSize * 4;
        ctx.globalAlpha = 1.0;
      } else if (currentTool === 'highlighter') {
        ctx.strokeStyle = currentColor;
        ctx.lineWidth = strokeSize * 3.5;
        ctx.globalAlpha = 0.35;
      } else {
        ctx.strokeStyle = currentColor;
        ctx.lineWidth = strokeSize;
        ctx.globalAlpha = 1.0;
      }

      ctx.lineTo(x, y);
      ctx.stroke();
    }

    function stopDrawing() {
      if (isDrawing) {
        ctx.closePath();
        isDrawing = false;
      }
    }

    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mousemove', draw);
    window.addEventListener('mouseup', stopDrawing);

    canvas.addEventListener('touchstart', startDrawing, { passive: false });
    canvas.addEventListener('touchmove', draw, { passive: false });
    window.addEventListener('touchend', stopDrawing);

    function saveState() {
      if (history.length > 15) history.shift();
      history.push(ctx.getImageData(0, 0, canvas.width, canvas.height));
    }

    // Toolbar Buttons
    const toolPen = document.getElementById('toolPen');
    const toolHighlighter = document.getElementById('toolHighlighter');
    const toolEraser = document.getElementById('toolEraser');
    const sizeSlider = document.getElementById('scratchpadSize');
    const undoBtn = document.getElementById('scratchpadUndoBtn');
    const clearBtn = document.getElementById('scratchpadClearBtn');
    const colorDots = document.querySelectorAll('.scratchpad-toolbar .color-dot');

    function setActiveTool(tool, btn) {
      currentTool = tool;
      [toolPen, toolHighlighter, toolEraser].forEach(b => b && b.classList.remove('active'));
      if (btn) btn.classList.add('active');
    }

    if (toolPen) toolPen.addEventListener('click', () => setActiveTool('pen', toolPen));
    if (toolHighlighter) toolHighlighter.addEventListener('click', () => setActiveTool('highlighter', toolHighlighter));
    if (toolEraser) toolEraser.addEventListener('click', () => setActiveTool('eraser', toolEraser));

    if (sizeSlider) {
      sizeSlider.addEventListener('input', (e) => {
        strokeSize = parseInt(e.target.value, 10) || 3;
      });
    }

    colorDots.forEach(dot => {
      dot.addEventListener('click', () => {
        colorDots.forEach(d => d.classList.remove('active'));
        dot.classList.add('active');
        currentColor = dot.getAttribute('data-color') || '#1e293b';
        if (currentTool === 'eraser') setActiveTool('pen', toolPen);
      });
    });

    if (undoBtn) {
      undoBtn.addEventListener('click', () => {
        if (history.length > 0) {
          const prevState = history.pop();
          ctx.putImageData(prevState, 0, 0);
        }
      });
    }

    if (clearBtn) {
      clearBtn.addEventListener('click', () => {
        saveState();
        ctx.clearRect(0, 0, canvas.width, canvas.height);
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initScratchpad);
  } else {
    initScratchpad();
  }
})();
