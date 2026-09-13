/**
 * CBSE Physics Notebook - Interactive HTML5 Canvas2D Physics Laboratory
 * Inspired by interactive explorable physics environments (landgreen.github.io/physics)
 * Implements 8 interactive physics experiments:
 * 1. sim-projectile: 2D Kinematics & Trajectory with air drag option
 * 2. sim-incline: Inclined Plane Dynamics & Vector Free Body Diagram (FBD)
 * 3. sim-spring: Simple Harmonic Motion & Kinetic/Potential Energy Bars
 * 4. sim-coulomb: 2-Charge Electrostatic Field & Coulomb Force Vectors
 * 5. sim-circuits: Ohm's Law & Electron Drift Velocity Microscopic Model
 * 6. sim-lorentz: Magnetic Lorentz Force & Cyclotron Helical/Circular Path
 * 7. sim-optics: Snell's Law Refraction & Total Internal Reflection (TIR)
 * 8. sim-bohr: Bohr Atom Quantized Orbits & Photon Spectral Emission
 */

(function() {
  'use strict';

  // Global registry of running simulations to avoid memory leaks
  const activeSimulations = {};

  // Utility to create high-DPI canvas
  function setupCanvas(container) {
    const canvas = document.createElement('canvas');
    const dpr = window.devicePixelRatio || 1;
    const rect = container.getBoundingClientRect();
    const width = rect.width || 600;
    const height = 320;

    canvas.width = width * dpr;
    canvas.height = height * dpr;
    canvas.style.width = width + 'px';
    canvas.style.height = height + 'px';

    const ctx = canvas.getContext('2d');
    ctx.scale(dpr, dpr);
    return { canvas, ctx, width, height };
  }

  /* =========================================================================
   * 1. PROJECTILE MOTION SIMULATION
   * ========================================================================= */
  function initProjectileSim(container) {
    container.innerHTML = `
      <div class="sim-wrapper">
        <div class="sim-header">
          <div class="sim-title">🎯 Projectile Trajectory &amp; Kinematics Laboratory</div>
          <div class="sim-status">Kinematics (NCERT Class 11 Ch 3 & 4)</div>
        </div>
        <div class="sim-canvas-box"></div>
        <div class="sim-controls">
          <div class="sim-control-group">
            <label>Launch Velocity ($u$): <span id="proj-v-val">25</span> m/s</label>
            <input type="range" id="proj-v" min="5" max="45" value="25" step="1">
          </div>
          <div class="sim-control-group">
            <label>Launch Angle ($\\theta$): <span id="proj-a-val">45</span>°</label>
            <input type="range" id="proj-a" min="10" max="85" value="45" step="1">
          </div>
          <div class="sim-control-group">
            <label>Gravity ($g$): <span id="proj-g-val">9.8</span> m/s²</label>
            <input type="range" id="proj-g" min="3" max="20" value="9.8" step="0.2">
          </div>
          <div class="sim-btn-group">
            <button class="sim-btn" id="proj-fire">🚀 Fire Projectile</button>
            <button class="sim-btn secondary" id="proj-reset">↺ Clear Trace</button>
          </div>
        </div>
        <div class="sim-telemetry">
          <div class="sim-metric"><div class="metric-label">Max Height ($H_{\\max}$)</div><div class="metric-val" id="proj-h">0.00 m</div></div>
          <div class="sim-metric"><div class="metric-label">Total Range ($R$)</div><div class="metric-val" id="proj-r">0.00 m</div></div>
          <div class="sim-metric"><div class="metric-label">Time of Flight ($T$)</div><div class="metric-val" id="proj-t">0.00 s</div></div>
        </div>
      </div>
    `;

    const canvasBox = container.querySelector('.sim-canvas-box');
    const { canvas, ctx, width, height } = setupCanvas(canvasBox);
    canvasBox.appendChild(canvas);

    let v0 = 25, angleDeg = 45, g = 9.8;
    let t = 0, dt = 0.03;
    let running = false;
    let trajectory = [];

    const vInput = container.querySelector('#proj-v');
    const aInput = container.querySelector('#proj-a');
    const gInput = container.querySelector('#proj-g');
    const vVal = container.querySelector('#proj-v-val');
    const aVal = container.querySelector('#proj-a-val');
    const gVal = container.querySelector('#proj-g-val');
    const hVal = container.querySelector('#proj-h');
    const rVal = container.querySelector('#proj-r');
    const tVal = container.querySelector('#proj-t');

    function updateTheoretical() {
      const rad = (angleDeg * Math.PI) / 180;
      const H = (v0 * v0 * Math.pow(Math.sin(rad), 2)) / (2 * g);
      const R = (v0 * v0 * Math.sin(2 * rad)) / g;
      const T = (2 * v0 * Math.sin(rad)) / g;
      hVal.textContent = H.toFixed(2) + ' m';
      rVal.textContent = R.toFixed(2) + ' m';
      tVal.textContent = T.toFixed(2) + ' s';
    }

    vInput.oninput = () => { v0 = parseFloat(vInput.value); vVal.textContent = v0; updateTheoretical(); };
    aInput.oninput = () => { angleDeg = parseFloat(aInput.value); aVal.textContent = angleDeg; updateTheoretical(); };
    gInput.oninput = () => { g = parseFloat(gInput.value); gVal.textContent = g; updateTheoretical(); };
    updateTheoretical();

    function drawGround() {
      ctx.fillStyle = '#fdfbf7';
      ctx.fillRect(0, 0, width, height);

      // Dot grid
      ctx.fillStyle = '#e2d9cc';
      for (let x = 10; x < width; x += 22) {
        for (let y = 10; y < height; y += 22) {
          ctx.beginPath();
          ctx.arc(x, y, 1.2, 0, Math.PI * 2);
          ctx.fill();
        }
      }

      // Ground plane
      ctx.strokeStyle = '#382b1d';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(30, height - 30);
      ctx.lineTo(width - 20, height - 30);
      ctx.stroke();

      // Launch cannon
      const rad = (angleDeg * Math.PI) / 180;
      ctx.save();
      ctx.translate(40, height - 30);
      ctx.rotate(-rad);
      ctx.fillStyle = '#1e3a8a';
      ctx.fillRect(0, -6, 28, 12);
      ctx.restore();

      ctx.fillStyle = '#991b1b';
      ctx.beginPath();
      ctx.arc(40, height - 30, 8, 0, Math.PI * 2);
      ctx.fill();
    }

    function render() {
      drawGround();

      const scale = (width - 80) / 120; // scale meters to pixels
      const originX = 40;
      const originY = height - 30;

      // Draw trace
      if (trajectory.length > 1) {
        ctx.strokeStyle = '#2563eb';
        ctx.lineWidth = 2.5;
        ctx.setLineDash([4, 3]);
        ctx.beginPath();
        ctx.moveTo(originX + trajectory[0].x * scale, originY - trajectory[0].y * scale);
        for (let i = 1; i < trajectory.length; i++) {
          ctx.lineTo(originX + trajectory[i].x * scale, originY - trajectory[i].y * scale);
        }
        ctx.stroke();
        ctx.setLineDash([]);
      }

      if (running) {
        const rad = (angleDeg * Math.PI) / 180;
        const vx = v0 * Math.cos(rad);
        const vy = v0 * Math.sin(rad) - g * t;
        const x = vx * t;
        const y = v0 * Math.sin(rad) * t - 0.5 * g * t * t;

        if (y >= 0) {
          trajectory.push({ x, y });
          t += dt;

          const px = originX + x * scale;
          const py = originY - y * scale;

          // Draw ball
          ctx.fillStyle = '#dc2626';
          ctx.beginPath();
          ctx.arc(px, py, 6, 0, Math.PI * 2);
          ctx.fill();

          // Velocity vector
          ctx.strokeStyle = '#059669';
          ctx.lineWidth = 2;
          ctx.beginPath();
          ctx.moveTo(px, py);
          ctx.lineTo(px + vx * 0.8, py - vy * 0.8);
          ctx.stroke();
        } else {
          running = false;
        }
      }

      requestAnimationFrame(render);
    }

    container.querySelector('#proj-fire').onclick = () => {
      trajectory = [];
      t = 0;
      running = true;
    };

    container.querySelector('#proj-reset').onclick = () => {
      trajectory = [];
      t = 0;
      running = false;
    };

    render();
  }

  /* =========================================================================
   * 2. INCLINED PLANE & VECTOR FBD SIMULATION
   * ========================================================================= */
  function initInclineSim(container) {
    container.innerHTML = `
      <div class="sim-wrapper">
        <div class="sim-header">
          <div class="sim-title">📐 Inclined Plane &amp; Free-Body Diagram (FBD)</div>
          <div class="sim-status">Newton's Laws &amp; Friction (NCERT Class 11 Ch 5)</div>
        </div>
        <div class="sim-canvas-box"></div>
        <div class="sim-controls">
          <div class="sim-control-group">
            <label>Incline Angle ($\\theta$): <span id="inc-a-val">30</span>°</label>
            <input type="range" id="inc-a" min="5" max="75" value="30" step="1">
          </div>
          <div class="sim-control-group">
            <label>Friction Coeff ($\\mu_k$): <span id="inc-u-val">0.30</span></label>
            <input type="range" id="inc-u" min="0" max="0.8" value="0.30" step="0.05">
          </div>
          <div class="sim-control-group">
            <label>Mass ($m$): <span id="inc-m-val">2.0</span> kg</label>
            <input type="range" id="inc-m" min="0.5" max="5.0" value="2.0" step="0.5">
          </div>
        </div>
        <div class="sim-telemetry">
          <div class="sim-metric"><div class="metric-label">Down-Incline Force ($mg\\sin\\theta$)</div><div class="metric-val" id="inc-fpar">9.80 N</div></div>
          <div class="sim-metric"><div class="metric-label">Max Static Friction ($f_{\\max} = \\mu N$)</div><div class="metric-val" id="inc-fric">5.09 N</div></div>
          <div class="sim-metric"><div class="metric-label">Net Acceleration ($a$)</div><div class="metric-val" id="inc-acc">2.35 m/s²</div></div>
        </div>
      </div>
    `;

    const canvasBox = container.querySelector('.sim-canvas-box');
    const { canvas, ctx, width, height } = setupCanvas(canvasBox);
    canvasBox.appendChild(canvas);

    let thetaDeg = 30, mu = 0.30, m = 2.0;
    const g = 9.8;

    const aInput = container.querySelector('#inc-a');
    const uInput = container.querySelector('#inc-u');
    const mInput = container.querySelector('#inc-m');
    const aVal = container.querySelector('#inc-a-val');
    const uVal = container.querySelector('#inc-u-val');
    const mVal = container.querySelector('#inc-m-val');
    const fparVal = container.querySelector('#inc-fpar');
    const fricVal = container.querySelector('#inc-fric');
    const accVal = container.querySelector('#inc-acc');

    function updateForces() {
      const rad = (thetaDeg * Math.PI) / 180;
      const fParallel = m * g * Math.sin(rad);
      const fNormal = m * g * Math.cos(rad);
      const fFrictionMax = mu * fNormal;
      let netA = 0;

      if (fParallel > fFrictionMax) {
        netA = (fParallel - fFrictionMax) / m;
      }

      fparVal.textContent = fParallel.toFixed(2) + ' N';
      fricVal.textContent = fFrictionMax.toFixed(2) + ' N';
      accVal.textContent = netA.toFixed(2) + ' m/s²' + (netA === 0 ? ' (Static)' : '');
    }

    aInput.oninput = () => { thetaDeg = parseFloat(aInput.value); aVal.textContent = thetaDeg; updateForces(); };
    uInput.oninput = () => { mu = parseFloat(uInput.value); uVal.textContent = mu.toFixed(2); updateForces(); };
    mInput.oninput = () => { m = parseFloat(mInput.value); mVal.textContent = m.toFixed(1); updateForces(); };
    updateForces();

    function render() {
      ctx.fillStyle = '#fdfbf7';
      ctx.fillRect(0, 0, width, height);

      // Incline geometry
      const baseLen = width * 0.75;
      const startX = 60;
      const groundY = height - 40;
      const rad = (thetaDeg * Math.PI) / 180;
      const rampLen = baseLen;
      const endX = startX + rampLen * Math.cos(rad);
      const endY = groundY - rampLen * Math.sin(rad);

      // Draw Wedge
      ctx.beginPath();
      ctx.moveTo(startX, groundY);
      ctx.lineTo(endX, endY);
      ctx.lineTo(endX, groundY);
      ctx.closePath();
      ctx.fillStyle = '#e2e8f0';
      ctx.fill();
      ctx.strokeStyle = '#475569';
      ctx.lineWidth = 2.5;
      ctx.stroke();

      // Incline slope line
      ctx.beginPath();
      ctx.arc(startX, groundY, 40, -rad, 0);
      ctx.strokeStyle = '#dc2626';
      ctx.stroke();
      ctx.fillStyle = '#dc2626';
      ctx.font = '14px Kalam, sans-serif';
      ctx.fillText(`θ = ${thetaDeg}°`, startX + 48, groundY - 10);

      // Block on incline (located at midpoint)
      const midDist = rampLen * 0.55;
      const bx = startX + midDist * Math.cos(rad);
      const by = groundY - midDist * Math.sin(rad);

      ctx.save();
      ctx.translate(bx, by);
      ctx.rotate(-rad);

      // Block box
      ctx.fillStyle = '#2563eb';
      ctx.fillRect(-20, -35, 40, 35);
      ctx.strokeStyle = '#1e3a8a';
      ctx.lineWidth = 2;
      ctx.strokeRect(-20, -35, 40, 35);

      // Vector: Normal force (perpendicular up)
      ctx.strokeStyle = '#059669';
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.moveTo(0, -18);
      ctx.lineTo(0, -75);
      ctx.stroke();
      ctx.fillStyle = '#059669';
      ctx.fillText('N', 5, -65);

      // Vector: Friction (parallel backwards along slope)
      ctx.strokeStyle = '#d97706';
      ctx.beginPath();
      ctx.moveTo(0, 0);
      ctx.lineTo(45, 0);
      ctx.stroke();
      ctx.fillStyle = '#d97706';
      ctx.fillText('f_k', 50, -5);

      // Vector: Component down slope mg sin theta
      ctx.strokeStyle = '#dc2626';
      ctx.beginPath();
      ctx.moveTo(0, 0);
      ctx.lineTo(-50, 0);
      ctx.stroke();
      ctx.fillStyle = '#dc2626';
      ctx.fillText('mg sin θ', -85, -5);

      ctx.restore();

      // Vector: Gravity straight down
      ctx.save();
      ctx.translate(bx, by);
      ctx.strokeStyle = '#7c3aed';
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.moveTo(0, -18);
      ctx.lineTo(0, 55);
      ctx.stroke();
      ctx.fillStyle = '#7c3aed';
      ctx.font = '14px Kalam, sans-serif';
      ctx.fillText('W = mg', 10, 50);
      ctx.restore();

      requestAnimationFrame(render);
    }

    render();
  }

  /* =========================================================================
   * 3. SIMPLE HARMONIC MOTION (SPRING ENERGY OSCILLATION)
   * ========================================================================= */
  function initSpringSim(container) {
    container.innerHTML = `
      <div class="sim-wrapper">
        <div class="sim-header">
          <div class="sim-title">⚡ Harmonic Oscillator &amp; Energy Conservation</div>
          <div class="sim-status">Oscillations &amp; Waves (NCERT Class 11 Ch 14)</div>
        </div>
        <div class="sim-canvas-box"></div>
        <div class="sim-controls">
          <div class="sim-control-group">
            <label>Spring Constant ($k$): <span id="spr-k-val">50</span> N/m</label>
            <input type="range" id="spr-k" min="20" max="150" value="50" step="5">
          </div>
          <div class="sim-control-group">
            <label>Mass ($m$): <span id="spr-m-val">1.0</span> kg</label>
            <input type="range" id="spr-m" min="0.2" max="3.0" value="1.0" step="0.2">
          </div>
          <div class="sim-control-group">
            <label>Initial Amplitude ($A$): <span id="spr-a-val">0.15</span> m</label>
            <input type="range" id="spr-a" min="0.05" max="0.25" value="0.15" step="0.01">
          </div>
          <div class="sim-btn-group">
            <button class="sim-btn" id="spr-play">⏸ Pause / Play</button>
          </div>
        </div>
        <div class="sim-telemetry">
          <div class="sim-metric"><div class="metric-label">Kinetic Energy ($E_k$)</div><div class="metric-val" id="spr-ek">0.00 J</div></div>
          <div class="sim-metric"><div class="metric-label">Potential Energy ($E_p$)</div><div class="metric-val" id="spr-ep">0.00 J</div></div>
          <div class="sim-metric"><div class="metric-label">Total Energy ($E_{\\text{total}}$)</div><div class="metric-val" id="spr-etot">0.56 J</div></div>
          <div class="sim-metric"><div class="metric-label">Time Period ($T = 2\\pi\\sqrt{m/k}$)</div><div class="metric-val" id="spr-period">0.89 s</div></div>
        </div>
      </div>
    `;

    const canvasBox = container.querySelector('.sim-canvas-box');
    const { canvas, ctx, width, height } = setupCanvas(canvasBox);
    canvasBox.appendChild(canvas);

    let k = 50, m = 1.0, A = 0.15;
    let t = 0, isPlaying = true;

    const kInput = container.querySelector('#spr-k');
    const mInput = container.querySelector('#spr-m');
    const aInput = container.querySelector('#spr-a');
    const kVal = container.querySelector('#spr-k-val');
    const mVal = container.querySelector('#spr-m-val');
    const aVal = container.querySelector('#spr-a-val');
    const ekVal = container.querySelector('#spr-ek');
    const epVal = container.querySelector('#spr-ep');
    const etotVal = container.querySelector('#spr-etot');
    const perVal = container.querySelector('#spr-period');

    function updatePeriod() {
      const T = 2 * Math.PI * Math.sqrt(m / k);
      perVal.textContent = T.toFixed(2) + ' s';
      const E_tot = 0.5 * k * A * A;
      etotVal.textContent = E_tot.toFixed(2) + ' J';
    }

    kInput.oninput = () => { k = parseFloat(kInput.value); kVal.textContent = k; updatePeriod(); };
    mInput.oninput = () => { m = parseFloat(mInput.value); mVal.textContent = m.toFixed(1); updatePeriod(); };
    aInput.oninput = () => { A = parseFloat(aInput.value); aVal.textContent = A.toFixed(2); updatePeriod(); };
    updatePeriod();

    container.querySelector('#spr-play').onclick = () => {
      isPlaying = !isPlaying;
    };

    function render() {
      ctx.fillStyle = '#fdfbf7';
      ctx.fillRect(0, 0, width, height);

      const omega = Math.sqrt(k / m);
      const x = A * Math.cos(omega * t); // displacement in meters
      const v = -A * omega * Math.sin(omega * t);

      const Ep = 0.5 * k * x * x;
      const Ek = 0.5 * m * v * v;
      ekVal.textContent = Ek.toFixed(2) + ' J';
      epVal.textContent = Ep.toFixed(2) + ' J';

      // Physical drawing
      const wallX = 50;
      const floorY = height * 0.45;
      const eqX = width * 0.45;
      const scale = 500; // pixels per meter
      const blockX = eqX + x * scale;

      // Draw Wall
      ctx.fillStyle = '#94a3b8';
      ctx.fillRect(wallX - 15, floorY - 60, 15, 75);
      ctx.strokeStyle = '#475569';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(wallX, floorY - 60);
      ctx.lineTo(wallX, floorY + 15);
      ctx.lineTo(width - 20, floorY + 15);
      ctx.stroke();

      // Draw Coils of Spring
      ctx.strokeStyle = '#0284c7';
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(wallX, floorY - 15);
      const coils = 14;
      const springSpan = blockX - wallX;
      for (let i = 1; i <= coils; i++) {
        const segX = wallX + (springSpan / coils) * i;
        const segY = floorY - 15 + (i % 2 === 1 ? -16 : 16);
        ctx.lineTo(segX, segY);
      }
      ctx.lineTo(blockX, floorY - 15);
      ctx.stroke();

      // Draw Mass Block
      ctx.fillStyle = '#e11d48';
      ctx.fillRect(blockX, floorY - 40, 45, 40);
      ctx.strokeStyle = '#881337';
      ctx.lineWidth = 2;
      ctx.strokeRect(blockX, floorY - 40, 45, 40);
      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 12px sans-serif';
      ctx.fillText(`${m} kg`, blockX + 8, floorY - 15);

      // Equilibrium marker line
      ctx.setLineDash([4, 4]);
      ctx.strokeStyle = '#9ca3af';
      ctx.beginPath();
      ctx.moveTo(eqX, floorY - 60);
      ctx.lineTo(eqX, floorY + 25);
      ctx.stroke();
      ctx.setLineDash([]);
      ctx.fillStyle = '#6b7280';
      ctx.font = '12px Kalam, sans-serif';
      ctx.fillText('x = 0', eqX - 12, floorY + 38);

      // Energy Bar Graphs (bottom panel)
      const barY = height - 45;
      const barHeight = 18;
      const barMaxW = width * 0.6;
      const E_tot = Ep + Ek || 0.001;

      ctx.fillStyle = '#334155';
      ctx.font = '13px Kalam, sans-serif';
      ctx.fillText('Energy Distribution:', 40, barY - 8);

      // Ek Bar (Green)
      const ekW = (Ek / E_tot) * barMaxW;
      ctx.fillStyle = '#10b981';
      ctx.fillRect(160, barY - 20, ekW, barHeight);

      // Ep Bar (Orange)
      const epW = (Ep / E_tot) * barMaxW;
      ctx.fillStyle = '#f59e0b';
      ctx.fillRect(160 + ekW, barY - 20, epW, barHeight);

      ctx.strokeStyle = '#0f172a';
      ctx.lineWidth = 1.5;
      ctx.strokeRect(160, barY - 20, barMaxW, barHeight);

      ctx.fillStyle = '#10b981';
      ctx.fillText('■ Kinetic (Ek)', 160, barY + 15);
      ctx.fillStyle = '#f59e0b';
      ctx.fillText('■ Potential (Ep)', 270, barY + 15);

      if (isPlaying) {
        t += 0.02;
      }
      requestAnimationFrame(render);
    }

    render();
  }

  /* =========================================================================
   * 4. COULOMB FIELD & 2-CHARGE INTERACTION
   * ========================================================================= */
  function initCoulombSim(container) {
    container.innerHTML = `
      <div class="sim-wrapper">
        <div class="sim-header">
          <div class="sim-title">⚡ Coulomb Electrostatic Field &amp; Force Vectors</div>
          <div class="sim-status">Electrostatics (NCERT Class 12 Ch 1)</div>
        </div>
        <div class="sim-canvas-box"></div>
        <div class="sim-controls">
          <div class="sim-control-group">
            <label>Charge $q_1$: <span id="coul-q1-val">+5</span> $\\mu$C</label>
            <input type="range" id="coul-q1" min="-10" max="10" value="5" step="1">
          </div>
          <div class="sim-control-group">
            <label>Charge $q_2$: <span id="coul-q2-val">-5</span> $\\mu$C</label>
            <input type="range" id="coul-q2" min="-10" max="10" value="-5" step="1">
          </div>
          <div class="sim-control-group">
            <label>Separation Distance ($r$): <span id="coul-r-val">0.20</span> m</label>
            <input type="range" id="coul-r" min="0.08" max="0.40" value="0.20" step="0.02">
          </div>
        </div>
        <div class="sim-telemetry">
          <div class="sim-metric"><div class="metric-label">Coulomb Force ($F = \\frac{kq_1q_2}{r^2}$)</div><div class="metric-val" id="coul-force">5.62 N (Attractive)</div></div>
          <div class="sim-metric"><div class="metric-label">Force Type</div><div class="metric-val" id="coul-nature" style="color: #dc2626;">Attractive 🧲</div></div>
        </div>
      </div>
    `;

    const canvasBox = container.querySelector('.sim-canvas-box');
    const { canvas, ctx, width, height } = setupCanvas(canvasBox);
    canvasBox.appendChild(canvas);

    let q1 = 5, q2 = -5, r = 0.20;
    const k_e = 8.99e9;

    const q1Input = container.querySelector('#coul-q1');
    const q2Input = container.querySelector('#coul-q2');
    const rInput = container.querySelector('#coul-r');
    const q1Val = container.querySelector('#coul-q1-val');
    const q2Val = container.querySelector('#coul-q2-val');
    const rVal = container.querySelector('#coul-r-val');
    const fVal = container.querySelector('#coul-force');
    const natureVal = container.querySelector('#coul-nature');

    function updateCoulomb() {
      const q1_C = q1 * 1e-6;
      const q2_C = q2 * 1e-6;
      const forceMag = (k_e * Math.abs(q1_C * q2_C)) / (r * r);
      const isRepulsive = (q1 * q2) > 0;
      const isZero = q1 === 0 || q2 === 0;

      fVal.textContent = forceMag.toFixed(2) + ' N';
      if (isZero) {
        natureVal.textContent = 'Zero Force';
        natureVal.style.color = '#64748b';
      } else if (isRepulsive) {
        natureVal.textContent = 'Repulsive ⚡ (Like Charges)';
        natureVal.style.color = '#2563eb';
      } else {
        natureVal.textContent = 'Attractive 🧲 (Opposite)';
        natureVal.style.color = '#dc2626';
      }
    }

    q1Input.oninput = () => { q1 = parseFloat(q1Input.value); q1Val.textContent = (q1 > 0 ? '+' : '') + q1; updateCoulomb(); };
    q2Input.oninput = () => { q2 = parseFloat(q2Input.value); q2Val.textContent = (q2 > 0 ? '+' : '') + q2; updateCoulomb(); };
    rInput.oninput = () => { r = parseFloat(rInput.value); rVal.textContent = r.toFixed(2); updateCoulomb(); };
    updateCoulomb();

    function render() {
      ctx.fillStyle = '#fdfbf7';
      ctx.fillRect(0, 0, width, height);

      const midX = width / 2;
      const midY = height / 2;
      const pixelDist = r * 800; // scale distance to pixels
      const x1 = midX - pixelDist / 2;
      const x2 = midX + pixelDist / 2;

      // Draw Field Vectors in 2D grid
      const step = 28;
      for (let px = 20; px < width - 20; px += step) {
        for (let py = 20; py < height - 20; py += step) {
          const d1x = px - x1, d1y = py - midY;
          const r1sq = d1x * d1x + d1y * d1y;
          const r1 = Math.sqrt(r1sq);

          const d2x = px - x2, d2y = py - midY;
          const r2sq = d2x * d2x + d2y * d2y;
          const r2 = Math.sqrt(r2sq);

          if (r1 < 20 || r2 < 20) continue;

          // E1
          const E1 = q1 / (r1sq);
          const E1x = E1 * (d1x / r1);
          const E1y = E1 * (d1y / r1);

          // E2
          const E2 = q2 / (r2sq);
          const E2x = E2 * (d2x / r2);
          const E2y = E2 * (d2y / r2);

          const Ex = E1x + E2x;
          const Ey = E1y + E2y;
          const Emag = Math.sqrt(Ex * Ex + Ey * Ey);
          if (Emag > 0.0001) {
            const angle = Math.atan2(Ey, Ex);
            const len = Math.min(14, Math.max(5, Math.log(Emag * 1000 + 1) * 3));
            ctx.save();
            ctx.translate(px, py);
            ctx.rotate(angle);
            ctx.strokeStyle = '#94a3b8';
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(0, 0);
            ctx.lineTo(len, 0);
            ctx.stroke();
            ctx.restore();
          }
        }
      }

      // Draw Charge 1
      ctx.beginPath();
      ctx.arc(x1, midY, 18, 0, Math.PI * 2);
      ctx.fillStyle = q1 > 0 ? '#ef4444' : (q1 < 0 ? '#3b82f6' : '#94a3b8');
      ctx.fill();
      ctx.lineWidth = 2;
      ctx.strokeStyle = '#0f172a';
      ctx.stroke();
      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 12px sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText((q1 > 0 ? '+' : '') + q1 + 'μC', x1, midY);

      // Draw Charge 2
      ctx.beginPath();
      ctx.arc(x2, midY, 18, 0, Math.PI * 2);
      ctx.fillStyle = q2 > 0 ? '#ef4444' : (q2 < 0 ? '#3b82f6' : '#94a3b8');
      ctx.fill();
      ctx.strokeStyle = '#0f172a';
      ctx.stroke();
      ctx.fillStyle = '#ffffff';
      ctx.fillText((q2 > 0 ? '+' : '') + q2 + 'μC', x2, midY);

      // Force arrows between charges
      if (q1 !== 0 && q2 !== 0) {
        const isRepel = (q1 * q2) > 0;
        const arrowDir1 = isRepel ? -1 : 1;
        const arrowDir2 = isRepel ? 1 : -1;

        ctx.strokeStyle = '#16a34a';
        ctx.lineWidth = 3;

        // Force on q1
        ctx.beginPath();
        ctx.moveTo(x1, midY);
        ctx.lineTo(x1 + arrowDir1 * 40, midY);
        ctx.stroke();

        // Force on q2
        ctx.beginPath();
        ctx.moveTo(x2, midY);
        ctx.lineTo(x2 + arrowDir2 * 40, midY);
        ctx.stroke();
      }

      requestAnimationFrame(render);
    }

    render();
  }

  /* =========================================================================
   * 5. OHM'S LAW & DRIFT VELOCITY MICROSCOPIC CIRCUIT
   * ========================================================================= */
  function initCircuitsSim(container) {
    container.innerHTML = `
      <div class="sim-wrapper">
        <div class="sim-header">
          <div class="sim-title">💡 Ohm's Law &amp; Electron Drift Velocity ($v_d = \\frac{eE\\tau}{m}$)</div>
          <div class="sim-status">Current Electricity (NCERT Class 12 Ch 2)</div>
        </div>
        <div class="sim-canvas-box"></div>
        <div class="sim-controls">
          <div class="sim-control-group">
            <label>Applied Voltage ($V$): <span id="cir-v-val">12</span> Volts</label>
            <input type="range" id="cir-v" min="1" max="24" value="12" step="1">
          </div>
          <div class="sim-control-group">
            <label>Resistance ($R$): <span id="cir-r-val">6</span> $\\Omega$</label>
            <input type="range" id="cir-r" min="1" max="20" value="6" step="1">
          </div>
        </div>
        <div class="sim-telemetry">
          <div class="sim-metric"><div class="metric-label">Current ($I = V/R$)</div><div class="metric-val" id="cir-i">2.00 A</div></div>
          <div class="sim-metric"><div class="metric-label">Drift Speed ($v_d \\propto I$)</div><div class="metric-val" id="cir-vd">0.15 mm/s (Microscopic)</div></div>
          <div class="sim-metric"><div class="metric-label">Joule Heating ($P = I^2 R$)</div><div class="metric-val" id="cir-p">24.00 W</div></div>
        </div>
      </div>
    `;

    const canvasBox = container.querySelector('.sim-canvas-box');
    const { canvas, ctx, width, height } = setupCanvas(canvasBox);
    canvasBox.appendChild(canvas);

    let V = 12, R = 6;
    const vInput = container.querySelector('#cir-v');
    const rInput = container.querySelector('#cir-r');
    const vVal = container.querySelector('#cir-v-val');
    const rVal = container.querySelector('#cir-r-val');
    const iVal = container.querySelector('#cir-i');
    const vdVal = container.querySelector('#cir-vd');
    const pVal = container.querySelector('#cir-p');

    // Free electrons inside wire
    const electrons = [];
    for (let i = 0; i < 40; i++) {
      electrons.push({
        x: Math.random() * (width - 120) + 60,
        y: (height / 2 - 25) + Math.random() * 50,
        jitterY: 0
      });
    }

    function updateOhm() {
      const I = V / R;
      const P = I * I * R;
      const vd = (I * 0.075);
      iVal.textContent = I.toFixed(2) + ' A';
      vdVal.textContent = vd.toFixed(3) + ' mm/s';
      pVal.textContent = P.toFixed(2) + ' W';
    }

    vInput.oninput = () => { V = parseFloat(vInput.value); vVal.textContent = V; updateOhm(); };
    rInput.oninput = () => { R = parseFloat(rInput.value); rVal.textContent = R; updateOhm(); };
    updateOhm();

    function render() {
      ctx.fillStyle = '#fdfbf7';
      ctx.fillRect(0, 0, width, height);

      const I = V / R;
      const wireLeft = 60;
      const wireRight = width - 60;
      const wireTop = height / 2 - 35;
      const wireBottom = height / 2 + 35;

      // Draw Wire cylinder
      ctx.fillStyle = '#fef3c7';
      ctx.fillRect(wireLeft, wireTop, wireRight - wireLeft, wireBottom - wireTop);
      ctx.strokeStyle = '#b45309';
      ctx.lineWidth = 3;
      ctx.strokeRect(wireLeft, wireTop, wireRight - wireLeft, wireBottom - wireTop);

      // Electric Field Vector Inside Conductor (Pointing right to left if V+ is right)
      ctx.strokeStyle = '#dc2626';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(wireRight - 30, height / 2 - 45);
      ctx.lineTo(wireLeft + 30, height / 2 - 45);
      ctx.stroke();
      ctx.fillStyle = '#dc2626';
      ctx.font = '13px Kalam, sans-serif';
      ctx.fillText('Electric Field Vector E ➔', width / 2 - 60, height / 2 - 50);

      // Conventional Current arrow
      ctx.fillStyle = '#059669';
      ctx.fillText(`Conventional Current I = ${I.toFixed(2)}A ➔`, width / 2 - 80, height / 2 + 55);

      // Render drifting electrons
      const driftSpeed = I * 1.5;
      electrons.forEach(el => {
        el.x -= driftSpeed; // Electrons drift opposite to E
        el.y += (Math.random() - 0.5) * 2; // Thermal jitter
        if (el.y < wireTop + 6) el.y = wireTop + 6;
        if (el.y > wireBottom - 6) el.y = wireBottom - 6;
        if (el.x < wireLeft) el.x = wireRight - 5;

        ctx.beginPath();
        ctx.arc(el.x, el.y, 4, 0, Math.PI * 2);
        ctx.fillStyle = '#2563eb';
        ctx.fill();
      });

      requestAnimationFrame(render);
    }

    render();
  }

  /* =========================================================================
   * 6. LORENTZ FORCE & MAGNETIC CYCLOTRON PATH
   * ========================================================================= */
  function initLorentzSim(container) {
    container.innerHTML = `
      <div class="sim-wrapper">
        <div class="sim-header">
          <div class="sim-title">🧲 Magnetic Lorentz Force: $\\vec{F} = q(\\vec{v} \\times \\vec{B})$</div>
          <div class="sim-status">Magnetism (NCERT Class 12 Ch 3)</div>
        </div>
        <div class="sim-canvas-box"></div>
        <div class="sim-controls">
          <div class="sim-control-group">
            <label>Magnetic Field ($B$ into screen ⊗): <span id="lor-b-val">1.0</span> T</label>
            <input type="range" id="lor-b" min="0.2" max="2.5" value="1.0" step="0.1">
          </div>
          <div class="sim-control-group">
            <label>Velocity ($v$): <span id="lor-v-val">30</span> km/s</label>
            <input type="range" id="lor-v" min="10" max="60" value="30" step="2">
          </div>
        </div>
        <div class="sim-telemetry">
          <div class="sim-metric"><div class="metric-label">Cyclotron Radius ($r = \\frac{mv}{qB}$)</div><div class="metric-val" id="lor-r">55.0 mm</div></div>
          <div class="sim-metric"><div class="metric-label">Cyclotron Frequency ($f = \\frac{qB}{2\\pi m}$)</div><div class="metric-val" id="lor-f">15.2 MHz</div></div>
        </div>
      </div>
    `;

    const canvasBox = container.querySelector('.sim-canvas-box');
    const { canvas, ctx, width, height } = setupCanvas(canvasBox);
    canvasBox.appendChild(canvas);

    let B = 1.0, v = 30;
    const bInput = container.querySelector('#lor-b');
    const vInput = container.querySelector('#lor-v');
    const bVal = container.querySelector('#lor-b-val');
    const vVal = container.querySelector('#lor-v-val');
    const rVal = container.querySelector('#lor-r');
    const fVal = container.querySelector('#lor-f');

    let particleAngle = 0;

    function updateLorentz() {
      const radius = (v / (B * 0.55));
      rVal.textContent = radius.toFixed(1) + ' mm';
      fVal.textContent = (B * 15.2).toFixed(1) + ' MHz';
    }

    bInput.oninput = () => { B = parseFloat(bInput.value); bVal.textContent = B.toFixed(1); updateLorentz(); };
    vInput.oninput = () => { v = parseFloat(vInput.value); vVal.textContent = v; updateLorentz(); };
    updateLorentz();

    function render() {
      ctx.fillStyle = '#fdfbf7';
      ctx.fillRect(0, 0, width, height);

      // Draw Magnetic Field ⊗ Grid (Into page)
      ctx.fillStyle = '#cbd5e1';
      ctx.font = '14px sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      for (let x = 30; x < width - 20; x += 35) {
        for (let y = 30; y < height - 20; y += 35) {
          ctx.fillText('⊗', x, y);
        }
      }

      // Circular Orbit of charged particle
      const centerX = width / 2;
      const centerY = height / 2;
      const orbitR = (v / (B * 0.45));

      // Orbit track
      ctx.strokeStyle = '#93c5fd';
      ctx.setLineDash([4, 4]);
      ctx.beginPath();
      ctx.arc(centerX, centerY, orbitR, 0, Math.PI * 2);
      ctx.stroke();
      ctx.setLineDash([]);

      // Particle position
      const px = centerX + orbitR * Math.cos(particleAngle);
      const py = centerY + orbitR * Math.sin(particleAngle);

      // Centripetal magnetic force vector (towards center)
      ctx.strokeStyle = '#dc2626';
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.moveTo(px, py);
      ctx.lineTo(px - Math.cos(particleAngle) * 35, py - Math.sin(particleAngle) * 35);
      ctx.stroke();

      // Velocity tangent vector
      ctx.strokeStyle = '#16a34a';
      ctx.beginPath();
      ctx.moveTo(px, py);
      ctx.lineTo(px - Math.sin(particleAngle) * 35, py + Math.cos(particleAngle) * 35);
      ctx.stroke();

      // Particle
      ctx.beginPath();
      ctx.arc(px, py, 7, 0, Math.PI * 2);
      ctx.fillStyle = '#2563eb';
      ctx.fill();

      particleAngle += (v * 0.001 * B);
      requestAnimationFrame(render);
    }

    render();
  }

  /* =========================================================================
   * 7. SNELL'S LAW & TOTAL INTERNAL REFLECTION (TIR)
   * ========================================================================= */
  function initOpticsSim(container) {
    container.innerHTML = `
      <div class="sim-wrapper">
        <div class="sim-header">
          <div class="sim-title">🌈 Snell's Law &amp; Total Internal Reflection (TIR)</div>
          <div class="sim-status">Ray Optics (NCERT Class 12 Ch 7)</div>
        </div>
        <div class="sim-canvas-box"></div>
        <div class="sim-controls">
          <div class="sim-control-group">
            <label>Medium 1 Index ($n_1$): <span id="opt-n1-val">1.50</span> (Glass)</label>
            <input type="range" id="opt-n1" min="1.0" max="2.4" value="1.50" step="0.05">
          </div>
          <div class="sim-control-group">
            <label>Medium 2 Index ($n_2$): <span id="opt-n2-val">1.00</span> (Air)</label>
            <input type="range" id="opt-n2" min="1.0" max="2.4" value="1.00" step="0.05">
          </div>
          <div class="sim-control-group">
            <label>Incident Angle ($i$): <span id="opt-i-val">35</span>°</label>
            <input type="range" id="opt-i" min="0" max="85" value="35" step="1">
          </div>
        </div>
        <div class="sim-telemetry">
          <div class="sim-metric"><div class="metric-label">Critical Angle ($\\theta_c = \\sin^{-1}(n_2/n_1)$)</div><div class="metric-val" id="opt-ic">41.81°</div></div>
          <div class="sim-metric"><div class="metric-label">Refraction Angle ($r$)</div><div class="metric-val" id="opt-r">59.37°</div></div>
          <div class="sim-metric"><div class="metric-label">Phenomenon</div><div class="metric-val" id="opt-state" style="color: #059669;">Refraction</div></div>
        </div>
      </div>
    `;

    const canvasBox = container.querySelector('.sim-canvas-box');
    const { canvas, ctx, width, height } = setupCanvas(canvasBox);
    canvasBox.appendChild(canvas);

    let n1 = 1.50, n2 = 1.00, degI = 35;
    const n1Input = container.querySelector('#opt-n1');
    const n2Input = container.querySelector('#opt-n2');
    const iInput = container.querySelector('#opt-i');
    const n1Val = container.querySelector('#opt-n1-val');
    const n2Val = container.querySelector('#opt-n2-val');
    const iVal = container.querySelector('#opt-i-val');
    const icVal = container.querySelector('#opt-ic');
    const rVal = container.querySelector('#opt-r');
    const stateVal = container.querySelector('#opt-state');

    function updateSnell() {
      const radI = (degI * Math.PI) / 180;
      let hasTIR = false;
      let critDeg = null;

      if (n1 > n2) {
        critDeg = (Math.asin(n2 / n1) * 180) / Math.PI;
        icVal.textContent = critDeg.toFixed(2) + '°';
        if (degI > critDeg) hasTIR = true;
      } else {
        icVal.textContent = 'None (n1 ≤ n2)';
      }

      if (hasTIR) {
        rVal.textContent = 'Total Reflection (i = r)';
        stateVal.textContent = '⚡ Total Internal Reflection (TIR)';
        stateVal.style.color = '#dc2626';
      } else {
        const sinR = (n1 * Math.sin(radI)) / n2;
        const radR = Math.asin(Math.min(1.0, sinR));
        const degR = (radR * 180) / Math.PI;
        rVal.textContent = degR.toFixed(2) + '°';
        stateVal.textContent = 'Refraction (Snell\'s Law)';
        stateVal.style.color = '#059669';
      }
    }

    n1Input.oninput = () => { n1 = parseFloat(n1Input.value); n1Val.textContent = n1.toFixed(2); updateSnell(); };
    n2Input.oninput = () => { n2 = parseFloat(n2Input.value); n2Val.textContent = n2.toFixed(2); updateSnell(); };
    iInput.oninput = () => { degI = parseFloat(iInput.value); iVal.textContent = degI; updateSnell(); };
    updateSnell();

    function render() {
      ctx.fillStyle = '#fdfbf7';
      ctx.fillRect(0, 0, width, height);

      const midY = height / 2;
      const midX = width / 2;

      // Medium 1 (Bottom)
      ctx.fillStyle = '#e0f2fe';
      ctx.fillRect(0, midY, width, height - midY);

      // Interface line
      ctx.strokeStyle = '#0284c7';
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.moveTo(0, midY);
      ctx.lineTo(width, midY);
      ctx.stroke();

      // Normal line (dashed)
      ctx.setLineDash([4, 4]);
      ctx.strokeStyle = '#64748b';
      ctx.beginPath();
      ctx.moveTo(midX, 20);
      ctx.lineTo(midX, height - 20);
      ctx.stroke();
      ctx.setLineDash([]);

      ctx.fillStyle = '#475569';
      ctx.font = '13px Kalam, sans-serif';
      ctx.fillText(`Medium 2 (n = ${n2.toFixed(2)})`, 30, 40);
      ctx.fillText(`Medium 1 (n = ${n1.toFixed(2)})`, 30, midY + 40);

      // Incident ray from Medium 1 (bottom left upwards to interface)
      const radI = (degI * Math.PI) / 180;
      const rayLen = 130;
      const incStartX = midX - rayLen * Math.sin(radI);
      const incStartY = midY + rayLen * Math.cos(radI);

      ctx.strokeStyle = '#dc2626';
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(incStartX, incStartY);
      ctx.lineTo(midX, midY);
      ctx.stroke();

      // Check TIR
      let hasTIR = false;
      if (n1 > n2) {
        const crit = Math.asin(n2 / n1);
        if (radI > crit) hasTIR = true;
      }

      if (hasTIR) {
        // Reflected ray back into Medium 1
        const refEndX = midX + rayLen * Math.sin(radI);
        const refEndY = midY + rayLen * Math.cos(radI);
        ctx.strokeStyle = '#dc2626';
        ctx.beginPath();
        ctx.moveTo(midX, midY);
        ctx.lineTo(refEndX, refEndY);
        ctx.stroke();
      } else {
        // Refracted ray into Medium 2
        const sinR = (n1 * Math.sin(radI)) / n2;
        const radR = Math.asin(Math.min(1.0, sinR));
        const refEndX = midX + rayLen * Math.sin(radR);
        const refEndY = midY - rayLen * Math.cos(radR);
        ctx.strokeStyle = '#16a34a';
        ctx.beginPath();
        ctx.moveTo(midX, midY);
        ctx.lineTo(refEndX, refEndY);
        ctx.stroke();

        // Partial weak reflection
        const partEndX = midX + rayLen * Math.sin(radI);
        const partEndY = midY + rayLen * Math.cos(radI);
        ctx.strokeStyle = 'rgba(220, 38, 38, 0.35)';
        ctx.beginPath();
        ctx.moveTo(midX, midY);
        ctx.lineTo(partEndX, partEndY);
        ctx.stroke();
      }

      requestAnimationFrame(render);
    }

    render();
  }

  /* =========================================================================
   * 8. BOHR ATOM & QUANTIZED SPECTRAL TRANSITIONS
   * ========================================================================= */
  function initBohrSim(container) {
    container.innerHTML = `
      <div class="sim-wrapper">
        <div class="sim-header">
          <div class="sim-title">⚛️ Bohr Atom &amp; Hydrogen Spectral Transitions</div>
          <div class="sim-status">Atoms &amp; Nuclei (NCERT Class 12 Ch 10)</div>
        </div>
        <div class="sim-canvas-box"></div>
        <div class="sim-controls">
          <div class="sim-control-group">
            <label>Initial Orbit ($n_i$): <span id="bohr-ni-val">3</span></label>
            <input type="range" id="bohr-ni" min="2" max="5" value="3" step="1">
          </div>
          <div class="sim-control-group">
            <label>Final Orbit ($n_f$): <span id="bohr-nf-val">2</span> (Balmer Series)</label>
            <input type="range" id="bohr-nf" min="1" max="4" value="2" step="1">
          </div>
          <div class="sim-btn-group">
            <button class="sim-btn" id="bohr-emit">🌟 Trigger Photon Transition</button>
          </div>
        </div>
        <div class="sim-telemetry">
          <div class="sim-metric"><div class="metric-label">Energy Emitted ($\\Delta E$)</div><div class="metric-val" id="bohr-de">1.89 eV</div></div>
          <div class="sim-metric"><div class="metric-label">Wavelength ($\\lambda = \\frac{hc}{\\Delta E}$)</div><div class="metric-val" id="bohr-wave">656.3 nm (H-alpha Red)</div></div>
          <div class="sim-metric"><div class="metric-label">Spectral Series</div><div class="metric-val" id="bohr-series" style="color: #dc2626;">Balmer Series (Visible)</div></div>
        </div>
      </div>
    `;

    const canvasBox = container.querySelector('.sim-canvas-box');
    const { canvas, ctx, width, height } = setupCanvas(canvasBox);
    canvasBox.appendChild(canvas);

    let ni = 3, nf = 2;
    const niInput = container.querySelector('#bohr-ni');
    const nfInput = container.querySelector('#bohr-nf');
    const niVal = container.querySelector('#bohr-ni-val');
    const nfVal = container.querySelector('#bohr-nf-val');
    const deVal = container.querySelector('#bohr-de');
    const waveVal = container.querySelector('#bohr-wave');
    const seriesVal = container.querySelector('#bohr-series');

    function updateBohr() {
      if (ni <= nf) {
        ni = nf + 1;
        niInput.value = ni;
        niVal.textContent = ni;
      }

      const Ei = -13.6 / (ni * ni);
      const Ef = -13.6 / (nf * nf);
      const deltaE = Ef - Ei; // positive for emitted photon
      const lambdaNm = 1240 / deltaE;

      deVal.textContent = deltaE.toFixed(2) + ' eV';
      waveVal.textContent = lambdaNm.toFixed(1) + ' nm';

      let seriesName = 'Higher Series (Infrared)';
      let color = '#7c3aed';
      if (nf === 1) {
        seriesName = 'Lyman Series (Ultraviolet)';
        color = '#2563eb';
      } else if (nf === 2) {
        seriesName = 'Balmer Series (Visible Light 🌈)';
        color = '#dc2626';
      } else if (nf === 3) {
        seriesName = 'Paschen Series (Infrared)';
        color = '#d97706';
      }
      seriesVal.textContent = seriesName;
      seriesVal.style.color = color;
    }

    niInput.oninput = () => { ni = parseInt(niInput.value); niVal.textContent = ni; updateBohr(); };
    nfInput.oninput = () => { nf = parseInt(nfInput.value); nfVal.textContent = nf; updateBohr(); };
    updateBohr();

    let electronAngle = 0;
    let photonWave = null;

    container.querySelector('#bohr-emit').onclick = () => {
      photonWave = { x: width / 2, y: height / 2, phase: 0 };
      if (window.NotebookAnimations && typeof window.NotebookAnimations.spawnConfetti === 'function') {
        window.NotebookAnimations.spawnConfetti(width / 2, height / 2);
      }
    };

    function render() {
      ctx.fillStyle = '#fdfbf7';
      ctx.fillRect(0, 0, width, height);

      const midX = width / 2;
      const midY = height / 2;

      // Draw Nucleus
      ctx.beginPath();
      ctx.arc(midX, midY, 12, 0, Math.PI * 2);
      ctx.fillStyle = '#dc2626';
      ctx.fill();
      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 11px sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText('+Ze', midX, midY);

      // Draw Quantized Orbits (n = 1, 2, 3, 4, 5)
      const orbitRadii = [0, 32, 60, 92, 125, 155];
      for (let n = 1; n <= 5; n++) {
        ctx.strokeStyle = n === nf ? '#16a34a' : (n === ni ? '#2563eb' : '#cbd5e1');
        ctx.lineWidth = (n === nf || n === ni) ? 2 : 1;
        ctx.setLineDash([3, 3]);
        ctx.beginPath();
        ctx.arc(midX, midY, orbitRadii[n], 0, Math.PI * 2);
        ctx.stroke();
        ctx.setLineDash([]);

        ctx.fillStyle = '#64748b';
        ctx.font = '11px Kalam, sans-serif';
        ctx.fillText(`n=${n}`, midX + orbitRadii[n] + 4, midY - 6);
      }

      // Draw orbiting electron on ni or transition
      const curR = orbitRadii[ni];
      const ex = midX + curR * Math.cos(electronAngle);
      const ey = midY + curR * Math.sin(electronAngle);

      ctx.beginPath();
      ctx.arc(ex, ey, 6, 0, Math.PI * 2);
      ctx.fillStyle = '#2563eb';
      ctx.fill();

      // Draw outgoing photon wave packet if triggered
      if (photonWave) {
        photonWave.x += 4;
        ctx.strokeStyle = '#e11d48';
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        for (let i = 0; i < 30; i++) {
          const wx = photonWave.x - i * 2;
          const wy = midY + Math.sin(i * 0.6 + photonWave.phase) * 12;
          if (i === 0) ctx.moveTo(wx, wy);
          else ctx.lineTo(wx, wy);
        }
        ctx.stroke();
        photonWave.phase += 0.4;
        if (photonWave.x > width + 40) photonWave = null;
      }

      electronAngle += 0.03;
      requestAnimationFrame(render);
    }

    render();
  }

  /* =========================================================================
   * SIMULATION METADATA & POP-UP MODAL WINDOW SYSTEM
   * ========================================================================= */
  const SIMULATION_DETAILS = {
    'projectile': {
      title: '🎯 2D Projectile Trajectory & Kinematics Laboratory',
      domain: 'Kinematics (Class 11 Ch 3 & 4)'
    },
    'incline': {
      title: '📐 Inclined Plane Dynamics & Vector Free Body Diagram (FBD)',
      domain: 'Laws of Motion (Class 11 Ch 4)'
    },
    'spring': {
      title: '🌀 Harmonic Oscillator & Mechanical Energy Distribution',
      domain: 'Oscillations & Waves (Class 11 Ch 13 & 14)'
    },
    'coulomb': {
      title: '⚡ Coulomb Force Vectors & Electrostatic Field Simulation',
      domain: 'Electrostatics (Class 12 Ch 1)'
    },
    'circuits': {
      title: '💡 Ohm\'s Law & Microscopic Electron Drift Velocity',
      domain: 'Current Electricity (Class 12 Ch 2)'
    },
    'lorentz': {
      title: '🧲 Magnetic Lorentz Force & Helical Cyclotron Orbit',
      domain: 'Moving Charges & Magnetism (Class 12 Ch 3)'
    },
    'optics': {
      title: '🔍 Snell\'s Law Refraction & Total Internal Reflection (TIR)',
      domain: 'Ray & Wave Optics (Class 12 Ch 7 & 8)'
    },
    'bohr': {
      title: '⚛️ Bohr Quantized Atomic Transitions & Spectral Emission',
      domain: 'Atoms & Nuclei (Class 12 Ch 10)'
    }
  };

  function launchSimulationModal(simType) {
    if (!simType) return;
    const overlay = document.getElementById('simulationModalOverlay');
    const modalBody = document.getElementById('simModalBody');
    const titleElem = document.getElementById('simModalTitleText');
    const badgeElem = document.getElementById('simModalDomainBadge');

    if (!overlay || !modalBody) return;

    const details = SIMULATION_DETAILS[simType] || {
      title: '🔬 Interactive Physics Laboratory',
      domain: 'Physics Experiment'
    };

    if (titleElem) titleElem.textContent = details.title;
    if (badgeElem) badgeElem.textContent = details.domain;

    modalBody.innerHTML = `<div class="physics-sim-container" data-sim="${simType}"></div>`;
    overlay.style.display = 'flex';
    setTimeout(() => {
      overlay.classList.add('open');
      document.body.style.overflow = 'hidden';

      const container = modalBody.querySelector('.physics-sim-container');
      if (container) {
        initSingleSimulation(container, simType);
      }
    }, 40);
  }

  function closeSimulationModal() {
    const overlay = document.getElementById('simulationModalOverlay');
    const modalBody = document.getElementById('simModalBody');
    if (!overlay) return;

    overlay.classList.remove('open');
    setTimeout(() => {
      overlay.style.display = 'none';
      if (modalBody) modalBody.innerHTML = '';
      document.body.style.overflow = '';
    }, 200);
  }

  function initSingleSimulation(container, simType) {
    switch (simType) {
      case 'projectile':
        initProjectileSim(container);
        break;
      case 'incline':
        initInclineSim(container);
        break;
      case 'spring':
        initSpringSim(container);
        break;
      case 'coulomb':
        initCoulombSim(container);
        break;
      case 'circuits':
        initCircuitsSim(container);
        break;
      case 'lorentz':
        initLorentzSim(container);
        break;
      case 'optics':
        initOpticsSim(container);
        break;
      case 'bohr':
        initBohrSim(container);
        break;
    }
  }

  /* =========================================================================
   * EVENT BINDINGS & DISPATCHER
   * ========================================================================= */
  function setupSimulationModalEvents() {
    const overlay = document.getElementById('simulationModalOverlay');
    const closeBtn = document.getElementById('closeSimModalBtn');

    if (closeBtn) {
      closeBtn.addEventListener('click', closeSimulationModal);
    }

    if (overlay) {
      overlay.addEventListener('click', (e) => {
        if (e.target === overlay) {
          closeSimulationModal();
        }
      });
    }

    window.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        const overlay = document.getElementById('simulationModalOverlay');
        if (overlay && overlay.classList.contains('open')) {
          closeSimulationModal();
        }
      }
    });

    // Delegate click on launch buttons
    document.addEventListener('click', (e) => {
      const btn = e.target.closest('[data-launch-sim]');
      if (btn) {
        e.preventDefault();
        const simType = btn.getAttribute('data-launch-sim');
        if (simType) {
          launchSimulationModal(simType);
        }
      }
    });
  }

  function initAllSimulations() {
    setupSimulationModalEvents();

    // Also initialize any inline containers if present
    document.querySelectorAll('.physics-sim-container').forEach(container => {
      const simType = container.getAttribute('data-sim');
      if (!simType || container.hasAttribute('data-initialized') || container.closest('#simModalBody')) return;
      container.setAttribute('data-initialized', 'true');
      initSingleSimulation(container, simType);
    });
  }

  document.addEventListener('DOMContentLoaded', initAllSimulations);
  window.launchSimulationModal = launchSimulationModal;
  window.closeSimulationModal = closeSimulationModal;
  window.initAllSimulations = initAllSimulations;
})();

