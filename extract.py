import re
import os
import json
from datetime import datetime

with open('create_pdf.py', 'r', encoding='utf-8') as f:
    content = f.read()

# We can find all the Modul sections
# Modules start with story.append(section_banner("MODUL X..."))
sections = re.split(r'story\.append\(section_banner\("MODUL', content)

out_dir = "src/content/articles/"
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

def clean_html(text):
    text = re.sub(r'<b>(.*?)</b>', r'**\1**', text)
    text = re.sub(r'<i>(.*?)</i>', r'*\1*', text)
    text = text.replace('<br/>', '\n')
    text = text.replace('<br>', '\n')
    return text

for idx, section in enumerate(sections[1:]): # skip the preamble/TOC
    # Modul number and title
    header_match = re.match(r'\s*([^\"]+)"\)\)', section)
    if header_match:
        mod_name = header_match.group(1).split(' — ')[0].strip()
    else:
        mod_name = f"{idx}"

    mod_num = mod_name.split()[-1] if ' ' in mod_name else mod_name
    
    # We will build markdown
    md_content = ""
    
    # Simple state machine to parse story.append(...)
    lines = section.split('\n')
    i = 0
    in_code = False
    code_block = ""
    
    while i < len(lines):
        line = lines[i].strip()
        
        if line.startswith('for ln in code("""'):
            in_code = True
            code_block = line.replace('for ln in code("""', '')
        elif in_code:
            if '"""):' in line or '"""): \n' in line or line.endswith('"""):'):
                code_block += '\n' + line.replace('"""):', '')
                md_content += f"\n```matlab\n{code_block.strip()}\n```\n\n"
                in_code = False
                code_block = ""
                # skip next line which is story.append(ln)
                i += 1
            else:
                code_block += '\n' + line
        elif line.startswith('story.append(h1("'):
            m = re.search(r'story\.append\(h1\("([^"]+)"\)\)', line)
            if m: md_content += f"# {clean_html(m.group(1))}\n\n"
        elif line.startswith('story.append(h2("'):
            m = re.search(r'story\.append\(h2\("([^"]+)"\)\)', line)
            if m: md_content += f"## {clean_html(m.group(1))}\n\n"
        elif line.startswith('story.append(h3("'):
            m = re.search(r'story\.append\(h3\("([^"]+)"\)\)', line)
            if m: md_content += f"### {clean_html(m.group(1))}\n\n"
        elif line.startswith('story.append(body('):
            # Might be multiline
            body_txt = line.replace('story.append(body(', '')
            while not body_txt.rstrip().endswith('))') and i+1 < len(lines):
                i += 1
                body_txt += " " + lines[i].strip()
            # Clean up
            body_txt = body_txt.rstrip(')')
            if body_txt.startswith('"') and body_txt.endswith('"'):
                body_txt = body_txt[1:-1]
            md_content += f"{clean_html(body_txt)}\n\n"
        elif line.startswith('story.append(bullet("'):
            m = re.search(r'story\.append\(bullet\("([^"]+)"\)\)', line)
            if m: md_content += f"- {clean_html(m.group(1))}\n"
        elif line.startswith('story.append(note('):
            body_txt = line.replace('story.append(note(', '')
            while not body_txt.rstrip().endswith('))') and i+1 < len(lines):
                i += 1
                body_txt += " " + lines[i].strip()
            body_txt = body_txt.rstrip(')')
            if body_txt.startswith('"') and body_txt.endswith('"'):
                body_txt = body_txt[1:-1]
            md_content += f"> {clean_html(body_txt)}\n\n"
        
        i += 1

    title = f"Modul {mod_num}: Belajar MATLAB"
    slug = f"modul-{mod_num}-belajar-matlab".lower().replace(' ', '-').replace('&', 'dan')
    
    frontmatter = f"""---
title: "{title}"
description: "Materi Modul {mod_num} untuk pembelajaran MATLAB."
date: 2026-06-09
thumbnail: "https://d1d1c1tnh6i0t6.cloudfront.net/wp-content/uploads/sites/2/2020/05/matlab-logo-227x300.jpg"
author: "Mr Dhuha"
series: "Belajar MATLAB"
topic: "Sains Data"
tags: ["matlab", "tutorial", "sains data"]
readingTime: 5
layout: layouts/article.njk
---

"""
    
    file_path = os.path.join(out_dir, slug, "index.md")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding='utf-8') as f:
        f.write(frontmatter + md_content)
    print(f"Created {file_path}")

print("Done parsing.")
