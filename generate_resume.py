"""
Generate a modern two-column resume PDF matching the original layout:
  - Left sidebar: Contact, Skills, Education, Languages
  - Right main: Summary, Experience, Projects, Achievements
Clean fonts, larger text for readability, and elegant color palette.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

OUTPUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "My Resume.pdf")

# ─── Page dimensions ───
W, H = A4  # 595.28 x 841.89 points
SIDEBAR_W = 205
MAIN_X = SIDEBAR_W + 25
MAIN_W = W - MAIN_X - 25

# ─── Colors ───
# Elegant Dark Charcoal & Blue theme
SIDEBAR_BG = HexColor("#232F3E")       # AWS-like dark slate
SIDEBAR_TEXT = HexColor("#D5D8DC")     # Light gray for readability
SIDEBAR_HEADING = HexColor("#FFFFFF")  # Pure white for headings
SIDEBAR_ACCENT = HexColor("#3498DB")   # Professional soft blue
SIDEBAR_DIM = HexColor("#ABB2B9")      # Dimmed text

MAIN_BG = HexColor("#FAF9F6")          # Elegant mud-white / cream
MAIN_HEADING = HexColor("#1E272E")     # Darker slate for sharper contrast
MAIN_TEXT = HexColor("#111111")        # Deep near-black for maximum readability
MAIN_ACCENT = HexColor("#2980B9")      # Matching blue for main accents
MAIN_DIM = HexColor("#555555")         # Darker gray for dates/meta
RULE_COLOR = HexColor("#E0E0E0")       # Slightly darker rule line for off-white bg
ACCENT_DOT = HexColor("#3498DB")


def draw_wrapped(c, text, x, y, max_width, font_name, font_size, color, leading=None):
    """Draw text with word wrapping. Returns the new y position."""
    if leading is None:
        leading = font_size * 1.4
    c.setFont(font_name, font_size)
    c.setFillColor(color)
    
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        test = current_line + (" " if current_line else "") + word
        if pdfmetrics.stringWidth(test, font_name, font_size) <= max_width:
            current_line = test
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    
    return y


def draw_bullet(c, text, x, y, max_width, font_name, font_size, color, leading=None):
    """Draw a bullet point with wrapped text."""
    if leading is None:
        leading = font_size * 1.4
    
    bullet_indent = 10
    text_x = x + bullet_indent + 6
    text_width = max_width - bullet_indent - 6
    
    # Draw bullet dot
    c.setFillColor(ACCENT_DOT)
    c.circle(x + 5, y - 3, 2.5, fill=1, stroke=0)
    
    # Draw wrapped text
    c.setFont(font_name, font_size)
    c.setFillColor(color)
    
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        test = current_line + (" " if current_line else "") + word
        if pdfmetrics.stringWidth(test, font_name, font_size) <= text_width:
            current_line = test
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    
    for i, line in enumerate(lines):
        c.drawString(text_x, y, line)
        y -= leading
    
    return y


def draw_sidebar_section(c, title, y):
    """Draw a sidebar section header with accent underline."""
    c.setFont("Modern-Bold", 12)
    c.setFillColor(SIDEBAR_HEADING)
    c.drawString(22, y, title.upper())
    y -= 6
    c.setStrokeColor(SIDEBAR_ACCENT)
    c.setLineWidth(2)
    c.line(22, y, 22 + pdfmetrics.stringWidth(title.upper(), "Modern-Bold", 12), y)
    return y - 16


def draw_main_section(c, title, y):
    """Draw a main section header with a rule line and a modern accent line."""
    c.setStrokeColor(RULE_COLOR)
    c.setLineWidth(1.5)
    c.line(MAIN_X, y + 8, W - 25, y + 8)
    
    c.setFont("Modern-Bold", 13.5)
    c.setFillColor(MAIN_HEADING)
    c.drawString(MAIN_X, y - 6, title.upper())
    
    # Modern short accent line under the title
    c.setStrokeColor(MAIN_ACCENT)
    c.setLineWidth(2.5)
    c.line(MAIN_X, y - 12, MAIN_X + 25, y - 12)
    
    return y - 32


def draw_skill_tag(c, text, x, y, bg_color=None):
    """Draw a skill tag pill. Returns (new_x, new_y) after the tag."""
    font_name = "Modern"
    font_size = 9.5
    pad_x = 9
    pad_y = 5
    gap_x = 8
    gap_y = 8
    
    tw = pdfmetrics.stringWidth(text, font_name, font_size)
    tag_w = tw + pad_x * 2
    tag_h = font_size + pad_y * 2 + 1
    
    # Check if tag overflows sidebar
    if x + tag_w > SIDEBAR_W - 22:
        x = 22
        y -= tag_h + gap_y
    
    # Draw drop shadow for depth
    c.setFillColor(HexColor("#17202A")) # Darker color for shadow
    c.roundRect(x + 1.5, y - tag_h + pad_y + 3 - 1.5, tag_w, tag_h, 5, fill=1, stroke=0)
    
    # Draw rounded rect background
    c.setFillColor(HexColor("#34495E")) # Slightly lighter than sidebar bg
    c.roundRect(x, y - tag_h + pad_y + 3, tag_w, tag_h, 5, fill=1, stroke=0)
    
    # Draw text
    c.setFont(font_name, font_size)
    c.setFillColor(SIDEBAR_TEXT)
    c.drawString(x + pad_x, y - font_size + 4, text)
    
    return x + tag_w + gap_x, y


def build_resume():
    # Register modern fonts (fallback to Helvetica if SegoeUI is missing)
    try:
        pdfmetrics.registerFont(TTFont('Modern', 'C:\\Windows\\Fonts\\segoeui.ttf'))
        pdfmetrics.registerFont(TTFont('Modern-Bold', 'C:\\Windows\\Fonts\\segoeuib.ttf'))
    except:
        pdfmetrics.registerFont(TTFont('Modern', 'Helvetica'))
        pdfmetrics.registerFont(TTFont('Modern-Bold', 'Helvetica-Bold'))

    c = canvas.Canvas(OUTPUT_PATH, pagesize=A4)
    c.setTitle("Sarvesh Salam - GenAI & Python Developer")
    c.setAuthor("Sarvesh Salam")
    c.setSubject("Resume")
    
    # ─── Background ───
    c.setFillColor(SIDEBAR_BG)
    c.rect(0, 0, SIDEBAR_W, H, fill=1, stroke=0)
    c.setFillColor(MAIN_BG)
    c.rect(SIDEBAR_W, 0, W - SIDEBAR_W, H, fill=1, stroke=0)
    
    # Modern Vertical Partition with Depth/Shadow
    # We draw a series of light lines to simulate a drop shadow falling on the white page
    shadow_colors = ["#E5E8E8", "#EBEDEF", "#F2F3F4", "#F8F9F9"]
    for i, color in enumerate(shadow_colors):
        c.setStrokeColor(HexColor(color))
        c.setLineWidth(1)
        c.line(SIDEBAR_W + 1 + i, 0, SIDEBAR_W + 1 + i, H)
        
    c.setStrokeColor(MAIN_ACCENT)
    c.setLineWidth(1.5)
    c.line(SIDEBAR_W, 0, SIDEBAR_W, H)
    
    # ════════════════════════════════════════════
    # SIDEBAR
    # ════════════════════════════════════════════
    sy = H - 45
    
    # Name
    c.setFont("Modern-Bold", 22)
    c.setFillColor(SIDEBAR_HEADING)
    c.drawString(22, sy, "Sarvesh Salam")
    sy -= 20
    
    # Title
    c.setFont("Modern", 11)
    c.setFillColor(SIDEBAR_ACCENT)
    # Split across two lines to avoid horizontal overlap, but keep identical styling
    c.drawString(22, sy, "GenAI & Python Developer")
    sy -= 14
    c.drawString(22, sy, "AI/ML Engineer")
    sy -= 30
    
    # ─── Contact ───
    sy = draw_sidebar_section(c, "Contact", sy)
    
    contact_items = [
        ("salam.sarvesh@gmail.com",),
        ("+91 9373151669",),
        ("Mumbai, India",),
        ("sarvesh-salam.vercel.app",),
        ("linkedin.com/in/sarvesh-salam",),
        ("github.com/sarvesh0809",),
    ]
    
    c.setFont("Modern", 9.5)
    c.setFillColor(SIDEBAR_TEXT)
    for item in contact_items:
        c.drawString(22, sy, item[0])
        sy -= 16
    
    sy -= 20
    
    # ─── Skills ───
    sy = draw_sidebar_section(c, "Skills", sy)
    
    skills = [
        "Python", "GenAI", "LLMs", "FastAPI",
        "Django", "AWS", "GCP", "Docker",
        "Kubernetes", "DynamoDB", "Neptune",
        "Gremlin", "Azure OCR", "OpenAI APIs",
        "Git", "CI/CD", "SQL", "MongoDB",
        "Selenium", "Pytest",
    ]
    
    tag_x = 22
    tag_y = sy
    for skill in skills:
        tag_x, tag_y = draw_skill_tag(c, skill, tag_x, tag_y)
    
    sy = tag_y - 35  # Increased spacing between Skills and Education
    
    # ─── Education ───
    sy = draw_sidebar_section(c, "Education", sy)
    
    c.setFont("Modern-Bold", 9.5)
    c.setFillColor(SIDEBAR_HEADING)
    c.drawString(22, sy, "B.Tech in Computer Science")
    sy -= 14
    
    c.setFont("Modern", 9.5)
    c.setFillColor(SIDEBAR_TEXT)
    c.drawString(22, sy, "University of Mumbai")
    sy -= 14
    c.setFont("Modern", 8.5)
    c.setFillColor(SIDEBAR_DIM)
    c.drawString(22, sy, "Jul 2017 - Jun 2021  |  CGPA: 7.1")
    sy -= 35  # Increased spacing before next section
    
    # ─── Achievement ───
    sy = draw_sidebar_section(c, "Achievement", sy)
    
    c.setFont("Modern-Bold", 9.5)
    c.setFillColor(SIDEBAR_HEADING)
    c.drawString(22, sy, "ACE Award")
    sy -= 14
    c.setFont("Modern", 9)
    c.setFillColor(SIDEBAR_TEXT)
    sy = draw_wrapped(c, "Recognized by Accenture for delivering innovative solutions with Karseva PWA.",
                       22, sy, SIDEBAR_W - 44, "Modern", 9, SIDEBAR_TEXT, leading=13)
    sy -= 25  # Increased spacing before next section
    
    # ─── Languages ───
    sy = draw_sidebar_section(c, "Languages", sy)
    
    languages = [
        ("English", "Full Professional Proficiency"),
        ("Hindi", "Native or Bilingual Proficiency"),
        ("Marathi", "Native or Bilingual Proficiency"),
    ]
    for lang, level in languages:
        c.setFont("Modern-Bold", 9.5)
        c.setFillColor(SIDEBAR_HEADING)
        c.drawString(22, sy, lang)
        sy -= 12
        c.setFont("Modern", 8.5)
        c.setFillColor(SIDEBAR_DIM)
        c.drawString(22, sy, level)
        sy -= 16
    
    # ════════════════════════════════════════════
    # MAIN CONTENT
    # ════════════════════════════════════════════
    my = H - 45
    
    # ─── Professional Summary ───
    c.setFont("Modern-Bold", 13.5)
    c.setFillColor(MAIN_HEADING)
    c.drawString(MAIN_X, my, "PROFESSIONAL SUMMARY")
    c.setStrokeColor(MAIN_ACCENT)
    c.setLineWidth(2.5)
    c.line(MAIN_X, my - 6, MAIN_X + 25, my - 6)
    my -= 28  # Increased spacing
    
    summary = (
        "Results-driven AI/ML & Python Developer with 5 years of experience building scalable cloud "
        "applications, automating complex data workflows, and delivering ML-powered solutions. Core "
        "expertise in designing end-to-end Generative AI architectures, advanced OCR pipelines, and "
        "containerized microservices (AWS EKS, FastAPI). Proven track record of leveraging multi-model "
        "LLM orchestration (Claude, GPT, Azure) to drive high-impact business value, backed by strong "
        "foundations in robust CI/CD practices (Tekton, ArgoCD) and system optimization."
    )
    my = draw_wrapped(c, summary, MAIN_X, my, MAIN_W, "Modern", 9.5, MAIN_TEXT, leading=14)
    my -= 15
    
    # ─── Work Experience ───
    my = draw_main_section(c, "Work Experience", my)
    
    # Accenture
    c.setFont("Modern-Bold", 11.5)
    c.setFillColor(MAIN_HEADING)
    c.drawString(MAIN_X, my, "AI/ML Engineer | Python Developer")
    my -= 18  # Increased spacing between job title and company
    
    c.setFont("Modern-Bold", 9.5)
    c.setFillColor(MAIN_ACCENT)
    c.drawString(MAIN_X, my, "Accenture Solutions Pvt Ltd.")
    
    c.setFont("Modern", 9.5)
    c.setFillColor(MAIN_DIM)
    date_text = "Feb 2022 - Present"
    date_w = pdfmetrics.stringWidth(date_text, "Modern", 9.5)
    c.drawString(W - 25 - date_w, my, date_text)
    my -= 16
    
    accenture_bullets = [
        "Architecting an end-to-end Generative AI and OCR pipeline for a leading global healthcare client, automating bulk extraction of complex claims documents.",
        "Integrated Claude, GPT, and Azure Document Intelligence with sophisticated LLM orchestration to achieve 68% data extraction accuracy on unstructured data.",
        "Deployed containerized Python microservices on Amazon EKS with automated CI/CD pipelines using Tekton and ArgoCD.",
        "Designed scalable APIs using FastAPI and AWS Lambda, integrating DynamoDB for high-throughput, low-latency distributed workloads.",
        "Engineered a bulk loader with AWS Lambda for massive dataset ingestion into Amazon Neptune, optimizing graph-based data modeling.",
        "Created advanced Gremlin queries reducing data retrieval times by 30%, enabling faster analytical workflows.",
        "Migrated to AWS Secrets Manager for secure credential retrieval, enhancing compliance and system security.",
    ]
    
    for b_text in accenture_bullets:
        my = draw_bullet(c, b_text, MAIN_X, my, MAIN_W, "Modern", 9.2, MAIN_TEXT, leading=13.5)
        my -= 4
    
    my -= 8

    
    # Forms9
    c.setFont("Modern-Bold", 11.5)
    c.setFillColor(MAIN_HEADING)
    c.drawString(MAIN_X, my, "Software / Web Developer")
    my -= 14
    
    c.setFont("Modern-Bold", 9.5)
    c.setFillColor(MAIN_ACCENT)
    c.drawString(MAIN_X, my, "Forms9")
    
    c.setFont("Modern", 9.5)
    c.setFillColor(MAIN_DIM)
    date_text = "Jul 2021 - Jan 2022"
    date_w = pdfmetrics.stringWidth(date_text, "Modern", 9.5)
    c.drawString(W - 25 - date_w, my, date_text)
    my -= 16
    
    forms9_bullets = [
        "Built an end-to-end Inventory Management System using Django, automating operator workflows and reducing manual tracking errors by 40%.",
        "Implemented automated web scraping solutions using Python (BeautifulSoup, Selenium) to extract real-time data from external platforms (e.g., NSE), integrating into Excel reports.",
        "Deployed on Linux server using Nginx & Gunicorn with strict security measures including IP restrictions and VPN-only access.",
    ]
    
    for b_text in forms9_bullets:
        my = draw_bullet(c, b_text, MAIN_X, my, MAIN_W, "Modern", 9.2, MAIN_TEXT, leading=13.5)
        my -= 4
    
    my -= 8
    
    # ─── Projects ───
    my = draw_main_section(c, "Projects", my)
    
    projects = [
        ("Karseva (Progressive Web App)", "Developed a PWA using Python, Django, and AWS to foster intergenerational connections, enhancing elderly care. Awarded the ACE Award by Accenture."),
        ("Inventory Management System", "Built a comprehensive inventory platform using Django that streamlined stock control and improved data accuracy by 40%."),
        ("Bill Management System", "Designed a secure billing platform with Django, focusing on transaction efficiency, rapid query times, and Razor Pay integration."),
    ]
    
    for title, desc in projects:
        c.setFont("Modern-Bold", 10)
        c.setFillColor(MAIN_HEADING)
        c.drawString(MAIN_X, my, title)
        my -= 13
        my = draw_wrapped(c, desc, MAIN_X, my, MAIN_W, "Modern", 9.2, MAIN_TEXT, leading=13)
        my -= 8
    
    # ─── Save ───
    c.save()
    print(f"[OK] Resume generated: {OUTPUT_PATH}")
    print(f"     Size: {os.path.getsize(OUTPUT_PATH):,} bytes")


if __name__ == "__main__":
    build_resume()
