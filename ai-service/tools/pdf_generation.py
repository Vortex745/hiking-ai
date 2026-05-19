from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from langchain_core.tools import tool

WORKSPACE_DIR = Path("./workspace")
WORKSPACE_DIR.mkdir(exist_ok=True)


@tool
async def generate_pdf(title: str, content: str) -> str:
    """Generate a PDF document from text content.

    Args:
        title: The title of the PDF document
        content: The main text content of the document
    """
    safe_filename = "".join(c if c.isalnum() or c in " _-" else "_" for c in title)[:50]
    filepath = WORKSPACE_DIR / f"{safe_filename}.pdf"

    try:
        doc = SimpleDocTemplate(
            str(filepath),
            pagesize=A4,
            title=title,
        )

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "CustomTitle",
            parent=styles["Title"],
            fontSize=18,
            spaceAfter=20,
        )
        body_style = ParagraphStyle(
            "CustomBody",
            parent=styles["Normal"],
            fontSize=11,
            leading=16,
            spaceAfter=10,
        )

        elements = []
        elements.append(Paragraph(title, title_style))
        elements.append(Spacer(1, 12))

        for paragraph in content.split("\n"):
            paragraph = paragraph.strip()
            if paragraph:
                elements.append(Paragraph(paragraph, body_style))

        doc.build(elements)
        return f"PDF 已生成: {filepath}（{filepath.stat().st_size} bytes）"
    except Exception as e:
        return f"PDF 生成失败: {str(e)}"
