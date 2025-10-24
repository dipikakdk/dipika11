import os
import shutil
import requests

# Base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create necessary directories
os.makedirs(os.path.join(BASE_DIR, 'static', 'images'), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'static', 'css'), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'static', 'js'), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'media', 'profile_pic'), exist_ok=True)

# List of required images and their default URLs (if needed)
required_images = {
    'admin.png': 'https://cdn-icons-png.flaticon.com/512/2206/2206368.png',
    'doctor.png': 'https://cdn-icons-png.flaticon.com/512/2965/2965879.png',
    'patient.jpg': 'https://cdn-icons-png.flaticon.com/512/1946/1946429.png',
    'back.jpg': 'https://images.unsplash.com/photo-1505751172876-fa1f5fbc42f8?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80'
}

def download_file(url, filepath):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

# Check and download missing images
for image, url in required_images.items():
    image_path = os.path.join(BASE_DIR, 'static', 'images', image)
    if not os.path.exists(image_path):
        print(f"Downloading {image}...")
        if download_file(url, image_path):
            print(f"Successfully downloaded {image}")
        else:
            print(f"Using placeholder for {image}")
            # Create a simple placeholder if download fails
            with open(image_path, 'wb') as f:
                f.write(b'Placeholder image')
    else:
        print(f"{image} already exists")

print("\nStatic files check complete!")
