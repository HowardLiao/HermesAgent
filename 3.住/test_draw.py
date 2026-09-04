from PIL import Image, ImageDraw, ImageFont
import math

def create_banner():
    width, height = 1200, 240
    img = Image.new("RGBA", (width, height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Fluid watercolor/alcohol ink warm orange wash background
    for x in range(width):
        t = x / width
        # Warm orange (#D9531E / #E65100), Rust (#8B3A1C), Amber (#D97706), Citrus (#FB923C)
        # soft horizontal gradient with subtle sinusoidal fluid wave
        wave = math.sin(t * math.pi * 3) * 20
        r = int(255 - t * 40 + math.sin(t * 8) * 10)
        g = int(120 + t * 40 + math.cos(t * 6) * 15)
        b = int(30 + t * 50)
        alpha = int(180 + 50 * math.sin(t * math.pi))
        # draw soft fluid spots
    
    img.save("/Users/howardliao/legal_strategy_project/test_banner.png")
    print("Banner generated successfully")

create_banner()
