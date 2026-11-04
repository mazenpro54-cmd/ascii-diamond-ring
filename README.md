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

# Run standard monochrome mode (as seen in the reel)
python art.py

# Run in full 24-bit TrueColor with Cyan palette
python art.py --color --theme cyan

# Run with custom dedication message and Gold theme
python art.py --color --theme gold --message "Happy Anniversary ❤️"
```

### 🎮 Terminal Interactive Controls
- `Space` : Pause / Resume rotation & formation
- `R`     : Reset & replay formation from 0.0s
- `C`     : Cycle color theme live (Cyan → Gold → Rose → Matrix → Classic)
- `+` / `-`: Increase / decrease rotation speed
- `Q`     : Clean exit

### ⚙️ Command-Line Options
| Flag | Default | Description |
|---|---|---|
| `--color` | `False` | Enable 24-bit TrueColor ANSI output |
| `--theme` | `cyan` | Color palette (`classic`, `cyan`, `matrix`, `gold`, `rose`) |
| `--duration` | `8.07` | Formation animation time in seconds (`0` for instant full form) |
| `--speed` | `1.0` | Rotation speed multiplier |
| `--message` | `@jin_22ee · 2026` | Dedication message displayed on the top HUD |
| `--fps` | `30` | Target frame rate (10 – 60 FPS) |

---

## 🌐 Live Web Studio & Dedication Card

Experience the live interactive web version with crystal chime acoustics:
👉 **[mazenpro54-cmd.github.io/ascii-diamond-ring](https://mazenpro54-cmd.github.io/ascii-diamond-ring/)**

### Web Features
- 💎 **Gemstone Switcher**: Choose between Diamond, Ruby, Sapphire, Emerald, Amethyst, and Canary Yellow.
- 🎵 **Web Audio Synthesis**: Real-time synthesized pentatonic crystal glockenspiel chimes reacting to diamond glints.
- 💌 **Custom Dedication URLs**: Click **Dedicate / Share** to create a custom URL with your recipient's name or love note (e.g., `?to=Sarah&msg=Forever+%26+Always`).
- 📜 **ASCII TXT Export**: Download any animated frame snapshot as a raw text art file.
- 📺 **CRT Bloom & Scanlines**: Toggle retro terminal phosphor glow and glass scanline overlay.
- ⏱️ **Interactive Formation Scrubber**: Slide through 0.0s to 8.07s frame-by-frame.

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
