
import os
from PIL import Image
import argparse

VALID_EXT = (".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff")

def resize_images(input_folder, output_folder, width, height, keep_aspect=True, out_format=None):
    size = (int(width), int(height))
    os.makedirs(output_folder, exist_ok=True)

    for fn in os.listdir(input_folder):
        if not fn.lower().endswith(VALID_EXT):
            continue
        in_path = os.path.join(input_folder, fn)
        base, _ = os.path.splitext(fn)

        with Image.open(in_path) as img:
            original_format = img.format or "PNG"
            img_copy = img.copy()

            if keep_aspect:
                img_copy.thumbnail(size)   
            else:
                img_copy = img_copy.resize(size)

            save_format = (out_format or original_format).upper()
            if save_format == "JPEG":
                if img_copy.mode in ("RGBA", "LA"):
                    background = Image.new("RGB", img_copy.size, (255, 255, 255))
                    background.paste(img_copy, mask=img_copy.split()[-1])
                    to_save = background
                else:
                    to_save = img_copy.convert("RGB")
            else:
                to_save = img_copy

            out_name = f"{base}.{save_format.lower()}"
            out_path = os.path.join(output_folder, out_name)
            to_save.save(out_path, save_format)
            print("Saved:", out_path)

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Batch resize images")
    p.add_argument("input_folder")
    p.add_argument("output_folder")
    p.add_argument("width", type=int)
    p.add_argument("height", type=int)
    p.add_argument("--no-aspect", action="store_true", help="Disable aspect-ratio preserving resize")
    p.add_argument("--format", help="Output format like PNG or JPEG")
    args = p.parse_args()

    resize_images(args.input_folder, args.output_folder, args.width, args.height,
                  keep_aspect=not args.no_aspect, out_format=args.format)
