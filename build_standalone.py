"""Build a single self-contained index.html:
   - inline css/styles.css
   - inline js/script.js
   - embed img/*.png as base64 data URIs
   Result works with no sibling files, anywhere it is opened.
"""
from __future__ import annotations

import base64
from pathlib import Path

HERE = Path(__file__).resolve().parent
css = (HERE / "css" / "styles.css").read_text(encoding="utf-8")
js = (HERE / "js" / "script.js").read_text(encoding="utf-8")
html = (HERE / "index.html").read_text(encoding="utf-8")

# 1) replace the stylesheet link with an inline <style>
html = html.replace('<link rel="stylesheet" href="css/styles.css">',
                    f"<style>\n{css}\n</style>")

# 2) replace the script tag with inline <script>
html = html.replace('<script src="js/script.js"></script>',
                    f"<script>\n{js}\n</script>")

# 3) embed every img/*.png as a base64 data URI
import re
def embed(m):
    name = m.group(1)
    p = HERE / "img" / name
    b64 = base64.b64encode(p.read_bytes()).decode("ascii")
    return f'src="data:image/png;base64,{b64}"'

html = re.sub(r'src="img/([a-z0-9_-]+\.png)"', embed, html)

# 4) embed the CV pdf as a base64 data URI so the download link works offline
def embed_pdf(m):
    b64 = base64.b64encode((HERE / "Vedant_Konde_Resume_MIM.pdf").read_bytes()).decode("ascii")
    return f'href="data:application/pdf;base64,{b64}"'

html = re.sub(r'href="Vedant_Konde_Resume_MIM\.pdf"', embed_pdf, html)

out = HERE / "index.standalone.html"
out.write_text(html, encoding="utf-8")
print(f"wrote {out.name}  ({out.stat().st_size/1024:.0f} KB, self-contained)")
