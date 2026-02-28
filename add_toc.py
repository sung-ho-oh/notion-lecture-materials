import os
import re

def create_toc(content):
    lines = content.split('\n')
    toc_lines = []
    
    # Simple regex to find headers (# Header, ## Header, etc.)
    header_pattern = re.compile(r'^(#{1,6})\s+(.*)')
    
    for line in lines:
        match = header_pattern.match(line)
        if match:
            level = len(match.group(1))
            title = match.group(2).strip()
            # Convert title to a valid github-style anchor link
            # Remove punctuation, convert to lowercase, replace spaces with hyphens
            anchor = title.lower()
            anchor = re.sub(r'[^\w\s-]', '', anchor)
            anchor = re.sub(r'[\s]+', '-', anchor)
            
            indent = "  " * (level - 1)
            toc_lines.append(f"{indent}- [{title}](#{anchor})")
            
    if not toc_lines:
        return ""
        
    return "## 목차 (Table of Contents)\n\n" + "\n".join(toc_lines) + "\n\n---\n\n"

def process_markdown_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Check if TOC already exists to avoid duplication
    if "## 목차 (Table of Contents)" in content:
        print(f"Skipping {os.path.basename(filepath)} - TOC already exists.")
        return
        
    toc = create_toc(content)
    
    if toc:
        # We'll try to put the TOC after the main H1 title if it exists, otherwise at the very top
        lines = content.split('\n')
        insert_idx = 0
        if lines and lines[0].startswith('# '):
             insert_idx = 1
             # skip empty lines after H1
             while insert_idx < len(lines) and lines[insert_idx].strip() == '':
                 insert_idx += 1
                 
        new_content = '\n'.join(lines[:insert_idx]) + '\n\n' + toc + '\n'.join(lines[insert_idx:])
        
        with open(filepath, 'w', encoding='utf-8') as f:
             f.write(new_content)
        print(f"Added TOC to {os.path.basename(filepath)}")
    else:
        print(f"No headers found in {os.path.basename(filepath)}")

def main():
    target_dir = r"c:\Users\USER\.gemini\antigravity\lecture-materials\export\part1"
    
    for filename in os.listdir(target_dir):
        if filename.endswith(".md"):
            filepath = os.path.join(target_dir, filename)
            process_markdown_file(filepath)

if __name__ == "__main__":
    main()
