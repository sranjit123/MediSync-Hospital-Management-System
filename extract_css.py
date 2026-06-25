import os
import re
import hashlib

base_dir = r"e:\College\Semester\project2\recommendation\templates\recommendation"
css_dir = r"e:\College\Semester\project2\recommendation\static\recommendation\styles"
categories = ['admin', 'doctor', 'patient', 'public', 'shared']

def extract_styles(filepath, cat):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    css_rules = []
    
    # 1. Extract internal <style> blocks
    style_blocks = re.findall(r'<style[^>]*>(.*?)</style>', content, re.DOTALL)
    for block in style_blocks:
        css_rules.append(block.strip())
    content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL)
    
    # 2. Extract inline styles
    # We will use a regex to match an entire opening HTML tag: <tag ... >
    def tag_replacer(match):
        tag_content = match.group(0)
        # Check if this tag has a style attribute
        style_match = re.search(r'style="([^"]+)"', tag_content)
        if not style_match:
            return tag_content
            
        style_str = style_match.group(1).strip()
        if not style_str:
            return tag_content.replace('style=""', '')
            
        h = hashlib.md5(style_str.encode('utf-8')).hexdigest()[:6]
        cls_name = f"c-{h}"
        css_rules.append(f".{cls_name} {{ {style_str} }}")
        
        # Remove style attribute
        tag_content = tag_content.replace(style_match.group(0), '')
        
        # Add to class attribute
        class_match = re.search(r'class="([^"]*)"', tag_content)
        if class_match:
            old_class = class_match.group(1)
            new_class = f'{old_class} {cls_name}'.strip()
            tag_content = tag_content.replace(class_match.group(0), f'class="{new_class}"')
        else:
            # Tag doesn't have class attribute, add it before the closing angle bracket
            if tag_content.endswith('/>'):
                tag_content = tag_content[:-2] + f' class="{cls_name}"/>'
            else:
                tag_content = tag_content[:-1] + f' class="{cls_name}">'
                
        return tag_content

    # Regex to match Opening HTML tags (excluding Django template tags which start with {)
    content = re.sub(r'<[a-zA-Z0-9]+(?:\s+[^>]*?)?(?<!\?)>', tag_replacer, content)
    
    # 3. Inject CSS Link
    # Prepend {% load static %} if not present.
    # Add link to head, or at the top if no head.
    if '{% load static %}' not in content:
        # If it extends, put load static right after extends
        if '{% extends' in content:
            content = re.sub(r'({% extends [^}]+ %})', r'\1\n{% load static %}', content, 1)
        else:
            content = '{% load static %}\n' + content
            
    # Add the link tag
    link_tag = f'\n<!-- CSS linking -->\n<link rel="stylesheet" href="{{% static \'recommendation/styles/{cat}.css\' %}}">\n'
    
    # If the file has a head block, or a head tag, inject it there. 
    # Or if the file doesn't have a head tag but extends base, just injecting it at top won't work 
    # because it will render before the body or inside block content.
    # ACTUALLY, Django blocks: if we extend base.html, we must put the link inside a block (e.g. block content).
    # Since base.html has no block extra_head, we can put the link inside {% block content %}.
    if '{% block content %}' in content:
        content = content.replace('{% block content %}', f'{{% block content %}}{link_tag}')
    elif '<head>' in content:
        content = content.replace('</head>', f'{link_tag}</head>')
    else:
        # Just append it at the top after load static
        content = content.replace('{% load static %}', f'{{% load static %}}{link_tag}')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    return css_rules

for cat in categories:
    cat_dir = os.path.join(base_dir, cat)
    if not os.path.exists(cat_dir):
        continue
    
    all_css = []
    for filename in os.listdir(cat_dir):
        if not filename.endswith('.html'):
            continue
        filepath = os.path.join(cat_dir, filename)
        rules = extract_styles(filepath, cat)
        all_css.extend(rules)
        
    if all_css:
        css_file = os.path.join(css_dir, f"{cat}.css")
        with open(css_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(set(all_css))) # set() removes duplicates
            
print("CSS Extraction Complete!")
