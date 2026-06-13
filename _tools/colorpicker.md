---
layout: default
title: Color Picker
---

<style>
  .color-picker *, .color-picker * > * {
    box-sizing: border-box;
    font-family: sans-serif;
  }

  .color-picker {
    max-width: 20rem;
    width: 100%;
    background: var(--surface-color);
    padding: 1.5rem;
    border: 1px solid var(--background-color);
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    margin: 2rem 0;
  }

  .preview {
    height: 100px;
    border: 1px solid #333;
  }

  .picker {
    display: grid;
    grid-template-columns: 1fr 24px;
    gap: 12px;
    align-items: stretch;
  }

  .sv-grid {
    position: relative;
    height: 220px;
    overflow: hidden;
    border: 1px solid #333;
    cursor: crosshair;
  }

  .sv-base {
    position: absolute;
    inset: 0;
  }

  .sv-white {
    background: linear-gradient(to right, #fff, rgba(255,255,255,0));
  }

  .sv-black {
    background: linear-gradient(to top, #000, rgba(0,0,0,0));
  }

  .sv-selector {
    position: absolute;
    width: 10px;
    height: 10px;
    border: 2px solid #fff;
    transform: translate(-50%, -50%);
    pointer-events: none;
    box-shadow: 0 0 2px #000;
  }

  .hue-slider {
    position: relative;
    border: 1px solid #333;
    background: linear-gradient(
      to bottom,
      red, yellow, lime, cyan, blue, magenta, red
    );
    cursor: ns-resize;
  }

  .hue-indicator {
    position: absolute;
    left: 50%;
    width: 18px;
    height: 4px;
    background: #fff;
    transform: translate(-50%, -50%);
    pointer-events: none;
  }

  section.output {
    margin-top: 14px;
    display: grid;
    gap: 8px;
  }

  input[type="text"], button {
    width: 100%;
    background: var(--background-color);
    color: var(--on-background-color);
    border: 1px solid var(--background-color);
    padding: 0.5rem;
  }
</style>

<div class="color-picker">
  <div id="preview" class="preview"></div>

  <div class="picker">
    <div class="sv-grid" id="grid">
      <div id="gridColor" class="sv-base"></div>
      <div class="sv-base sv-white"></div>
      <div class="sv-base sv-black"></div>
      <div id="selector" class="sv-selector"></div>
    </div>
    <div class="hue-slider" id="hue" aria-label="Hue selector">
      <div id="hueSelector" class="hue-indicator"></div>
    </div>
  </div>

  <section class="output">
    <input id="hex" type="text" value="#ff0000"/>
    <button id="copy" type="button">Copy HEX</button>
    <output id="rgb">RGB(255, 0, 0)</output>
  </section>
</div>

<script>
let h = 0, s = 100, v = 100;

const grid = document.getElementById('grid'),
  hue = document.getElementById('hue'),
  selector = document.getElementById('selector'),
  hueSelector = document.getElementById('hueSelector'),
  preview = document.getElementById('preview'),
  hexInput = document.getElementById('hex'),
  rgbOut = document.getElementById('rgb'),
  gridColor = document.getElementById('gridColor'),
  copyBtn = document.getElementById('copy');

function hsvToRgb(h, s, v) {
  s /= 100;
  v /= 100;

  const c = v * s;
  const x = c * (1 - Math.abs((h / 60) % 2 - 1));
  const m = v - c;

  let r=0,g=0,b=0;

  if (h < 60) [r,g,b] = [c,x,0];
  else if (h < 120) [r,g,b] = [x,c,0];
  else if (h < 180) [r,g,b] = [0,c,x];
  else if (h < 240) [r,g,b] = [0,x,c];
  else if (h < 300) [r,g,b] = [x,0,c];
  else [r,g,b] = [c,0,x];

  return {
    r: Math.round((r+m)*255),
    g: Math.round((g+m)*255),
    b: Math.round((b+m)*255)
  };
}

function rgbToHex(r,g,b){
  return "#" + [r,g,b]
    .map(x => x.toString(16).padStart(2,'0'))
    .join('');
}

function hexToRgb(hex){
  hex = hex.replace('#','');
  if(hex.length !== 6) return null;

  return {
    r: parseInt(hex.slice(0,2),16),
    g: parseInt(hex.slice(2,4),16),
    b: parseInt(hex.slice(4,6),16)
  };
}

function update(){
  const rgb = hsvToRgb(h,s,v);
  const hex = rgbToHex(rgb.r,rgb.g,rgb.b);

  preview.style.background = hex;
  hexInput.value = hex;
  rgbOut.textContent = `RGB(${rgb.r}, ${rgb.g}, ${rgb.b})`;

  gridColor.style.background = `hsl(${h}, 100%, 50%)`;

  selector.style.left = `${s}%`;
  selector.style.top = `${100 - v}%`;

  hueSelector.style.top = `${(h / 360) * 100}%`;
}

function setSV(e){
  const rect = grid.getBoundingClientRect();

  let x = (e.clientX - rect.left) / rect.width;
  let y = (e.clientY - rect.top) / rect.height;

  x = Math.max(0, Math.min(1, x));
  y = Math.max(0, Math.min(1, y));

  s = x * 100;
  v = (1 - y) * 100;

  update();
}

grid.addEventListener('pointerdown', e => {
  grid.setPointerCapture(e.pointerId);
  setSV(e);
  grid.onpointermove = setSV;
});

grid.addEventListener('pointerup', () => grid.onpointermove = null);

function setHue(e){
  const rect = hue.getBoundingClientRect();

  let y = (e.clientY - rect.top) / rect.height;
  y = Math.max(0, Math.min(1, y));

  h = y * 360;
  update();
}

hue.addEventListener('pointerdown', e => {
  hue.setPointerCapture(e.pointerId);
  setHue(e);
  hue.onpointermove = setHue;
});

hue.addEventListener('pointerup', () => hue.onpointermove = null);

hexInput.addEventListener('input', () => {
  const rgb = hexToRgb(hexInput.value);
  if(!rgb) return;

  const max = Math.max(rgb.r,rgb.g,rgb.b);
  const min = Math.min(rgb.r,rgb.g,rgb.b);
  const delta = max - min;

  const vCalc = max / 255;
  let sCalc = max === 0 ? 0 : delta / max;

  let hCalc = 0;
  if(delta !== 0){
    if(max === rgb.r) hCalc = ((rgb.g - rgb.b) / delta) % 6;
    else if(max === rgb.g) hCalc = (rgb.b - rgb.r) / delta + 2;
    else hCalc = (rgb.r - rgb.g) / delta + 4;

    hCalc *= 60;
    if(hCalc < 0) hCalc += 360;
  }

  h = hCalc;
  s = sCalc * 100;
  v = vCalc * 100;

  update();
});

copyBtn.addEventListener('click', async () => {
  try {
    await navigator.clipboard.writeText(hexInput.value);
    copyBtn.textContent = "Copied!";
    setTimeout(() => copyBtn.textContent = "Copy HEX", 800);
  } catch {
    copyBtn.textContent = "Failed";
    setTimeout(() => copyBtn.textContent = "Copy HEX", 800);
  }
});

update();
</script>
