import os

base_dir = r"e:\College\Semester\project2\recommendation\templates\recommendation"
for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.html'):
            filepath = os.path.join(root, f)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            
            content = content.replace("{% extends 'recommendation/base.html' %}", "{% extends 'recommendation/shared/base.html' %}")
            content = content.replace('{% extends "recommendation/base.html" %}', '{% extends "recommendation/shared/base.html" %}')
            
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(content)
print("Extends fixed.")
