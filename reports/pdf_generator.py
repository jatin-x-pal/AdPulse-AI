import re
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.colors import HexColor

def generate_pdf_from_md(md_string: str) -> bytes:
    """Generates PDF directly using reportlab.platypus to ensure Streamlit Cloud native compliance."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            rightMargin=40, leftMargin=40,
                            topMargin=40, bottomMargin=40)
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'MainTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=HexColor('#2c3e50'),
        spaceAfter=15
    )
    
    h2_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=HexColor('#34495e'),
        spaceBefore=15,
        spaceAfter=10
    )
    
    body_style = ParagraphStyle(
        'NormalBody',
        parent=styles['Normal'],
        fontSize=10,
        textColor=HexColor('#333333'),
        spaceAfter=6,
        leading=14
    )
    
    story = []
    
    def process_text(text):
        # Translate MD styles into reportlab supported XML tags
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        text = re.sub(r'_(.*?)_', r'<i>\1</i>', text)
        return text
    
    lines = md_string.split('\n')
    
    for line in lines:
        line = line.strip()
        if line.startswith('---') or line == '':
            if line == '':
                story.append(Spacer(1, 6))
            continue
            
        if line.startswith('# '):
            text = process_text(line[2:])
            story.append(Paragraph(text, title_style))
        elif line.startswith('## '):
            text = process_text(line[3:])
            story.append(Paragraph(text, h2_style))
        elif line.startswith('### '):
            text = process_text(line[4:])
            story.append(Paragraph(text, styles['Heading3']))
        elif line.startswith('- ') or line.startswith('* '):
            text = process_text(line[2:])
            story.append(Paragraph(f"&bull; {text}", body_style))
        else:
            text = process_text(line)
            story.append(Paragraph(text, body_style))
            
    doc.build(story)
    return buffer.getvalue()
