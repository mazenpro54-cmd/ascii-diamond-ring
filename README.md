# 💍 3D ASCII Diamond Ring

> An exact, high-fidelity recreation of the viral generative art Instagram Reel by [@jin_22ee](https://www.instagram.com/reel/DfTmTeQJEOi/): *"Send this to someone you love #diamond #asciiart #generativeart #python #love"*.

Featuring real-time 3D raycasting, progressive materialization from 0.0s to 8.07s, 57-facet brilliant diamond scintillation, Blinn-Phong metallic torus luster, vertical light flares, cosmic atomic orbits, and live terminal HUD counters.

---

## ✨ Features

- **Progressive Slow Formation (0.0s → 8.07s)**:
  - **0.0s – 3.2s (Band Sweeps)**: The shank sweeps upward symmetrically from the bottom floor to form the ring loop.
  - **3.0s – 5.4s (Prongs Rise)**: 4 structural claw prongs rise vertically from the band mount.
  - **5.2s – 7.4s (Diamond Crystallizes)**: The brilliant diamond crystalizes upward from culet to crown.
  - **7.2s – 8.07s (Aura Flares)**: Vertical beam erupts into space as the letter count locks onto `1,366`.
- **Exact Code Matching**: Lines 77 to 94 in [`art.py`](art.py) match the video source code verbatim.
- **Parametric 3D Raycasting**: Z-buffer depth sorting and lighting calculations running at a silky 30 FPS.
- **Interactive Web Studio (`index.html`)**:
  - **Reel Mode**: 9:16 vertical split view matching the Instagram Reel layout.
  - **Studio Mode**: Dual-pane widescreen desktop layout.
  - **Cinema Mode**: Pure fullscreen glowing 3D ASCII terminal with CRT scanlines.
  - **Formation Scrubber**: Drag through time to inspect the step-by-step assembly.
  - **Theme Presets**: Diamond Ice, Pure Monochrome, Matrix Phosphor, Rose Gold, and Cyberpunk.
  - **360° Orbit Drag**: Rotate and inspect the setting from any angle.

---

## 🚀 Quick Start (Terminal)

### Requirements
- Python 3.8+
- `numpy`

```bash
git clone https://github.com/mazenpro54-cmd/ascii-diamond-ring.git
cd ascii-diamond-ring
pip install -r requirements.txt
python art.py
```

---

## 🌐 Web Studio Preview

Open `index.html` in any modern web browser or deploy directly to GitHub Pages for instant zero-dependency interactive 3D ASCII rendering.

---

## 📐 Mathematical Formulation

### 1. 4-Prong Cathedral Setting (Lines 77–89)
```python
def prongs():
    P, N = [], []
    for i in range(4):
        a = TAU * (i + 0.5) / 4
        base = np.array([0.08 * np.cos(a), R_BAND + 0.02, 0.08 * np.sin(a)])
        tip = np.array([(GIRDLE_R + 0.015) * np.cos(a), TABLE_Y - 0.03, (GIRDLE_R + 0.015) * np.sin(a)])
        u, phi = [x.ravel() for x in np.meshgrid(np.linspace(0, 1, 40), np.linspace(0, TAU, 16))]
        d = (tip - base) / np.linalg.norm(tip - base)
        s = np.cross(d, [0, 0, 1.0]); s /= np.linalg.norm(s)
        w = np.cross(s, d)
        n = np.cos(phi)[:, None] * s + np.sin(phi)[:, None] * w
        P.append(base + u[:, None] * (tip - base) + n * 0.022), N.append(n)
    return np.concatenate(P), np.concatenate(N)
```

### 2. Torus Band
$$P(\theta, \phi) = \left( (R_{band} + r_{tube}\cos\phi)\sin\theta,\ (R_{band} + r_{tube}\cos\phi)\cos\theta,\ r_{tube}\sin\phi \right)$$

### 3. Faceted Diamond & Scintillation
Calculated with Blinn-Phong halfway vectors and surface normals for crown, table, girdle, and pavilion:
$$\text{specular} = \max\left(0, \vec{N} \cdot \vec{H}\right)^{14}$$

---

## 📜 License

MIT License. Inspired by [@jin_22ee](https://www.instagram.com/jin_22ee/).
