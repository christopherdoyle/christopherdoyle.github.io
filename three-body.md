---
layout: page
title: Three Body Problem
---

<style>
#simulation-container {
}

#canvas {
    border: 1px solid var(--on-background-color);
    background: var(--background-color);
    cursor: crosshair;
    max-width: 100%;
    height: auto;
}

.controls {
    margin-top: 1.5rem;
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    justify-content: center;
    max-width: 100%;
}

.controls button {
    padding: 0.5rem 1rem;
    font-size: 1rem;
    background: var(--background-color);
    color: var(--on-background-color);
    border: 1px solid var(--on-background-color);
    cursor: pointer;
    font-family: inherit;
}

.controls button:hover {
    background: var(--on-background-color);
    color: var(--background-color);
}

.controls label {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 1rem;
}

.controls input[type="range"] {
    width: 100px;
}

.controls input[type="checkbox"] {
    cursor: pointer;
}

.controls select {
    padding: 0.25rem 0.5rem;
    font-size: 1rem;
    background: var(--background-color);
    color: var(--on-background-color);
    border: 1px solid var(--on-background-color);
    cursor: pointer;
    font-family: inherit;
}
</style>

I am reading The Three Body problem by Liu Cixin and wanted to see what all the fuss was about.

<div id="simulation-container">
    <canvas id="canvas" width="700" height="700"></canvas>

    <div class="controls">
        <select id="configSelect">
            <option value="0">Figure-8</option>
            <option value="1">Circular</option>
            <option value="2">Binary + Perturber</option>
            <option value="3">Chaotic Triple</option>
            <option value="random" selected>Random</option>
        </select>
        <button id="resetBtn">Reset</button>
        <button id="pauseBtn">Pause</button>
        <label>
            Speed:
            <input type="range" id="speedSlider" min="0.1" max="3" step="0.1" value="1">
            <span id="speedValue">1.0x</span>
        </label>
        <label>
            <input type="checkbox" id="trailsCheckbox" checked>
            Trails
        </label>
    </div>
</div>

Select a configuration from the dropdown or choose **Random**. Click **Reset** to restart with the same settings.

<script>
(function() {
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;

    const BODY_COLORS = ['#e63946', '#06ffa5', '#ffbe0b'];

    // Simulation parameters
    const G = 50.0;
    const softening = 15;
    let isPaused = false;
    let showTrails = true;
    const baseSpeed = 0.25;
    let speedMultiplier = 1.0;
    const maxTrailLength = 150;

    class Body {
        constructor(x, y, vx, vy, mass, color) {
            this.x = x;
            this.y = y;
            this.vx = vx;
            this.vy = vy;
            this.mass = mass;
            this.color = color;
            this.trail = [];
            this.radius = Math.sqrt(mass) * 1.5;
        }

        addToTrail() {
            this.trail.push({ x: this.x, y: this.y });
            if (this.trail.length > maxTrailLength) {
                this.trail.shift();
            }
        }

        clearTrail() {
            this.trail = [];
        }
    }

    let bodies = [];
    let frameCount = 0;

    const configs = [
        // figure-8
        function() {
            return [
                new Body(width/2 - 100, height/2, 0, 2, 40, BODY_COLORS[0]),
                new Body(width/2 + 100, height/2, 0, 2, 40, BODY_COLORS[1]),
                new Body(width/2, height/2 + 80, 0, -4, 40, BODY_COLORS[2])
            ];
        },
        // circular
        function() {
            const cx = width / 2;
            const cy = height / 2;
            const r = 120;
            return [
                new Body(cx + r, cy, 0, 2.2, 45, BODY_COLORS[0]),
                new Body(cx - r/2, cy + r * 0.866, -1.9, -1.1, 45, BODY_COLORS[1]),
                new Body(cx - r/2, cy - r * 0.866, 1.9, -1.1, 45, BODY_COLORS[2])
            ];
        },
        // binary system with small perturber
        function() {
            return [
                new Body(width/2 - 70, height/2, 0, 2.5, 60, BODY_COLORS[0]),
                new Body(width/2 + 70, height/2, 0, -2.5, 60, BODY_COLORS[1]),
                new Body(width/2 - 150, height/2 - 150, 3, 1, 25, BODY_COLORS[2])
            ];
        },
        // chaotic triple
        function() {
            return [
                new Body(width/2 - 110, height/2 - 60, 1.2, 0.8, 42, BODY_COLORS[0]),
                new Body(width/2 + 120, height/2 + 50, -0.9, 1.1, 38, BODY_COLORS[1]),
                new Body(width/2 + 20, height/2 + 140, -0.3, -1.9, 36, BODY_COLORS[2])
            ];
        }
    ];

    function generateRandomBodies() {
        const newBodies = [];
        const margin = 100;

        for (let i = 0; i < 3; i++) {
            // everything random
            const x = margin + Math.random() * (width - 2 * margin);
            const y = margin + Math.random() * (height - 2 * margin);
            // todo: expose random numbers to controls, currently very constrained
            const vx = (Math.random() - 0.5) * 4;
            const vy = (Math.random() - 0.5) * 4;
            const mass = 30 + Math.random() * 30;

            newBodies.push(new Body(x, y, vx, vy, mass, BODY_COLORS[i]));
        }

        return newBodies;
    }

    function initializeBodies() {
        bodies = [];

        const selectedValue = document.getElementById('configSelect').value;

        if (selectedValue === 'random') {
            bodies = generateRandomBodies();
        } else {
            const configIndex = parseInt(selectedValue);
            bodies = configs[configIndex]();
        }

        frameCount = 0;
    }

    function updatePhysics(dt) {
        // calculate forces and update velocities
        for (let i = 0; i < bodies.length; i++) {
            let ax = 0;
            let ay = 0;

            for (let j = 0; j < bodies.length; j++) {
                if (i === j) continue;

                const dx = bodies[j].x - bodies[i].x;
                const dy = bodies[j].y - bodies[i].y;
                // softening to prevent numerical explosion when very close, small lie.
                const distSq = dx * dx + dy * dy + softening * softening;
                const dist = Math.sqrt(distSq);
                // gravity maths
                const force = G * bodies[j].mass / (dist * distSq);

                ax += force * dx;
                ay += force * dy;
            }

            bodies[i].vx += ax * dt;
            bodies[i].vy += ay * dt;
        }

        // update positions
        for (let i = 0; i < bodies.length; i++) {
            bodies[i].x += bodies[i].vx * dt;
            bodies[i].y += bodies[i].vy * dt;
        }
    }

    function draw() {
        // better way to do this? is dumb
        const bgColor = getComputedStyle(document.documentElement).getPropertyValue('--background-color').trim();
        ctx.fillStyle = bgColor;
        ctx.fillRect(0, 0, width, height);

        if (showTrails) {
            // show the trails!
            bodies.forEach(body => {
                if (body.trail.length > 1) {
                    ctx.strokeStyle = body.color;
                    ctx.lineWidth = 1.5;
                    ctx.globalAlpha = 0.4;
                    ctx.beginPath();
                    ctx.moveTo(body.trail[0].x, body.trail[0].y);
                    for (let i = 1; i < body.trail.length; i++) {
                        ctx.lineTo(body.trail[i].x, body.trail[i].y);
                    }
                    ctx.stroke();
                    ctx.globalAlpha = 1.0;
                }
            });
        }

        bodies.forEach(body => {
            // glow
            const gradient = ctx.createRadialGradient(
                body.x, body.y, 0,
                body.x, body.y, body.radius * 2.5
            );
            gradient.addColorStop(0, body.color);
            gradient.addColorStop(0.4, body.color + '66');
            gradient.addColorStop(1, body.color + '00');

            ctx.fillStyle = gradient;
            ctx.beginPath();
            ctx.arc(body.x, body.y, body.radius * 2.5, 0, Math.PI * 2);
            ctx.fill();

            // mass
            ctx.fillStyle = body.color;
            ctx.beginPath();
            ctx.arc(body.x, body.y, body.radius, 0, Math.PI * 2);
            ctx.fill();

            // highlight
            ctx.fillStyle = 'rgba(255, 255, 255, 0.5)';
            ctx.beginPath();
            ctx.arc(
                body.x - body.radius * 0.3,
                body.y - body.radius * 0.3,
                body.radius * 0.35,
                0, Math.PI * 2
            );
            ctx.fill();
        });
    }

    function animate() {
        if (!isPaused) {
            const substeps = 4;
            const dt = baseSpeed * speedMultiplier / substeps;

            for (let s = 0; s < substeps; s++) {
                updatePhysics(dt);
            }

            frameCount++;
            if (frameCount % 2 === 0 && showTrails) {
                bodies.forEach(body => body.addToTrail());
            }
        }

        draw();
        requestAnimationFrame(animate);
    }

    document.getElementById('configSelect').addEventListener('change', () => {
        initializeBodies();
    });
    document.getElementById('resetBtn').addEventListener('click', () => {
        initializeBodies();
    });
    document.getElementById('pauseBtn').addEventListener('click', (e) => {
        isPaused = !isPaused;
        e.target.textContent = isPaused ? 'Resume' : 'Pause';
    });
    document.getElementById('speedSlider').addEventListener('input', (e) => {
        speedMultiplier = parseFloat(e.target.value);
        document.getElementById('speedValue').textContent = speedMultiplier.toFixed(1) + 'x';
    });
    document.getElementById('trailsCheckbox').addEventListener('change', (e) => {
        showTrails = e.target.checked;
        if (!showTrails) {
            bodies.forEach(body => body.clearTrail());
        }
    });

    initializeBodies();
    animate();
})();
</script>
