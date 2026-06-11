import markdown
from xhtml2pdf import pisa
from io import BytesIO

def generate_pdf_from_md(md_string: str) -> bytes:
    """Uses xhtml2pdf to render markdown files into raw PDF byte traces."""
    html_body = markdown.markdown(md_string, extensions=["tables"])
    html_content = f"""
    <html>
    <head>
    <style>
        body {{ font-family: Helvetica, Arial, sans-serif; font-size: 11px; color: #333; }}
        h1 {{ color: #2c3e50; font-size: 16px; margin-bottom: 5px; }}
        h2 {{ color: #34495e; font-size: 14px; border-bottom: 1px solid #ddd; padding-bottom: 3px; margin-top: 15px; }}
        h3 {{ color: #555; font-size: 12px; margin-top: 10px; }}
        p {{ margin-bottom: 10px; line-height: 1.4; }}
        ul {{ margin-bottom: 10px; }}
        li {{ margin-bottom: 4px; }}
    </style>
    </head>
    <body>
    {html_body}
    </body>
    </html>
    """
    
    result = BytesIO()
    pisa_status = pisa.CreatePDF(html_content, dest=result)
    
    if pisa_status.err:
        raise Exception("Failed to compile PDF from Markdown via xhtml2pdf")
        
    return result.getvalue()
