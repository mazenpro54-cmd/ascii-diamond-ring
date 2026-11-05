# 💍 3D Real Diamond Engagement Ring Studio & Generative Art

> An exact, high-fidelity recreation of the viral generative art Instagram Reel by [@jin_22ee](https://www.instagram.com/reel/DfTmTeQJEOi/) paired with a **Photorealistic 3D Real Jewelry Showcase** (smooth solid gold & brilliant crystal diamond, not pixelated).

Featuring real-time 3D PBR WebGL jewelry rendering, 18K Yellow Gold/Platinum/Rose Gold metals, 57-facet brilliant diamond refraction and fire dispersion, 90° angle controls, progressive 5-stage goldsmith forging from 0.0s to 8.07s, and retro ASCII terminal art.

---

## ✨ Features

- **💎 Photorealistic 3D Real Ring Mode (Non-pixel)**:
  - **Solid 3D Mesh**: Smooth, high-DPI solid geometry (no text/pixels) with comfort-fit D-profile cathedral shank, under-bezel gallery collar, and 4 delicate claw prongs clutching the diamond.
  - **Realistic PBR Shading**: Specular reflections on 18K Yellow Gold, Platinum, Rose Gold, and Obsidian Titanium with soft contact shadows.
  - **57-Facet Brilliant Diamond**: High-refraction (IOR 2.42) crystal physics, Fresnel transparency, specular sparkle point lights, and dispersion fire flares!
  - **📐 90° Angle Controls**: Dedicated 1-click presets for **90° Upright**, **90° Side Profile**, **90° Overhead**, and **90° Lay Flat**.
- **💍 5-Stage Goldsmith Forge Sequence (0.0s → 8.07s)**:
  - `Stage 1 (0.0s – 2.8s)`: **Shank Forging** — precious metal band forms around a ring mandrel into a seamless circular comfort-fit loop.
  - `Stage 2 (2.8s – 4.5s)`: **Basket Mounting** — cathedral shoulders and 4 claw prongs with under-bezel gallery rail mount onto the ring bridge.
  - `Stage 3 (4.5s – 6.0s)`: **Gemstone Descent** — the cut diamond lowers from above directly into the prong basket.
  - `Stage 4 (6.0s – 7.0s)`: **Claw Setting** — claw tips bend inward over the diamond crown, locking the stone in place.
  - `Stage 5 (7.0s – 8.07s)`: **Brilliance & Flares** — high-polish metal luster, facet scintillation, and cosmic flare burst.
- **✨ Viral Reel Mode**: Switch anytime to the exact 1:1 original Instagram reel ASCII terminal geometry and timing (`python art.py --style reel` or toggle in UI).
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
- `9`     : Cycle **90° angle modes** (90° Upright Perpendicular → 90° Overhead → 90° Side Profile → 90° Lay Flat)
- `O`     : Toggle 90° horizontal laying-flat orientation on/off
- `M`     : Toggle style live between **Realistic Jeweler** (`real`) and **Viral Reel** (`reel`)
- `Space` : Pause / Resume rotation & formation
- `R`     : Reset & replay formation from 0.0s
- `C`     : Cycle color theme live (Cyan → Gold → Rose → Matrix → Classic)
- `+` / `-`: Increase / decrease rotation speed
- `Q`     : Clean exit

### ⚙️ Command-Line Options
| Flag | Default | Description |
|---|---|---|
| `--style` | `real` | Ring style: `real` (realistic jeweler engagement ring) or `reel` (Instagram reel) |
| `--rot` | `90.0` | Initial rotation / yaw angle in degrees (default: `90.0`) |
| `--tilt` | `None` | Camera tilt angle in degrees (`0` for 90° upright perpendicular, `90` for overhead) |
| `--orient90` | `False` | Rotate ring 90° into horizontal laying-flat orientation (XZ plane) |
| `--freeze` | `False` | Freeze rotation at the given angle without auto-spinning |
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
