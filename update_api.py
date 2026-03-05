import os
import glob

frontend_dir = r"c:\Users\lakshmi\OneDrive\Desktop\kerala assistant\frontend"
files = glob.glob(os.path.join(frontend_dir, "*.html"))

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the Render API with relative API base since we are migrating the backend to Vercel
    new_content = content.replace('https://agrisathi-ai-farming-assistant.onrender.com', '')
    if new_content != content:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {os.path.basename(file)}")
