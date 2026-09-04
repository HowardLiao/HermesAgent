import os
import math
import random
from PIL import Image, ImageDraw, ImageFilter

random.seed(42)
OUT_DIR = "/Users/howardliao/legal_strategy_project"

# Color Palette: Warm Monochromatic Orange, Rust, Amber, Citrus
# Background: Pure White
C_WHITE = (255, 255, 255, 255)
C_TRANSPARENT = (255, 255, 255, 0)
C_RUST = (168, 50, 18, 255)       # 鐵鏽 #A83212
C_ORANGE = (222, 88, 20, 255)     # 標題橘 #DE5814
C_AMBER = (217, 119, 6, 255)      # 琥珀 #D97706
C_CITRUS = (245, 158, 11, 255)    # 柑橘金 #F59E0B
C_LIGHT_AMBER = (254, 243, 199, 255) # 淺琥珀淡色
C_CHARCOAL = (45, 55, 72, 255)    # 黑灰 #2D3748

def apply_fluid_wash(draw, w, h, base_color=(235, 120, 30), num_blobs=40):
    # Generates soft watercolor / alcohol ink wash texture
    wash_layer = Image.new("RGBA", (w, h), (255, 255, 255, 0))
    wash_draw = ImageDraw.Draw(wash_layer)
    for _ in range(num_blobs):
        cx = random.uniform(0, w)
        cy = random.uniform(0, h)
        rx = random.uniform(w * 0.1, w * 0.35)
        ry = random.uniform(h * 0.1, h * 0.35)
        # Randomize warm tones
        r_var = random.randint(-25, 25)
        g_var = random.randint(-20, 30)
        b_var = random.randint(0, 40)
        col = (
            min(255, max(0, base_color[0] + r_var)),
            min(255, max(0, base_color[1] + g_var)),
            min(255, max(0, base_color[2] + b_var)),
            random.randint(18, 55) # light wash
        )
        wash_draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=col)
    
    # Blur to create fluid alcohol ink gradient
    wash_layer = wash_layer.filter(ImageFilter.GaussianBlur(radius=int(w * 0.05)))
    return wash_layer

def make_cover_artwork():
    # 3x supersampling for high resolution
    SCALE = 3
    W, H = 800 * SCALE, 500 * SCALE
    img = Image.new("RGBA", (W, H), C_WHITE)
    
    # Fluid watercolor & alcohol ink background texture
    wash = apply_fluid_wash(None, W, H, base_color=(230, 110, 30), num_blobs=45)
    img = Image.alpha_composite(img, wash)
    draw = ImageDraw.Draw(img)
    
    cx, cy = W // 2, int(H * 0.52)
    
    # Concentric decorative fine-line halos (Egyptian Sun Disc & Orbit)
    for radius, stroke_w, color in [
        (int(170 * SCALE), int(2.5 * SCALE), C_AMBER),
        (int(150 * SCALE), int(1.5 * SCALE), C_CITRUS),
        (int(130 * SCALE), int(1.0 * SCALE), C_RUST),
        (int(110 * SCALE), int(2.0 * SCALE), C_AMBER),
        (int(85 * SCALE), int(4.0 * SCALE), C_ORANGE)
    ]:
        draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], outline=color, width=stroke_w)
    
    # Geometric rays radiating from sun disc (fine strokes)
    num_rays = 36
    for i in range(num_rays):
        angle = i * (2 * math.pi / num_rays)
        r1 = int(175 * SCALE)
        r2 = int(215 * SCALE if i % 2 == 0 else 195 * SCALE)
        x1 = cx + math.cos(angle) * r1
        y1 = cy + math.sin(angle) * r1
        x2 = cx + math.cos(angle) * r2
        y2 = cy + math.sin(angle) * r2
        col = C_AMBER if i % 2 == 0 else C_CITRUS
        draw.line([x1, y1, x2, y2], fill=col, width=int(1.5 * SCALE))
    
    # Egyptian Winged Sun Disc / Horus Wings (stylized geometric feathers)
    wing_span = int(320 * SCALE)
    wing_y = cy - int(45 * SCALE)
    for side in [-1, 1]:
        for layer in range(4):
            pts = []
            for f in range(8):
                fx = cx + side * (int(90 * SCALE) + f * int(28 * SCALE))
                fy = wing_y + (f * int(7 * SCALE)) + (layer * int(12 * SCALE))
                # draw stylized stepped geometric feather
                draw.polygon([
                    (fx, fy),
                    (fx + side * int(22 * SCALE), fy - int(6 * SCALE)),
                    (fx + side * int(26 * SCALE), fy + int(10 * SCALE)),
                    (fx, fy + int(14 * SCALE))
                ], fill=C_CITRUS if layer % 2 == 0 else C_AMBER, outline=C_RUST)

    # Central Majestic Pyramid
    pyr_base = int(140 * SCALE)
    pyr_h = int(115 * SCALE)
    pyr_top = (cx, cy - int(10 * SCALE) - pyr_h)
    pyr_bl = (cx - pyr_base, cy + int(60 * SCALE))
    pyr_br = (cx + pyr_base, cy + int(60 * SCALE))
    pyr_mid = (cx, cy + int(60 * SCALE))
    
    # Pyramid faces (Amber & Rust shading)
    draw.polygon([pyr_top, pyr_bl, pyr_mid], fill=(245, 158, 11, 230), outline=C_RUST)
    draw.polygon([pyr_top, pyr_br, pyr_mid], fill=(217, 119, 6, 240), outline=C_RUST)
    
    # Golden Capstone (Pyramidion)
    cap_h = int(32 * SCALE)
    cap_top = pyr_top
    cap_bl = (cx - int(pyr_base * (cap_h / pyr_h)), pyr_top[1] + cap_h)
    cap_br = (cx + int(pyr_base * (cap_h / pyr_h)), pyr_top[1] + cap_h)
    cap_mid = (cx, pyr_top[1] + cap_h)
    draw.polygon([cap_top, cap_bl, cap_mid], fill=(255, 215, 0, 255), outline=C_RUST)
    draw.polygon([cap_top, cap_br, cap_mid], fill=(234, 88, 12, 255), outline=C_RUST)

    # Eye of Horus inside central sun / floating above
    eye_x, eye_y = cx, cy - int(55 * SCALE)
    ew, eh = int(55 * SCALE), int(25 * SCALE)
    
    # Eye contour
    draw.arc([eye_x - ew, eye_y - eh, eye_x + ew, eye_y + eh], start=0, end=180, fill=C_RUST, width=int(3 * SCALE))
    draw.arc([eye_x - ew, eye_y - eh - int(10 * SCALE), eye_x + ew, eye_y + eh - int(10 * SCALE)], start=180, end=360, fill=C_RUST, width=int(3 * SCALE))
    # Pupil
    draw.ellipse([eye_x - int(12 * SCALE), eye_y - int(12 * SCALE), eye_x + int(12 * SCALE), eye_y + int(12 * SCALE)], fill=C_RUST)
    draw.ellipse([eye_x - int(5 * SCALE), eye_y - int(5 * SCALE), eye_x + int(5 * SCALE), eye_y + int(5 * SCALE)], fill=C_CITRUS)
    # Eye of Horus teardrop and spiral spiral
    draw.line([eye_x, eye_y + eh - int(8 * SCALE), eye_x, eye_y + eh + int(30 * SCALE)], fill=C_RUST, width=int(2.5 * SCALE))
    # Spiral curl
    spiral_pts = []
    for deg in range(0, 360, 15):
        rad = math.radians(deg)
        r = int(5 * SCALE) + (deg / 360.0) * int(18 * SCALE)
        sx = eye_x - int(25 * SCALE) - r * math.cos(rad)
        sy = eye_y + eh + int(8 * SCALE) + r * math.sin(rad)
        spiral_pts.append((sx, sy))
    for k in range(len(spiral_pts)-1):
        draw.line([spiral_pts[k], spiral_pts[k+1]], fill=C_RUST, width=int(2.5 * SCALE))

    # Ankh symbols on left and right flanks
    for ax in [cx - int(240 * SCALE), cx + int(240 * SCALE)]:
        ay = cy + int(20 * SCALE)
        # Oval loop
        draw.ellipse([ax - int(20 * SCALE), ay - int(50 * SCALE), ax + int(20 * SCALE), ay], outline=C_RUST, width=int(3 * SCALE))
        # Horizontal bar
        draw.line([ax - int(30 * SCALE), ay + int(5 * SCALE), ax + int(30 * SCALE), ay + int(5 * SCALE)], fill=C_RUST, width=int(3.5 * SCALE))
        # Vertical stem
        draw.line([ax, ay + int(5 * SCALE), ax, ay + int(65 * SCALE)], fill=C_RUST, width=int(3.5 * SCALE))
        # Decorative dots
        draw.ellipse([ax - int(6 * SCALE), ay - int(28 * SCALE), ax + int(6 * SCALE), ay - int(16 * SCALE)], fill=C_CITRUS)

    # Downsample with Lanczos for ultra crisp vector look
    final_img = img.resize((800, 500), Image.Resampling.LANCZOS)
    final_img.save(os.path.join(OUT_DIR, "pharaoh_cover_art.png"), "PNG")
    print("pharaoh_cover_art.png generated")

def make_icons():
    SCALE = 3
    S = 180 * SCALE
    
    # 1. Icon Ankh (生命之符 / 正義權杖)
    img_ankh = Image.new("RGBA", (S, S), C_WHITE)
    wash = apply_fluid_wash(None, S, S, base_color=(235, 120, 20), num_blobs=20)
    img_ankh = Image.alpha_composite(img_ankh, wash)
    draw = ImageDraw.Draw(img_ankh)
    
    cx, cy = S // 2, S // 2
    # Decorative halo
    draw.ellipse([cx - int(72 * SCALE), cy - int(72 * SCALE), cx + int(72 * SCALE), cy + int(72 * SCALE)], outline=C_CITRUS, width=int(2 * SCALE))
    # Loop
    draw.ellipse([cx - int(22 * SCALE), cy - int(56 * SCALE), cx + int(22 * SCALE), cy - int(6 * SCALE)], outline=C_RUST, width=int(4 * SCALE))
    draw.ellipse([cx - int(12 * SCALE), cy - int(44 * SCALE), cx + int(12 * SCALE), cy - int(18 * SCALE)], fill=C_CITRUS)
    # Crossbar
    draw.line([cx - int(38 * SCALE), cy, cx + int(38 * SCALE), cy], fill=C_RUST, width=int(5 * SCALE))
    # Shaft
    draw.line([cx, cy, cx, cy + int(60 * SCALE)], fill=C_RUST, width=int(5 * SCALE))
    # Ends accents
    draw.rectangle([cx - int(40 * SCALE), cy - int(3 * SCALE), cx - int(35 * SCALE), cy + int(3 * SCALE)], fill=C_AMBER)
    draw.rectangle([cx + int(35 * SCALE), cy - int(3 * SCALE), cx + int(40 * SCALE), cy + int(3 * SCALE)], fill=C_AMBER)
    draw.rectangle([cx - int(4 * SCALE), cy + int(56 * SCALE), cx + int(4 * SCALE), cy + int(61 * SCALE)], fill=C_AMBER)
    
    img_ankh.resize((180, 180), Image.Resampling.LANCZOS).save(os.path.join(OUT_DIR, "icon_ankh.png"), "PNG")

    # 2. Icon Eye of Horus (荷魯斯之眼 / 司法洞察與保全)
    img_eye = Image.new("RGBA", (S, S), C_WHITE)
    wash = apply_fluid_wash(None, S, S, base_color=(230, 100, 30), num_blobs=20)
    img_eye = Image.alpha_composite(img_eye, wash)
    draw = ImageDraw.Draw(img_eye)
    
    draw.ellipse([cx - int(72 * SCALE), cy - int(72 * SCALE), cx + int(72 * SCALE), cy + int(72 * SCALE)], outline=C_AMBER, width=int(2 * SCALE))
    
    ew, eh = int(46 * SCALE), int(22 * SCALE)
    ey = cy - int(8 * SCALE)
    # Eye arcs
    draw.arc([cx - ew, ey - eh, cx + ew, ey + eh], start=0, end=180, fill=C_RUST, width=int(4 * SCALE))
    draw.arc([cx - ew, ey - eh - int(8 * SCALE), cx + ew, ey + eh - int(8 * SCALE)], start=180, end=360, fill=C_RUST, width=int(4 * SCALE))
    # Pupil
    draw.ellipse([cx - int(12 * SCALE), ey - int(12 * SCALE), cx + int(12 * SCALE), ey + int(12 * SCALE)], fill=C_RUST)
    draw.ellipse([cx - int(5 * SCALE), ey - int(5 * SCALE), cx + int(5 * SCALE), ey + int(5 * SCALE)], fill=C_CITRUS)
    # Tear line
    draw.line([cx + int(10 * SCALE), ey + eh - int(8 * SCALE), cx + int(10 * SCALE), ey + eh + int(24 * SCALE)], fill=C_RUST, width=int(3 * SCALE))
    # Spiral
    draw.arc([cx - int(35 * SCALE), ey + eh - int(4 * SCALE), cx - int(5 * SCALE), ey + eh + int(26 * SCALE)], start=40, end=280, fill=C_RUST, width=int(3 * SCALE))
    
    img_eye.resize((180, 180), Image.Resampling.LANCZOS).save(os.path.join(OUT_DIR, "icon_eye_horus.png"), "PNG")

    # 3. Icon Ma'at Scales of Justice (天秤與正義之羽 / 剩餘財產清算)
    img_scales = Image.new("RGBA", (S, S), C_WHITE)
    wash = apply_fluid_wash(None, S, S, base_color=(240, 130, 25), num_blobs=20)
    img_scales = Image.alpha_composite(img_scales, wash)
    draw = ImageDraw.Draw(img_scales)
    
    draw.ellipse([cx - int(72 * SCALE), cy - int(72 * SCALE), cx + int(72 * SCALE), cy + int(72 * SCALE)], outline=C_CITRUS, width=int(2 * SCALE))
    
    # Central pillar
    draw.line([cx, cy - int(45 * SCALE), cx, cy + int(50 * SCALE)], fill=C_RUST, width=int(4 * SCALE))
    # Base
    draw.rectangle([cx - int(35 * SCALE), cy + int(48 * SCALE), cx + int(35 * SCALE), cy + int(54 * SCALE)], fill=C_RUST)
    # Balance Beam
    draw.line([cx - int(48 * SCALE), cy - int(25 * SCALE), cx + int(48 * SCALE), cy - int(25 * SCALE)], fill=C_ORANGE, width=int(3.5 * SCALE))
    # Scale pans (left and right)
    for px in [cx - int(45 * SCALE), cx + int(45 * SCALE)]:
        draw.line([px, cy - int(25 * SCALE), px - int(15 * SCALE), cy + int(8 * SCALE)], fill=C_AMBER, width=int(1.5 * SCALE))
        draw.line([px, cy - int(25 * SCALE), px + int(15 * SCALE), cy + int(8 * SCALE)], fill=C_AMBER, width=int(1.5 * SCALE))
        draw.arc([px - int(18 * SCALE), cy + int(2 * SCALE), px + int(18 * SCALE), cy + int(18 * SCALE)], start=0, end=180, fill=C_RUST, width=int(3 * SCALE))
    # Top finial: Sun disc
    draw.ellipse([cx - int(10 * SCALE), cy - int(56 * SCALE), cx + int(10 * SCALE), cy - int(36 * SCALE)], fill=C_CITRUS, outline=C_RUST, width=int(2 * SCALE))

    img_scales.resize((180, 180), Image.Resampling.LANCZOS).save(os.path.join(OUT_DIR, "icon_scales.png"), "PNG")

    # 4. Icon Pyramid & Sun Disc (神聖基石 / 財產保全防脫產)
    img_pyr = Image.new("RGBA", (S, S), C_WHITE)
    wash = apply_fluid_wash(None, S, S, base_color=(235, 110, 15), num_blobs=20)
    img_pyr = Image.alpha_composite(img_pyr, wash)
    draw = ImageDraw.Draw(img_pyr)
    
    draw.ellipse([cx - int(72 * SCALE), cy - int(72 * SCALE), cx + int(72 * SCALE), cy + int(72 * SCALE)], outline=C_ORANGE, width=int(2 * SCALE))
    
    # Sun disk in background
    draw.ellipse([cx - int(24 * SCALE), cy - int(54 * SCALE), cx + int(24 * SCALE), cy - int(6 * SCALE)], fill=C_CITRUS, outline=C_RUST, width=int(2 * SCALE))
    
    # Pyramid
    p_top = (cx, cy - int(10 * SCALE))
    p_bl = (cx - int(52 * SCALE), cy + int(42 * SCALE))
    p_br = (cx + int(52 * SCALE), cy + int(42 * SCALE))
    p_mid = (cx + int(6 * SCALE), cy + int(42 * SCALE))
    
    draw.polygon([p_top, p_bl, p_mid], fill=C_CITRUS, outline=C_RUST)
    draw.polygon([p_top, p_br, p_mid], fill=C_AMBER, outline=C_RUST)
    
    # Capstone
    c_top = p_top
    c_bl = (cx - int(16 * SCALE), cy + int(6 * SCALE))
    c_br = (cx + int(18 * SCALE), cy + int(6 * SCALE))
    c_mid = (cx + int(2 * SCALE), cy + int(6 * SCALE))
    draw.polygon([c_top, c_bl, c_mid], fill=(255, 220, 50, 255), outline=C_RUST)
    draw.polygon([c_top, c_br, c_mid], fill=(234, 88, 12, 255), outline=C_RUST)
    
    img_pyr.resize((180, 180), Image.Resampling.LANCZOS).save(os.path.join(OUT_DIR, "icon_pyramid.png"), "PNG")

    # 5. Horizontal decorative Egyptian divider bar
    DW, DH = 900 * SCALE, 28 * SCALE
    img_div = Image.new("RGBA", (DW, DH), C_WHITE)
    d_draw = ImageDraw.Draw(img_div)
    
    mid_y = DH // 2
    # Fine center line
    d_draw.line([int(40 * SCALE), mid_y, DW - int(40 * SCALE), mid_y], fill=C_AMBER, width=int(1.5 * SCALE))
    # Center ornament
    dcx = DW // 2
    d_draw.ellipse([dcx - int(12 * SCALE), mid_y - int(12 * SCALE), dcx + int(12 * SCALE), mid_y + int(12 * SCALE)], fill=C_CITRUS, outline=C_RUST, width=int(2 * SCALE))
    # Diamond flanking accents
    for offset in [-120, -70, 70, 120]:
        ox = dcx + int(offset * SCALE)
        d_draw.polygon([
            (ox, mid_y - int(6 * SCALE)),
            (ox + int(6 * SCALE), mid_y),
            (ox, mid_y + int(6 * SCALE)),
            (ox - int(6 * SCALE), mid_y)
        ], fill=C_ORANGE)
    
    img_div.resize((900, 28), Image.Resampling.LANCZOS).save(os.path.join(OUT_DIR, "egypt_divider.png"), "PNG")
    print("All icons and divider generated successfully!")

make_cover_artwork()
make_icons()
