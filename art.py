"""
ASCII 3D Diamond Ring Animation
Recreation of @jin_22ee generative art reel
"""
import os, sys, time, math
import numpy as np

TAU = 2 * np.pi
R_BAND, R_TUBE = 1.05, 0.18
TABLE_Y, GIRDLE_Y, CULET_Y = 1.62, 1.36, 1.08
GIRDLE_R, TABLE_R = 0.56, 0.35


def band():
    # Ring band torus standing vertically in the X-Y plane
    theta = np.linspace(0, TAU, 360, endpoint=False)
    phi = np.linspace(0, TAU, 56, endpoint=False)
    T, P = np.meshgrid(theta, phi)
    t, p = T.ravel(), P.ravel()

    # Centerline: (R_BAND * sin(t), R_BAND * cos(t), 0)
    sx, sy = np.sin(t), np.cos(t)
    nx = np.cos(p) * sx
    ny = np.cos(p) * sy
    nz = np.sin(p)
    N = np.column_stack([nx, ny, nz])

    px = (R_BAND + R_TUBE * np.cos(p)) * sx
    py = (R_BAND + R_TUBE * np.cos(p)) * sy
    pz = R_TUBE * np.sin(p)
    return np.column_stack([px, py, pz]), N


def diamond():
    pts, normals, facet_ids = [], [], []

    # Flat table facet at top (Y = TABLE_Y)
    r_vals = np.linspace(0, TABLE_R, 20)
    t_vals = np.linspace(0, TAU, 64, endpoint=False)
    R_grid, T_grid = np.meshgrid(r_vals, t_vals)
    tx, tz = (R_grid * np.cos(T_grid)).ravel(), (R_grid * np.sin(T_grid)).ravel()
    ty = np.full_like(tx, TABLE_Y)
    pts.append(np.column_stack([tx, ty, tz]))
    normals.append(np.repeat([[0.0, 1.0, 0.0]], len(tx), axis=0))
    facet_ids.append(np.zeros(len(tx), dtype=int))

    # Crown & Pavilion brilliant facets
    num_facets = 16
    for f in range(num_facets):
        a1, a2 = TAU * f / num_facets, TAU * (f + 1) / num_facets
        amid = 0.5 * (a1 + a2)
        u, v = np.meshgrid(np.linspace(0, 1, 16), np.linspace(0, 1, 12))
        u_f, v_f = u.ravel(), v.ravel()
        ang = a1 + u_f * (a2 - a1)

        # Crown facet
        r_c = TABLE_R + v_f * (GIRDLE_R - TABLE_R)
        y_c = TABLE_Y + v_f * (GIRDLE_Y - TABLE_Y)
        pts.append(np.column_stack([r_c * np.cos(ang), y_c, r_c * np.sin(ang)]))
        n_c = np.array([np.cos(amid) * 0.72, 0.69, np.sin(amid) * 0.72])
        normals.append(np.repeat([n_c / np.linalg.norm(n_c)], len(ang), axis=0))
        facet_ids.append(np.full(len(ang), f + 1, dtype=int))

        # Pavilion facet
        r_p = GIRDLE_R * (1 - v_f)
        y_p = GIRDLE_Y + v_f * (CULET_Y - GIRDLE_Y)
        pts.append(np.column_stack([r_p * np.cos(ang), y_p, r_p * np.sin(ang)]))
        n_p = np.array([np.cos(amid) * 0.75, -0.66, np.sin(amid) * 0.75])
        normals.append(np.repeat([n_p / np.linalg.norm(n_p)], len(ang), axis=0))
        facet_ids.append(np.full(len(ang), f + 17, dtype=int))

    return np.concatenate(pts), np.concatenate(normals), np.concatenate(facet_ids)




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


BAND_P, BAND_N = band()
GEM_P, GEM_N, GEM_F = diamond()
PRONG_P, PRONG_N = prongs()

# Formation tracking metadata
BAND_T = np.abs(np.pi - (np.arctan2(BAND_P[:, 0], BAND_P[:, 1]) % TAU))
PRONG_U = np.tile(np.repeat(np.linspace(0, 1, 40), 16), 4)

# Set up background elements: atomic orbits and ambient glints
def init_orbits():
    pts = []
    t = np.linspace(0, TAU, 280, endpoint=False)
    # Orbit 1 tilted at +38 degrees
    x1 = 2.15 * np.cos(t)
    y1 = 1.25 * np.sin(t) * np.cos(math.radians(38))
    z1 = 1.25 * np.sin(t) * np.sin(math.radians(38))
    # Orbit 2 tilted at -38 degrees
    x2 = 2.15 * np.cos(t)
    y2 = 1.25 * np.sin(t) * np.cos(math.radians(-38))
    z2 = 1.25 * np.sin(t) * np.sin(math.radians(-38))
    pts.append(np.column_stack([x1, y1, z1]))
    pts.append(np.column_stack([x2, y2, z2]))
    return np.concatenate(pts)

# 272 ambient glints
np.random.seed(42)
GLINT_COUNT = 272
glint_phi = np.random.uniform(0, TAU, GLINT_COUNT)
glint_theta = np.random.uniform(-np.pi/2, np.pi/2, GLINT_COUNT)
glint_dist = np.random.uniform(1.3, 3.0, GLINT_COUNT)
glint_speeds = np.random.uniform(1.8, 4.5, GLINT_COUNT)
glint_phases = np.random.uniform(0, TAU, GLINT_COUNT)

GLINT_X = glint_dist * np.cos(glint_theta) * np.cos(glint_phi)
GLINT_Y = glint_dist * np.sin(glint_theta) + 0.6
GLINT_Z = glint_dist * np.cos(glint_theta) * np.sin(glint_phi)

ORBIT_PTS = init_orbits()

# Light direction and viewer
LIGHT = np.array([0.577, 0.707, -0.408])
LIGHT /= np.linalg.norm(LIGHT)

RAMP = " .:-=+*#%@"

def render_frame(rot_y_deg, elapsed_sec, width=64, height=34):
    rot_y = math.radians(rot_y_deg)
    tilt_x = math.radians(12.0)

    cos_y, sin_y = math.cos(rot_y), math.sin(rot_y)
    cos_x, sin_x = math.cos(tilt_x), math.sin(tilt_x)

    def transform(pts, normals=None):
        x = pts[:, 0]
        y = pts[:, 1]
        z = pts[:, 2]

        y1 = y * cos_x - z * sin_x
        z1 = y * sin_x + z * cos_x
        x1 = x

        x2 = x1 * cos_y + z1 * sin_y
        y2 = y1
        z2 = -x1 * sin_y + z1 * cos_y

        if normals is not None:
            nx = normals[:, 0]
            ny = normals[:, 1]
            nz = normals[:, 2]
            ny1 = ny * cos_x - nz * sin_x
            nz1 = ny * sin_x + nz * cos_x
            nx1 = nx
            nx2 = nx1 * cos_y + nz1 * sin_y
            ny2 = ny1
            nz2 = -nx1 * sin_y + nz1 * cos_y
            return (x2, y2, z2), (nx2, ny2, nz2)
        return (x2, y2, z2)

    # Formation Progression (Forms slowly and gracefully over the first 8 seconds)
    band_p = min(1.0, max(0.0, elapsed_sec / 3.2))
    prong_p = min(1.0, max(0.0, (elapsed_sec - 2.8) / 2.4))
    gem_p = min(1.0, max(0.0, (elapsed_sec - 5.0) / 2.3))
    flare_p = min(1.0, max(0.0, (elapsed_sec - 7.0) / 1.07))

    # Framebuffers
    zbuf = np.full((height, width), -9999.0)
    charbuf = np.full((height, width), " ", dtype="<U1")

    # Perspective camera (enlarged scale for prominent visibility)
    dist = 3.65
    Kx = 56.0
    Ky = 28.0
    cx = width / 2.0
    cy = height / 2.0 + 1.2

    hx, hy, hz = LIGHT[0], LIGHT[1], LIGHT[2] - 1.0
    hlen = math.sqrt(hx*hx + hy*hy + hz*hz)
    hx /= hlen; hy /= hlen; hz /= hlen

    # 1. Render Band (sweeps up symmetrically from bottom to top)
    if band_p > 0.0:
        band_mask = BAND_T <= (band_p * np.pi)
        if np.any(band_mask):
            sub_P = BAND_P[band_mask]
            sub_N = BAND_N[band_mask]
            (bx, by, bz), (bnx, bny, bnz) = transform(sub_P, sub_N)
            ooz = 1.0 / (bz + dist)
            xp = (cx + Kx * bx * ooz).astype(int)
            yp = (cy - Ky * by * ooz).astype(int)
            diff = bnx * LIGHT[0] + bny * LIGHT[1] + bnz * LIGHT[2]
            spec_b = (bnx * hx + bny * hy + bnz * hz)
            valid = (xp >= 0) & (xp < width) & (yp >= 0) & (yp < height)
            for i in np.where(valid)[0]:
                x_i, y_i = xp[i], yp[i]
                oz = ooz[i]
                if oz > zbuf[y_i, x_i]:
                    zbuf[y_i, x_i] = oz
                    df = max(0.0, diff[i])
                    sp = max(0.0, spec_b[i]) ** 16
                    lum = 0.28 + 0.65 * df + 0.40 * sp
                    idx = min(len(RAMP) - 1, max(1, int(lum * (len(RAMP) - 1))))
                    charbuf[y_i, x_i] = RAMP[idx]

    # 2. Render Prongs (grows upward from mounting to girdle)
    if prong_p > 0.0:
        prong_mask = PRONG_U <= prong_p
        if np.any(prong_mask):
            sub_P = PRONG_P[prong_mask]
            sub_N = PRONG_N[prong_mask]
            (px, py, pz), (pnx, pny, pnz) = transform(sub_P, sub_N)
            ooz = 1.0 / (pz + dist)
            xp = (cx + Kx * px * ooz).astype(int)
            yp = (cy - Ky * py * ooz).astype(int)
            diff = pnx * LIGHT[0] + pny * LIGHT[1] + pnz * LIGHT[2]
            spec_p = (pnx * hx + pny * hy + pnz * hz)
            valid = (xp >= 0) & (xp < width) & (yp >= 0) & (yp < height)
            for i in np.where(valid)[0]:
                x_i, y_i = xp[i], yp[i]
                oz = ooz[i]
                if oz > zbuf[y_i, x_i]:
                    zbuf[y_i, x_i] = oz
                    df = max(0.0, diff[i])
                    sp = max(0.0, spec_p[i]) ** 14
                    lum = 0.38 + 0.52 * df + 0.32 * sp
                    idx = min(len(RAMP) - 1, max(2, int(lum * (len(RAMP) - 1))))
                    charbuf[y_i, x_i] = RAMP[idx]

    # 3. Render Diamond (crystallizes upwards from culet cone to table facet)
    if gem_p > 0.0:
        gem_y_cutoff = CULET_Y + (TABLE_Y - CULET_Y) * gem_p
        gem_mask = GEM_P[:, 1] <= gem_y_cutoff
        if np.any(gem_mask):
            sub_P = GEM_P[gem_mask]
            sub_N = GEM_N[gem_mask]
            (gx, gy, gz), (gnx, gny, gnz) = transform(sub_P, sub_N)
            ooz = 1.0 / (gz + dist)
            xp = (cx + Kx * gx * ooz).astype(int)
            yp = (cy - Ky * gy * ooz).astype(int)
            diff = gnx * LIGHT[0] + gny * LIGHT[1] + gnz * LIGHT[2]
            spec = gnx * hx + gny * hy + gnz * hz

            valid = (xp >= 0) & (xp < width) & (yp >= 0) & (yp < height)
            for i in np.where(valid)[0]:
                x_i, y_i = xp[i], yp[i]
                oz = ooz[i]
                if oz > zbuf[y_i, x_i]:
                    zbuf[y_i, x_i] = oz
                    sp = max(0.0, spec[i]) ** 14
                    df = max(0.0, diff[i])
                    if sp > 0.48:
                        charbuf[y_i, x_i] = "*" if sp < 0.78 else "#"
                    else:
                        lum = 0.35 + 0.55 * df + 0.30 * sp
                        idx = min(len(RAMP) - 1, max(2, int(lum * (len(RAMP) - 1))))
                        charbuf[y_i, x_i] = RAMP[idx]

    # 4. Render Top Diamond Flare Beam (erupts once diamond forms)
    if flare_p > 0.0:
        max_flare_y = TABLE_Y + 0.90 * flare_p
        for vy in np.linspace(TABLE_Y + 0.04, max_flare_y, int(16 * flare_p)):
            for vx in [-0.05, -0.02, 0.0, 0.02, 0.05]:
                t_pt = np.array([[vx, vy, 0.0]])
                (tx, ty, tz) = transform(t_pt)
                oz = 1.0 / (tz[0] + dist)
                t_xp = int(cx + Kx * tx[0] * oz)
                t_yp = int(cy - Ky * ty[0] * oz)
                if 0 <= t_xp < width and 0 <= t_yp < height:
                    if oz > zbuf[t_yp, t_xp] - 0.02:
                        if abs(vx) < 0.01:
                            charbuf[t_yp, t_xp] = "|"
                        elif abs(vx) < 0.03:
                            charbuf[t_yp, t_xp] = ":" if (int(vy * 10) % 2 == 0) else "|"
                        else:
                            charbuf[t_yp, t_xp] = "."

    # 5. Render Background Orbits
    (ox, oy, oz_pts) = transform(ORBIT_PTS)
    ooz_o = 1.0 / (oz_pts + dist)
    xp_o = (cx + Kx * ox * ooz_o).astype(int)
    yp_o = (cy - Ky * oy * ooz_o).astype(int)
    valid_o = (xp_o >= 0) & (xp_o < width) & (yp_o >= 0) & (yp_o < height)
    for i in np.where(valid_o)[0]:
        x_i, y_i = xp_o[i], yp_o[i]
        if zbuf[y_i, x_i] <= 0:
            charbuf[y_i, x_i] = "." if i % 2 == 0 else "'"

    # 6. Render Twinkling Glints
    active_glints = 0
    for i in range(GLINT_COUNT):
        twinkle = math.sin(elapsed_sec * glint_speeds[i] + glint_phases[i])
        if twinkle > 0.15:
            active_glints += 1
            gpt = np.array([[GLINT_X[i], GLINT_Y[i], GLINT_Z[i]]])
            (gx_i, gy_i, gz_i) = transform(gpt)
            oz = 1.0 / (gz_i[0] + dist)
            g_xp = int(cx + Kx * gx_i[0] * oz)
            g_yp = int(cy - Ky * gy_i[0] * oz)
            if 0 <= g_xp < width and 0 <= g_yp < height:
                if oz > zbuf[g_yp, g_xp]:
                    charbuf[g_yp, g_xp] = "+" if twinkle > 0.82 else "."

    # Count letters
    non_space_count = int(np.count_nonzero(charbuf != " "))

    # Overlay HUD
    timer_str = f"•f {elapsed_sec:05.2f}s"
    t_start = width - len(timer_str) - 2
    if t_start >= 0:
        for idx, ch in enumerate(timer_str):
            charbuf[1, t_start + idx] = ch

    hud1 = "@jin_22ee · 2026"
    hud2 = f"rotation {rot_y_deg % 360.0:06.2f}°   glints {active_glints}"
    hud3 = f"letters {non_space_count:,}"

    for idx, ch in enumerate(hud1):
        if 2 + idx < width:
            charbuf[height - 4, 2 + idx] = ch
    for idx, ch in enumerate(hud2):
        if 2 + idx < width:
            charbuf[height - 3, 2 + idx] = ch
    for idx, ch in enumerate(hud3):
        if 2 + idx < width:
            charbuf[height - 2, 2 + idx] = ch

    lines = ["".join(row) for row in charbuf]
    status_bar = f"$ py art.py" + " " * (width - 27) + "running · 30 fps"
    lines.append(status_bar)

    return "\n".join(lines)


def main():
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass
    os.system("")
    sys.stdout.write("\033[?25l\033[2J")
    sys.stdout.flush()

    start_time = time.time()
    rot = 56.0
    fps = 30.0
    frame_duration = 1.0 / fps

    try:
        while True:
            t0 = time.time()
            elapsed = t0 - start_time
            rot += 1.25

            frame_text = render_frame(rot, elapsed)
            sys.stdout.write("\033[H" + frame_text)
            sys.stdout.flush()

            dt = time.time() - t0
            sleep_time = frame_duration - dt
            if sleep_time > 0:
                time.sleep(sleep_time)
    except KeyboardInterrupt:
        sys.stdout.write("\033[?25h\n")
        sys.stdout.flush()
        print("\nExited.")


if __name__ == "__main__":
    main()
