#!/usr/bin/env python3
"""
CBSE Physics Notebook Web Portal Compiler
Builds the complete interactive offline study website for CBSE Class 11 & 12 Physics
following the latest NCERT curriculum with handwriting whiteboard theme, 
fluorescent highlighter formula boxes, doodle sketch tags, interactive HTML5 physics simulations,
ELI5 intuition toggles, and step-wise CBSE marking rubrics.
"""

import os
import re
import json
import glob
import markdown
import sys
from datetime import datetime, timezone

# Ensure UTF-8 output on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from jee_advanced_data import render_jee_advanced_tab

ROOT_DIR = r"E:\physics_cbse"
OUT_DIR = r"E:\physics_cbse\physics_html_notebook"

# Comprehensive metadata for all 25 Physics Chapters
CHAPTER_METADATA = {
    "Class_11": [
        {
            "dir_pattern": "Units_and_Measurements_*",
            "slug": "01-units-and-measurements",
            "title": "Units and Measurements",
            "domain": "Measurement & Dimensions",
            "priority": "⭐⭐⭐⭐",
            "yield": "Foundational Core",
            "sim": None,
            "eli5": {
                "title": "Dimensional Analysis & Principle of Homogeneity",
                "standard": "Only physical quantities having the identical dimensions can be added, subtracted, or equated: $[LHS] = [RHS]$. Dimensional consistency does not ensure dimensionless constants are correct.",
                "intuitive": "Think of physical dimensions like currency: you can add 5 dollars to 10 dollars to get 15 dollars, but you cannot add 5 apples to 10 meters! Every term in a physics formula must measure the exact same physical thing."
            },
            "advanced_keywords": ["vernier calliper screw gauge errors", "significant figures rounding rules", "least count error analysis"],
            "key_concepts": ["SI Base Units", "Dimensional Homogeneity", "$[M^a L^b T^c]$", "Error Propagation $\\frac{\\Delta X}{X}$"]
        },
        {
            "dir_pattern": "Motion_in_a_Straight_Line_*",
            "slug": "02-motion-in-a-straight-line",
            "title": "Motion in a Straight Line",
            "domain": "Kinematics",
            "priority": "⭐⭐⭐⭐",
            "yield": "High Yield 🔥",
            "sim": None,
            "eli5": {
                "title": "Instantaneous Velocity vs Average Speed",
                "standard": "Instantaneous velocity $v = \\lim_{\\Delta t \\to 0} \\frac{\\Delta x}{\\Delta t} = \\frac{dx}{dt}$ is the derivative of position with respect to time, representing the tangent slope on an $x-t$ curve.",
                "intuitive": "If you drive 60 km in one hour, your average speed is 60 km/h. But when you look down at your speedometer for a split-second when overtaking a truck, it reads 95 km/h! That speedometer reading right now is instantaneous velocity."
            },
            "advanced_keywords": ["stopping distance reaction time", "relative motion in one dimension"],
            "key_concepts": ["$v = u + at$", "$s = ut + \\frac{1}{2}at^2$", "$v^2 = u^2 + 2as$", "$v-t$ Graph Area = Displacement"]
        },
        {
            "dir_pattern": "Motion_in_a_Plane_*",
            "slug": "03-motion-in-a-plane",
            "title": "Motion in a Plane",
            "domain": "Kinematics",
            "priority": "⭐⭐⭐⭐⭐",
            "yield": "High Yield 🔥",
            "sim": "projectile",
            "eli5": {
                "title": "Independence of Horizontal & Vertical Projectile Motion",
                "standard": "In 2D projectile motion, $a_x = 0$ and $a_y = -g$. The orthogonal components $x(t) = (u\\cos\\theta)t$ and $y(t) = (u\\sin\\theta)t - \\frac{1}{2}gt^2$ evolve completely independently of each other.",
                "intuitive": "Imagine dropping a ball straight down from your hand while shooting an identical bullet horizontally forward at 500 m/s from the exact same height. If there's no air, both will hit the flat ground at the exact same millisecond! Gravity pulls down with zero care for how fast you travel sideways."
            },
            "advanced_keywords": ["relative velocity rain man river boat", "projectile on inclined plane"],
            "key_concepts": ["$R = \\frac{u^2 \\sin 2\\theta}{g}$", "$H_{\\max} = \\frac{u^2 \\sin^2\\theta}{2g}$", "$T = \\frac{2u\\sin\\theta}{g}$", "Centripetal $a_c = \\frac{v^2}{r}$"]
        },
        {
            "dir_pattern": "Laws_of_Motion_*",
            "slug": "04-laws-of-motion",
            "title": "Laws of Motion",
            "domain": "Mechanics",
            "priority": "⭐⭐⭐⭐⭐",
            "yield": "High Yield 🔥",
            "sim": "incline",
            "eli5": {
                "title": "Newton's Third Law & Action-Reaction Pairs",
                "standard": "To every action there is always an equal and opposite reaction: $\\vec{F}_{AB} = -\\vec{F}_{BA}$. Action and reaction forces act on different interacting bodies, never on the same body.",
                "intuitive": "If you stand on a skateboard on smooth ice and push a heavy friend forward, you fly backwards! You cannot push against anything in the universe without the universe pushing you back with the exact same strength."
            },
            "advanced_keywords": ["pseudo force non-inertial frames", "banking of rough curved road"],
            "key_concepts": ["$\\vec{F} = \\frac{d\\vec{p}}{dt} = m\\vec{a}$", "Friction $f_s \\le \\mu_s N$", "Banking $v = \\sqrt{rg\\tan\\theta}$", "Impulse $J = \\int F\\,dt = \\Delta p$"]
        },
        {
            "dir_pattern": "Work_Energy_and_Power_*",
            "slug": "05-work-energy-and-power",
            "title": "Work, Energy and Power",
            "domain": "Mechanics",
            "priority": "⭐⭐⭐⭐⭐",
            "yield": "High Yield 🔥",
            "sim": None,
            "eli5": {
                "title": "Work-Energy Theorem & Conservation of Energy",
                "standard": "The net work done by all forces (conservative, non-conservative, external) on a particle equals the change in its kinetic energy: $W_{\\text{net}} = \\Delta K = \\frac{1}{2}mv_f^2 - \\frac{1}{2}mv_i^2$.",
                "intuitive": "Think of kinetic energy as a bank account of motion. Work done is a deposit (if you push in the direction of motion) or a withdrawal (like friction draining your speed). The change in your motion bank balance is strictly equal to the net work deposited."
            },
            "advanced_keywords": ["potential energy curves equilibrium stable unstable", "vertical circular motion critical velocity"],
            "key_concepts": ["$W = \\vec{F}\\cdot\\vec{d} = Fd\\cos\\theta$", "Work-Energy $W_{\\text{net}} = \\Delta K$", "Spring $U = \\frac{1}{2}kx^2$", "Power $P = \\vec{F}\\cdot\\vec{v}$"]
        },
        {
            "dir_pattern": "System_of_Particles_and_Rotati_*",
            "slug": "06-system-of-particles-and-rotational-motion",
            "title": "System of Particles & Rotational Motion",
            "domain": "Rotational Mechanics",
            "priority": "⭐⭐⭐⭐⭐",
            "yield": "High Yield 🔥",
            "sim": None,
            "eli5": {
                "title": "Moment of Inertia & Rotational Analogy",
                "standard": "Moment of inertia $I = \\sum m_i r_i^2 = \\int r^2 dm$ measures a rigid body's resistance to rotational acceleration, functioning as the exact rotational counterpart of linear mass $m$.",
                "intuitive": "Try balancing a long broomstick on your finger with the heavy bristles at the top versus at the bottom. When the heavy bristles are far up away from your hand, it is much harder to tip over because mass situated far from the axis creates enormous rotational inertia!"
            },
            "advanced_keywords": ["parallel and perpendicular axes theorems proofs", "rolling motion without slipping on incline"],
            "key_concepts": ["Torque $\\vec{\\tau} = \\vec{r}\\times\\vec{F}$", "Angular Momentum $\\vec{L} = I\\vec{\\omega}$", "$I = \\sum m_i r_i^2$", "Conservation of $\\vec{L}$"]
        },
        {
            "dir_pattern": "Gravitation_*",
            "slug": "07-gravitation",
            "title": "Gravitation",
            "domain": "Gravitation",
            "priority": "⭐⭐⭐⭐",
            "yield": "High Yield 🔥",
            "sim": None,
            "eli5": {
                "title": "Orbital Motion & Free Fall",
                "standard": "An orbiting satellite is in continuous free fall toward Earth, but its tangential velocity $v_o = \\sqrt{GM/r}$ is so large that Earth's spherical surface curves away underneath it at the exact same rate.",
                "intuitive": "If you throw a ball, it lands a few meters away. If you throw it faster, it lands further. If you shoot it horizontally at 8 km/s, as gravity bends the ball downward, the curvature of the Earth curves downward away at the exact same rate. The ball falls forever without ever touching the ground!"
            },
            "advanced_keywords": ["gravitational potential self energy of sphere", "kepler third law derivation"],
            "key_concepts": ["$F = G\\frac{m_1 m_2}{r^2}$", "Variation $g(h) = g(1 - \\frac{2h}{R})$", "Escape $v_e = \\sqrt{2gR}$", "Orbital $v_o = \\sqrt{gR}$"]
        },
        {
            "dir_pattern": "Mechanical_Properties_of_Solid_*",
            "slug": "08-mechanical-properties-of-solids",
            "title": "Mechanical Properties of Solids",
            "domain": "Properties of Matter",
            "priority": "⭐⭐⭐",
            "yield": "Core Foundation",
            "sim": None,
            "eli5": {
                "title": "Young's Modulus & Elastic Recovery",
                "standard": "Young's modulus $Y = \\frac{\\text{Tensile Stress}}{\\text{Tensile Strain}} = \\frac{F/A}{\\Delta L/L}$ is an intrinsic property of the material reflecting interatomic bonding spring stiffness.",
                "intuitive": "Imagine solid atoms as tiny billiard balls connected by stiff microscopic steel springs. When you pull on a steel bar, you slightly stretch billions of atomic springs. Release the pull, and the springs instantly snap the atoms right back to their original spacing."
            },
            "advanced_keywords": ["bulk and shear modulus relation", "poisson ratio theoretical limits"],
            "key_concepts": ["Stress-Strain Curve", "Hooke's Law $\\sigma = Y\\epsilon$", "$Y = \\frac{FL}{A\\Delta L}$", "Energy Density $u = \\frac{1}{2}\\sigma\\epsilon$"]
        },
        {
            "dir_pattern": "Mechanical_Properties_of_Fluid_*",
            "slug": "09-mechanical-properties-of-fluids",
            "title": "Mechanical Properties of Fluids",
            "domain": "Properties of Matter",
            "priority": "⭐⭐⭐⭐⭐",
            "yield": "High Yield 🔥",
            "sim": None,
            "eli5": {
                "title": "Bernoulli's Principle: Pressure vs Speed",
                "standard": "For an incompressible, non-viscous streamline fluid: $P + \\frac{1}{2}\\rho v^2 + \\rho gh = \\text{constant}$. Wherever fluid velocity $v$ increases, static pressure $P$ must decrease.",
                "intuitive": "Hold two thin sheets of paper 2 inches apart and blow hard air directly between them. Instead of blowing apart, they violently snap together! The fast-moving air between them drops in pressure, and the calm, higher-pressure atmospheric air outside pushes them shut."
            },
            "advanced_keywords": ["poiseuille formula viscous flow", "reynolds number turbulence criteria"],
            "key_concepts": ["Pascal's Law", "Bernoulli $P + \\frac{1}{2}\\rho v^2 + \\rho gh = C$", "Surface Tension $T = \\frac{F}{L}$", "Terminal $v_t = \\frac{2r^2(\\rho-\\sigma)g}{9\\eta}$"]
        },
        {
            "dir_pattern": "Thermal_Properties_of_Matter_*",
            "slug": "10-thermal-properties-of-matter",
            "title": "Thermal Properties of Matter",
            "domain": "Thermal Physics",
            "priority": "⭐⭐⭐⭐",
            "yield": "High Yield 🔥",
            "sim": None,
            "eli5": {
                "title": "Latent Heat & Phase Transition",
                "standard": "During a first-order phase change (e.g. melting ice or boiling water), heat energy $Q = mL$ is absorbed without any temperature change, as thermal energy is spent breaking intermolecular bonds.",
                "intuitive": "When you boil water, why doesn't its temperature rise past 100°C? Because every drop of stove heat is no longer speeding up the water molecules—it is being completely consumed as 'bond-breaking fees' to rip water molecules apart into steam."
            },
            "advanced_keywords": ["blackbody radiation wien displacement law", "stefan boltzmann law radiation"],
            "key_concepts": ["$\\Delta L = \\alpha L\\Delta T$", "$Q = mc\\Delta T$", "Latent Heat $Q = mL$", "Newton's Cooling $\\frac{dT}{dt} = -k(T-T_0)$"]
        },
        {
            "dir_pattern": "Thermodynamics_*",
            "slug": "11-thermodynamics",
            "title": "Thermodynamics",
            "domain": "Thermal Physics",
            "priority": "⭐⭐⭐⭐⭐",
            "yield": "High Yield 🔥",
            "sim": None,
            "eli5": {
                "title": "First Law of Thermodynamics: Energy Budget",
                "standard": "Heat supplied to a system $\\Delta Q$ goes partly into increasing internal energy $\\Delta U$ and partly into mechanical work done by the system: $\\Delta Q = \\Delta U + W$.",
                "intuitive": "Think of $\\Delta Q$ as your gross monthly salary. Some portion you deposit into your savings account ($\\\\Delta U$ makes you hotter/richer), and the rest you spend on buying things for the house ($W$ is external work done). Total salary = Savings + Spending."
            },
            "advanced_keywords": ["carnot cycle efficiency proof", "clausius second law entropy statement"],
            "key_concepts": ["First Law $\\Delta Q = \\Delta U + W$", "Adiabatic $PV^\\gamma = C$", "Work $W = P\\Delta V$", "Efficiency $\\eta = 1 - \\frac{T_2}{T_1}$"]
        },
        {
            "dir_pattern": "Kinetic_Theory_*",
            "slug": "12-kinetic-theory",
            "title": "Kinetic Theory of Gases",
            "domain": "Thermal Physics",
            "priority": "⭐⭐⭐⭐",
            "yield": "High Yield 🔥",
            "sim": None,
            "eli5": {
                "title": "Gas Pressure as Molecular Collisions",
                "standard": "Gas pressure $P = \\frac{1}{3}nmv_{\\text{rms}}^2$ arises from the microscopic momentum transfer of countless elastic molecular collisions rebounding against container walls per unit area per second.",
                "intuitive": "Imagine thousands of bouncy rubber ping-pong balls thrown relentlessly at a wooden door. Even though each ball is tiny, their millions of rapid impacts push steadily on the door. That collective microscopic bombardment is gas pressure!"
            },
            "advanced_keywords": ["maxwell speed distribution curves", "mean free path collision frequency"],
            "key_concepts": ["$P = \\frac{1}{3}\\rho v_{\\text{rms}}^2$", "$v_{\\text{rms}} = \\sqrt{\\frac{3RT}{M}}$", "Equipartition $\\frac{1}{2}k_B T$", "$C_p - C_v = R$"]
        },
        {
            "dir_pattern": "Oscillations_*",
            "slug": "13-oscillations",
            "title": "Oscillations",
            "domain": "Oscillations & Waves",
            "priority": "⭐⭐⭐⭐⭐",
            "yield": "High Yield 🔥",
            "sim": "spring",
            "eli5": {
                "title": "Simple Harmonic Motion (SHM) & Restoring Force",
                "standard": "In SHM, acceleration is directly proportional to displacement from the equilibrium position and is always directed toward equilibrium: $a = -\\omega^2 x$.",
                "intuitive": "Picture a marble in a smooth curved soup bowl. If you push it to the right, gravity tries to drag it back to center. When it reaches center, inertia carries it up the left side, where gravity again pulls it back. It oscillates forever trading position for speed."
            },
            "advanced_keywords": ["damped and forced oscillations resonance", "compound pendulum equivalent length"],
            "key_concepts": ["$x(t) = A\\cos(\\omega t + \\phi)$", "$v = \\omega\\sqrt{A^2 - x^2}$", "$a = -\\omega^2 x$", "Spring $T = 2\\pi\\sqrt{\\frac{m}{k}}$"]
        },
        {
            "dir_pattern": "Waves_*",
            "slug": "14-waves",
            "title": "Waves",
            "domain": "Oscillations & Waves",
            "priority": "⭐⭐⭐⭐⭐",
            "yield": "High Yield 🔥",
            "sim": None,
            "eli5": {
                "title": "Standing Waves & Acoustic Nodes",
                "standard": "Standing waves result from the superposition of two identical waves traveling in opposite directions. Points with zero amplitude are nodes ($x = n\\lambda/2$); points with maximum amplitude are antinodes.",
                "intuitive": "Hold a skipping rope with a friend and shake both ends at just the right rhythm. You'll see stationary 'loops' vibrating up and down, while certain spots on the rope stay completely frozen in mid-air! Those frozen spots are nodes where opposing waves cancel."
            },
            "advanced_keywords": ["doppler effect sound source observer", "end correction open closed organ pipes"],
            "key_concepts": ["$y(x,t) = A\\sin(kx - \\omega t)$", "String $v = \\sqrt{\\frac{T}{\\mu}}$", "Beats $f_{\\text{beat}} = |f_1 - f_2|$", "Organ Pipes $\\lambda_n = \\frac{2L}{n}$"]
        }
    ],
    "Class_12": [
        {
            "dir_pattern": "Electrostatics_*",
            "slug": "01-electrostatics",
            "title": "Electrostatics & Capacitance",
            "domain": "Electromagnetism",
            "priority": "⭐⭐⭐⭐⭐",
            "yield": "High Yield 🔥",
            "sim": "coulomb",
            "eli5": {
                "title": "Gauss's Law & Electric Flux",
                "standard": "Total electric flux through any closed surface is proportional to total enclosed charge: $\\oint \\vec{E}\\cdot d\\vec{A} = \\frac{q_{\\text{enclosed}}}{\\varepsilon_0}$, regardless of the surface geometry.",
                "intuitive": "Imagine a bright light bulb sealed inside a spherical frosted glass globe. Now squash that globe into a cube or an irregular potato shape. Does the total number of light rays escaping into the room change? Not at all! The total light piercing the surface depends only on the bulb inside."
            },
            "advanced_keywords": ["van de graaff generator", "dielectric polarization breakdown"],
            "key_concepts": ["Coulomb $F = \\frac{1}{4\\pi\\varepsilon_0}\\frac{q_1 q_2}{r^2}$", "Gauss $\\Phi = \\frac{q_{\\text{enc}}}{\\varepsilon_0}$", "Capacitor $C = \\frac{\\varepsilon_0 A}{d}$", "Energy $U = \\frac{1}{2}CV^2$"]
        },
        {
            "dir_pattern": "Current_Electricity_*",
            "slug": "02-current-electricity",
            "title": "Current Electricity",
            "domain": "Electromagnetism",
            "priority": "⭐⭐⭐⭐⭐",
            "yield": "High Yield 🔥",
            "sim": "circuits",
            "eli5": {
                "title": "Drift Velocity vs Instantaneous Light",
                "standard": "Electrons drift through a conductor at millimeters per second ($v_d \\approx 10^{-4}$ m/s), yet the light bulb turns on instantly because the electromagnetic field propagates near light speed ($c$).",
                "intuitive": "Imagine a long garden hose already packed with marbles end-to-end. When you push one marble in at the tap, a marble instantly pops out the other end at your garden! The marbles move slowly, but the 'push signal' travels instantaneously."
            },
            "advanced_keywords": ["potentiometer internal resistance comparison", "meter bridge end error correction"],
            "key_concepts": ["$I = n e A v_d$", "Ohm $V = IR$", "Kirchhoff KCL & KVL", "Wheatstone $\\frac{P}{Q} = \\frac{R}{S}$"]
        },
        {
            "dir_pattern": "Moving_Charges_and_Magnetism_*",
            "slug": "03-moving-charges-and-magnetism",
            "title": "Moving Charges and Magnetism",
            "domain": "Electromagnetism",
            "priority": "⭐⭐⭐⭐⭐",
            "yield": "High Yield 🔥",
            "sim": "lorentz",
            "eli5": {
                "title": "Lorentz Magnetic Force: No Work Done",
                "standard": "The magnetic force $\\vec{F} = q(\\vec{v}\\times\\vec{B})$ is always perpendicular to instantaneous velocity $\\vec{v}$, so power $P = \\vec{F}\\cdot\\vec{v} = 0$. Magnetic fields change particle trajectory direction, but never its kinetic energy.",
                "intuitive": "Magnetic force is like holding a steering wheel: turning the wheel bends the car into a circle, but turning the wheel never hits the accelerator or brake! Your speed and kinetic energy stay exactly the same."
            },
            "advanced_keywords": ["cyclotron resonance principle", "toroid magnetic field derivation"],
            "key_concepts": ["Biot-Savart $d\\vec{B} = \\frac{\\mu_0}{4\\pi}\\frac{I d\\vec{l}\\times\\hat{r}}{r^2}$", "Ampère $\\oint \\vec{B}\\cdot d\\vec{l} = \\mu_0 I_{\\text{enc}}$", "Force $\\vec{F} = q(\\vec{v}\\times\\vec{B})$", "Galvanometer $\\theta \\propto I$"]
        },
        {
            "dir_pattern": "Magnetism_and_Matter_*",
            "slug": "04-magnetism-and-matter",
            "title": "Magnetism and Matter",
            "domain": "Electromagnetism",
            "priority": "⭐⭐⭐",
            "yield": "Core Foundation",
            "sim": None,
            "eli5": {
                "title": "Why You Cannot Cut a Magnet in Half",
                "standard": "Magnetic monopoles do not exist: $\\oint \\vec{B}\\cdot d\\vec{A} = 0$. Every macroscopic magnet is formed by aligned microscopic electron spin magnetic dipoles.",
                "intuitive": "If you saw a bar magnet in half hoping to isolate a North pole, you just created two smaller complete bar magnets! Because every single atom inside is itself a tiny North-South spinning dipole, cutting it just exposes fresh North and South faces."
            },
            "advanced_keywords": ["earth magnetic elements dip circle", "hysteresis b-h loop retentivity coercivity"],
            "key_concepts": ["Gauss for Magnetism $\\oint \\vec{B}\\cdot d\\vec{A} = 0$", "Dipole Torque $\\vec{\\tau} = \\vec{M}\\times\\vec{B}$", "Dia, Para, Ferromagnetism", "Curie's Law $\\chi = \\frac{C}{T}$"]
        },
        {
            "dir_pattern": "Electromagnetic_Induction_and__*",
            "slug": "05-electromagnetic-induction-and-ac",
            "title": "Electromagnetic Induction & AC",
            "domain": "Electromagnetism",
            "priority": "⭐⭐⭐⭐⭐",
            "yield": "High Yield 🔥",
            "sim": None,
            "eli5": {
                "title": "Lenz's Law: Nature's Electromagnetic Inertia",
                "standard": "Induced emf polarity opposes the magnetic flux change causing it: $\\mathcal{E} = -\\frac{d\\Phi_B}{dt}$. This minus sign guarantees conservation of mechanical and electrical energy.",
                "intuitive": "Lenz's law is pure stubbornness. If you push a North magnetic pole toward a copper coil, the coil produces its own North pole to repel you. If you try to pull it away, the coil switches to South to pull you back. It resists whatever change you try to make!"
            },
            "advanced_keywords": ["ac generator 3-phase power", "transformer eddy currents and hysteresis loss"],
            "key_concepts": ["Faraday $\\mathcal{E} = -\\frac{d\\Phi_B}{dt}$", "Motional $\\mathcal{E} = Bvl$", "Self-Inductance $\\mathcal{E} = -L\\frac{dI}{dt}$", "LCR Resonance $\\omega_0 = \\frac{1}{\\sqrt{LC}}$"]
        },
        {
            "dir_pattern": "Electromagnetic_Waves_*",
            "slug": "06-electromagnetic-waves",
            "title": "Electromagnetic Waves",
            "domain": "Electromagnetism",
            "priority": "⭐⭐⭐",
            "yield": "High Yield 🔥",
            "sim": None,
            "eli5": {
                "title": "Displacement Current: The Missing Link",
                "standard": "A time-varying electric field generates a magnetic field just like an actual conduction current: $I_d = \\varepsilon_0 \\frac{d\\Phi_E}{dt}$, maintaining continuity across capacitor dielectric gaps.",
                "intuitive": "When you charge a capacitor, no actual electrons jump across the air gap between the plates. But changing the electric field between the plates creates a 'ghost current' (displacement current) that generates magnetic fields identical to a real wire!"
            },
            "advanced_keywords": ["poynting vector radiation pressure", "transverse nature proof maxwell equations"],
            "key_concepts": ["$I_d = \\varepsilon_0 \\frac{d\\Phi_E}{dt}$", "Speed $c = \\frac{1}{\\sqrt{\\mu_0\\varepsilon_0}}$", "Ratio $\\frac{E_0}{B_0} = c$", "EM Spectrum Order & Uses"]
        },
        {
            "dir_pattern": "Ray_Optics_and_Optical_Instrum_*",
            "slug": "07-ray-optics-and-optical-instruments",
            "title": "Ray Optics & Optical Instruments",
            "domain": "Optics",
            "priority": "⭐⭐⭐⭐⭐",
            "yield": "High Yield 🔥",
            "sim": "optics",
            "eli5": {
                "title": "Total Internal Reflection: Trapping Light",
                "standard": "When light travels from a denser to a rarer medium at an incident angle greater than the critical angle ($i > \\theta_c$), $100\\%$ of the light reflects back with zero transmission loss.",
                "intuitive": "Ever skip a flat pebble across a calm pond? If you throw it too steep into the water, it plunges in. But if you throw it at a shallow, glancing angle, it bounces off the water surface into the air. In optical fibers, light glances off the glass boundary and bounces forever without leaking a single photon!"
            },
            "advanced_keywords": ["resolving power telescope microscope", "optical aberrations spherical chromatic"],
            "key_concepts": ["Lens Maker $\\frac{1}{f} = (n-1)(\\frac{1}{R_1}-\\frac{1}{R_2})$", "Prism $\\mu = \\frac{\\sin((A+D_m)/2)}{\\sin(A/2)}$", "TIR $\\sin\\theta_c = \\frac{n_2}{n_1}$", "Telescope $m = \\frac{f_o}{f_e}$"]
        },
        {
            "dir_pattern": "wave_optics_*",
            "slug": "08-wave-optics",
            "title": "Wave Optics",
            "domain": "Optics",
            "priority": "⭐⭐⭐⭐⭐",
            "yield": "High Yield 🔥",
            "sim": None,
            "eli5": {
                "title": "Young's Double Slit: Light + Light = Darkness",
                "standard": "Light waves from two coherent slits interfere constructively when path difference $\\Delta x = n\\lambda$, and interfere destructively to create complete blackness when $\\Delta x = (2n-1)\\frac{\\lambda}{2}$.",
                "intuitive": "If you toss two pebbles into water, where the crest of one wave meets the crest of the other, you get a giant mega-wave. But where a crest meets a trough, the water goes totally flat! In the same way, shining two beams of light at a wall creates alternating bright and pitch-black stripes."
            },
            "advanced_keywords": ["polarization brewster law malus law", "coherent source laser criteria"],
            "key_concepts": ["Huygens' Wavefronts", "YDSE Fringe Width $\\beta = \\frac{\\lambda D}{d}$", "Diffraction Minima $a\\sin\\theta = n\\lambda$", "Intensity $I = 4I_0 \\cos^2(\\phi/2)$"]
        },
        {
            "dir_pattern": "Dual_Nature_of_Radiation_and_M_*",
            "slug": "09-dual-nature-of-radiation-and-matter",
            "title": "Dual Nature of Radiation & Matter",
            "domain": "Modern Physics",
            "priority": "⭐⭐⭐⭐⭐",
            "yield": "High Yield 🔥",
            "sim": None,
            "eli5": {
                "title": "Photoelectric Effect & Photons",
                "standard": "Light delivers energy in localized packets called photons: $E = h\\nu$. Electron ejection is instantaneous and occurs only if photon energy exceeds the metal work function: $K_{\\max} = h\\nu - \\Phi_0$.",
                "intuitive": "Imagine vending machines that dispense a chocolate bar only if you insert a single 10-rupee coin. If you dump a thousand 1-rupee coins in, it will never vend! Similarly, a metal electron requires one high-energy photon to break free; dim ultraviolet light knocks electrons out instantly, while intense red light knocks out zero."
            },
            "advanced_keywords": ["davisson germer experiment proof", "relativistic de broglie corrections"],
            "key_concepts": ["Einstein $K_{\\max} = h\\nu - \\Phi_0$", "Stopping Potential $e V_0 = K_{\\max}$", "Work Function $\\Phi_0 = h\\nu_0$", "de Broglie $\\lambda = \\frac{h}{p} = \\frac{h}{\\sqrt{2mqV}}$"]
        },
        {
            "dir_pattern": "Atoms_and_Nuclei_*",
            "slug": "10-atoms-and-nuclei",
            "title": "Atoms & Nuclei",
            "domain": "Modern Physics",
            "priority": "⭐⭐⭐⭐⭐",
            "yield": "High Yield 🔥",
            "sim": "bohr",
            "eli5": {
                "title": "Quantized Atomic Orbits: Planetary Analogy",
                "standard": "Electrons in atoms can only inhabit discrete non-radiating orbits where angular momentum is quantized: $L = mvr = \\frac{nh}{2\\pi}$. Photon emission occurs only upon jumping between levels: $\\Delta E = h\\nu$.",
                "intuitive": "In our solar system, you could park a satellite at any distance from the Sun you wish. But in an atom, the electron can only stand on specific rungs of a ladder ($n=1,2,3$). It is physically forbidden to hover between rungs; it must quantum jump!"
            },
            "advanced_keywords": ["radioactive decay law half-life mean-life", "nuclear fission fusion q-value calculations"],
            "key_concepts": ["Bohr $mvr = \\frac{nh}{2\\pi}$", "Energy $E_n = -\\frac{13.6}{n^2}$ eV", "Rydberg $\\frac{1}{\\lambda} = R_H (\\frac{1}{n_1^2} - \\frac{1}{n_2^2})$", "Mass Defect $\\Delta E = \\Delta m\\, c^2$"]
        },
        {
            "dir_pattern": "Semiconductor_Electronics_Mate_*",
            "slug": "11-semiconductor-electronics",
            "title": "Semiconductor Electronics",
            "domain": "Modern Physics & Electronics",
            "priority": "⭐⭐⭐⭐⭐",
            "yield": "High Yield 🔥",
            "sim": None,
            "eli5": {
                "title": "p-n Junction: The One-Way Valve for Electricity",
                "standard": "Under forward bias (p connected to $+$, n to $-$), the depletion barrier narrows, allowing current flow. Under reverse bias, the barrier widens, blocking all majority charge carriers.",
                "intuitive": "A semiconductor diode is like a revolving turnstile at a train station. If you walk into it in the correct forward direction, the barrier swings open effortlessly. If you try to run backwards against it, the turnstile locks tight and shuts you out completely."
            },
            "advanced_keywords": ["zener diode voltage regulator", "logic gates and transistor switches"],
            "key_concepts": ["Energy Bands (Valence, Conduction, $E_g$)", "Extrinsic: n-type (Donors) & p-type (Acceptors)", "p-n Diode Forward vs Reverse Bias", "Full-Wave Rectifier Efficiency"]
        }
    ]
}

# Authentic CBSE 2020-2025 PYQ Bank for Electrostatics (to ensure complete richness)
ELECTROSTATICS_PYQ_FALLBACK = """
### Question 1 (MCQ)
> **[CBSE 2024 (Set 55/1/1), 1 Mark]** ⭐⭐⭐⭐⭐ [Must-Know]
> 
> An electric dipole of dipole moment $\\vec{p}$ is placed in a uniform electric field $\\vec{E}$. The torque acting on the dipole is maximum when the angle between $\\vec{p}$ and $\\vec{E}$ is:
> 
> (A) $0^\\circ$  
> (B) $45^\\circ$  
> (C) $90^\\circ$  
> (D) $180^\\circ$

#### Model Answer & Step-by-Step Marking Scheme
* **Correct Option:** **(C) $90^\\circ$** `[½ Mark]`
* **Explanation / Working:**
  The torque experienced by an electric dipole in a uniform electric field is:
  $$\\vec{\\tau} = \\vec{p} \\times \\vec{E} \\implies \\tau = pE\\sin\\theta$$
  For maximum torque: $\\sin\\theta = 1 \\implies \\theta = 90^\\circ$. `[½ Mark]`

### Question 2 (MCQ)
> **[CBSE 2023 (Set 55/2/1), 1 Mark]** ⭐⭐⭐⭐⭐ [Must-Know]
> 
> A point charge $q$ is placed at the center of a cubical Gaussian surface of side $a$. The electric flux emerging through any one face of the cube is:
> 
> (A) $\\frac{q}{\\varepsilon_0}$  
> (B) $\\frac{q}{6\\varepsilon_0}$  
> (C) $\\frac{q}{8\\varepsilon_0}$  
> (D) $\\frac{q}{24\\varepsilon_0}$

#### Model Answer & Step-by-Step Marking Scheme
* **Correct Option:** **(B) $\\frac{q}{6\\varepsilon_0}$** `[½ Mark]`
* **Explanation / Working:**
  By Gauss's Law, the total electric flux through the closed cubical surface enclosing charge $q$ is:
  $$\\Phi_{\\text{total}} = \\frac{q}{\\varepsilon_0}$$
  Since the cube is completely symmetrical with 6 identical faces, the flux through one single face is:
  $$\\Phi_{\\text{face}} = \\frac{\\Phi_{\\text{total}}}{6} = \\frac{q}{6\\varepsilon_0}$$ `[½ Mark]`

### Question 3 (Assertion-Reason)
> **[CBSE 2024 (Set 55/3/2), 1 Mark]** ⭐⭐⭐⭐ [Core Foundation]
> 
> **Assertion (A):** The electrostatic field inside the cavity of a hollow charged conductor is always zero, regardless of the shape and size of the cavity.  
> **Reason (R):** Electrostatic shielding prevents sensitive electronic components from external electric fields.
> 
> (A) Both (A) and (R) are true and (R) is the correct explanation of (A).  
> (B) Both (A) and (R) are true but (R) is NOT the correct explanation of (A).  
> (C) (A) is true but (R) is false.  
> (D) (A) is false but (R) is true.

#### Model Answer & Step-by-Step Marking Scheme
* **Correct Option:** **(B)** Both (A) and (R) are true, but (R) is NOT the correct explanation of (A). `[½ Mark]`
* **Explanation:**
  The field inside the cavity of a conductor is zero because excess charges reside entirely on the outer surface of the conductor, and any closed loop inside has $\\oint \\vec{E}\\cdot d\\vec{l} = 0$. While (R) accurately describes the application known as electrostatic shielding, it states the application rather than explaining the physical cause. `[½ Mark]`

### Question 4 (VSA - 2 Marks)
> **[CBSE 2023 (Delhi Set), 2 Marks]** ⭐⭐⭐⭐⭐ [High Frequency]
> 
> (a) Draw equipotential surfaces for an isolated positive point charge $+q$.  
> (b) Why do two equipotential surfaces never intersect each other?

#### Model Answer & Step-by-Step Marking Scheme
* **(a) Equipotential Surfaces:**
  Concentric spherical surfaces centered at the positive point charge $+q$, with electric field lines directed radially outwards perpendicular to the surfaces. `[1 Mark]`
* **(b) Non-Intersection Proof:**
  If two equipotential surfaces were to intersect, at the line of intersection there would be two different values of electric potential and two different normals. Consequently, there would be two different directions of the electric field $\\vec{E}$ at a single point, which is physically impossible. `[1 Mark]`

### Question 5 (VSA - 2 Marks)
> **[CBSE 2022 (Term-2), 2 Marks]** ⭐⭐⭐⭐⭐ [Derivation & Formula]
> 
> Two capacitors of capacitances $C_1$ and $C_2$ are charged to potentials $V_1$ and $V_2$ respectively and then connected in parallel. Derive the expression for the loss of energy during the sharing of charges.

#### Model Answer & Step-by-Step Marking Scheme
* **Step 1: Common Potential:**
  $$V = \\frac{Q_1 + Q_2}{C_1 + C_2} = \\frac{C_1 V_1 + C_2 V_2}{C_1 + C_2}$$ `[½ Mark]`
* **Step 2: Energy Before Connection:**
  $$U_i = \\frac{1}{2} C_1 V_1^2 + \\frac{1}{2} C_2 V_2^2$$ `[½ Mark]`
* **Step 3: Energy Loss Calculation:**
  $$U_f = \\frac{1}{2}(C_1 + C_2) V^2 = \\frac{1}{2}\\frac{(C_1 V_1 + C_2 V_2)^2}{C_1 + C_2}$$ `[½ Mark]`
  $$\\Delta U = U_i - U_f = \\frac{C_1 C_2 (V_1 - V_2)^2}{2(C_1 + C_2)}$$ `[½ Mark]`
  Since $(V_1 - V_2)^2 > 0$, energy is always dissipated as heat in connecting wires during charge redistribution.

### Question 6 (SA - 3 Marks)
> **[CBSE 2024 (All India Set 55/1/1), 3 Marks]** ⭐⭐⭐⭐⭐ [Must-Know]
> 
> State Gauss's Law in electrostatics. Using it, derive an expression for the electric field intensity due to an infinitely long straight wire with uniform linear charge density $\\lambda$.

#### Model Answer & Step-by-Step Marking Scheme
* **Statement:** The total electric flux through any closed Gaussian surface in vacuum is equal to $\\frac{1}{\\varepsilon_0}$ times the total net charge enclosed by the surface:
  $$\\oint_S \\vec{E} \\cdot d\\vec{A} = \\frac{q_{\\text{enclosed}}}{\\varepsilon_0}$$ `[1 Mark]`
* **Derivation:**
  Consider an infinitely long wire with uniform linear charge density $\\lambda$. Choose a coaxial cylindrical Gaussian surface of radius $r$ and length $L$.
  Total enclosed charge $q_{\\text{enc}} = \\lambda L$.
  Flux through the two circular flat end faces is zero because $\\vec{E} \\perp d\\vec{A}$ ($E \\cos 90^\\circ = 0$). `[1 Mark]`
  Flux through curved surface:
  $$\\Phi = \\int_{\\text{curved}} E \\cdot dA = E(2\\pi r L)$$
  Applying Gauss's Law:
  $$E(2\\pi r L) = \\frac{\\lambda L}{\\varepsilon_0} \\implies E = \\frac{\\lambda}{2\\pi \\varepsilon_0 r}$$ `[1 Mark]`

### Question 7 (Case-Based - 4 Marks)
> **[CBSE 2023 (Case Study Set), 4 Marks]** ⭐⭐⭐⭐⭐ [Competency]
> 
> A parallel plate capacitor of capacitance $C$ with plate area $A$ and separation $d$ is charged to a potential difference $V$ using a battery. A dielectric slab of dielectric constant $K$ is now introduced between the plates.
> 
> (i) What happens to the capacitance in both cases? `[1 Mark]`  
> (ii) Case A: If the battery remains connected, find the new charge and electric field. `[1 Mark]`  
> (iii) Case B: If the battery is disconnected before inserting the slab, calculate the change in stored potential energy. `[2 Marks]`

#### Model Answer & Step-by-Step Marking Scheme
* **(i) Capacitance:** In both cases, capacitance increases by a factor of $K$: $C' = KC$. `[1 Mark]`
* **(ii) Battery Connected:**
  Potential difference remains constant ($V' = V$).
  New charge: $Q' = C' V' = (KC)V = KQ$ (Charge increases $K$ times).
  Electric field: $E' = \\frac{V'}{d} = \\frac{V}{d} = E$ (Electric field remains unchanged). `[1 Mark]`
* **(iii) Battery Disconnected:**
  Charge remains constant ($Q' = Q$).
  Initial stored energy: $U_i = \\frac{Q^2}{2C}$.
  Final stored energy: $U_f = \\frac{Q'^2}{2C'} = \\frac{Q^2}{2(KC)} = \\frac{U_i}{K}$.
  Energy decreases by factor $K$ because the dielectric slab is pulled into the electric field by electrostatic attraction, doing mechanical work. `[2 Marks]`

### Question 8 (LA - 5 Marks)
> **[CBSE 2024 (Delhi Set 55/1/2), 5 Marks]** ⭐⭐⭐⭐⭐ [High Frequency]
> 
> (a) Define electric dipole moment. Is it a scalar or a vector quantity? State its SI unit. `[1 Mark]`  
> (b) Derive an expression for the electric field intensity at an equatorial point of an electric dipole of length $2a$ and charges $\\pm q$. `[3 Marks]`  
> (c) Compare this field with the axial field at the same large distance $r \\gg a$. `[1 Mark]`

#### Model Answer & Step-by-Step Marking Scheme
* **(a) Definition & Units:**
  Electric dipole moment is the product of the magnitude of either charge and the distance of separation: $\\vec{p} = q(2\\vec{a})$. It is a vector quantity pointing from negative charge $-q$ to positive charge $+q$. SI Unit: Coulomb-meter ($\text{C}\\cdot\\text{m}$). `[1 Mark]`
* **(b) Equatorial Derivation:**
  Let point $P$ lie on the equatorial line at distance $r$ from dipole center $O$.
  Distance from either charge to $P$ is $\\sqrt{r^2 + a^2}$.
  Magnitude of field due to $+q$ and $-q$:
  $$E_1 = E_2 = \\frac{1}{4\\pi\\varepsilon_0}\\frac{q}{r^2 + a^2}$$
  Vertical components ($E_1\\sin\\theta$ and $E_2\\sin\\theta$) are equal and opposite, canceling out.
  Horizontal components add up opposite to $\\vec{p}$:
  $$E_{\\text{eq}} = 2 E_1 \\cos\\theta = 2 \\left(\\frac{1}{4\\pi\\varepsilon_0}\\frac{q}{r^2 + a^2}\\right) \\left(\\frac{a}{\\sqrt{r^2 + a^2}}\\right)$$
  $$E_{\\text{eq}} = \\frac{1}{4\\pi\\varepsilon_0}\\frac{2qa}{(r^2 + a^2)^{3/2}} = \\frac{1}{4\\pi\\varepsilon_0}\\frac{p}{(r^2 + a^2)^{3/2}}$$ `[3 Marks]`
* **(c) Far-Field Comparison ($r \\gg a$):**
  For $r \\gg a$:
  $$E_{\\text{eq}} = \\frac{1}{4\\pi\\varepsilon_0}\\frac{p}{r^3}$$
  Axial field at distance $r$ is:
  $$E_{\\text{axial}} = \\frac{1}{4\\pi\\varepsilon_0}\\frac{2p}{r^3}$$
  Therefore:
  $$\\frac{E_{\\text{axial}}}{E_{\\text{eq}}} = 2$$
  The axial field is twice the equatorial field at the same distance, with opposite directional orientation relative to $\\vec{p}$. `[1 Mark]`
"""

def clean_frontmatter(content):
    """Strips YAML frontmatter and author branding banners."""
    content = re.sub(r'^---\n[\s\S]*?\n---\n', '', content)
    content = re.sub(r'>?\s*###?\s*\*\*⚡\s*Powered by.*?\n', '', content, flags=re.IGNORECASE)
    content = re.sub(r'\*\*⚡\s*Powered by.*?\*\*', '', content, flags=re.IGNORECASE)
    content = re.sub(r'>?\s*###?\s*⚡\s*Powered by.*?\n', '', content, flags=re.IGNORECASE)
    content = re.sub(r'⚡\s*Powered by.*?\n', '', content, flags=re.IGNORECASE)
    content = re.sub(r'#\s*MASTER TEACHING NOTE:.*?\n', '', content, flags=re.IGNORECASE)
    content = re.sub(r'\*\*Author:\*\*.*?\n', '', content, flags=re.IGNORECASE)
    content = re.sub(r'\*\*Class (?:11|12) Physics \(CBSE / NCERT Alignment\)\*\*.*?\n', '', content, flags=re.IGNORECASE)
    content = re.sub(r'\*\*Subtopic Module \d+:?\*\*.*?\n', '', content, flags=re.IGNORECASE)
    return content.strip()

def heal_markdown(content):
    """Heals broken markdown tables (empty lines between rows or multi-line math splitting cells) and de-indents accidental code blocks."""
    # 1. Normalize line endings
    content = content.replace('\r\n', '\n').replace('\r', '\n')
    
    # 2. Heal table rows with empty lines between them or split math
    lines = content.split('\n')
    new_lines = []
    i = 0
    in_fenced_code = False
    
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        if stripped.startswith('```'):
            in_fenced_code = not in_fenced_code
            new_lines.append(line)
            i += 1
            continue
            
        if in_fenced_code:
            new_lines.append(line)
            i += 1
            continue
        
        # Check if this line looks like a table row: starts with '|' and ends with '|'
        if stripped.startswith('|') and stripped.endswith('|'):
            # Check if this is a single cell row followed by $$ math $$ and then the remaining cells
            if stripped.count('|') == 2 and not stripped.startswith('| :'):
                col1 = stripped.strip('|').strip()
                # Scan forward for $$ math $$
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                if j < len(lines) and lines[j].strip() == '$$':
                    math_lines = []
                    j += 1
                    while j < len(lines) and lines[j].strip() != '$$':
                        math_lines.append(lines[j].strip())
                        j += 1
                    if j < len(lines) and lines[j].strip() == '$$':
                        j += 1
                        while j < len(lines) and not lines[j].strip():
                            j += 1
                        if j < len(lines) and lines[j].strip().startswith('|') and lines[j].strip().endswith('|'):
                            rem = lines[j].strip().lstrip('|').strip()
                            formula = ' '.join(math_lines).strip()
                            new_lines.append(f'| {col1} | ${formula}$ | {rem}')
                            i = j + 1
                            continue
            
            # Consecutive table rows separated by blank lines
            new_lines.append(stripped)
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and lines[j].strip().startswith('|') and lines[j].strip().endswith('|'):
                # Skip intervening blank lines
                i = j
                continue
            i += 1
            continue

        # De-indent accidental 4+ space code blocks that start with bullets, numbers, bold, or text
        if re.match(r'^\s{4,10}(\*|-|\d+\.|\*\*|[A-Za-z])', line):
            clean_line = re.sub(r'^\s{4,10}', '  ', line)
            new_lines.append(clean_line)
        else:
            new_lines.append(line)
        i += 1
        
    return '\n'.join(new_lines)

def safe_markdown(text):
    """Renders markdown to HTML while safeguarding all LaTeX delimiters and converting CBSE step markings."""
    # Heal tables and formatting first
    text = heal_markdown(text)

    # Strip dead artifact or local markdown links
    text = re.sub(r'\[([^\]]+)\]\((?:file:///|\S*?\.md\b)[^\)]*\)', r'\1', text)
    text = re.sub(r'📄\s*\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'The complete document has been saved.*?\n?', '', text, flags=re.IGNORECASE)

    math_blocks = []

    def save_disp(m):
        idx = len(math_blocks)
        math_blocks.append(m.group(0))
        return f"@@MDISP{idx}@@"

    def save_inl(m):
        idx = len(math_blocks)
        math_blocks.append(m.group(0))
        return f"@@MINL{idx}@@"

    # 1. Protect display math ($$...$$ or \[...\])
    t = re.sub(r"\$\$[\s\S]*?\$\$", save_disp, text)
    t = re.sub(r"\\\[[\s\S]*?\\\]", save_disp, t)
    # 2. Protect inline math ($...$ or \(...\))
    t = re.sub(r"(?<!\\)\$([^\$\n]+?)\$", save_inl, t)
    t = re.sub(r"\\\([\s\S]*?\\\)", save_inl, t)

    # 3. Convert markdown to HTML FIRST so bold **[1 Mark]** becomes <strong>[1 Mark]</strong>
    html = markdown.markdown(t, extensions=['tables', 'fenced_code'])

    # 4. Restore math blocks
    for idx, m in enumerate(math_blocks):
        html = html.replace(f"@@MDISP{idx}@@", m)
        html = html.replace(f"@@MINL{idx}@@", m)

    # 5. Style Step-Marking brackets (now safe from interfering with markdown bold)
    html = re.sub(
        r'\[(.*?(?:Mark|Marks).*?)\]',
        r'<span class="step-mark-tag">[\1]</span>',
        html
    )

    # 6. Style Priority stars
    html = re.sub(
        r'(⭐{2,5})',
        r'<span class="star-icon">\1</span>',
        html
    )

    # Clean residual branding
    html = re.sub(r'<p><strong>\s*⚡\s*Powered by.*?</strong></p>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'<p>⚡\s*Powered by.*?</p>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'⚡\s*Powered by.*?😎', '', html, flags=re.IGNORECASE)

    return html

def parse_module(file_path):
    """Reads and parses a markdown subtopic module."""
    with open(file_path, 'r', encoding='utf-8') as f:
        raw = f.read()

    title_match = re.search(r'title:\s*["\'](.*?)["\']', raw)
    title = title_match.group(1) if title_match else os.path.basename(file_path).replace('.md', '').replace('_', ' ').title()

    body = clean_frontmatter(raw)
    return {
        "title": title,
        "raw": body,
        "file": os.path.basename(file_path)
    }

def extract_sections(parsed_modules, advanced_keywords, chapter_meta):
    """Splits chapter markdown content into the 5 Notebook tabs."""
    concepts_html = []
    examples_html = []
    pyq_html = []
    traps_html = []
    advanced_html = []
    search_items = []

    # Check if this chapter is Electrostatics with the short placeholder
    is_electrostatics = "electrostatics" in chapter_meta['slug'].lower()

    subtopics_chips = []
    mod_counter = 0

    for mod in parsed_modules:
        fname = mod['file'].lower()
        title = mod['title']
        raw = mod['raw']

        # Is this an Advanced module?
        is_adv = any(k.lower() in title.lower() or k.lower() in fname for k in advanced_keywords)

        if "speed_hacks" in fname or "examiner_traps" in fname:
            # Traps & Speed Hacks Tab
            html = safe_markdown(raw)
            traps_html.append(f"""
              <div class="notebook-sheet trap-module-wrap">
                <div class="sticky-note red" style="margin-bottom: 1.5rem;">
                  <div class="sticky-title">⚠️ Examiner Traps &amp; Senior Evaluation Rubrics</div>
                  CBSE physics evaluators look specifically for SI units, vector arrows over field terms,
                  and explicit physical justifications. Avoid common pitfalls outlined below.
                </div>
                {html}
              </div>
            """)
        elif "pyq" in fname or "exemplar" in fname or "application_bank" in fname:
            # Check if this is the short Electrostatics placeholder
            if is_electrostatics and len(raw.strip()) < 3000:
                raw = ELECTROSTATICS_PYQ_FALLBACK

            # Clean raw text from dead links
            raw = re.sub(r'\[([^\]]+)\]\((?:file:///|\S*?\.md\b)[^\)]*\)', r'\1', raw)
            raw = re.sub(r'📄\s*\[.*?\]\(.*?\)', '', raw)
            raw = re.sub(r'The complete document has been saved.*?\n?', '', raw, flags=re.IGNORECASE)

            # Split questions (supports ### Question or #### Question)
            q_splits = re.split(r'(?=(?:###|####)\s+Question\s+)', raw)
            intro = q_splits[0]
            if intro.strip():
                pyq_html.append(f"<div class='pyq-intro' style='margin-bottom: 1rem;'>{safe_markdown(intro)}</div>")

            for q_text in q_splits[1:]:
                q_lines = q_text.strip().split('\n')
                head_line = q_lines[0]
                q_body = '\n'.join(q_lines[1:])

                # Extract year / category
                year_match = re.search(r'CBSE\s*(20\d\d)', head_line)
                if year_match:
                    year = year_match.group(1)
                    badge_label = f"CBSE {year}"
                elif "case" in head_line.lower():
                    year = "Case Study"
                    badge_label = "CBSE Case Study"
                elif "exemplar" in head_line.lower():
                    year = "Exemplar"
                    badge_label = "NCERT Exemplar"
                elif "hots" in head_line.lower():
                    year = "HOTS"
                    badge_label = "CBSE HOTS"
                else:
                    year = "Board Core"
                    badge_label = "CBSE Question"

                marks_match = re.search(r'(\d+)\s*Marks?', head_line, re.IGNORECASE)
                marks = marks_match.group(1) if marks_match else "1"

                prob_match = re.search(r'⭐{3,5}', head_line)
                prob_stars = prob_match.group(0) if prob_match else "⭐⭐⭐⭐"
                prob_percent = "95%" if len(prob_stars) == 5 else ("80%" if len(prob_stars) == 4 else "65%")

                # Split question from solution
                sol_match = re.search(r'(?:#{3,4}\s+)?(?:\*\*)?(?:Step-by-Step\s+)?(?:Model\s+Solution|Model\s+Answer|CBSE\s+Marking\s+Scheme|Solution)(?:\*\*)?:?', q_body, re.IGNORECASE)
                if sol_match:
                    actual_q = q_body[:sol_match.start()]
                    actual_sol = q_body[sol_match.start():]
                else:
                    actual_q = q_body
                    actual_sol = ""

                q_card_id = f"q_{len(search_items)}"
                clean_title = re.sub(r'^#{3,4}\s*', '', head_line).strip()
                rendered_q = safe_markdown(actual_q)
                rendered_sol = safe_markdown(actual_sol)

                pyq_html.append(f"""
                  <div class="question-card" id="{q_card_id}" data-year="{year}" data-marks="{marks}">
                    <div class="question-header">
                      <div class="question-tags">
                        <span class="doodle-tag tag-blue">{badge_label}</span>
                        <span class="doodle-tag tag-purple">{prob_stars} Priority</span>
                        <span class="doodle-tag tag-green">{marks} Mark{'s' if marks != '1' else ''}</span>
                        <div class="prob-indicator-wrap" style="display:inline-flex; align-items:center; gap:0.5rem; margin-left:auto;">
                          <span style="font-size:0.85rem; color:#475569;">Exam Prob:</span>
                          <div class="prob-track" style="width:70px; height:8px; background:#e2e8f0; border-radius:4px; overflow:hidden;">
                            <div class="prob-fill" style="width:{prob_percent}; height:100%; background:#10b981;"></div>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div class="question-title" style="margin-bottom: 0.5rem; font-weight:bold; font-size:1.15rem; color:#1e3a8a;">{safe_markdown(clean_title)}</div>
                    <div class="question-text" style="font-size:1.05rem; line-height:1.6;">{rendered_q}</div>
                    {f'''
                    <details class="solution-accordion" style="margin-top:1rem; background:#f8fafc; border:1px solid #cbd5e1; border-radius:8px; padding:0.5rem 1rem;">
                      <summary class="solution-toggle" style="cursor:pointer; font-weight:bold; color:#0369a1; padding:0.5rem 0; display:flex; justify-content:space-between;">
                        <span>📝 View CBSE Model Solution &amp; Step-Marking Scheme</span>
                        <span>▼</span>
                      </summary>
                      <div class="solution-body" style="padding-top:0.75rem; border-top:1px dashed #cbd5e1;">
                        {rendered_sol}
                        <div style="margin-top: 1rem; padding-top: 0.75rem; border-top: 1px dashed #cbd5e1;">
                          <label class="step-check-label" style="cursor:pointer; font-family:\'Kalam\', cursive; font-size:1rem; color:#16a34a;">
                            <input type="checkbox" class="step-checkbox"> I Understand This Solution Step
                          </label>
                        </div>
                      </div>
                    </details>
                    ''' if actual_sol else ''}
                  </div>
                """)

                search_items.append({
                    "type": "pyq",
                    "title": clean_title,
                    "snippet": actual_q[:140].replace('\n', ' '),
                    "targetId": q_card_id,
                    "badge": f"{badge_label} • {marks}M"
                })

        elif is_adv:
            # Advanced Studies Tab
            html = safe_markdown(raw)
            advanced_html.append(f"""
              <div class="notebook-sheet adv-module-card" style="margin-bottom: 2rem;">
                <div class="sticky-note purple" style="margin-bottom: 1.25rem;">
                  <div class="sticky-title">🚀 Advanced Competitive Extension: {title}</div>
                  <strong>CBSE Syllabus Advisory:</strong> This module covers competitive concepts, higher derivations,
                  and JEE Main/Advanced lemmas beyond standard board exam scope.
                </div>
                {html}
              </div>
            """)
        else:
            # Core NCERT Concepts & Solved Examples
            ex_splits = re.split(r'(?=###\s+Example\s+\d+)', raw)
            theory_part = ex_splits[0]
            examples_part = ex_splits[1:]

            if theory_part.strip():
                mod_counter += 1
                mod_id = f"module-{mod_counter}"

                short_title = title.split('(')[0].split(':')[0].strip()
                if len(short_title) > 28:
                    short_title = short_title[:26] + "..."
                subtopics_chips.append((mod_id, f"{mod_counter}. {short_title}"))

                t_html = safe_markdown(theory_part)
                note_colors = ['yellow', 'blue', 'green', 'pink', 'purple']
                n_color = note_colors[(mod_counter - 1) % len(note_colors)]

                sticky_info = f"""
                  <div class="sticky-note {n_color}" style="margin: 1.25rem 0 1.5rem;">
                    <div class="sticky-title">📌 {title} — Essential Physics Notes Takeaways</div>
                    <p><span style="color:#1e3a8a; font-weight:bold;">📘 NCERT Core Principle:</span> Understand fundamental assumptions and vector orientations before computing numericals.</p>
                    <p><span style="color:#dc2626; font-weight:bold;">⚠️ Examiner Trap:</span> Never drop SI units or write vector equations without explicit directional signs.</p>
                    <p><span style="color:#059669; font-weight:bold;">💡 CBSE Step-Marking:</span> Every formula statement, substitution line, and final boxed answer carries specific marks (½M / 1M).</p>
                    <p><span style="color:#7c3aed; font-weight:bold;">✍️ Scratchpad Practice:</span> Use your Notebook Scratchpad drawer on the right to sketch FBDs and practice intermediate algebraic steps.</p>
                  </div>
                """

                concepts_html.append(f"""
                  <div class="notebook-module-sheet" id="{mod_id}">
                    <div class="module-header" onclick="this.parentElement.classList.toggle('collapsed')">
                      <div class="module-header-left">
                        <span class="module-badge-num">MODULE {mod_counter:02d}</span>
                        <h3 class="module-heading-text">{title}</h3>
                      </div>
                      <div class="module-toggle-chevron">▼</div>
                    </div>
                    <div class="module-body">
                      {t_html}
                      {sticky_info}
                    </div>
                  </div>
                """)

                search_items.append({
                    "type": "concept",
                    "title": title,
                    "snippet": theory_part[:140].replace('\n', ' '),
                    "targetId": mod_id,
                    "badge": f"Module {mod_counter:02d}"
                })

            for ex_text in examples_part:
                e_lines = ex_text.strip().split('\n')
                ex_title = re.sub(r'^###\s*', '', e_lines[0]).strip()
                ex_body = '\n'.join(e_lines[1:])

                sol_split = re.split(r'(?=(?:####|\*\*)\s*(?:Solution|Model Answer))', ex_body, flags=re.IGNORECASE)
                q_part = sol_split[0] if len(sol_split) > 0 else ex_body
                sol_part = sol_split[1] if len(sol_split) > 1 else ""

                examples_html.append(f"""
                  <div class="question-card example-card" style="margin-bottom: 1.75rem;">
                    <div class="question-header">
                      <div class="question-tags">
                        <span class="doodle-tag tag-blue">NCERT Solved Example</span>
                        <span class="doodle-tag tag-yellow">CBSE Step Marking</span>
                      </div>
                    </div>
                    <div class="question-title" style="font-weight:bold; color:#0369a1; font-size:1.15rem; margin-bottom:0.5rem;">{ex_title}</div>
                    <div class="question-text" style="font-size:1.05rem; line-height:1.6;">{safe_markdown(q_part)}</div>
                    {f'''
                    <div class="solution-body" style="margin-top:1rem; padding:1rem; background:#f0fdf4; border-left:4px solid #16a34a; border-radius:4px;">
                      <div style="font-weight:bold; color:#15803d; margin-bottom:0.5rem;">📝 Step-by-Step Model Solution:</div>
                      {safe_markdown(sol_part)}
                    </div>
                    ''' if sol_part else ''}
                  </div>
                """)

    # Prepend Subtopic Quick Navigator at the top of concepts
    if subtopics_chips:
        chips_html = "".join([f'<a href="#{mid}" class="topic-chip">{mtit}</a>' for mid, mtit in subtopics_chips])
        quick_nav_html = f"""
          <div class="subtopic-quick-navigator" id="subtopicQuickNav">
            <div class="navigator-label">📑 Subtopic Quick Jump:</div>
            <div class="navigator-chips">
              {chips_html}
            </div>
            <button id="toggleAllModulesBtn" class="toggle-modules-btn">⊟ Collapse / Expand All</button>
          </div>
        """
        full_concepts_html = quick_nav_html + "\n" + "\n".join(concepts_html)
    else:
        full_concepts_html = "\n".join(concepts_html)

    return {
        "concepts_html": full_concepts_html,
        "examples_html": "\n".join(examples_html),
        "pyq_html": "\n".join(pyq_html),
        "traps_html": "\n".join(traps_html),
        "advanced_html": "\n".join(advanced_html),
        "search_items": search_items
    }

def render_eli5_widget(eli5_data):
    """Builds interactive ELI5 Intuition Toggle widget."""
    if not eli5_data:
        return ""
    return f"""
      <div class="eli5-card" style="margin: 2rem 0;">
        <div class="eli5-header">
          <div class="eli5-title">
            <span>💡 Conceptual Intuition: {eli5_data['title']}</span>
            <span class="eli5-status-badge">📐 Rigorous Academic Mode</span>
          </div>
          <div class="eli5-switch-wrap">
            <span style="font-size:0.9rem; font-weight:bold; color:#475569;">ELI5 Analogy</span>
            <label class="eli5-switch">
              <input type="checkbox">
              <span class="eli5-slider"></span>
            </label>
          </div>
        </div>
        <div class="eli5-body">
          <div class="eli5-standard-view">
            <div style="font-size:1.05rem; line-height:1.7; color:#1e293b;">
              {eli5_data['standard']}
            </div>
          </div>
          <div class="eli5-intuitive-view" style="display:none;">
            <div class="eli5-analogy-box">
              <div style="font-size:1.2rem; font-weight:bold; color:#b45309; margin-bottom:0.5rem;">🎈 Think of it like this:</div>
              <div style="font-size:1.1rem; line-height:1.7; color:#78350f;">
                {eli5_data['intuitive']}
              </div>
            </div>
          </div>
        </div>
      </div>
    """

def get_scratchpad_html():
    """Builds interactive Whiteboard Scratchpad Drawer HTML and floating toggle button."""
    return """
  <!-- Interactive Whiteboard Scratchpad Drawer -->
  <div id="scratchpadModal">
    <div class="scratchpad-header">
      <div class="scratchpad-title">
        <span>✏️</span> Whiteboard Scratchpad
      </div>
      <button id="scratchpadCloseBtn" class="scratchpad-btn" title="Close Scratchpad">&times;</button>
    </div>
    <div class="scratchpad-toolbar">
      <button id="toolPen" class="scratchpad-btn active">Pen</button>
      <button id="toolHighlighter" class="scratchpad-btn">Highlighter</button>
      <button id="toolEraser" class="scratchpad-btn">Eraser</button>
      <span style="font-size: 0.8rem; color: #64748b; margin-left: 0.4rem;">Color:</span>
      <div class="color-dot active" data-color="#1e293b" style="background: #1e293b;" title="Charcoal"></div>
      <div class="color-dot" data-color="#1d4ed8" style="background: #1d4ed8;" title="Royal Blue"></div>
      <div class="color-dot" data-color="#dc2626" style="background: #dc2626;" title="Red Marker"></div>
      <div class="color-dot" data-color="#15803d" style="background: #15803d;" title="Green"></div>
      <div class="color-dot" data-color="#7e22ce" style="background: #7e22ce;" title="Purple"></div>
      <input type="range" id="scratchpadSize" min="1" max="15" value="3" style="width: 60px; margin-left: auto;" title="Stroke Size">
      <button id="scratchpadUndoBtn" class="scratchpad-btn">Undo</button>
      <button id="scratchpadClearBtn" class="scratchpad-btn" style="color: #dc2626;">Clear</button>
    </div>
    <div class="scratchpad-canvas-wrap">
      <canvas id="scratchpadCanvas"></canvas>
    </div>
  </div>

  <!-- Floating Scratchpad Trigger Button -->
  <button id="scratchpadToggleBtn" class="btn-scratchpad-toggle" title="Open Whiteboard Scratchpad to Solve Problems">
    <span>✏️</span> Whiteboard Pad
  </button>
"""

def get_simulation_modal_html():
    """Builds interactive Physics Simulation Pop-up Modal Window."""
    return """
  <!-- Interactive Physics Simulation Pop-up Modal Window -->
  <div id="simulationModalOverlay" class="sim-modal-overlay" style="display:none;">
    <div class="sim-modal-dialog">
      <div class="sim-modal-header">
        <div class="sim-modal-title">
          <span>🔬</span>
          <span id="simModalTitleText">Interactive Physics Laboratory</span>
          <span class="doodle-tag tag-purple" id="simModalDomainBadge" style="font-size:0.8rem; padding:0.15rem 0.5rem;">HTML5 Lab</span>
        </div>
        <button id="closeSimModalBtn" class="sim-modal-close-btn" title="Close Simulation">&times;</button>
      </div>
      <div class="sim-modal-body" id="simModalBody">
        <!-- Dynamic simulation injected here -->
      </div>
    </div>
  </div>
"""

def render_simulation_widget(sim_type):
    """Builds interactive HTML5 Physics Simulation launcher card for pop-up window."""
    if not sim_type:
        return ""
    sim_info = {
        'projectile': ('🎯 2D Projectile Trajectory & Kinematics Lab', 'Adjust launch speed, angle, and gravity to trace parabolic trajectories and inspect range & max height in real-time.'),
        'incline': ('📐 Inclined Plane & Free Body Diagram (FBD) Lab', 'Vary slope angle, friction, and mass to observe real-time normal force, friction, and gravity component vectors.'),
        'spring': ('🌀 Harmonic Oscillator & Mechanical Energy Distribution Lab', 'Inspect kinetic vs potential energy bar graphs proving total mechanical energy conservation.'),
        'coulomb': ('⚡ Coulomb Force & Electric Field Vectors Lab', 'Position point charges and visualize electric field lines and repulsive/attractive vector forces.'),
        'circuits': ('💡 Ohm\'s Law & Electron Drift Velocity Lab', 'Vary voltage and resistance to observe microscopic drift motion of electrons and live current telemetry.'),
        'lorentz': ('🧲 Magnetic Lorentz Force & Cyclotron Orbit Lab', 'Control magnetic field strength and velocity to trace circular and helical cyclotron particle orbits.'),
        'optics': ('🔍 Snell\'s Law & Total Internal Reflection (TIR) Lab', 'Vary refractive indices and incidence angle to observe critical angle reflection phenomena.'),
        'bohr': ('⚛️ Bohr Atom Quantized Transitions & Spectral Lab', 'Trigger electron orbit jumps (n=1 to 5) and calculate emitted photon wavelengths.')
    }
    title, desc = sim_info.get(sim_type, ('Interactive Physics Lab', 'Explore physical variables in real-time.'))
    return f"""
      <div class="sim-launch-card">
        <div class="sim-launch-info">
          <div class="sim-launch-title-row">
            <span style="font-size: 1.6rem;">🔬</span>
            <h3 class="sim-launch-heading">{title}</h3>
            <span class="doodle-tag tag-yellow" style="font-size: 0.8rem; padding: 0.15rem 0.55rem;">Interactive HTML5 Lab</span>
          </div>
          <p class="sim-launch-desc">{desc}</p>
        </div>
        <button class="sim-launch-btn" data-launch-sim="{sim_type}" title="Launch simulation in pop-up window">
          <span>🚀 Launch Simulation</span>
          <span style="font-size: 0.82rem; opacity: 0.9;">(Pop-up Window)</span>
        </button>
      </div>
    """

def get_google_verification_meta():
    """Reads Google verification code if provided in google_verification.txt or env var."""
    ver_file = os.path.join(OUT_DIR, "google_verification.txt")
    code = os.environ.get("GOOGLE_SITE_VERIFICATION", "")
    if not code and os.path.exists(ver_file):
        try:
            with open(ver_file, "r", encoding="utf-8") as f:
                code = f.read().strip()
        except Exception:
            code = ""
    if code:
        return f'<meta name="google-site-verification" content="{code}">'
    return '<!-- Google Search Console Verification Meta Tag: add code to google_verification.txt or place here -->'

def generate_sitemap(all_chapters_meta):
    """Generates a standard sitemap.xml for Google Search Console and crawlers."""
    base_url = "https://kedar773.github.io/cbse-physics/"
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        '  <url>',
        f'    <loc>{base_url}</loc>',
        f'    <lastmod>{now_str}</lastmod>',
        '    <changefreq>weekly</changefreq>',
        '    <priority>1.0</priority>',
        '  </url>'
    ]
    
    for class_key in ["Class_11", "Class_12"]:
        cls_num = "11" if class_key == "Class_11" else "12"
        folder = f"class-{cls_num}"
        for ch in all_chapters_meta.get(class_key, []):
            slug = ch['slug']
            ch_url = f"{base_url}{folder}/{slug}/index.html"
            xml_lines.extend([
                '  <url>',
                f'    <loc>{ch_url}</loc>',
                f'    <lastmod>{now_str}</lastmod>',
                '    <changefreq>weekly</changefreq>',
                '    <priority>0.8</priority>',
                '  </url>'
            ])
            
    xml_lines.append('</urlset>')
    sitemap_path = os.path.join(OUT_DIR, "sitemap.xml")
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write("\n".join(xml_lines) + "\n")
    print(f"🗺️ Sitemap generated: {sitemap_path} ({len(xml_lines)-3} URLs)")

def generate_robots_txt():
    """Generates robots.txt for search engine crawlers and Googlebot."""
    content = """User-agent: *
Allow: /

Sitemap: https://kedar773.github.io/cbse-physics/sitemap.xml
"""
    robots_path = os.path.join(OUT_DIR, "robots.txt")
    with open(robots_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"🤖 robots.txt generated: {robots_path}")

def build_chapter_page(class_name, chapter_meta, sections, all_chapters_menu):
    """Generates the full standalone HTML page for a Physics chapter."""
    cls_num = "11" if class_name == "Class_11" else "12"
    slug = chapter_meta['slug']
    title = chapter_meta['title']
    domain = chapter_meta['domain']
    priority = chapter_meta['priority']
    yield_tag = chapter_meta['yield']
    sim_type = chapter_meta.get('sim')
    eli5_data = chapter_meta.get('eli5')
    key_concepts = chapter_meta.get('key_concepts', [])

    # Relative asset paths from class-xx/slug/
    rel_base = "../../"

    # Build Key Concept Tags HTML
    concept_tags_html = " ".join([f'<span class="doodle-tag tag-blue">{c}</span>' for c in key_concepts])

    # Build Chapter Switcher dropdown
    switcher_options = []
    for c_group, c_list in all_chapters_menu.items():
        c_name = "Class 11" if c_group == "Class_11" else "Class 12"
        switcher_options.append(f'<optgroup label="{c_name}">')
        for ch in c_list:
            sel = "selected" if (ch['slug'] == slug and c_group == class_name) else ""
            c_folder = "class-11" if c_group == "Class_11" else "class-12"
            switcher_options.append(f'<option value="{rel_base}{c_folder}/{ch["slug"]}/index.html" {sel}>{ch["title"]}</option>')
        switcher_options.append('</optgroup>')
    switcher_html = "\n".join(switcher_options)

    # Widgets
    eli5_widget = render_eli5_widget(eli5_data)
    sim_widget = render_simulation_widget(sim_type)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — CBSE Class {cls_num} Physics | Kedar's Physics Engine</title>
  <meta name="description" content="Comprehensive NCERT pure-line revision notes, step-by-step derivations, solved numerical examples, and 2020-2025 board exam PYQs for {title} (CBSE Class {cls_num} Physics).">
  <meta name="keywords" content="{title}, CBSE Class {cls_num} Physics, NCERT {title}, Physics Derivations, CBSE Board PYQs, JEE Main Physics, NEET Physics">
  <meta name="author" content="Kedar Krishna">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://kedar773.github.io/cbse-physics/class-{cls_num}/{slug}/index.html">
  
  <!-- OpenGraph / Social Sharing -->
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://kedar773.github.io/cbse-physics/class-{cls_num}/{slug}/index.html">
  <meta property="og:title" content="{title} — CBSE Class {cls_num} Physics | Kedar's Physics Engine">
  <meta property="og:description" content="Comprehensive NCERT pure-line revision notes, derivations, and board PYQs for {title}.">
  <meta property="og:site_name" content="Kedar's Physics Engine">
  
  <!-- Handwriting & Whiteboard Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Caveat:wght@400;600;700&family=Kalam:wght@300;400;700&family=Patrick+Hand&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
  
  <!-- KaTeX Math Engine -->
  <link rel="stylesheet" href="{rel_base}assets/vendor/katex/katex.min.css">
  <script defer src="{rel_base}assets/vendor/katex/katex.min.js"></script>
  <script defer src="{rel_base}assets/vendor/katex/contrib/auto-render.min.js"></script>
  
  <!-- Stylesheets -->
  <link rel="stylesheet" href="{rel_base}assets/css/notebook.css">
  <link rel="stylesheet" href="{rel_base}assets/css/notebook-animations.css">
  <link rel="stylesheet" href="{rel_base}assets/css/chapter.css">
  <link rel="stylesheet" href="{rel_base}assets/css/simulations.css">
</head>
<body data-chapter-slug="{slug}" class="notebook-canvas">

  <!-- Mobile Floating Header Toggle Pill -->
  <button id="headerTogglePill" class="mobile-header-pill" aria-label="Toggle Header">▼ Show Tabs / Header</button>

  <!-- Smart Auto-Hiding Top Bar -->
  <header class="chapter-top-bar header-visible">
    <div class="top-bar-inner">
      <div class="top-bar-left">
        <a href="{rel_base}index.html" class="portal-back-btn">← Portal</a>
        <span class="chapter-badge-class">Class {cls_num}</span>
        <span class="chapter-domain-badge">{domain}</span>
        <h1 class="chapter-title-heading">{title}</h1>
      </div>
      <div class="top-bar-right">
        <select class="chapter-select-menu" onchange="if(this.value) location.href=this.value;">
          {switcher_html}
        </select>
        <button class="search-trigger-btn open-search-trigger" title="Search (Ctrl+K)">🔍 Search</button>
        <button class="scratchpad-toggle-btn" id="openScratchpadBtn" title="Student Scratchpad">✏️ Scratchpad</button>
        <button class="academy-toggle-btn academy-modal-trigger" title="Kedar's STEM Academy — Switch between Physics, Maths, &amp; Chemistry">🏛️ Academy</button>
      </div>
    </div>

    <!-- 5-Tab Marker Tray -->
    <nav class="tab-marker-tray">
      <button class="tab-marker-btn active" data-tab="tab-concepts">
        <span class="tab-marker-num">01</span>
        <span class="tab-marker-label">NCERT Core Notes</span>
      </button>
      <button class="tab-marker-btn" data-tab="tab-examples">
        <span class="tab-marker-num">02</span>
        <span class="tab-marker-label">Solved Examples</span>
      </button>
      <button class="tab-marker-btn" data-tab="tab-pyq">
        <span class="tab-marker-num">03</span>
        <span class="tab-marker-label">2020–2025 PYQ Vault</span>
      </button>
      <button class="tab-marker-btn" data-tab="tab-traps">
        <span class="tab-marker-num">04</span>
        <span class="tab-marker-label">Examiner Traps &amp; Hacks</span>
      </button>
      <button class="tab-marker-btn" data-tab="tab-advanced">
        <span class="tab-marker-num">05</span>
        <span class="tab-marker-label">Advanced Studies (JEE)</span>
      </button>
    </nav>
  </header>

  <!-- Main Notebook Viewport -->
  <main class="notebook-viewport">
    
    <!-- Red Notebook Margin Guide -->
    <div class="notebook-margin-line"></div>

    <div class="notebook-page-container">

      <!-- Chapter Hero Header Banner -->
      <div class="chapter-hero-banner">
        <div class="hero-top-meta">
          <span class="doodle-tag tag-purple">CBSE Class {cls_num} Physics</span>
          <span class="doodle-tag tag-yellow">{priority} Priority</span>
          <span class="doodle-tag tag-green">{yield_tag}</span>
        </div>
        <h2 class="hero-main-title">{title}</h2>
        <div class="hero-concept-tags">
          {concept_tags_html}
        </div>
      </div>

      <!-- Tab Panes Container -->
      <div class="notebook-tabs-content">

        <!-- TAB 1: NCERT CORE CONCEPTS -->
        <section id="tab-concepts" class="notebook-tab-pane active">
          {eli5_widget}
          {sim_widget}
          <div class="chapter-content-body">
            {sections['concepts_html']}
          </div>
        </section>

        <!-- TAB 2: SOLVED EXAMPLES -->
        <section id="tab-examples" class="notebook-tab-pane">
          <div class="sticky-note green" style="margin-bottom: 2rem;">
            <div class="sticky-title">✍️ CBSE Model Solved Examples &amp; Step Rubrics</div>
            Study how official CBSE marking schemes reward every intermediate algebraic transformation,
            dimensional unit check, and vector diagram.
          </div>
          <div class="examples-grid">
            {sections['examples_html']}
          </div>
        </section>

        <!-- TAB 3: 2020-2025 PYQ VAULT -->
        <section id="tab-pyq" class="notebook-tab-pane">
          
          <!-- PYQ Filter Tray -->
          <div class="pyq-controls-panel">
            <div class="pyq-filter-group">
              <span class="filter-title">Year Filter:</span>
              <button class="pyq-filter-btn pyq-filter-year active" data-val="all">All</button>
              <button class="pyq-filter-btn pyq-filter-year" data-val="2024">2024</button>
              <button class="pyq-filter-btn pyq-filter-year" data-val="2023">2023</button>
              <button class="pyq-filter-btn pyq-filter-year" data-val="2022">2022</button>
              <button class="pyq-filter-btn pyq-filter-year" data-val="case">Case Study</button>
              <button class="pyq-filter-btn pyq-filter-year" data-val="exemplar">Exemplar</button>
            </div>
            <div class="pyq-filter-group">
              <span class="filter-title">Marks:</span>
              <button class="pyq-filter-btn pyq-filter-mark active" data-val="all">All</button>
              <button class="pyq-filter-btn pyq-filter-mark" data-val="1">1M</button>
              <button class="pyq-filter-btn pyq-filter-mark" data-val="2">2M</button>
              <button class="pyq-filter-btn pyq-filter-mark" data-val="3">3M</button>
              <button class="pyq-filter-btn pyq-filter-mark" data-val="4">4M</button>
              <button class="pyq-filter-btn pyq-filter-mark" data-val="5">5M</button>
            </div>
          </div>

          <!-- Mastery Tracker Bar -->
          <div class="mastery-tracker-box">
            <div class="mastery-meta">
              <span style="font-weight:bold; color:#1e3a8a;">🎯 Student Chapter Mastery:</span>
              <span id="masteryProgressText">0 of 0 Completed (0%)</span>
            </div>
            <div class="mastery-track">
              <div id="masteryProgressFill" class="mastery-fill" style="width: 0%;"></div>
            </div>
          </div>

          <div class="pyq-list-container">
            {sections['pyq_html']}
          </div>
        </section>

        <!-- TAB 4: EXAMINER TRAPS & SPEED HACKS -->
        <section id="tab-traps" class="notebook-tab-pane">
          {sections['traps_html']}
        </section>

        <!-- TAB 5: ADVANCED STUDIES (JEE) -->
        <section id="tab-advanced" class="notebook-tab-pane">
          {render_jee_advanced_tab(slug)}
        </section>

      </div>
    </div>
  </main>

  {get_scratchpad_html()}

  {get_simulation_modal_html()}


  <!-- Floating Quick Navigation Widget -->
  <div class="floating-quick-nav">
    <button class="quick-nav-btn" onclick="window.scrollTo({{top: 0, behavior: 'smooth'}})" title="Jump to Top">▲</button>
    <button class="quick-nav-btn secondary" onclick="document.getElementById('subtopicQuickNav')?.scrollIntoView({{behavior: 'smooth'}})" title="Subtopic Quick Index">📑</button>
    <button class="quick-nav-btn secondary" onclick="document.querySelector('[data-tab=\'tab-pyq\']')?.click()" title="PYQ Vault">🎯</button>
    <button class="quick-nav-btn secondary" id="quickNavScratchpadBtn" title="Scratchpad">✏️</button>
  </div>

  <!-- Site Footer -->
  <footer class="notebook-footer">
    <div class="footer-inner">
      <div class="footer-brand">
        <strong>Powered by Kedar's Physics Engine</strong>
        <p>CBSE Class 11 &amp; 12 Physics Engine • NCERT Pure Line Alignment</p>
      </div>
      <div class="footer-contact">
        <button class="footer-contact-trigger open-contact-trigger">👨‍🏫 Instructor Contact</button>
      </div>
    </div>
  </footer>

  <!-- Scripts -->
  <script src="{rel_base}assets/js/notebook-animations.js"></script>
  <script src="{rel_base}assets/js/notebook-scratchpad.js"></script>
  <script src="{rel_base}assets/js/eli5-engine.js"></script>
  <script src="{rel_base}assets/js/physics-simulations.js"></script>
  <script src="{rel_base}assets/js/chapter-engine.js"></script>
  <script src="{rel_base}assets/js/search-engine.js"></script>
  <script src="{rel_base}assets/js/contact-modal.js"></script>
  <script src="{rel_base}assets/js/academy-modal.js"></script>
</body>
</html>
"""
    return html

def build_landing_page(all_chapters_meta):
    """Generates the master landing page index.html."""
    total_chapters = sum(len(v) for v in all_chapters_meta.values())
    
    cards_html = []

    for class_key in ["Class_11", "Class_12"]:
        cls_num = "11" if class_key == "Class_11" else "12"
        folder = "class-11" if class_key == "Class_11" else "class-12"
        chapters = all_chapters_meta[class_key]

        for idx, ch in enumerate(chapters, 1):
            slug = ch['slug']
            title = ch['title']
            domain = ch['domain']
            priority = ch['priority']
            yield_tag = ch['yield']
            sim_type = ch.get('sim')
            key_concepts = ch.get('key_concepts', [])

            # Generate tags from key concepts (NOT just "PYQ")
            tags_html = " ".join([f'<span class="doodle-tag tag-blue">{c}</span>' for c in key_concepts[:3]])
            if sim_type:
                tags_html += f' <span class="doodle-tag tag-yellow" data-launch-sim="{sim_type}" style="cursor:pointer;" title="Click to launch interactive simulation in pop-up window">🔬 Lab Simulation</span>'

            cards_html.append(f"""
              <div class="notebook-chapter-card" data-class="{cls_num}" data-domain="{domain.lower()}">
                <div class="card-top-meta">
                  <span class="doodle-tag tag-purple">Class {cls_num} • Ch {idx:02d}</span>
                  <span class="doodle-tag tag-green">{yield_tag}</span>
                  <span class="card-domain-label">{domain}</span>
                </div>
                <h3 class="card-title">
                  <a href="{folder}/{slug}/index.html">{title}</a>
                </h3>
                <div class="card-tags-tray">
                  {tags_html}
                </div>
                <div class="card-actions-tray">
                  <a href="{folder}/{slug}/index.html" class="card-action-btn primary">📘 Notes &amp; Theory</a>
                  <a href="{folder}/{slug}/index.html#tab-pyq" class="card-action-btn secondary">🎯 PYQ Vault</a>
                </div>
              </div>
            """)

    rendered_cards = "\n".join(cards_html)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Kedar's Physics Engine — CBSE Class 11 &amp; 12 Senior Physics</title>
  <meta name="description" content="Comprehensive interactive study notebook for CBSE Class 11 &amp; 12 Physics. Strictly NCERT pure-line notes, first-principles derivations, 2020-2025 PYQ vault with step-wise CBSE marking rubrics, interactive HTML5 physics lab simulations, and JEE/NEET competitive concepts.">
  <meta name="keywords" content="CBSE Physics, Class 11 Physics, Class 12 Physics, NCERT Physics, CBSE Board Exam, PYQ Vault, Physics Derivations, Formula Sheet, JEE Physics, NEET Physics">
  <meta name="author" content="Kedar Krishna">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://kedar773.github.io/cbse-physics/">
  
  {get_google_verification_meta()}

  <!-- OpenGraph / Social Sharing -->
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://kedar773.github.io/cbse-physics/">
  <meta property="og:title" content="Kedar's Physics Engine — CBSE Class 11 &amp; 12 Senior Physics">
  <meta property="og:description" content="Comprehensive interactive study notebook for CBSE Class 11 &amp; 12 Physics. Strictly NCERT pure-line notes, derivations, and 2020-2025 PYQ vault.">
  <meta property="og:site_name" content="Kedar's Physics Engine">

  <!-- Schema.org Educational JSON-LD -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "EducationalOrganization",
    "name": "Kedar's Physics Engine",
    "url": "https://kedar773.github.io/cbse-physics/",
    "description": "Comprehensive CBSE Class 11 and Class 12 Physics digital notebook with NCERT pure-line notes, solved examples, PYQs, and HTML5 simulations.",
    "founder": {{
      "@type": "Person",
      "name": "Kedar Krishna"
    }}
  }}
  </script>
  
  <!-- Handwriting & Whiteboard Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Caveat:wght@400;600;700&family=Kalam:wght@300;400;700&family=Patrick+Hand&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
  
  <!-- KaTeX Math Engine -->
  <link rel="stylesheet" href="assets/vendor/katex/katex.min.css">
  <script defer src="assets/vendor/katex/katex.min.js"></script>
  <script defer src="assets/vendor/katex/contrib/auto-render.min.js"></script>
  
  <!-- Stylesheets -->
  <link rel="stylesheet" href="assets/css/notebook.css">
  <link rel="stylesheet" href="assets/css/notebook-animations.css">
  <link rel="stylesheet" href="assets/css/chapter.css">
  <link rel="stylesheet" href="assets/css/simulations.css">
</head>
<body class="notebook-canvas portal-home">

  <!-- No top bar; Stacked Hero Title as requested -->
  <main class="portal-main-wrap">
    
    <!-- Hero Section -->
    <header class="portal-hero-section">
      <!-- Academy Switcher Trigger (Top-Right) -->
      <button class="portal-corner-academy academy-modal-trigger" title="Kedar's STEM Academy — Switch between Physics, Maths, &amp; Chemistry">
        <span class="academy-btn-icon">🏛️</span>
        <span class="academy-btn-label">Academy</span>
      </button>

      <div class="portal-brand-stacked">
        <div class="stacked-brand-line1">Kedar's</div>
        <div class="stacked-brand-line2">Physics Engine</div>
      </div>

      <div class="educator-stacked-title" style="margin: 0.75rem auto 1.25rem;">
        <span class="doodle-tag tag-purple" style="font-size:1.05rem; padding:0.4rem 1rem; white-space:normal; max-width:min(780px, 94vw); text-align:center; line-height:1.45;">Senior Secondary Physics Engine • NCERT Pure-Line Notes, Interactive Labs &amp; PYQ Vault</span>
      </div>

      <div class="portal-standard-badge">
        <span class="badge-icon">🏛️</span>
        <span>CBSE Class 11 &amp; 12 Senior Physics • NCERT Pure Line Curriculum &amp; 2020–2025 Board Archive</span>
      </div>

      <!-- Quick Search Trigger -->
      <div class="portal-search-box open-search-trigger" style="margin: 1.75rem auto; max-width: 640px; cursor: pointer;">
        <span class="search-box-icon">🔍</span>
        <span class="search-box-placeholder">Search all 25 chapters, formulas, laws, derivations, or PYQs...</span>
        <span class="search-box-kbd">Ctrl + K</span>
      </div>

      <!-- Curriculum Stats HUD -->
      <div class="portal-stats-hud">
        <div class="stat-bubble">
          <div class="portal-stat-num" data-count="25">25</div>
          <div class="stat-label">NCERT Chapters</div>
        </div>
        <div class="stat-bubble">
          <div class="portal-stat-num" data-count="180" data-suffix="+">180+</div>
          <div class="stat-label">Core Concepts</div>
        </div>
        <div class="stat-bubble">
          <div class="portal-stat-num" data-count="350" data-suffix="+">350+</div>
          <div class="stat-label">Solved Examples</div>
        </div>
        <div class="stat-bubble">
          <div class="portal-stat-num" data-count="420" data-suffix="+">420+</div>
          <div class="stat-label">2020–2025 PYQs</div>
        </div>
        <div class="stat-bubble">
          <div class="portal-stat-num" data-count="8">8</div>
          <div class="stat-label">Interactive Labs</div>
        </div>
      </div>
    </header>

    <!-- Portal Filter Controls -->
    <section class="portal-filter-bar">
      <div class="portal-class-tabs">
        <button class="portal-class-tab active" data-class="all">All Curriculum ({total_chapters})</button>
        <button class="portal-class-tab" data-class="11">Class 11 ({len(all_chapters_meta['Class_11'])})</button>
        <button class="portal-class-tab" data-class="12">Class 12 ({len(all_chapters_meta['Class_12'])})</button>
      </div>

      <div class="portal-domain-chips">
        <button class="portal-domain-chip active" data-domain="all">All Branches</button>
        <button class="portal-domain-chip" data-domain="kinematics">Kinematics</button>
        <button class="portal-domain-chip" data-domain="mechanics">Mechanics</button>
        <button class="portal-domain-chip" data-domain="thermal">Thermal Physics</button>
        <button class="portal-domain-chip" data-domain="electromagnetism">Electromagnetism</button>
        <button class="portal-domain-chip" data-domain="optics">Optics</button>
        <button class="portal-domain-chip" data-domain="modern">Modern Physics</button>
      </div>

      <div id="portalVisibleChapterCount" class="portal-visible-count">
        {total_chapters} Chapters Displayed
      </div>
    </section>

    <!-- Chapter Grid -->
    <section class="portal-cards-grid">
      {rendered_cards}
    </section>

  </main>

  {get_scratchpad_html()}

  {get_simulation_modal_html()}

  <!-- Site Footer -->
  <footer class="notebook-footer">
    <div class="footer-inner">
      <div class="footer-brand">
        <strong>Powered by Kedar's Physics Engine</strong>
        <p>CBSE Class 11 &amp; 12 Physics Engine • Mentored by Kedar Krishna (Senior Chemistry Educator)</p>
      </div>
      <div class="footer-contact">
        <button class="footer-contact-trigger open-contact-trigger">👨‍🏫 Instructor Contact</button>
      </div>
    </div>
  </footer>

  <!-- Scripts -->
  <script src="assets/js/notebook-animations.js"></script>
  <script src="assets/js/notebook-scratchpad.js"></script>
  <script src="assets/js/physics-simulations.js"></script>
  <script src="assets/js/portal-engine.js"></script>
  <script src="assets/js/search-engine.js"></script>
  <script src="assets/js/contact-modal.js"></script>
  <script src="assets/js/academy-modal.js"></script>
</body>
</html>
"""
    return html

def build_all():
    """Main compilation pipeline."""
    print("🚀 Starting CBSE Physics Notebook Build Pipeline...")

    all_chapters_meta = {"Class_11": [], "Class_12": []}
    global_search_index = []
    manifest = {"curriculum": "CBSE Physics Class 11 & 12", "chapters": []}

    # Pass 1: Build each chapter
    for class_key in ["Class_11", "Class_12"]:
        cls_num = "11" if class_key == "Class_11" else "12"
        class_src_dir = os.path.join(ROOT_DIR, class_key)
        class_out_folder = f"class-{cls_num}"
        class_out_dir = os.path.join(OUT_DIR, class_out_folder)
        os.makedirs(class_out_dir, exist_ok=True)

        meta_list = CHAPTER_METADATA[class_key]

        for ch_meta in meta_list:
            slug = ch_meta['slug']
            dir_pat = ch_meta['dir_pattern']

            # Locate matching source folder
            matches = glob.glob(os.path.join(class_src_dir, dir_pat))
            if not matches:
                print(f"⚠️ Warning: No folder found matching {dir_pat} in {class_src_dir}")
                continue

            src_chapter_dir = matches[0]
            print(f"📂 Processing [{class_key}] {ch_meta['title']} ({os.path.basename(src_chapter_dir)})...")

            # Collect and sort subtopic markdown files (excluding compiled FULL_*)
            md_files = sorted([
                os.path.join(src_chapter_dir, f)
                for f in os.listdir(src_chapter_dir)
                if f.endswith('.md') and not f.startswith('FULL_')
            ])

            parsed_modules = [parse_module(mf) for mf in md_files]

            # Extract sections for 5 tabs
            sections = extract_sections(parsed_modules, ch_meta.get('advanced_keywords', []), ch_meta)

            # Store chapter in menu
            all_chapters_meta[class_key].append(ch_meta)

            # Create chapter output folder
            ch_out_dir = os.path.join(class_out_dir, slug)
            os.makedirs(ch_out_dir, exist_ok=True)

            # Store search index entries
            for s_item in sections['search_items']:
                global_search_index.append({
                    "class": cls_num,
                    "chapter": ch_meta['title'],
                    "title": s_item['title'],
                    "snippet": s_item['snippet'],
                    "url": f"{class_out_folder}/{slug}/index.html#{s_item['targetId']}",
                    "type": s_item['type'],
                    "badge": s_item['badge'],
                    "keywords": ch_meta.get('key_concepts', [])
                })

            # Manifest entry
            manifest["chapters"].append({
                "class": cls_num,
                "slug": slug,
                "title": ch_meta['title'],
                "domain": ch_meta['domain'],
                "priority": ch_meta['priority'],
                "path": f"{class_out_folder}/{slug}/index.html",
                "modules_count": len(parsed_modules)
            })

    # Pass 2: Render Chapter HTML files (now that all_chapters_meta is complete for menu dropdown)
    for class_key in ["Class_11", "Class_12"]:
        cls_num = "11" if class_key == "Class_11" else "12"
        class_src_dir = os.path.join(ROOT_DIR, class_key)
        class_out_folder = f"class-{cls_num}"
        class_out_dir = os.path.join(OUT_DIR, class_out_folder)

        meta_list = CHAPTER_METADATA[class_key]

        for ch_meta in meta_list:
            slug = ch_meta['slug']
            dir_pat = ch_meta['dir_pattern']
            matches = glob.glob(os.path.join(class_src_dir, dir_pat))
            if not matches:
                continue

            src_chapter_dir = matches[0]
            md_files = sorted([
                os.path.join(src_chapter_dir, f)
                for f in os.listdir(src_chapter_dir)
                if f.endswith('.md') and not f.startswith('FULL_')
            ])
            parsed_modules = [parse_module(mf) for mf in md_files]
            sections = extract_sections(parsed_modules, ch_meta.get('advanced_keywords', []), ch_meta)

            ch_html = build_chapter_page(class_key, ch_meta, sections, all_chapters_meta)
            out_file = os.path.join(class_out_dir, slug, "index.html")
            with open(out_file, 'w', encoding='utf-8') as f:
                f.write(ch_html)

            f_size = os.path.getsize(out_file) / 1024
            print(f"  ✓ Built: {out_file} ({f_size:.1f} KB)")

    # Pass 3: Build Master Landing Page index.html
    landing_html = build_landing_page(all_chapters_meta)
    landing_out_file = os.path.join(OUT_DIR, "index.html")
    with open(landing_out_file, 'w', encoding='utf-8') as f:
        f.write(landing_html)
    print(f"🌟 Master Landing Page generated: {landing_out_file} ({os.path.getsize(landing_out_file)/1024:.1f} KB)")

    # Pass 4: Save Search Index & Manifest
    data_dir = os.path.join(OUT_DIR, "assets", "data")
    os.makedirs(data_dir, exist_ok=True)

    search_index_file = os.path.join(data_dir, "search_index.json")
    with open(search_index_file, 'w', encoding='utf-8') as f:
        json.dump(global_search_index, f, indent=2, ensure_ascii=False)
    print(f"🔍 Search index generated: {search_index_file} ({len(global_search_index)} items)")

    manifest_file = os.path.join(data_dir, "curriculum_manifest.json")
    with open(manifest_file, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"📋 Manifest generated: {manifest_file}")

    # Pass 5: Generate Sitemap & Robots.txt for Google Search Console
    generate_sitemap(all_chapters_meta)
    generate_robots_txt()

    print("\n🎉 ALL 25 CHAPTERS & LANDING PAGE COMPILED SUCCESSFULLY!")

if __name__ == "__main__":
    build_all()
