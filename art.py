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


# Formation tracking metadata for Reel mode
BAND_T = np.abs(np.pi - (np.arctan2(BAND_P[:, 0], BAND_P[:, 1]) % TAU))
PRONG_U = np.tile(np.repeat(np.linspace(0, 1, 40), 16), 4)

# ==============================================================================
# REALISTIC JEWELER RING MODEL (Cathedral Shank, Gallery Wire, Claws, 57-Facet Cut)
# ==============================================================================
def init_real_ring():
    # 1. Comfort-fit shank with cathedral tapered shoulders
    band_pts, band_nrms, band_t = [], [], []
    nT, nP = 220, 36
    for i in range(nT):
        t = (i / nT) * TAU
        sx, sy = math.sin(t), math.cos(t)
        angle_from_bot = abs(math.pi - t)
        
        top_f = max(0.0, (angle_from_bot - 2.1) / (math.pi - 2.1))
        r_band = 1.05 + 0.07 * (top_f ** 2)
        r_tube_x = 0.16 + 0.05 * top_f
        r_tube_z = 0.19 + 0.05 * top_f
        
        for j in range(nP):
            p = (j / nP) * TAU
            cp, sp = math.cos(p), math.sin(p)
            rad_offset = (cp * 0.82 if cp < 0 else cp * 1.18) * r_tube_x
            px = (r_band + rad_offset) * sx
            py = (r_band + rad_offset) * sy
            pz = sp * r_tube_z
            band_pts.append([px, py, pz])
            band_nrms.append([cp * sx, cp * sy, sp])
            band_t.append(angle_from_bot)

    # 2. Under-bezel gallery rail (collar bracing the prongs)
    gal_pts, gal_nrms = [], []
    for t in np.linspace(0, TAU, 90, endpoint=False):
        gx, gz = 0.38 * math.cos(t), 0.38 * math.sin(t)
        for p in np.linspace(0, TAU, 10, endpoint=False):
            cp, sp = math.cos(p), math.sin(p)
            gal_pts.append([gx + 0.024 * cp * math.cos(t), 1.25 + 0.024 * sp, gz + 0.024 * cp * math.sin(t)])
            gal_nrms.append([cp * math.cos(t), sp, cp * math.sin(t)])

    # 3. 4 Claw prongs with inward curving tips
    prong_pts, prong_nrms, prong_u = [], [], []
    for i in range(4):
        a = TAU * (i + 0.5) / 4
        ca, sa = math.cos(a), math.sin(a)
        for u in np.linspace(0, 1, 38):
            if u < 0.65:
                tu = u / 0.65
                r = 0.14 + tu * (0.58 - 0.14)
                y = 1.05 + tu * (1.36 - 1.05)
            else:
                tu = (u - 0.65) / 0.35
                r = 0.58 - tu * 0.10
                y = 1.36 + tu * 0.22
            
            for phi in np.linspace(0, TAU, 14, endpoint=False):
                cp, sp = math.cos(phi), math.sin(phi)
                th = 0.026 * (1.0 - 0.25 * u)
                px = r * ca - sa * th * cp
                pz = r * sa + ca * th * cp
                py = y + th * sp
                prong_pts.append([px, py, pz])
                prong_nrms.append([-sa * cp, sp, ca * cp])
                prong_u.append(u)

    # 4. Brilliant cut faceted diamond (57-facet geometry)
    gem_pts, gem_nrms, gem_ids = [], [], []
    # Table facet
    for r in np.linspace(0.01, 0.35, 14):
        for t in np.linspace(0, TAU, 36, endpoint=False):
            gem_pts.append([r * math.cos(t), 1.62, r * math.sin(t)])
            gem_nrms.append([0.0, 1.0, 0.0])
            gem_ids.append(0)

    # Star & Kite facets (crown)
    for k in range(8):
        a0 = TAU * k / 8
        a1 = TAU * (k + 1) / 8
        amid = 0.5 * (a0 + a1)
        v0 = np.array([0.35 * math.cos(a0), 1.62, 0.35 * math.sin(a0)])
        v1 = np.array([0.35 * math.cos(a1), 1.62, 0.35 * math.sin(a1)])
        v_star = np.array([0.45 * math.cos(amid), 1.50, 0.45 * math.sin(amid)])
        n_star = np.cross(v1 - v0, v_star - v0)
        n_star /= np.linalg.norm(n_star)
        for u in np.linspace(0.1, 0.9, 6):
            for v in np.linspace(0.1, 0.9 - u, 6):
                gem_pts.append((1 - u - v) * v0 + u * v1 + v * v_star)
                gem_nrms.append(n_star)
                gem_ids.append(k + 1)

    # Pavilion main facets
    culet = np.array([0.0, 1.08, 0.0])
    for k in range(8):
        a0 = TAU * k / 8
        a1 = TAU * (k + 1) / 8
        v0 = np.array([0.56 * math.cos(a0), 1.36, 0.56 * math.sin(a0)])
        v1 = np.array([0.56 * math.cos(a1), 1.36, 0.56 * math.sin(a1)])
        n_pav = np.cross(v1 - v0, culet - v0)
        n_pav /= np.linalg.norm(n_pav)
        for u in np.linspace(0.05, 0.95, 8):
            for v in np.linspace(0.05, 0.95 - u, 8):
                gem_pts.append((1 - u - v) * v0 + u * v1 + v * culet)
                gem_nrms.append(n_pav)
                gem_ids.append(k + 9)

    return (np.array(band_pts), np.array(band_nrms), np.array(band_t)), \
           (np.array(gal_pts), np.array(gal_nrms)), \
           (np.array(prong_pts), np.array(prong_nrms), np.array(prong_u)), \
           (np.array(gem_pts), np.array(gem_nrms), np.array(gem_ids))

(REAL_BAND_P, REAL_BAND_N, REAL_BAND_T), \
(REAL_GAL_P, REAL_GAL_N), \
(REAL_PRONG_P, REAL_PRONG_N, REAL_PRONG_U), \
(REAL_GEM_P, REAL_GEM_N, REAL_GEM_F) = init_real_ring()

# Set up background elements: atomic orbits and ambient glints
def init_orbits():
    pts = []
    t = np.linspace(0, TAU, 280, endpoint=False)
    x1 = 2.15 * np.cos(t)
    y1 = 1.25 * np.sin(t) * np.cos(math.radians(38))
    z1 = 1.25 * np.sin(t) * np.sin(math.radians(38))
    x2 = 2.15 * np.cos(t)
    y2 = 1.25 * np.sin(t) * np.cos(math.radians(-38))
    z2 = 1.25 * np.sin(t) * np.sin(math.radians(-38))
    pts.append(np.column_stack([x1, y1, z1]))
    pts.append(np.column_stack([x2, y2, z2]))
    return np.concatenate(pts)

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

LIGHT = np.array([0.577, 0.707, -0.408])
LIGHT /= np.linalg.norm(LIGHT)

RAMP = " .:-=+*#%@"

# Color themes (RGB palettes for TrueColor mode)
THEMES = {
    "classic": {
        "band": (210, 215, 225),
        "prong": (230, 235, 245),
        "gem": (255, 255, 255),
        "spec": (255, 255, 255),
        "flare": (200, 240, 255),
        "orbit": (130, 160, 200),
        "glint": (180, 220, 255),
        "hud": (150, 170, 190),
    },
    "cyan": {
        "band": (170, 200, 220),
        "prong": (200, 240, 255),
        "gem": (100, 235, 255),
        "spec": (255, 255, 255),
        "flare": (120, 255, 255),
        "orbit": (80, 140, 210),
        "glint": (150, 250, 255),
        "hud": (100, 200, 240),
    },
    "matrix": {
        "band": (60, 180, 80),
        "prong": (90, 220, 110),
        "gem": (120, 255, 140),
        "spec": (220, 255, 220),
        "flare": (100, 255, 120),
        "orbit": (40, 120, 60),
        "glint": (90, 255, 120),
        "hud": (80, 200, 100),
    },
    "gold": {
        "band": (235, 185, 90),
        "prong": (255, 215, 120),
        "gem": (255, 245, 200),
        "spec": (255, 255, 240),
        "flare": (255, 220, 130),
        "orbit": (170, 130, 60),
        "glint": (255, 210, 100),
        "hud": (220, 180, 100),
    },
    "rose": {
        "band": (235, 150, 150),
        "prong": (250, 180, 180),
        "gem": (255, 215, 225),
        "spec": (255, 255, 255),
        "flare": (255, 180, 200),
        "orbit": (160, 90, 120),
        "glint": (255, 170, 200),
        "hud": (230, 140, 170),
    }
}


def render_frame(rot_y_deg, elapsed_sec, width=64, height=34, duration=8.07, message="@jin_22ee · 2026", color_mode=False, theme_name="cyan", style="real", tilt_deg=None, orient_90=False):
    rot_y = math.radians(rot_y_deg)
    if tilt_deg is not None:
        tilt_x = math.radians(tilt_deg)
    else:
        tilt_x = math.radians(24.0 if style == "real" else 12.0)

    cos_y, sin_y = math.cos(rot_y), math.sin(rot_y)
    cos_x, sin_x = math.cos(tilt_x), math.sin(tilt_x)

    def transform(points, normals=None):
        if orient_90:
            # Rotate model 90 degrees around X into horizontal laying-down orientation
            x0 = points[:, 0]
            y0 = -points[:, 2]
            z0 = points[:, 1]
        else:
            x0 = points[:, 0]
            y0 = points[:, 1]
            z0 = points[:, 2]

        y1 = y0 * cos_x - z0 * sin_x
        z1 = y0 * sin_x + z0 * cos_x
        x1 = x0

        x2 = x1 * cos_y + z1 * sin_y
        y2 = y1
        z2 = -x1 * sin_y + z1 * cos_y

        if normals is not None:
            if orient_90:
                nx0 = normals[:, 0]
                ny0 = -normals[:, 2]
                nz0 = normals[:, 1]
            else:
                nx0 = normals[:, 0]
                ny0 = normals[:, 1]
                nz0 = normals[:, 2]

            ny1 = ny0 * cos_x - nz0 * sin_x
            nz1 = ny0 * sin_x + nz0 * cos_x
            nx1 = nx0
            nx2 = nx1 * cos_y + nz1 * sin_y
            ny2 = ny1
            nz2 = -nx1 * sin_y + nz1 * cos_y
            return (x2, y2, z2), (nx2, ny2, nz2)
        return (x2, y2, z2)

    # Formation Progression & Stages
    stage_tag = ""
    if duration > 0.0:
        norm_t = min(1.0, elapsed_sec / duration)
        if style == "real":
            # Realistic Jeweler Formation
            band_p = min(1.0, max(0.0, norm_t / 0.35))
            basket_p = min(1.0, max(0.0, (norm_t - 0.30) / 0.25))
            gem_p = min(1.0, max(0.0, (norm_t - 0.50) / 0.25))
            crimp_p = min(1.0, max(0.0, (norm_t - 0.72) / 0.14))
            flare_p = min(1.0, max(0.0, (norm_t - 0.85) / 0.15))

            if norm_t < 0.32:
                stage_tag = "[1/5 FORGING SHANK]"
            elif norm_t < 0.52:
                stage_tag = "[2/5 MOUNTING BASKET]"
            elif norm_t < 0.72:
                stage_tag = "[3/5 SETTING GEMSTONE]"
            elif norm_t < 0.85:
                stage_tag = "[4/5 CRIMPING CLAWS]"
            else:
                stage_tag = "[5/5 BRILLIANCE LOCKED]"
        else:
            # Viral Reel Progression
            band_p = min(1.0, max(0.0, norm_t / 0.40))
            basket_p = min(1.0, max(0.0, (norm_t - 0.35) / 0.30))
            gem_p = min(1.0, max(0.0, (norm_t - 0.62) / 0.28))
            crimp_p = 1.0
            flare_p = min(1.0, max(0.0, (norm_t - 0.88) / 0.12))
            stage_tag = "[REEL MODE]"
    else:
        band_p = basket_p = gem_p = crimp_p = flare_p = 1.0
        stage_tag = "[CRAFTED]"

    # Select geometry
    if style == "real":
        B_P, B_N, B_T = REAL_BAND_P, REAL_BAND_N, REAL_BAND_T
        P_P, P_N, P_U = REAL_PRONG_P, REAL_PRONG_N, REAL_PRONG_U
        G_P, G_N, G_F = REAL_GEM_P, REAL_GEM_N, REAL_GEM_F
    else:
        B_P, B_N, B_T = BAND_P, BAND_N, BAND_T
        P_P, P_N, P_U = PRONG_P, PRONG_N, PRONG_U
        G_P, G_N, G_F = GEM_P, GEM_N, GEM_F

    # Framebuffers
    zbuf = np.full((height, width), -9999.0)
    charbuf = np.full((height, width), " ", dtype="<U1")
    colbuf = np.zeros((height, width, 3), dtype=np.uint8)

    palette = THEMES.get(theme_name, THEMES["cyan"])

    # Perspective camera
    dist = 3.65
    Kx = 56.0
    Ky = 28.0
    cx = width / 2.0
    cy = height / 2.0 + (0.8 if style == "real" else 1.2)

    hx, hy, hz = LIGHT[0], LIGHT[1], LIGHT[2] - 1.0
    hlen = math.sqrt(hx*hx + hy*hy + hz*hz)
    hx /= hlen; hy /= hlen; hz /= hlen

    # 1. Band
    if band_p > 0.0:
        band_mask = B_T <= (band_p * np.pi)
        if np.any(band_mask):
            sub_P = B_P[band_mask]
            sub_N = B_N[band_mask]
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
                    col = palette["spec"] if sp > 0.6 else palette["band"]
                    colbuf[y_i, x_i] = [min(255, max(0, int(c * lum))) for c in col]

    # 2. Gallery Rail (Real mode under-bezel collar)
    if style == "real" and basket_p > 0.2:
        (gal_x, gal_y, gal_z), (gal_nx, gal_ny, gal_nz) = transform(REAL_GAL_P, REAL_GAL_N)
        ooz = 1.0 / (gal_z + dist)
        xp = (cx + Kx * gal_x * ooz).astype(int)
        yp = (cy - Ky * gal_y * ooz).astype(int)
        diff = gal_nx * LIGHT[0] + gal_ny * LIGHT[1] + gal_nz * LIGHT[2]
        valid = (xp >= 0) & (xp < width) & (yp >= 0) & (yp < height)
        for i in np.where(valid)[0]:
            x_i, y_i = xp[i], yp[i]
            oz = ooz[i]
            if oz > zbuf[y_i, x_i]:
                zbuf[y_i, x_i] = oz
                df = max(0.0, diff[i])
                lum = 0.35 + 0.60 * df
                idx = min(len(RAMP) - 1, max(1, int(lum * (len(RAMP) - 1))))
                charbuf[y_i, x_i] = RAMP[idx]
                colbuf[y_i, x_i] = palette["prong"]

    # 3. Prongs & Claws
    if basket_p > 0.0:
        prong_mask = P_U <= basket_p
        if np.any(prong_mask):
            sub_P = P_P[prong_mask].copy()
            sub_N = P_N[prong_mask].copy()

            # In real mode, claw tips bend inward over crown during crimp stage
            if style == "real" and crimp_p > 0.0:
                is_tip = sub_P[:, 1] > 1.38
                if np.any(is_tip):
                    sub_P[is_tip, 0] *= (1.0 - 0.08 * crimp_p)
                    sub_P[is_tip, 2] *= (1.0 - 0.08 * crimp_p)

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
                    colbuf[y_i, x_i] = palette["prong"]

    # 4. Gemstone (Descends into prongs in real mode)
    if gem_p > 0.0:
        if style == "real":
            # Diamond descends from above into the basket seat
            descent_y = (1.0 - gem_p) * 1.5
            sub_P = G_P.copy()
            sub_P[:, 1] += descent_y
            sub_N = G_N
            sub_F = G_F
            gem_visible = True
        else:
            # Diamond crystallizes from culet to table
            gem_y_cutoff = CULET_Y + (TABLE_Y - CULET_Y) * gem_p
            gem_mask = G_P[:, 1] <= gem_y_cutoff
            gem_visible = np.any(gem_mask)
            if gem_visible:
                sub_P = G_P[gem_mask]
                sub_N = G_N[gem_mask]
                sub_F = G_F[gem_mask]

        if gem_visible:
            (gx, gy, gz), (gnx, gny, gnz) = transform(sub_P, sub_N)
            ooz = 1.0 / (gz + dist)
            xp = (cx + Kx * gx * ooz).astype(int)
            yp = (cy - Ky * gy * ooz).astype(int)
            diff = gnx * LIGHT[0] + gny * LIGHT[1] + gnz * LIGHT[2]
            spec_g = (gnx * hx + gny * hy + gnz * hz)

            valid = (xp >= 0) & (xp < width) & (yp >= 0) & (yp < height)
            for i in np.where(valid)[0]:
                x_i, y_i = xp[i], yp[i]
                oz = ooz[i]
                if oz > zbuf[y_i, x_i]:
                    zbuf[y_i, x_i] = oz
                    sp = max(0.0, spec_g[i])
                    fid = sub_F[i]
                    f_sparkle = math.sin(rot_y * 4.0 + fid * 1.618)
                    is_sparkle = (sp > 0.72) and (f_sparkle > 0.2)
                    is_super = (sp > 0.88) and (f_sparkle > 0.6)

                    if is_super:
                        charbuf[y_i, x_i] = "@"
                        colbuf[y_i, x_i] = palette["spec"]
                    elif is_sparkle:
                        charbuf[y_i, x_i] = "%"
                        colbuf[y_i, x_i] = palette["gem"]
                    else:
                        df = max(0.0, diff[i])
                        lum = 0.35 + 0.65 * df
                        idx = min(len(RAMP) - 1, max(2, int(lum * (len(RAMP) - 1))))
                        charbuf[y_i, x_i] = RAMP[idx]
                        colbuf[y_i, x_i] = palette["gem"]

    # 5. Vertical Flare Beam
    if flare_p > 0.0:
        table_world = np.array([[0.0, TABLE_Y + 0.05, 0.0]])
        (fx, fy, fz) = transform(table_world)
        ooz = 1.0 / (fz[0] + dist)
        fl_x = int(cx + Kx * fx[0] * ooz)
        fl_y = int(cy - Ky * fy[0] * ooz)

        flare_reach = int(14 * flare_p)
        for dy in range(1, flare_reach):
            y_pos = fl_y - dy
            if 0 <= y_pos < height and 0 <= fl_x < width:
                if ooz > zbuf[y_pos, fl_x]:
                    zbuf[y_pos, fl_x] = ooz
                    charbuf[y_pos, fl_x] = ":" if dy % 2 == 0 else "."
                    colbuf[y_pos, fl_x] = palette["flare"]
            if dy % 3 == 0:
                for off in [-1, 1]:
                    nx_pos = fl_x + off
                    if 0 <= y_pos < height and 0 <= nx_pos < width:
                        if ooz > zbuf[y_pos, nx_pos] and charbuf[y_pos, nx_pos] == " ":
                            charbuf[y_pos, nx_pos] = "."
                            colbuf[y_pos, nx_pos] = palette["flare"]

    # 6. Twin Atomic Orbits
    (ox, oy, oz) = transform(ORBIT_PTS)
    ooz = 1.0 / (oz + dist)
    xp = (cx + Kx * ox * ooz).astype(int)
    yp = (cy - Ky * oy * ooz).astype(int)
    valid = (xp >= 0) & (xp < width) & (yp >= 0) & (yp < height)
    for i in np.where(valid)[0]:
        x_i, y_i = xp[i], yp[i]
        oz_val = ooz[i]
        if oz_val > zbuf[y_i, x_i] and charbuf[y_i, x_i] == " ":
            charbuf[y_i, x_i] = "."
            colbuf[y_i, x_i] = palette["orbit"]

    # 7. 272 Ambient Glints
    active_glints = 0
    (gx, gy, gz) = transform(np.column_stack([GLINT_X, GLINT_Y, GLINT_Z]))
    ooz = 1.0 / (gz + dist)
    xp = (cx + Kx * gx * ooz).astype(int)
    yp = (cy - Ky * gy * ooz).astype(int)
    phases = np.sin(elapsed_sec * glint_speeds + glint_phases)
    for i in range(GLINT_COUNT):
        p_val = phases[i]
        if p_val > 0.45:
            active_glints += 1
            x_i, y_i = xp[i], yp[i]
            if 0 <= x_i < width and 0 <= y_i < height:
                if ooz[i] > zbuf[y_i, x_i] and charbuf[y_i, x_i] == " ":
                    charbuf[y_i, x_i] = "+" if p_val > 0.88 else "."
                    colbuf[y_i, x_i] = palette["glint"]

    # Count non-space characters
    non_space_count = int(np.sum(charbuf != " "))

    # Overlay HUD
    timer_str = f"•f {elapsed_sec:05.2f}s"
    t_start = width - len(timer_str) - 2
    if t_start >= 0:
        for idx, ch in enumerate(timer_str):
            charbuf[1, t_start + idx] = ch

    orient_str = " 90°FLAT" if orient_90 else ""
    hud1 = f"{message[:20]}  {stage_tag}{orient_str}"[:width - 4]
    hud2 = f"rot {rot_y_deg % 360.0:05.1f}°  glints {active_glints}  style {style.upper()}"
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

    # Assemble lines (monochrome or 24-bit TrueColor)
    lines = []
    if not color_mode:
        for y in range(height):
            lines.append("".join(charbuf[y]))
    else:
        for y in range(height):
            row_str = ""
            for x in range(width):
                ch = charbuf[y, x]
                if ch == " ":
                    row_str += " "
                else:
                    r, g, b = colbuf[y, x]
                    if r == 0 and g == 0 and b == 0:
                        r, g, b = palette["hud"]
                    row_str += f"\033[38;2;{r};{g};{b}m{ch}\033[0m"
            lines.append(row_str)

    status_bar = f"$ py art.py" + " " * (width - 27) + "running · 30 fps"
    lines.append(status_bar)

    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="3D ASCII Diamond Ring - @jin_22ee Recreation & Realistic Jeweler")
    parser.add_argument("--style", choices=["real", "reel"], default="real", help="Ring style: 'real' (realistic engagement ring & forge) or 'reel' (exact Instagram reel)")
    parser.add_argument("--color", action="store_true", help="Enable 24-bit TrueColor ANSI output")
    parser.add_argument("--theme", choices=["classic", "cyan", "matrix", "gold", "rose"], default="cyan", help="Color theme")
    parser.add_argument("--duration", type=float, default=8.07, help="Formation duration in seconds (default: 8.07, 0 for instant)")
    parser.add_argument("--speed", type=float, default=1.0, help="Rotation speed multiplier")
    parser.add_argument("--rot", type=float, default=90.0, help="Starting rotation / yaw angle in degrees (default: 90.0)")
    parser.add_argument("--tilt", type=float, default=None, help="Camera tilt angle in degrees (e.g. 90 for overhead, 0 for 90-degree upright perpendicular)")
    parser.add_argument("--orient90", action="store_true", help="Rotate ring 90 degrees into horizontal laying-flat orientation")
    parser.add_argument("--freeze", action="store_true", help="Freeze rotation at the given angle")
    parser.add_argument("--message", type=str, default="@jin_22ee · 2026", help="Dedication message displayed on HUD")
    parser.add_argument("--fps", type=int, default=30, help="Target FPS (default: 30)")
    args = parser.parse_args()

    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass

    sys.stdout.write("\033[?25l\033[2J")
    sys.stdout.flush()

    is_windows = (os.name == "nt")
    if is_windows:
        import msvcrt

    rot = args.rot
    fps = max(10, min(60, args.fps))
    frame_duration = 1.0 / fps
    color_mode = args.color
    theme_name = args.theme
    speed_mult = args.speed
    style_mode = args.style
    tilt_deg = args.tilt
    orient_90 = args.orient90
    is_paused = args.freeze
    anim_time = 0.0

    print(f"Starting 3D ASCII Diamond Ring [{style_mode.upper()} - {rot:.0f}°]... [9]: 90° Mode | [O]: Lay Flat | Space: Pause | R: Replay | Q: Quit")
    time.sleep(0.4)

    last_clock = time.time()
    angle_mode_idx = 0
    angle_presets = [
        ("rot_90", 90.0, None, False),
        ("upright_90", 0.0, 0.0, False),
        ("overhead_90", 56.0, 90.0, False),
        ("flat_90", 56.0, 24.0, True),
    ]

    try:
        while True:
            t_now = time.time()
            dt = t_now - last_clock
            last_clock = t_now

            if is_windows and msvcrt.kbhit():
                key = msvcrt.getch()
                if key in (b"q", b"Q", b"\x1b"):
                    break
                elif key == b" ":
                    is_paused = not is_paused
                elif key in (b"r", b"R"):
                    anim_time = 0.0
                    rot = args.rot
                elif key in (b"m", b"M"):
                    style_mode = "reel" if style_mode == "real" else "real"
                elif key in (b"o", b"O"):
                    orient_90 = not orient_90
                elif key == b"9":
                    angle_mode_idx = (angle_mode_idx + 1) % len(angle_presets)
                    mode_name, new_rot, new_tilt, new_orient = angle_presets[angle_mode_idx]
                    rot = new_rot
                    tilt_deg = new_tilt
                    orient_90 = new_orient
                elif key in (b"c", b"C"):
                    themes_list = list(THEMES.keys())
                    curr_idx = themes_list.index(theme_name) if theme_name in themes_list else 0
                    theme_name = themes_list[(curr_idx + 1) % len(themes_list)]
                    color_mode = True
                elif key in (b"+", b"="):
                    speed_mult = min(4.0, speed_mult + 0.25)
                elif key in (b"-", b"_"):
                    speed_mult = max(0.2, speed_mult - 0.25)

            if not is_paused:
                anim_time += dt * speed_mult
                rot += 1.25 * speed_mult

            frame_text = render_frame(
                rot, anim_time,
                duration=args.duration,
                message=args.message,
                color_mode=color_mode,
                theme_name=theme_name,
                style=style_mode,
                tilt_deg=tilt_deg,
                orient_90=orient_90
            )
            sys.stdout.write("\033[H" + frame_text)
            sys.stdout.flush()

            elapsed_render = time.time() - t_now
            sleep_time = frame_duration - elapsed_render
            if sleep_time > 0:
                time.sleep(sleep_time)

    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\033[?25h\n")
        sys.stdout.flush()
        print("\nExited.")


if __name__ == "__main__":
    main()
