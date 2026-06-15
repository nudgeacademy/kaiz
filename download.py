import os
import re
import urllib.request
import hashlib

folder = "/Users/asifali/Desktop/KAIZ KITCHEN"
images_dir = os.path.join(folder, "IMAGES")
os.makedirs(images_dir, exist_ok=True)

html_files = [f for f in os.listdir(folder) if f.endswith('.html')]

# Download Tailwind
tailwind_url = "https://cdn.tailwindcss.com?plugins=forms,container-queries"
tailwind_path = os.path.join(folder, "tailwind.js")
print("Downloading Tailwind...")
try:
    req = urllib.request.Request(tailwind_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response, open(tailwind_path, 'wb') as out_file:
        out_file.write(response.read())
except Exception as e:
    print(f"Failed to download tailwind: {e}")

for file in html_files:
    filepath = os.path.join(folder, file)
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Replace tailwind
    content = content.replace('https://cdn.tailwindcss.com?plugins=forms,container-queries', 'tailwind.js')
    
    # Find all googleusercontent images
    urls = re.findall(r'https://lh3\.googleusercontent\.com/[^\s"\'<>]+', content)
    # Deduplicate
    urls = list(set(urls))
    
    for url in urls:
        # Create a unique filename based on hash
        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
        ext = ".jpg" # Assume jpg
        filename = f"img_{url_hash}{ext}"
        local_path = os.path.join(images_dir, filename)
        
        if not os.path.exists(local_path):
            try:
                print(f"Downloading {url} to {filename}")
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req) as response, open(local_path, 'wb') as out_file:
                    out_file.write(response.read())
            except Exception as e:
                print(f"Failed to download {url}: {e}")
        
        content = content.replace(url, f"IMAGES/{filename}")
        
    with open(filepath, 'w') as f:
        f.write(content)

print("Done downloading images and Tailwind.")
