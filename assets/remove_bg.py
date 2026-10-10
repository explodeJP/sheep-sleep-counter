from PIL import Image
import os
import sys

# Windows cp932対策
sys.stdout.reconfigure(encoding='utf-8')

input_files = [
    "image_7d3023ad.png",
    "image_8949a7a6.png",
    "image_b4b8379f.png",
]

assets_dir = os.path.dirname(os.path.abspath(__file__))

def remove_white_bg(input_path, output_path, threshold=240, feather=15):
    img = Image.open(input_path).convert("RGBA")
    pixels = img.load()
    width, height = img.size

    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            whiteness = min(r, g, b)
            if whiteness >= threshold:
                pixels[x, y] = (r, g, b, 0)
            elif whiteness >= threshold - feather:
                alpha = int(255 * (threshold - whiteness) / feather)
                pixels[x, y] = (r, g, b, alpha)

    img.save(output_path, "PNG")
    print(f"  OK: {os.path.basename(output_path)}")

print("=== Remove white background ===")
for fname in input_files:
    input_path = os.path.join(assets_dir, fname)
    name, ext = os.path.splitext(fname)
    output_path = os.path.join(assets_dir, f"{name}_transparent.png")
    print(f"Processing: {fname}")
    remove_white_bg(input_path, output_path)

print("Done!")
