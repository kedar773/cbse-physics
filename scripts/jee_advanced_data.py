# -*- coding: utf-8 -*-
"""
CBSE Physics Notebook - JEE Main & Advanced / NEET Extension Data Bank
Provides rigorous, deep competitive physics modules strictly segregated from CBSE Board syllabus.
Contains authentic derivations, non-inertial frame methods, calculus lemmas, speed-hacks,
and worked competitive problem paradigms for all 25 chapters.
"""

JEE_ADVISORY_BANNER_HTML = """
<div class="sticky-note purple" style="margin-bottom: 2rem; border-left: 6px solid #7c3aed;">
  <div class="sticky-title" style="font-size: 1.35rem; color: #581c87; display:flex; align-items:center; gap:0.5rem;">
    <span>🚀</span> Advanced Studies: JEE Main • JEE Advanced • NEET Competitive Extension
  </div>
  <div style="font-size: 1.05rem; line-height: 1.6; color: #3b0764; margin-top: 0.5rem;">
    <strong>📌 Strict Curriculum Segregation Notice:</strong><br>
    The concepts, non-inertial techniques, advanced calculus formulations, and shortcut speed-hacks presented in this tab
    fall <strong>outside the standard CBSE Class 11/12 Board Exam syllabus</strong>. They are curated specifically for students targeting
    <strong>JEE Main, JEE Advanced, NEET, and Olympiads</strong>.
    <br><br>
    <span style="display:inline-block; background: #ede9fe; padding: 0.3rem 0.8rem; border-radius: 8px; font-weight: bold; color: #6b21a8;">
      🛡️ CBSE Board Peace-of-Mind: Students focusing solely on 95%+ in Board Examinations can completely skip this tab without missing any board questions.
    </span>
  </div>
</div>
"""

JEE_ADVANCED_MODULES = {
    # =========================================================================
    # CLASS 11 CHAPTERS
    # =========================================================================
    "01-units-and-measurements": [
        {
            "title": "Vernier & Screw Gauge Precision Error Analysis, Backlash & Least Count",
            "scope": "JEE Advanced & JEE Main Experimental Physics",
            "content": """
### 1. Advanced Least Count of Measuring Instruments
In modern JEE Advanced experimental questions, division matching is rarely standard 1:1.
* **General Vernier Principle:**
  If $n$ divisions of the Vernier Scale ($VSD$) coincide with $m$ divisions of the Main Scale ($MSD$):
  $$n \\cdot VSD = m \\cdot MSD \\implies VSD = \\frac{m}{n} MSD$$
  $$\\text{Least Count (LC)} = 1 MSD - 1 VSD = \\left(1 - \\frac{m}{n}\\right) MSD$$
* **Screw Gauge (Micrometer) & Backlash Error:**
  $$\\text{Least Count} = \\frac{\\text{Pitch}}{\\text{Total Circular Scale Divisions (CSD)}}$$
  * *Backlash Error:* Arises due to mechanical wear and tear of screw threads. Corrected by advancing the screw strictly in one continuous direction during measurement.
  * *Zero Error Correction:*
    $$\\text{True Reading} = \\text{Observed Reading} - (\\pm \\text{Zero Error})$$

### 2. Logarithmic Fractional Error for Power Towers
For arbitrary physical laws $Z = \\frac{A^p B^q}{C^r D^s}$:
$$\\ln Z = p\\ln A + q\\ln B - r\\ln C - s\\ln D$$
Taking differentials and maximizing for worst-case cumulative experimental uncertainty:
$$\\left(\\frac{\\Delta Z}{Z}\\right)_{\\max} = p\\left|\\frac{\\Delta A}{A}\\right| + q\\left|\\frac{\\Delta B}{B}\\right| + r\\left|\\frac{\\Delta C}{C}\\right| + s\\left|\\frac{\\Delta D}{D}\\right|$$
            """,
            "speed_hack": "When $Z = f(x, y)$, if partial derivatives are easily computable, use total differential: $\\Delta Z = \\left|\\frac{\\partial f}{\\partial x}\\right|\\Delta x + \\left|\\frac{\\partial f}{\\partial y}\\right|\\Delta y$. This handles trigonometric and transcendental arguments like $\\theta$ and $e^x$ seamlessly.",
            "example_q": "A Vernier caliper has $1 MSD = 0.5\\text{ mm}$ and $20 VSD = 16 MSD$. When the jaws meet, the 0 of VSD lies to the right of 0 of MSD, with the 4th VSD coinciding with an MSD. Find the zero error.",
            "example_sol": "$LC = 1 MSD - \\frac{16}{20} MSD = 0.2 \\times 0.5\\text{ mm} = 0.10\\text{ mm}$. Since 0 of VSD is to the right, zero error is positive: $+4 \\times LC = +4 \\times 0.10\\text{ mm} = +0.40\\text{ mm}$."
        },
        {
            "title": "Dimensional Transformations & Fundamental Unit Systems (Planck Units)",
            "scope": "JEE Advanced Dimensional Invariance",
            "content": """
### Dimensional Re-scaling in Alternative Universes
JEE Advanced frequently tests expressing conventional mechanical quantities ($M, L, T$) in terms of fundamental constants: speed of light $c$, universal gravitational constant $G$, and reduced Planck constant $\\hbar$.
* Setting $M = c^a G^b \\hbar^c$:
  $$[M] = [LT^{-1}]^a [M^{-1}L^3T^{-2}]^b [ML^2T^{-1}]^c$$
  Matching dimensional exponents yields the **Planck Mass**:
  $$M_P = \\sqrt{\\frac{\\hbar c}{G}} \\approx 2.176 \\times 10^{-8}\\text{ kg}$$
  **Planck Length:** $L_P = \\sqrt{\\frac{\\hbar G}{c^3}} \\approx 1.616 \\times 10^{-35}\\text{ m}$; **Planck Time:** $t_P = \\sqrt{\\frac{\\hbar G}{c^5}} \\approx 5.391 \\times 10^{-44}\\text{ s}$.
            """,
            "speed_hack": "To quickly convert electromagnetic combinations to dimensions: recall $\\frac{E}{B} = [LT^{-1}]$ (velocity), $\\sqrt{\\frac{L}{C}} = [\\Omega]$ (impedance), $RC = [T]$ (time constant), and $\\frac{1}{\\sqrt{\\mu_0 \\varepsilon_0}} = c = [LT^{-1}]$.",
            "example_q": "Find the dimensional formula of electrical resistance in a system where Mass ($M$), Length ($L$), Time ($T$), and Charge ($Q$) are base dimensions.",
            "example_sol": "Power $P = I^2 R \\implies R = \\frac{P}{I^2} = \\frac{W/t}{(Q/t)^2} = \\frac{[M L^2 T^{-3}]}{[Q^2 T^{-2}]} = [M L^2 T^{-1} Q^{-2}]$."
        }
    ],

    "02-motion-in-a-straight-line": [
        {
            "title": "Calculus Kinematics with Velocity-Dependent Acceleration & Drag Forces",
            "scope": "JEE Advanced Differential Kinematics",
            "content": """
### Non-Uniform Acceleration $a = f(v)$ or $a = f(x)$
When acceleration depends continuously on velocity (such as fluid viscous drag $a = -kv$ or aerodynamic drag $a = -kv^2$):
1. **Time-Velocity Relation:**
   $$a = \\frac{dv}{dt} = f(v) \\implies t = \\int_{v_0}^{v} \\frac{dv'}{f(v')}$$
2. **Position-Velocity Relation:**
   $$a = v\\frac{dv}{dx} = f(v) \\implies x = \\int_{v_0}^{v} \\frac{v'\\,dv'}{f(v')}$$
* **Linear Viscous Deceleration ($a = -kv$):**
  $$v(t) = v_0 e^{-kt}, \\quad x_{\\max} = \\lim_{t \\to \\infty} \\int_0^t v_0 e^{-kt'}dt' = \\frac{v_0}{k}$$
  Notice that while the particle technically takes infinite time to halt ($t \\to \\infty$), its total stopping distance is strictly finite!
            """,
            "speed_hack": "Graph Curvature Theorem: For an $x-t$ curve, concavity indicates the sign of acceleration: concave upward ($\\frac{d^2x}{dt^2} > 0$) means $a > 0$; concave downward ($\\frac{d^2x}{dt^2} < 0$) means $a < 0$. Inflection points occur precisely when $a = 0$.",
            "example_q": "A particle moves along the $x$-axis with deceleration $a = -k\\sqrt{v}$. If initial velocity is $v_0$, find the total distance traversed before coming to rest.",
            "example_sol": "$v\\frac{dv}{dx} = -k\\sqrt{v} \\implies \\sqrt{v}\\,dv = -k\\,dx$. Integrating from $v_0$ to 0: $\\int_{v_0}^0 v^{1/2}dv = -kx_{\\max} \\implies \\frac{2}{3}v_0^{3/2} = k x_{\\max} \\implies x_{\\max} = \\frac{2 v_0^{3/2}}{3k}$."
        }
    ],

    "03-motion-in-a-plane": [
        {
            "title": "Projectile on an Inclined Plane & Radius of Curvature Analysis",
            "scope": "JEE Advanced Trajectory Analysis",
            "content": """
### 1. Motion on an Incline (Angle of Incline $\\beta$, Projection Angle $\\alpha$ with Incline)
Rotate the coordinate frame such that the $X$-axis lies parallel to the inclined plane and $Y$-axis is perpendicular:
* Accelerations: $a_x = -g\\sin\\beta$, $a_y = -g\\cos\\beta$.
* Initial velocities: $u_x = u\\cos\\alpha$, $u_y = u\\sin\\alpha$.
* **Time of Flight:** Setting $y = 0 \\implies T = \\frac{2 u_y}{|a_y|} = \\frac{2u\\sin\\alpha}{g\\cos\\beta}$.
* **Range Up the Incline ($R_{\\text{up}}$):**
  $$R_{\\text{up}} = u_x T + \\frac{1}{2}a_x T^2 = \\frac{u^2}{g\\cos^2\\beta}\\left[\\sin(2\\alpha + \\beta) - \\sin\\beta\\right]$$
  *Maximum Range condition:* $\\alpha = \\frac{\\pi}{4} - \\frac{\\beta}{2} \\implies R_{\\max} = \\frac{u^2}{g(1 + \\sin\\beta)}$.
* **Range Down the Incline ($R_{\\text{down}}$):**
  $$R_{\\text{down}} = \\frac{u^2}{g(1 - \\sin\\beta)} \\quad \\text{at } \\alpha = \\frac{\\pi}{4} + \\frac{\\beta}{2}$$

### 2. Radius of Curvature ($\\rho$) of Trajectories
The radius of curvature of any arbitrary path where speed is $v$ and normal acceleration is $a_\\perp$:
$$\\rho = \\frac{v^2}{a_\\perp}$$
At the apex of a ground-to-ground parabolic trajectory: $v = u\\cos\\theta$ and $a_\\perp = g$:
$$\\rho_{\\text{apex}} = \\frac{u^2 \\cos^2\\theta}{g}$$
            """,
            "speed_hack": "Condition for projectile to strike the inclined plane perpendicularly: at impact, $v_x = 0 \\implies u\\cos\\alpha - (g\\sin\\beta)T = 0$. Substituting $T = \\frac{2u\\sin\\alpha}{g\\cos\\beta}$ gives the famous JEE relation: $\\tan\\alpha = \\frac{1}{2}\\cot\\beta$.",
            "example_q": "A ball is launched from the bottom of an incline of slope $\\beta = 30^\\circ$ at speed $u = 20\\text{ m/s}$. Find the angle of projection $\\alpha$ relative to the incline that maximizes the range up the plane.",
            "example_sol": "$\\alpha_{\\max} = \\frac{\\pi}{4} - \\frac{\\beta}{2} = 45^\\circ - 15^\\circ = 30^\\circ$ relative to the incline (or $60^\\circ$ to horizontal). Maximum range $R_{\\max} = \\frac{u^2}{g(1 + \\sin 30^\\circ)} = \\frac{400}{9.8(1.5)} \\approx 27.2\\text{ m}$."
        }
    ],

    "04-laws-of-motion": [
        {
            "title": "Non-Inertial Reference Frames, Pseudo-Forces & Variable Mass Systems",
            "scope": "JEE Advanced Classical Dynamics",
            "content": """
### 1. Pseudo-Forces in Accelerated & Rotating Frames
In a non-inertial reference frame translating with acceleration $\\vec{a}_0$:
$$\\vec{F}_{\\text{net, apparent}} = \\vec{F}_{\\text{real}} + \\vec{F}_{\\text{pseudo}}, \\quad \\text{where } \\vec{F}_{\\text{pseudo}} = -m\\vec{a}_0$$
* *Centrifugal Force:* For a frame rotating with angular velocity $\\vec{\\omega}$: $\\vec{F}_{\\text{cf}} = m\\omega^2 \\vec{r}_{\\perp}$.
* *Coriolis Force (JEE Advanced Extension):* $\\vec{F}_{\\text{coriolis}} = -2m(\\vec{\\omega} \\times \\vec{v}_{\\text{rel}})$.

### 2. Variable Mass Systems (Tsiolkovsky Rocket Equation)
For a system whose mass changes at rate $\\frac{dm}{dt}$ with exhaust relative velocity $\\vec{u}_{\\text{rel}}$:
$$\\vec{F}_{\\text{ext}} + \\vec{v}_{\\text{rel}}\\frac{dm}{dt} = m\\frac{d\\vec{v}}{dt}$$
For a vertical rocket escaping in uniform gravity $g$:
$$v(t) = v_0 + u_{\\text{rel}}\\ln\\left(\\frac{m_0}{m(t)}\\right) - gt$$
Thrust force exerted on the vehicle: $F_{\\text{thrust}} = u_{\\text{rel}}\\left(-\\frac{dm}{dt}\\right)$.

### 3. Two-Block Friction & Wedges
When block $A$ sits on block $B$ atop a smooth floor:
$$\\text{Maximum possible acceleration of upper block without slip: } a_{\\max} = \\mu_s g$$
The threshold force applied to the bottom block to induce relative sliding is $F_{\\text{threshold}} = (m_A + m_B)\\mu_s g$.
            """,
            "speed_hack": "String Constraint Shortcut: For any ideal inextensible string-pulley network, $\\sum T_i \\cdot a_i = 0$ (or $\\sum \\vec{T}\\cdot\\vec{a} = 0$). This eliminates the tedious need to write coordinate length equations!",
            "example_q": "A rocket of initial mass $m_0 = 1000\\text{ kg}$ ejects gas at constant speed $u_{\\text{rel}} = 2000\\text{ m/s}$ at rate $r = 10\\text{ kg/s}$. Neglecting gravity, find the velocity after 50 seconds.",
            "example_sol": "$m(50) = 1000 - 10(50) = 500\\text{ kg}$. $v = 2000 \\ln\\left(\\frac{1000}{500}\\right) = 2000 \\ln 2 \\approx 2000 \\times 0.693 = 1386\\text{ m/s}$."
        }
    ],

    "05-work-energy-and-power": [
        {
            "title": "Potential Energy Curves $U(x)$, Equilibrium Stability & Oblique Collisions",
            "scope": "JEE Advanced Mechanical Conservation Laws",
            "content": """
### 1. Potential Energy Curves $U(x)$ & Stability Criteria
For conservative systems, force is the negative gradient of potential energy: $F(x) = -\\frac{dU}{dx}$.
* **Equilibrium condition:** $F(x_0) = 0 \\iff \\left.\\frac{dU}{dx}\\right|_{x_0} = 0$.
* **Stability Classification:**
  1. *Stable Equilibrium:* Local minimum of $U(x) \\implies \\left.\\frac{d^2U}{dx^2}\\right|_{x_0} > 0$. Small displacements generate restoring SHM with $\\omega = \\sqrt{\\frac{U''(x_0)}{m}}$.
  2. *Unstable Equilibrium:* Local maximum of $U(x) \\implies \\left.\\frac{d^2U}{dx^2}\\right|_{x_0} < 0$. Small perturbations accelerate the particle away.
  3. *Neutral Equilibrium:* $\\left.\\frac{d^2U}{dx^2}\\right|_{x_0} = 0$.

### 2. General 2D Oblique Inelastic Collisions
* Conserve linear momentum along both collision tangent (no impulse) and normal axis (impulsive).
* Coefficient of Restitution $e$ applies strictly along the common normal:
  $$e = -\\frac{v_{2n} - v_{1n}}{u_{2n} - u_{1n}}$$
* Energy loss in 1D collision:
  $$\\Delta E_{\\text{loss}} = \\frac{1}{2}\\frac{m_1 m_2}{m_1 + m_2}(1 - e^2)(u_1 - u_2)^2$$
            """,
            "speed_hack": "Reduced Mass Center-of-Mass Frame: When analyzing collisions or spring-mass systems, transform to the COM frame: $\\mu = \\frac{m_1 m_2}{m_1 + m_2}$. The relative kinetic energy is simply $K_{\\text{rel}} = \\frac{1}{2}\\mu v_{\\text{rel}}^2$.",
            "example_q": "The potential energy of a particle is $U(x) = \\frac{a}{x^2} - \\frac{b}{x}$ with $a, b > 0$. Find the stable equilibrium position and oscillation frequency for small oscillations.",
            "example_sol": "$U'(x) = -\\frac{2a}{x^3} + \\frac{b}{x^2} = 0 \\implies x_0 = \\frac{2a}{b}$. $U''(x_0) = \\frac{6a}{x_0^4} - \\frac{2b}{x_0^3} = \\frac{b^4}{8a^3} > 0$ (stable). Frequency $\\omega = \\sqrt{\\frac{U''(x_0)}{m}} = \\sqrt{\\frac{b^4}{8 m a^3}}$."
        }
    ],

    "06-system-of-particles-and-rotational-motion": [
        {
            "title": "Instantaneous Center of Rotation (ICOR) & Accelerated Rolling with Friction",
            "scope": "JEE Advanced Rotational Dynamics",
            "content": """
### 1. Instantaneous Center of Zero Velocity (ICOR)
In general planar rigid motion, there always exists a point $I$ in space that has instantaneous velocity $\\vec{v}_I = 0$.
* The entire motion of the rigid body can be treated as pure rotation about this instantaneous axis:
  $$\\vec{v}_P = \\vec{\\omega} \\times \\vec{r}_{P/I}$$
* *Locating ICOR:* Draw perpendicular lines to velocity vectors of any two points on the body; the intersection point is the ICOR.
* Kinetic energy about ICOR: $K = \\frac{1}{2}I_{\\text{ICOR}} \\omega^2$.

### 2. Accelerated Pure Rolling on Incline (Slope $\\theta$)
For a body of mass $m$, radius $R$, and radius of gyration $k$ ($I_{\\text{cm}} = m k^2$):
$$a_{\\text{cm}} = \\frac{g\\sin\\theta}{1 + \\frac{k^2}{R^2}}, \\quad f_s = \\frac{mg\\sin\\theta}{1 + \\frac{R^2}{k^2}}$$
* *Condition for pure rolling without slipping:* $f_s \\le \\mu_s N = \\mu_s mg\\cos\\theta$:
  $$\\mu_s \\ge \\frac{\\tan\\theta}{1 + \\frac{R^2}{k^2}}$$
* For Sphere ($k^2/R^2 = 2/5$): $a = \\frac{5}{7}g\\sin\\theta$; $\\mu_{\\min} = \\frac{2}{7}\\tan\\theta$.
* For Cylinder ($k^2/R^2 = 1/2$): $a = \\frac{2}{3}g\\sin\\theta$; $\\mu_{\\min} = \\frac{1}{3}\\tan\\theta$.
            """,
            "speed_hack": "Toppling vs Sliding: A block of height $h$ and width $b$ on a rough plane of inclination $\\theta$ will slide before toppling if $\\mu < \\frac{b}{h}$, and will topple before sliding if $\\mu > \\frac{b}{h}$. Critical angle for toppling is $\\tan\\theta_c = \\frac{b}{h}$.",
            "example_q": "A solid sphere and a hollow sphere of identical masses and radii are released from rest on a rough incline. Which body reaches the bottom first and why?",
            "example_sol": "$a_{\\text{cm}} = \\frac{g\\sin\\theta}{1 + k^2/R^2}$. For solid sphere, $k^2/R^2 = 0.4 \\implies a = \\frac{5}{7}g\\sin\\theta \\approx 0.71g\\sin\\theta$. For hollow sphere, $k^2/R^2 = 2/3 \\approx 0.67 \\implies a = \\frac{3}{5}g\\sin\\theta = 0.60g\\sin\\theta$. Solid sphere has higher acceleration, thus arrives first."
        }
    ],

    "07-gravitation": [
        {
            "title": "Gravitational Self-Energy, Tidal Forces & Hohmann Orbital Transfers",
            "scope": "JEE Advanced Celestial Mechanics",
            "content": """
### 1. Gravitational Self-Energy of Mass Distributions
The work done in assembling a celestial mass distribution from infinite dispersion:
* **Uniform Solid Sphere of Mass $M$ and Radius $R$:**
  $$U_{\\text{self}} = -\\int_0^R \\frac{G m(r)}{r} dm = -\\frac{3}{5}\\frac{GM^2}{R}$$
* **Thin Spherical Shell:**
  $$U_{\\text{self}} = -\\frac{1}{2}\\frac{GM^2}{R}$$

### 2. Elliptic Orbit Dynamics & Kepler's Equation
* Total energy in elliptic orbit with semi-major axis $a$:
  $$E = -\\frac{GMm}{2a}$$
* Speed at any distance $r$ (Vis-Viva Equation):
  $$v^2 = GM\\left(\\frac{2}{r} - \\frac{1}{a}\\right)$$
  * Perihelion speed ($r_p = a(1-e)$): $v_p = \\sqrt{\\frac{GM}{a}\\frac{1+e}{1-e}}$.
  * Aphelion speed ($r_a = a(1+e)$): $v_a = \\sqrt{\\frac{GM}{a}\\frac{1-e}{1+e}}$.
            """,
            "speed_hack": "Tunnel through non-diametric chord: The period of oscillation of a mass dropped in a frictionless tunnel drilled between any two arbitrary surface points of Earth is invariant: $T = 2\\pi\\sqrt{\\frac{R}{g}} \\approx 84.6\\text{ minutes}$, regardless of whether the tunnel passes through Earth's center!",
            "example_q": "Find the energy required to double the radius of a circular satellite orbit around Earth of mass $M$ from $r$ to $2r$.",
            "example_sol": "$E_i = -\\frac{GMm}{2r}$, $E_f = -\\frac{GMm}{4r}$. $\\Delta E = E_f - E_i = \\frac{GMm}{4r}$."
        }
    ],

    "08-mechanical-properties-of-solids": [
        {
            "title": "Torsion of Cylinders, Beam Deflection & Inter-Moduli Relations",
            "scope": "JEE Advanced Elasticity",
            "content": """
### 1. Torsional Couple of a Solid Cylinder (Wire)
When a solid cylinder of length $l$, radius $r$, and shear modulus $\\eta$ is twisted through angle $\\theta$:
$$\\tau = C\\theta, \\quad \\text{where } C = \\frac{\\pi \\eta r^4}{2l} \\text{ (Torsional Rigidity)}$$
Work done in twisting through angle $\\theta$: $W = \\frac{1}{2}C\\theta^2$.
Time period of a torsional pendulum of moment of inertia $I$:
$$T = 2\\pi\\sqrt{\\frac{I}{C}} = 2\\pi\\sqrt{\\frac{2Il}{\\pi \\eta r^4}}$$

### 2. Inter-Relations between Elastic Moduli ($Y, K, \\eta, \\sigma$)
$$Y = 3K(1 - 2\\sigma) = 2\\eta(1 + \\sigma)$$
$$\\frac{9}{Y} = \\frac{1}{K} + \\frac{3}{\\eta}, \\quad \\sigma = \\frac{3K - 2\\eta}{6K + 2\\eta}$$
*Theoretical limits of Poisson's Ratio:* $-1 \\le \\sigma \\le 0.5$. For actual incompressible solids (rubber): $\\sigma \\approx 0.5$.
            """,
            "speed_hack": "Depression in a horizontally supported beam under central load $W$: $\\delta = \\frac{W L^3}{4 Y b d^3}$ where $b$ is breadth and $d$ is depth. Notice depth $d$ enters to the 3rd power, which is why structural I-beams are engineered tall and thin rather than wide!",
            "example_q": "If Poisson's ratio for a material is $\\sigma = 0.25$, find the ratio of Young's modulus $Y$ to Shear modulus $\\eta$.",
            "example_sol": "$Y = 2\\eta(1 + \\sigma) = 2\\eta(1 + 0.25) = 2.5\\eta \\implies \\frac{Y}{\\eta} = 2.5 = \\frac{5}{2}$."
        }
    ],

    "09-mechanical-properties-of-fluids": [
        {
            "title": "Poiseuille Viscous Pipe Flow & Rotating Fluid Free-Surface Paraboloids",
            "scope": "JEE Advanced Fluid Dynamics",
            "content": """
### 1. Poiseuille's Law of Laminar Viscous Flow
Volume flow rate $Q = \\frac{dV}{dt}$ of a viscous fluid (viscosity $\\eta$) across pipe of radius $r$ and length $l$:
$$Q = \\frac{\\pi \\Delta P r^4}{8\\eta l}$$
* *Hydraulic Resistance Analogy:* $\\Delta P = Q \\cdot R_h$, where $R_h = \\frac{8\\eta l}{\\pi r^4}$.
* Pipes in series: $R_{\\text{eq}} = R_1 + R_2$; Pipes in parallel: $\\frac{1}{R_{\\text{eq}}} = \\frac{1}{R_1} + \\frac{1}{R_2}$.

### 2. Rotating Fluid Vessels
A cylindrical container filled with liquid rotated at constant angular speed $\\omega$ forms a parabolic meniscus:
$$z(r) = \\frac{\\omega^2 r^2}{2g}$$
The center depresses by $h_0 = \\frac{\\omega^2 R^2}{4g}$ and the rim rises by $\\Delta h = \\frac{\\omega^2 R^2}{4g}$ relative to the initial resting level.
            """,
            "speed_hack": "Torricelli Emptying Time: Time required to drain a container of cross-section $A(y)$ with orifice area $a$ from height $H$ to 0: $t = \\int_0^H \\frac{A(y)}{a\\sqrt{2gy}}dy$. For uniform cylinder: $t = \\frac{A}{a}\\sqrt{\\frac{2H}{g}}$.",
            "example_q": "Two capillary tubes of equal lengths but radii $r$ and $2r$ are connected in series. Find the ratio of pressure drop across the first tube to the second tube.",
            "example_sol": "$R_h \\propto \\frac{1}{r^4}$. For series flow, $Q$ is identical $\\implies \\frac{\\Delta P_1}{\\Delta P_2} = \\frac{R_1}{R_2} = \\left(\\frac{2r}{r}\\right)^4 = 16$."
        }
    ],

    "10-thermal-properties-of-matter": [
        {
            "title": "Radial Heat Conduction & Stefan-Boltzmann Cavity Radiation",
            "scope": "JEE Advanced Thermodynamics & Heat Transfer",
            "content": """
### 1. Radial Heat Conduction across Geometry
* **Coaxial Cylindrical Shell ($r_1 < r < r_2$, length $L$):**
  $$H = -k(2\\pi r L)\\frac{dT}{dr} \\implies H = \\frac{2\\pi k L(T_1 - T_2)}{\\ln(r_2/r_1)}$$
  *Thermal resistance:* $R_{\\text{th}} = \\frac{\\ln(r_2/r_1)}{2\\pi k L}$.
* **Concentric Spherical Shell ($r_1 < r < r_2$):**
  $$H = \\frac{4\\pi k r_1 r_2(T_1 - T_2)}{r_2 - r_1}, \\quad R_{\\text{th}} = \\frac{r_2 - r_1}{4\\pi k r_1 r_2}$$

### 2. Radiation Pressure & Stefan's Law
$$P_{\\text{rad}} = \\frac{I}{c} \\text{ (perfect absorber)}, \\quad P_{\\text{rad}} = \\frac{2I}{c} \\text{ (perfect reflector)}$$
Stefan-Boltzmann net rate of radiation loss to surroundings at $T_0$:
$$\\frac{dQ}{dt} = e\\sigma A(T^4 - T_0^4) = e\\sigma A(T - T_0)(T + T_0)(T^2 + T_0^2)$$
For small temperature increments $T - T_0 = \\Delta T \\ll T_0$, this reduces to Newton's Law of Cooling: $\\frac{dQ}{dt} \\approx (4e\\sigma A T_0^3)\\Delta T$.
            """,
            "speed_hack": "Wien's Law Temperature Ratio Shortcut: Since $\\lambda_{\\max} T = b = \\text{const}$, the ratio of emissive powers at peak wavelength scales as $E_{\\lambda,\\max} \\propto T^5$.",
            "example_q": "A spherical black body of radius $R$ at temperature $T$ is surrounded by a concentric spherical shell of radius $2R$ maintained at $0\\text{ K}$. Find the temperature of the outer shell if it is in radiative equilibrium with the inner body.",
            "example_sol": "Power emitted by inner body $P = \\sigma (4\\pi R^2)T^4$. Shell absorbs all $P$ on inner face and radiates from both inner and outer faces: $P = 2 \\times \\sigma (4\\pi (2R)^2)T_s^4 = 8\\sigma (4\\pi R^2)T_s^4 \\implies T_s = \\frac{T}{8^{1/4}} = \\frac{T}{2^{3/4}}$."
        }
    ],

    "11-thermodynamics": [
        {
            "title": "General Polytropic Processes $PV^n = C$ & Thermodynamic Cycles",
            "scope": "JEE Advanced Thermal Cycles",
            "content": """
### 1. Polytropic Gas Processes ($PV^n = \\text{constant}$)
* **Molar Heat Capacity:**
  $$C = C_v + \\frac{R}{1 - n}$$
  * Isobaric ($n = 0$): $C = C_v + R = C_p$.
  * Isothermal ($n = 1$): $C = \\infty$.
  * Adiabatic ($n = \\gamma$): $C = 0$.
  * Isochoric ($n = \\infty$): $C = C_v$.
* **Work done:**
  $$W = \\frac{P_1 V_1 - P_2 V_2}{n - 1} = \\frac{n_{\\text{moles}} R(T_1 - T_2)}{n - 1}$$
* **Bulk Modulus of Polytropic Gas:** $B = -V\\frac{dP}{dV} = n P$.

### 2. Efficiency of General Gas Engines
$$\\eta = \\frac{W_{\\text{net}}}{Q_{\\text{in}}} = 1 - \\frac{Q_{\\text{out}}}{Q_{\\text{in}}}$$
* For cycle consisting of straight line in $P-V$ diagram: Area enclosed equals net mechanical work.
            """,
            "speed_hack": "When is a polytropic process characterized by negative molar heat capacity? When $1 < n < \\gamma$. In this regime, the gas absorbs heat ($Q > 0$) while its temperature actually drops ($\\Delta T < 0$) because expansion work exceeds the heat supplied!",
            "example_q": "An ideal monoatomic gas ($\\gamma = 5/3$) undergoes a process $P = \\alpha V$. Find its molar heat capacity.",
            "example_sol": "$P V^{-1} = \\alpha \\implies n = -1$. $C = C_v + \\frac{R}{1 - n} = \\frac{3}{2}R + \\frac{R}{1 - (-1)} = \\frac{3}{2}R + \\frac{R}{2} = 2R$."
        }
    ],

    "12-kinetic-theory": [
        {
            "title": "Maxwell-Boltzmann Speed Distribution & Real Gas Van der Waals Isotherms",
            "scope": "JEE Advanced Statistical Physics",
            "content": """
### 1. Maxwell-Boltzmann Molecular Velocity Distribution
The fraction of molecules with speeds between $v$ and $v+dv$:
$$f(v)dv = 4\\pi\\left(\\frac{m}{2\\pi k_B T}\\right)^{3/2} v^2 e^{-\\frac{mv^2}{2k_B T}}dv$$
* **Characteristic Speeds:**
  1. *Most Probable Speed ($f'(v) = 0$):* $v_{\\text{mp}} = \\sqrt{\\frac{2k_B T}{m}} = \\sqrt{\\frac{2RT}{M}}$
  2. *Average Speed:* $v_{\\text{avg}} = \\sqrt{\\frac{8k_B T}{\\pi m}} = \\sqrt{\\frac{8RT}{\\pi M}}$
  3. *Root Mean Square Speed:* $v_{\\text{rms}} = \\sqrt{\\frac{3k_B T}{m}} = \\sqrt{\\frac{3RT}{M}}$
  $$v_{\\text{mp}} : v_{\\text{avg}} : v_{\\text{rms}} = 1 : 1.128 : 1.224 = \\sqrt{2} : \\sqrt{\\frac{8}{\\pi}} : \\sqrt{3}$$

### 2. Van der Waals Equation & Critical Constants
$$\\left(P + \\frac{a}{V_m^2}\\right)(V_m - b) = RT$$
At the critical point where $\\left.\\frac{\\partial P}{\\partial V}\\right|_{T_c} = 0$ and $\\left.\\frac{\\partial^2 P}{\\partial V^2}\\right|_{T_c} = 0$:
$$T_c = \\frac{8a}{27Rb}, \\quad P_c = \\frac{a}{27b^2}, \\quad V_c = 3b$$
Critical Compressibility Factor: $Z_c = \\frac{P_c V_c}{R T_c} = \\frac{3}{8} = 0.375$.
            """,
            "speed_hack": "Boyle Temperature $T_B$: The temperature at which a real gas behaves like an ideal gas over a wide pressure range: $T_B = \\frac{a}{Rb}$. Inversion temperature for Joule-Thomson cooling: $T_i = 2T_B = \\frac{2a}{Rb}$.",
            "example_q": "Find the ratio of molecules possessing the most probable speed at $400\\text{ K}$ compared to $100\\text{ K}$.",
            "example_sol": "$f(v_{\\text{mp}}) \\propto T^{-1/2} e^{-1} \\propto \\frac{1}{\\sqrt{T}}$. Thus $\\frac{f(v_{\\text{mp}})_{400}}{f(v_{\\text{mp}})_{100}} = \\sqrt{\\frac{100}{400}} = \\frac{1}{2}$."
        }
    ],

    "13-oscillations": [
        {
            "title": "Damped, Driven Oscillations & Coupled Physical Pendulums",
            "scope": "JEE Advanced Dynamic Oscillations",
            "content": """
### 1. Damped Harmonic Oscillator
Equation of motion with linear viscous damping force $F_d = -b\\frac{dx}{dt}$:
$$m\\frac{d^2x}{dt^2} + b\\frac{dx}{dt} + kx = 0 \\implies \\frac{d^2x}{dt^2} + 2\\gamma\\frac{dx}{dt} + \\omega_0^2 x = 0$$
where $\\gamma = \\frac{b}{2m}$ and $\\omega_0 = \\sqrt{\\frac{k}{m}}$.
* **Underdamped Solution ($\\gamma < \\omega_0$):**
  $$x(t) = A_0 e^{-\\gamma t}\\cos(\\omega' t + \\phi), \\quad \\omega' = \\sqrt{\\omega_0^2 - \\gamma^2} = \\sqrt{\\frac{k}{m} - \\frac{b^2}{4m^2}}$$
* **Quality Factor ($Q$):**
  $$Q = \\frac{\\omega_0}{2\\gamma} = \\frac{\\omega_0 m}{b} = 2\\pi \\frac{\\text{Energy Stored}}{\\text{Energy Dissipated per cycle}}$$

### 2. Compound (Physical) Pendulum
$$T = 2\\pi\\sqrt{\\frac{I}{mgd}} = 2\\pi\\sqrt{\\frac{k_g^2 + d^2}{gd}}$$
where $k_g$ is radius of gyration about COM, and $d$ is distance between suspension point and COM.
* **Minimum Time Period Condition:** $\\frac{dT}{dd} = 0 \\implies d = k_g \\implies T_{\\min} = 2\\pi\\sqrt{\\frac{2k_g}{g}}$.
            """,
            "speed_hack": "Two-Block Spring System: When two blocks of mass $m_1, m_2$ connected by spring $k$ are pulled apart and released on frictionless surface, both oscillate with identical angular frequency $\\omega = \\sqrt{\\frac{k}{\\mu}}$ where reduced mass $\\mu = \\frac{m_1 m_2}{m_1 + m_2}$.",
            "example_q": "A uniform thin rod of length $L$ oscillates as a physical pendulum about a horizontal axis through one end. Find its time period.",
            "example_sol": "$I = \\frac{1}{3}ML^2$, $d = L/2$. $T = 2\\pi\\sqrt{\\frac{ML^2/3}{Mg(L/2)}} = 2\\pi\\sqrt{\\frac{2L}{3g}}$."
        }
    ],

    "14-waves": [
        {
            "title": "Doppler Effect with Moving Reflectors, Acoustic Decibels & Dispersion",
            "scope": "JEE Advanced Wave Acoustics",
            "content": """
### 1. Advanced Doppler Effect with Reflected Echoes
When sound is reflected off a moving boundary (e.g., bat echolocation or radar tracking moving car):
* Reflector acts first as an observer receiving frequency $f_{\\text{refl}}$, then instantaneously reradiates as a moving source:
  $$f' = f_0\\left(\\frac{v \\pm v_o}{v \\mp v_s}\\right)$$
* For car moving with speed $u$ toward stationary detector emitting $f_0$:
  $$f_{\\text{echo}} = f_0\\left(\\frac{v + u}{v - u}\\right)$$
  Beat frequency detected: $\\Delta f = f_{\\text{echo}} - f_0 = f_0\\left(\\frac{2u}{v - u}\\right) \\approx \\frac{2u}{v}f_0$ for $u \\ll v$.

### 2. Sound Intensity Level in Decibels ($\\text{dB}$)
$$\\beta = 10 \\log_{10}\\left(\\frac{I}{I_0}\\right), \\quad I_0 = 10^{-12}\\text{ W/m}^2$$
* If intensity doubles: $\\Delta \\beta = 10\\log_{10}(2) \\approx +3.01\\text{ dB}$.
* If intensity increases 10-fold: $\\Delta \\beta = +10\\text{ dB}$.
* For point acoustic source: $I(r) \\propto \\frac{1}{r^2} \\implies \\beta_1 - \\beta_2 = 20\\log_{10}\\left(\\frac{r_2}{r_1}\\right)$.
            """,
            "speed_hack": "Phase vs Group Velocity: In dispersive wave propagation (such as surface water ripples), Phase velocity $v_p = \\frac{\\omega}{k}$ and Group velocity $v_g = \\frac{d\\omega}{dk} = v_p + k\\frac{dv_p}{dk}$. For deep-water gravity waves ($\\omega = \\sqrt{gk}$), $v_g = \\frac{1}{2}v_p$.",
            "example_q": "A siren emits $1000\\text{ Hz}$ sound toward a wall approaching at $10\\text{ m/s}$. Speed of sound is $330\\text{ m/s}$. What is the beat frequency heard by an observer standing near the siren?",
            "example_sol": "$f' = 1000 \\times \\frac{330 + 10}{330 - 10} = 1000 \\times \\frac{340}{320} = 1062.5\\text{ Hz}$. Beat frequency $\\Delta f = 1062.5 - 1000 = 62.5\\text{ Hz}$."
        }
    ],

    # =========================================================================
    # CLASS 12 CHAPTERS
    # =========================================================================
    "01-electrostatics": [
        {
            "title": "Method of Electrical Images, Electrostatic Pressure & Dielectric Forces",
            "scope": "JEE Advanced Classical Electrodynamics",
            "content": """
### 1. Method of Electrical Images
A grounded infinite conducting plane at $x = 0$ with a point charge $+q$ at $(d, 0, 0)$:
* The induced surface charge distribution is electrostatically equivalent to an imaginary mirror charge $-q$ positioned at $(-d, 0, 0)$.
* Attractive force on $+q$:
  $$F = \\frac{1}{4\\pi\\varepsilon_0}\\frac{q^2}{(2d)^2} = \\frac{q^2}{16\\pi\\varepsilon_0 d^2}$$
* Induced surface charge density on the grounded plane: $\\sigma(y, z) = -\\frac{q d}{2\\pi(d^2 + y^2 + z^2)^{3/2}}$.

### 2. Electrostatic Pressure on Charged Conductors
Every unit area of a charged conducting surface experiences an outward repulsive pressure:
$$P_e = \\frac{\\sigma^2}{2\\varepsilon_0} = \\frac{1}{2}\\varepsilon_0 E_{\\text{surface}}^2$$
Used to find the equilibrium radius of charged soap bubbles: $\\Delta P_{\\text{excess}} = \\frac{4T}{R} - \\frac{\\sigma^2}{2\\varepsilon_0} = 0$.

### 3. Lateral Force on a Dielectric Slab Entering a Capacitor
For a parallel plate capacitor (width $b$, spacing $d$) maintained at constant potential $V$:
$$C(x) = \\frac{\\varepsilon_0 b}{d}\\left[l + (K - 1)x\\right] \\implies F_x = \\frac{1}{2}V^2 \\frac{dC}{dx} = \\frac{\\varepsilon_0 b(K - 1)V^2}{2d}$$
The dielectric is actively pulled inwards into the capacitor!
            """,
            "speed_hack": "Charge sharing among concentric spherical shells: Always write potential $V_i = \\sum \\frac{q_k}{4\\pi\\varepsilon_0 r_k}$ where $r_k$ is the maximum of shell radius $R_i$ and the other shell's radius. Grounding a shell sets its total potential strictly to zero, not its charge!",
            "example_q": "A point charge $q$ is placed at distance $d$ from a grounded conducting plane. Find the work required to remove the charge to infinity.",
            "example_sol": "$W = \\int_d^\\infty \\frac{q^2}{16\\pi\\varepsilon_0 x^2}dx = \\frac{q^2}{16\\pi\\varepsilon_0 d}$. (Notice this is half of $\\frac{q^2}{8\\pi\\varepsilon_0 d}$ because the image charge is created dynamically)."
        }
    ],

    "02-current-electricity": [
        {
            "title": "Symmetry Nodal Analysis, Cube Resistor Networks & Infinite Ladders",
            "scope": "JEE Advanced Circuit Analysis",
            "content": """
### 1. Resistor Cube Network Symmetry Analysis
For a cube with 12 identical edges each of resistance $R$:
1. **Across Body Diagonal ($A$ to $G$):**
   Current splits into 3 equal parts at the input node, then each branch splits into 2, recombines into 3:
   $$R_{\\text{body}} = \\frac{R}{3} + \\frac{R}{6} + \\frac{R}{3} = \\frac{5}{6}R$$
2. **Across Face Diagonal ($A$ to $C$):**
   By mirror plane symmetry across diagonal slicing the cube:
   $$R_{\\text{face}} = \\frac{3}{4}R$$
3. **Across Single Edge ($A$ to $B$):**
   By superposition of currents fed into $A$ and extracted from $B$:
   $$R_{\\text{edge}} = \\frac{7}{12}R$$

### 2. Infinite Ladder Networks
For repeating $L$-section with series resistor $R_1$ and shunt resistor $R_2$:
$$R_{\\infty} = R_1 + (R_2 \\parallel R_{\\infty}) \\implies R_{\\infty} = R_1 + \\frac{R_2 R_{\\infty}}{R_2 + R_{\\infty}}$$
$$R_{\\infty}^2 - R_1 R_{\\infty} - R_1 R_2 = 0 \\implies R_{\\infty} = \\frac{R_1 + \\sqrt{R_1^2 + 4R_1 R_2}}{2}$$
            """,
            "speed_hack": "Delta-Wye ($\\Delta - Y$) Transformation: Replace a triangle of resistors $R_a, R_b, R_c$ with an equivalent star $R_1, R_2, R_3$: $R_1 = \\frac{R_b R_c}{R_a + R_b + R_c}$. When all delta resistors equal $R_\\Delta$, each star resistor equals $R_Y = \\frac{R_\\Delta}{3}$.",
            "example_q": "Find the equivalent resistance across adjacent vertices of a regular octahedron made of 12 equal $1\\,\\Omega$ resistors.",
            "example_sol": "By planar folding symmetry across the axis joining the adjacent terminals, $R_{\\text{eq}} = \\frac{1}{2}\\,\\Omega$."
        }
    ],

    "03-moving-charges-and-magnetism": [
        {
            "title": "Helical Motion in Crossed Fields, Magnetic Dipoles & Helmholtz Coils",
            "scope": "JEE Advanced Magnetostatics",
            "content": """
### 1. Particle Trajectories in Crossed Fields ($\\vec{E} \\perp \\vec{B}$)
When particle starts from rest in uniform $\\vec{E} = E\\hat{j}$ and $\\vec{B} = B\\hat{k}$:
* The trajectory is a **Cycloid** in the $x-y$ plane:
  $$x(t) = \\frac{E}{\\omega B}(\\omega t - \\sin\\omega t), \\quad y(t) = \\frac{E}{\\omega B}(1 - \\cos\\omega t)$$
  where $\\omega = \\frac{qB}{m}$.
* Maximum height reached: $y_{\\max} = \\frac{2E}{\\omega B} = \\frac{2mE}{qB^2}$.
* Drift velocity: $v_{\\text{drift}} = \\frac{E}{B}\\hat{i}$.

### 2. Gyromagnetic Ratio of Rotating Continuous Charges
For any uniformly distributed charge $Q$ and mass $M$ in rigid rotation:
$$\\frac{\\vec{M}_{\\text{mag}}}{\\vec{L}_{\\text{mech}}} = \\frac{Q}{2M} \\implies \\vec{M} = \\frac{Q}{2M}\\vec{L}$$
* Spinning solid sphere: $L = \\frac{2}{5}MR^2 \\omega \\implies M_{\\text{mag}} = \\frac{1}{5}QR^2 \\omega$.
* Rotating disk: $M_{\\text{mag}} = \\frac{1}{4}QR^2 \\omega$.

### 3. Helmholtz Coils Condition for Uniform Field
Two identical circular coils of radius $R$ carrying parallel current $I$, separated by distance $d = R$:
$$\\left.\\frac{dB}{dx}\\right|_{\\text{midpoint}} = 0, \\quad \\left.\\frac{d^2B}{dx^2}\\right|_{\\text{midpoint}} = 0$$
            """,
            "speed_hack": "Magnetic field at center of any regular polygon of $n$ sides circumscribing a circle of radius $R$: $B = \\frac{\\mu_0 I n}{\\pi R}\\tan\\left(\\frac{\\pi}{n}\\right)$. As $n \\to \\infty$, $\\tan(\\pi/n) \\to \\pi/n$, recovering the circular loop result $B = \\frac{\\mu_0 I}{2R}$.",
            "example_q": "A ring of radius $R$ carries charge $Q$ uniformly distributed along its circumference. It rotates at constant angular frequency $\\omega$. Find the magnetic field at its center.",
            "example_sol": "$I = \\frac{Q}{T} = \\frac{Q\\omega}{2\\pi}$. Magnetic field $B = \\frac{\\mu_0 I}{2R} = \\frac{\\mu_0 Q \\omega}{4\\pi R}$."
        }
    ],

    "04-magnetism-and-matter": [
        {
            "title": "Magnetic Dipole-Dipole Potential Energy & Magnetic Boundary Conditions",
            "scope": "JEE Advanced Magnetism",
            "content": """
### 1. Interaction Energy of Two Point Magnetic Dipoles
For two dipoles $\\vec{m}_1$ and $\\vec{m}_2$ separated by displacement vector $\\vec{r}$:
$$U = \\frac{\\mu_0}{4\\pi r^3}\\left[\\vec{m}_1 \\cdot \\vec{m}_2 - 3(\\vec{m}_1 \\cdot \\hat{r})(\\vec{m}_2 \\cdot \\hat{r})\\right]$$
* **Collinear Dipoles ($\\|\\hat{r}$):** $U = -\\frac{2\\mu_0 m_1 m_2}{4\\pi r^3} \\implies F = -\\frac{dU}{dr} = -\\frac{6\\mu_0 m_1 m_2}{4\\pi r^4}$ (Attractive).
* **Broadside Dipoles ($\\\\perp\\hat{r}$, parallel to each other):** $U = +\\frac{\\mu_0 m_1 m_2}{4\\pi r^3} \\implies F = +\\frac{3\\mu_0 m_1 m_2}{4\\pi r^4}$ (Repulsive).

### 2. Terrestrial Magnetic Elements & Vibration Magnetometer
$$T = 2\\pi\\sqrt{\\frac{I}{M B_H}}$$
If two magnets are placed in sum position ($M_1 + M_2$) vs difference position ($M_1 - M_2$):
$$\\frac{M_1}{M_2} = \\frac{T_2^2 + T_1^2}{T_2^2 - T_1^2}$$
            """,
            "speed_hack": "Demagnetizing Factor in Paramagnetic Rods: When an external field $H_{\\text{ext}}$ is applied to a short cylinder, internal field is reduced by shape demagnetization: $H_{\\text{int}} = H_{\\text{ext}} - N_d M$. For a long thin needle aligned with field, $N_d \\approx 0$.",
            "example_q": "Find the ratio of magnetic field on the axial line to the equatorial line of a short bar magnet at the same distance.",
            "example_sol": "$B_{\\text{axial}} = \\frac{\\mu_0}{4\\pi}\\frac{2M}{r^3}$, $B_{\\text{equatorial}} = \\frac{\\mu_0}{4\\pi}\\frac{M}{r^3} \\implies \\text{Ratio} = 2:1$."
        }
    ],

    "05-electromagnetic-induction-and-ac": [
        {
            "title": "LR, RC, LCR Transient Differentials & Mutual Inductance Theorems",
            "scope": "JEE Advanced Electromagnetic Induction",
            "content": """
### 1. Transient Analysis in $L-R$ and $L-C$ Circuits
* **$L-R$ Current Growth (DC source $V_0$):**
  $$L\\frac{dI}{dt} + R I = V_0 \\implies I(t) = \\frac{V_0}{R}\\left(1 - e^{-t/\\tau_L}\\right), \\quad \\tau_L = \\frac{L}{R}$$
* **$L-C$ Undamped Oscillations:**
  $$L\\frac{d^2q}{dt^2} + \\frac{q}{C} = 0 \\implies q(t) = Q_0 \\cos(\\omega_0 t), \\quad \\omega_0 = \\frac{1}{\\sqrt{LC}}$$
  Energy oscillates continuously between electrostatic $U_E = \\frac{q^2}{2C}$ and magnetic $U_B = \\frac{1}{2}L I^2$.

### 2. Reciprocity Theorem of Mutual Inductance
$$M_{12} = M_{21} = M$$
The mutual inductance between a tiny circular loop of radius $r$ at the center of a large coplanar loop of radius $R$ ($r \\ll R$):
$$M = \\frac{\\mu_0 \\pi r^2}{2R}$$
Notice it is far easier to calculate flux through the small coil due to current in the large coil than vice-versa!
            """,
            "speed_hack": "Parallel AC Resonance (Anti-Resonance Tank Circuit): For inductor with internal resistance $R$ in parallel with ideal capacitor $C$, resonant frequency is $\\omega_r = \\sqrt{\\frac{1}{LC} - \\frac{R^2}{L^2}}$. Dynamic impedance at resonance is purely resistive: $Z_p = \\frac{L}{CR}$.",
            "example_q": "A coil of inductance $2\\text{ H}$ and resistance $10\\,\\Omega$ is connected across a $100\\text{ V}$ battery. How long does it take for current to reach half its steady state value?",
            "example_sol": "$I(t) = I_{\\max}(1 - e^{-t/\\tau}) \\implies 0.5 = 1 - e^{-t/\\tau} \\implies t = \\tau \\ln 2 = \\frac{L}{R}\\ln 2 = \\frac{2}{10}(0.693) = 0.1386\\text{ s}$."
        }
    ],

    "06-electromagnetic-waves": [
        {
            "title": "Poynting Vector Energy Flux & Polarization State Transformations",
            "scope": "JEE Advanced Maxwell Electrodynamics",
            "content": """
### 1. Poynting Vector & Energy Transport
The directional energy flux per unit area per unit second carried by EM waves:
$$\\vec{S} = \\frac{1}{\\mu_0}(\\vec{E} \\times \\vec{B})$$
* Time-averaged intensity for plane sinusoidal EM wave:
  $$\\langle S \\rangle = \\frac{E_0 B_0}{2\\mu_0} = \\frac{1}{2}c\\varepsilon_0 E_0^2 = \\frac{E_{\\text{rms}}^2}{\\mu_0 c}$$
* Momentum density: $\\vec{g} = \\frac{\\vec{S}}{c^2} = \\varepsilon_0 (\\vec{E} \\times \\vec{B})$.

### 2. Radiation Pressure at Oblique Incidence
When EM beam of intensity $I$ strikes a flat surface at angle of incidence $\\theta$:
* **Perfect Absorber:** $P_{\\text{abs}} = \\frac{I}{c}\\cos^2\\theta$.
* **Perfect Reflector:** $P_{\\text{refl}} = \\frac{2I}{c}\\cos^2\\theta$.
* Tangential shear force density: $F_t = \\frac{I}{c}\\sin\\theta\\cos\\theta$ (only for absorbing surfaces).
            """,
            "speed_hack": "Circular vs Elliptical Polarization Condition: Superposition of $E_x = E_{0x}\\cos(kz - \\omega t)$ and $E_y = E_{0y}\\cos(kz - \\omega t + \\phi)$: Circular if $\\phi = \\pm \\frac{\\pi}{2}$ and $E_{0x} = E_{0y}$. Elliptical if $\\phi \\ne 0, \\pi$ or $E_{0x} \\ne E_{0y}$. Linear if $\\phi = 0$ or $\\pi$.",
            "example_q": "Find the peak electric field of a $100\\text{ W}$ isotropic bulb at a distance of $3\\text{ m}$.",
            "example_sol": "$I = \\frac{P}{4\\pi r^2} = \\frac{100}{4\\pi (9)} = \\frac{100}{36\\pi} \\approx 0.884\\text{ W/m}^2$. $I = \\frac{1}{2}c\\varepsilon_0 E_0^2 \\implies E_0 = \\sqrt{\\frac{2I}{c\\varepsilon_0}} = \\sqrt{2 \\times 0.884 \\times 377} \\approx 25.8\\text{ V/m}$."
        }
    ],

    "07-ray-optics-and-optical-instruments": [
        {
            "title": "Fermat's Least Action Principle, Silvered Lenses & Achromatism",
            "scope": "JEE Advanced Geometrical Optics",
            "content": """
### 1. Fermat's Principle of Stationary Optical Path
Light travels along a trajectory that renders the optical path length $\\mathcal{L} = \\int n(s)\\,ds$ stationary:
$$\\delta \\int n(s)\\,ds = 0$$
Derives Snell's law: $n_1 \\sin\\theta_1 = n_2 \\sin\\theta_2$ from first principles of time extremization.

### 2. Silvered Lens (Equivalent Mirror Formula)
When one face of a thin lens of focal length $f_l$ is silvered (converting it into a mirror of focal length $f_m$):
$$\\frac{1}{F_{\\text{eq}}} = \\frac{2}{f_l} + \\frac{1}{f_m}$$
*(Light passes through the lens, reflects off the silvered mirror face, and passes back through the lens).*

### 3. Achromatic Combination of Thin Lenses
To eliminate chromatic aberration (making focal lengths equal for red and violet light):
* **In Contact:** $\\frac{\\omega_1}{f_1} + \\frac{\\omega_2}{f_2} = 0 \\implies \\frac{f_1}{f_2} = -\\frac{\\omega_1}{\\omega_2}$ (One convex, one concave).
* **Separated by Distance $d$ (Same Material $\\omega_1 = \\omega_2$):** $d = \\frac{f_1 + f_2}{2}$ (Huygens eyepiece principle).
            """,
            "speed_hack": "Plano-convex lens with flat face silvered: $f_m = \\infty \\implies \\frac{1}{F_{\\text{eq}}} = \\frac{2}{f_l} \\implies F_{\\text{eq}} = \\frac{f_l}{2} = \\frac{R}{2(\\mu - 1)}$. Acts as a concave mirror of focal length $\\frac{R}{2(\\mu - 1)}$.",
            "example_q": "A plano-convex lens ($\\mu = 1.5$) of radius $R = 20\\text{ cm}$ has its curved surface silvered. Find the focal length of the resulting system.",
            "example_sol": "$\\frac{1}{f_l} = (1.5 - 1)\\frac{1}{R} = \\frac{1}{40} \\implies f_l = 40\\text{ cm}$. $f_m = \\frac{R}{2} = 10\\text{ cm}$. $\\frac{1}{F} = \\frac{2}{40} + \\frac{1}{10} = \\frac{6}{40} \\implies F = \\frac{20}{3}\\text{ cm}$ (concave mirror behavior)."
        }
    ],

    "08-wave-optics": [
        {
            "title": "Thin-Film Interference, Stokes' Phase Shift & Resolving Power",
            "scope": "JEE Advanced Wave Optics",
            "content": """
### 1. Thin-Film Interference (Stokes' Reversal Principle)
When light reflects at the boundary of an optically denser medium, it incurs an intrinsic phase shift of $\\pi$ radians (equivalent to path jump of $\\frac{\\lambda}{2}$).
* Optical path difference for film of thickness $t$, refractive index $\\mu$, refraction angle $r$:
  $$\\Delta x = 2\\mu t\\cos r - \\frac{\\lambda}{2}$$
* **Constructive Interference (Bright):** $2\\mu t\\cos r = \\left(m + \\frac{1}{2}\\right)\\lambda$.
* **Destructive Interference (Dark):** $2\\mu t\\cos r = m\\lambda$.
* **Non-Reflective Optical Coating (Anti-Reflection Glass):**
  $$t_{\\min} = \\frac{\\lambda}{4\\mu}$$

### 2. YDSE with Thin Transparent Slab Insertion
When a glass sheet of thickness $t$ and index $\\mu$ is placed in front of one slit:
* The optical path through that slit increases by $(\\mu - 1)t$.
* Shift in the entire interference fringe pattern on the screen:
  $$\\Delta y = \\frac{D}{d}(\\mu - 1)t$$
  Number of fringes shifted: $N = \\frac{(\\mu - 1)t}{\\lambda}$.
            """,
            "speed_hack": "Resolving Power of Microscope & Telescope: Rayleigh's Limit of Resolution for Telescope: $\\theta_{\\min} = \\frac{1.22\\lambda}{D} \\implies RP = \\frac{D}{1.22\\lambda}$. For Microscope: $d_{\\min} = \\frac{1.22\\lambda}{2\\mu\\sin\\theta} \\implies RP = \\frac{2\\mu\\sin\\theta}{1.22\\lambda}$ where $\\mu\\sin\\theta$ is the Numerical Aperture (NA).",
            "example_q": "In YDSE, light of wavelength $600\\text{ nm}$ is used. When a thin mica sheet ($\\mu = 1.6$) is placed over one slit, the central bright fringe shifts to the position of the 6th bright fringe. Find the thickness of the sheet.",
            "example_sol": "$(\\mu - 1)t = n\\lambda \\implies (1.6 - 1)t = 6 \\times 600 \\times 10^{-9}\\text{ m} \\implies 0.6 t = 3600 \\times 10^{-9} \\implies t = 6 \\times 10^{-6}\\text{ m} = 6\\,\\mu\\text{m}$."
        }
    ],

    "09-dual-nature-of-radiation-and-matter": [
        {
            "title": "Compton Scattering Wavelength Shift & Relativistic de Broglie Waves",
            "scope": "JEE Advanced Quantum Physics",
            "content": """
### 1. Compton Scattering Mechanics
When a high-energy X-ray or gamma photon scatters off a stationary free electron:
$$\\lambda' - \\lambda = \\frac{h}{m_e c}(1 - \\cos\\theta)$$
* **Compton Wavelength of Electron:**
  $$\\lambda_c = \\frac{h}{m_e c} \\approx 0.0243\\text{ \\AA} = 2.426 \\times 10^{-12}\\text{ m}$$
* Maximum wavelength shift occurs at backscattering ($\\theta = 180^\\circ$):
  $$\\Delta \\lambda_{\\max} = 2\\lambda_c \\approx 0.0485\\text{ \\AA}$$

### 2. Relativistic de Broglie Wavelength
When kinetic energy $K$ is comparable to rest mass energy $m_0 c^2$:
$$E^2 = p^2 c^2 + m_0^2 c^4 \\implies p = \\frac{\\sqrt{K(K + 2m_0 c^2)}}{c}$$
$$\\lambda = \\frac{h}{p} = \\frac{hc}{\\sqrt{K(K + 2m_0 c^2)}}$$
For non-relativistic limit ($K \\ll m_0 c^2$), this simplifies to standard $\\lambda = \\frac{h}{\\sqrt{2m_0 K}}$.
            """,
            "speed_hack": "Electron de Broglie Wavelength Shortcut: $\\lambda = \\frac{12.27}{\\sqrt{V}}\\text{ \\AA}$ where $V$ is accelerating potential in Volts. For Proton: $\\lambda = \\frac{0.286}{\\sqrt{V}}\\text{ \\AA}$; for Alpha particle: $\\lambda = \\frac{0.101}{\\sqrt{V}}\\text{ \\AA}$.",
            "example_q": "Find the voltage through which an electron must be accelerated so that its de Broglie wavelength equals $1\\text{ \\AA}$.",
            "example_sol": "$\\lambda = \\frac{12.27}{\\sqrt{V}} = 1\\text{ \\AA} \\implies \\sqrt{V} = 12.27 \\implies V \\approx 150.6\\text{ Volts}$."
        }
    ],

    "10-atoms-and-nuclei": [
        {
            "title": "Reduced Mass Nuclear Correction, Moseley's Law & Radioactive Series",
            "scope": "JEE Advanced Atomic & Nuclear Physics",
            "content": """
### 1. Finite Nuclear Mass Correction in Bohr Model
Since the nucleus has finite mass $M$ (not infinite), both electron and nucleus orbit their common center of mass.
* Replace electron mass $m_e$ with the **reduced mass** $\\mu$:
  $$\\mu = \\frac{m_e M}{m_e + M} = \\frac{m_e}{1 + \\frac{m_e}{M}}$$
* The corrected Rydberg constant becomes:
  $$R_M = R_\\infty \\left(\\frac{1}{1 + \\frac{m_e}{M}}\\right)$$
* Explains the subtle spectral difference between Hydrogen ($M_p$) and Deuterium ($M_d \\approx 2M_p$): $\\frac{\\Delta \\lambda}{\\lambda} \\approx \\frac{m_e}{2M_p} \\approx \\frac{1}{3670}$.

### 2. Moseley's Law for Characteristic X-Rays
$$\\sqrt{\\nu} = a(Z - b)$$
where $b$ is the screening constant ($b = 1$ for $K_\\alpha$ transition $L \\to K$; $b = 7.4$ for $L_\\alpha$).
$$\\frac{1}{\\lambda_{K_\\alpha}} = R(Z - 1)^2 \\left(1 - \\frac{1}{4}\\right) = \\frac{3}{4}R(Z - 1)^2$$

### 3. Successive Radioactive Decay (Bateman Equations)
$$A \\xrightarrow{\\lambda_1} B \\xrightarrow{\\lambda_2} C$$
$$\\frac{dN_B}{dt} = \\lambda_1 N_A - \\lambda_2 N_B$$
* **Secular Equilibrium (when parent is very long-lived, $\\lambda_1 \\ll \\lambda_2$):**
  $$N_1 \\lambda_1 = N_2 \\lambda_2 = \\text{Activity}_1 = \\text{Activity}_2$$
            """,
            "speed_hack": "Threshold kinetic energy of projectile mass $m$ to initiate endothermic nuclear reaction of $Q$-value $Q < 0$ on stationary target $M$: $K_{\\text{th}} = |Q|\\left(1 + \\frac{m}{M}\\right)$.",
            "example_q": "The $K_\\alpha$ X-ray wavelength from an element with $Z=43$ is $\\lambda$. Find the atomic number of an element whose $K_\\alpha$ wavelength is $4\\lambda$.",
            "example_sol": "$\\frac{1}{\\lambda} \\propto (Z - 1)^2 \\implies Z - 1 \\propto \\frac{1}{\\sqrt{\\lambda}}$. Thus $\\frac{Z_2 - 1}{43 - 1} = \\sqrt{\\frac{\\lambda}{4\\lambda}} = \\frac{1}{2} \\implies Z_2 - 1 = 21 \\implies Z_2 = 22$ (Titanium)."
        }
    ],

    "11-semiconductor-electronics": [
        {
            "title": "Hall Effect, Zener Dynamic Resistance & Early Effect in Semiconductors",
            "scope": "JEE Advanced Solid State Devices",
            "content": """
### 1. Hall Effect & Majority Carrier Characterization
When a current-carrying semiconductor slab (current $I$, thickness $d$) is placed in transverse magnetic field $B$:
$$V_H = \\frac{I B}{n q d}$$
* **Hall Coefficient ($R_H$):**
  $$R_H = \\frac{1}{n q} = \\frac{E_y}{J_x B_z}$$
  * If $V_H > 0$: Majority carriers are positively charged holes ($p$-type).
  * If $V_H < 0$: Majority carriers are negatively charged electrons ($n$-type).

### 2. Zener Diode Voltage Regulator Design Formulas
For input voltage varying between $V_{\\min}$ and $V_{\\max}$, and load current between $I_{L,\\min}$ and $I_{L,\\max}$:
* Series dropping resistor $R_s$:
  $$R_{s,\\max} = \\frac{V_{\\min} - V_z}{I_{z,\\min} + I_{L,\\max}}, \\quad R_{s,\\min} = \\frac{V_{\\max} - V_z}{I_{z,\\max} + I_{L,\\min}}$$
* Maximum power dissipation in Zener: $P_z = V_z \\cdot I_{z,\\max}$.
            """,
            "speed_hack": "LED Peak Emission Wavelength: The bandgap $E_g$ determines the emitted photon wavelength: $\\lambda = \\frac{hc}{E_g} \\approx \\frac{12400\\text{ eV}\\cdot\\text{\\AA}}{E_g\\text{ (in eV)}}$. For visible GaAsP (red, $E_g \\approx 1.9\\text{ eV}$), $\\lambda \\approx 6500\\text{ \\AA}$.",
            "example_q": "A Zener diode with breakdown voltage $V_z = 10\\text{ V}$ is used in a regulator circuit with supply voltage varying from $15\\text{ V}$ to $25\\text{ V}$. If the load requires constant $10\\text{ mA}$ and minimum Zener current is $5\\text{ mA}$, find the maximum allowable value of series resistor $R_s$.",
            "example_sol": "$R_{s,\\max} = \\frac{V_{\\min} - V_z}{I_{z,\\min} + I_L} = \\frac{15 - 10}{(5 + 10) \\times 10^{-3}} = \\frac{5}{15 \\times 10^{-3}} = \\frac{1000}{3} \\approx 333.3\\,\\Omega$."
        }
    ]
}


def render_jee_advanced_tab(chapter_slug):
    """
    Renders the complete, rich Advanced Studies tab HTML for a chapter
    with strict curriculum segregation banners, formula boxes, and speed-hacks.
    """
    modules = JEE_ADVANCED_MODULES.get(chapter_slug, [])
    if not modules:
        return """
        <div class="notebook-sheet" style="text-align:center; padding: 3rem 1.5rem;">
          <div style="font-size:2.5rem; margin-bottom:1rem;">🚀</div>
          <h3 style="color:#7c3aed; font-family:'Kalam', cursive;">NCERT &amp; Competitive Unified Scope</h3>
          <p style="color:#475569; max-width:600px; margin: 0.5rem auto 1.5rem; font-size:1.1rem;">
            All advanced analytical concepts, vector calculus derivations, and competitive problem-solving patterns
            for this chapter have been completely harmonized into the NCERT Core Notes and Solved Examples above!
          </p>
        </div>
        """

    import markdown
    md = markdown.Markdown(extensions=['tables', 'fenced_code', 'nl2br'])

    modules_html = []
    for idx, mod in enumerate(modules, 1):
        parsed_content = md.convert(mod['content'])
        
        modules_html.append(f"""
          <div class="notebook-sheet adv-module-card" style="margin-bottom: 2.25rem; border: 2px solid #ddd6fe; border-radius: 16px; padding: 1.75rem; background: #ffffff; box-shadow: 0 4px 18px rgba(124, 58, 237, 0.08);">
            <div class="adv-card-header" style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:0.5rem; margin-bottom:1.25rem; border-bottom:1.5px dashed #c4b5fd; padding-bottom:0.75rem;">
              <div style="display:flex; align-items:center; gap:0.6rem;">
                <span class="doodle-tag tag-purple" style="font-size:0.9rem;">ADVANCED MODULE {idx:02d}</span>
                <h3 style="margin:0; color:#581c87; font-size:1.35rem; font-family:var(--font-title);">{mod['title']}</h3>
              </div>
              <span class="doodle-tag tag-red" style="font-size:0.82rem;">🎯 {mod['scope']}</span>
            </div>

            <div class="adv-card-body" style="font-size:1.05rem; line-height:1.65; color:#1e293b;">
              {parsed_content}
            </div>

            <div class="sticky-note yellow" style="margin: 1.5rem 0 1rem; border-left: 5px solid #eab308;">
              <div class="sticky-title" style="color:#854d0e;">⚡ Competitive Speed-Hack &amp; Limiting Case Trick</div>
              <p style="margin:0; font-size:1.02rem; color:#713f12;">{mod['speed_hack']}</p>
            </div>

            <div class="adv-example-box" style="margin-top:1.25rem; background:#faf5ff; border:1px solid #e9d5ff; border-radius:10px; padding:1.1rem;">
              <div style="font-weight:bold; color:#6b21a8; margin-bottom:0.4rem; font-size:1.05rem;">
                💡 JEE Advanced Worked Problem Paradigm:
              </div>
              <div style="font-size:1.02rem; color:#374151; margin-bottom:0.75rem;">{mod['example_q']}</div>
              <details class="solution-accordion" style="background:#ffffff; border:1px solid #d8b4fe; border-radius:8px; padding:0.5rem 0.85rem;">
                <summary class="solution-toggle" style="cursor:pointer; font-weight:bold; color:#7e22ce; display:flex; justify-content:space-between;">
                  <span>🔍 View Mathematical Solution &amp; Answer</span>
                  <span>▼</span>
                </summary>
                <div class="solution-body" style="padding-top:0.6rem; border-top:1px dashed #e9d5ff; margin-top:0.5rem; font-size:1rem; color:#1f2937;">
                  {mod['example_sol']}
                </div>
              </details>
            </div>
          </div>
        """)

    return f"""
      {JEE_ADVISORY_BANNER_HTML}
      <div class="advanced-studies-container">
        {"".join(modules_html)}
      </div>
    """
