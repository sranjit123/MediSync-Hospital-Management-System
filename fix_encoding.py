
# Script to fix encoding of home.html
import os

file_path = r"e:\College\Semester\project2\recommendation\templates\recommendation\home.html"

# Content to write
content = """{% extends 'recommendation/base.html' %}

{% block content %}
<div class="card">
    <h2 style="margin-top:0;">Find Your Specialist</h2>
    <p class="text-gray-600 mb-4">Describe your symptoms below, and our AI will recommend the right department and specialists for you.</p>

    <form method="post" action="{% url 'home' %}">
        {% csrf_token %}
        <label for="symptoms">Describe your symptoms (e.g., chest pain, headache, fever):</label>
        <textarea id="symptoms" name="symptoms" rows="4" placeholder="Enter your symptoms here..."></textarea>
        
        <button type="submit" class="btn">Get Recommendation</button>
    </form>
</div>

<div class="info-section" style="margin-top: 2rem; background: #fff; padding: 2rem; border-radius: 0.5rem; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
    <h3>How it works</h3>
    <ol style="margin-left: 1.5rem;">
        <li>Enter your symptoms in the text box.</li>
        <li>Our Content-Based Filtering algorithm analyzes your input.</li>
        <li>We match your symptoms with specialized departments.</li>
        <li>You get a list of recommended doctors and related information.</li>
    </ol>
</div>
{% endblock %}
"""

# Write with utf-8 encoding
try:
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Successfully re-saved {file_path} with UTF-8 encoding.")
except Exception as e:
    print(f"Error saving file: {e}")
