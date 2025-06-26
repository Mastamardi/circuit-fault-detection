import os
import requests
from pathlib import Path

# Create the images directory if it doesn't exist
images_dir = Path('static/images/components')
images_dir.mkdir(parents=True, exist_ok=True)

# Dictionary of component images and their URLs
component_images = {
    'carbon-resistor.jpg': 'https://raw.githubusercontent.com/omkarmastamardi/circuit-components/main/images/carbon-resistor.jpg',
    'metal-film-resistor.jpg': 'https://raw.githubusercontent.com/omkarmastamardi/circuit-components/main/images/metal-film-resistor.jpg',
    'wire-wound-resistor.jpg': 'https://raw.githubusercontent.com/omkarmastamardi/circuit-components/main/images/wire-wound-resistor.jpg',
    'potentiometer.jpg': 'https://raw.githubusercontent.com/omkarmastamardi/circuit-components/main/images/potentiometer.jpg',
    'rheostat.jpg': 'https://raw.githubusercontent.com/omkarmastamardi/circuit-components/main/images/rheostat.jpg',
    'electrolytic-capacitor.jpg': 'https://raw.githubusercontent.com/omkarmastamardi/circuit-components/main/images/electrolytic-capacitor.jpg',
    'ceramic-capacitor.jpg': 'https://raw.githubusercontent.com/omkarmastamardi/circuit-components/main/images/ceramic-capacitor.jpg',
    'ic555.jpg': 'https://raw.githubusercontent.com/omkarmastamardi/circuit-components/main/images/ic555.jpg',
    'opamp.jpg': 'https://raw.githubusercontent.com/omkarmastamardi/circuit-components/main/images/opamp.jpg',
    'buck-converter.jpg': 'https://raw.githubusercontent.com/omkarmastamardi/circuit-components/main/images/buck-converter.jpg',
    'boost-converter.jpg': 'https://raw.githubusercontent.com/omkarmastamardi/circuit-components/main/images/boost-converter.jpg'
}

def download_image(url, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        filepath = images_dir / filename
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"Successfully downloaded {filename}")
    except Exception as e:
        print(f"Error downloading {filename}: {str(e)}")

def main():
    print("Starting image downloads...")
    for filename, url in component_images.items():
        download_image(url, filename)
    print("All downloads completed!")

if __name__ == "__main__":
    main() 