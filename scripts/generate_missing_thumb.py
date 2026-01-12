from PIL import Image
import os

def generate_thumb():
    source_path = "assets/images/raw/artist_broboticus_avatar.png"
    target_path = "assets/images/gallery-thumbs/brobot-001.jpg"
    
    if not os.path.exists(source_path):
        print(f"Error: Source {source_path} not found")
        return

    try:
        with Image.open(source_path) as img:
            # Convert to RGB (remove alpha) for JPG
            rgb_img = img.convert('RGB')
            
            # Resize logic (simple scale to width 600)
            base_width = 600
            w_percent = (base_width / float(rgb_img.size[0]))
            h_size = int((float(rgb_img.size[1]) * float(w_percent)))
            
            img_resized = rgb_img.resize((base_width, h_size), Image.Resampling.LANCZOS)
            
            img_resized.save(target_path, "JPEG", quality=85)
            print(f"Success: Created {target_path}")
            
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    generate_thumb()
