from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from xml.sax.saxutils import escape

ROOT = Path(__file__).parent / "sample_docs"
for md_path in ROOT.glob("*.md"):
    output = md_path.with_suffix(".pdf")
    doc = SimpleDocTemplate(str(output), pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    for line in md_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            story.append(Spacer(1, 8))
        elif line.startswith("# "):
            story.append(Paragraph(escape(line[2:]), styles["Title"]))
        elif line.startswith("## "):
            story.append(Paragraph(escape(line[3:]), styles["Heading2"]))
        else:
            story.append(Paragraph(escape(line), styles["BodyText"]))
            story.append(Spacer(1, 4))
    doc.build(story)
    print(f"Created {output}")
