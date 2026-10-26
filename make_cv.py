"""Generate Vedant_Konde_Resume_MIM.pdf — professional single-page CV,
matching the updated resume content. Fonts: Helvetica (PDF base14, embedded)."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle

INK = HexColor("#1d1d1f")
ACCENT = HexColor("#a3132e")
MUTED = HexColor("#55555c")
HAIR = HexColor("#d2d2d7")

S = {
    "name":  ParagraphStyle("name", fontName="Helvetica-Bold", fontSize=20, leading=24, textColor=INK),
    "contact": ParagraphStyle("contact", fontName="Helvetica", fontSize=8, leading=11, textColor=MUTED),
    "h":     ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=9, leading=11, textColor=ACCENT, spaceBefore=5, spaceAfter=1),
    "sub":   ParagraphStyle("sub", fontName="Helvetica-BoldOblique", fontSize=8.5, leading=10.5, textColor=INK, spaceBefore=2),
    "li":    ParagraphStyle("li", fontName="Helvetica", fontSize=8, leading=10.5, textColor=INK, leftIndent=8, bulletIndent=0, spaceBefore=0.5),
    "line":  ParagraphStyle("line", fontName="Helvetica", fontSize=8, leading=10.5, textColor=INK, spaceBefore=0.5),
}

L = lambda t: Paragraph("&#8226;&#8194;" + t, S["li"])

doc = SimpleDocTemplate(
    "Vedant_Konde_Resume_MIM.pdf", pagesize=A4,
    leftMargin=18*mm, rightMargin=18*mm, topMargin=14*mm, bottomMargin=14*mm,
    title="Vedant Konde — Resume", author="Vedant Konde",
)
story = [
    Paragraph("VEDANT KONDE", S["name"]),
    Spacer(1, 2),
    Paragraph("+91 88304 94337&#8194;|&#8194;vedantkondework@gmail.com&#8194;|&#8194;"
              '<a href="https://www.linkedin.com/in/vedant-konde" color="#a3132e">linkedin.com/in/vedant-konde</a>&#8194;|&#8194;'
              '<a href="https://github.com/Vedantk910" color="#a3132e">github.com/Vedantk910</a>', S["contact"]),

    Paragraph("WORK EXPERIENCE", S["h"]),
    Paragraph("<b>Amazon</b>, Remote&#8194;—&#8194;Sep 2024 &#8211; Aug 2026", S["sub"]),
    Paragraph("<i>Risk Specialist (Sep 2025 &#8211; Aug 2026); promoted after one year from Risk Investigator (Sep 2024 &#8211; Sep 2025)</i>", S["line"]),
    L("Built SQL- and Python-based ETL pipelines, automated reports and monitoring dashboards to analyse operational risk datasets, identify fraud patterns and support data-driven decisions, cutting weekly reporting time by 12%."),
    L("Resolved 67,000+ fraud cases over two years as a Subject Matter Expert and Risk Specialist, ranking in the top 5% for team productivity and accuracy and within the top 20% departmentally."),
    L("Recognised as Performer of the Month in September 2025, November 2025 and December 2025; became SME for Buyer Risk Prevention (BRP) process automation and joined the BRP AI Tool Assistance core team."),
    L("Redesigned BRP workflows, automated repetitive tasks and documented processes, improving operational efficiency by 15% and team adoption."),
    Paragraph("<b>Smartedge Solutions</b>, Remote&#8194;—&#8194;Jul 2024 &#8211; Aug 2024", S["sub"]),
    L("Analysed business datasets across multiple projects, identified 20+ operational improvement opportunities and supported initiatives that increased efficiency by 30%."),

    Paragraph("PROJECTS", S["h"]),
    Paragraph("<b>Business Management System</b>, Independent Project&#8194;—&#8194;Feb 2026", S["sub"]),
    L("Architected and deployed a full-stack business management system operational for 6+ months, covering 4,000+ SKUs, 7,000+ customers, sales tracking, and 3 branches."),
    L("Automated core inventory, customer, sales, and branch workflows, reducing manual effort by ~80%, saving 15&#8211;20 hours weekly, with zero operational support tickets for billing, transactions, or stock discrepancies."),
    Paragraph("<b>Automated Dental Cavity Detection</b> (IEEE TKD-24 Paper)&#8194;—&#8194;May 2023 &#8211; May 2024", S["sub"]),
    L("Coauthored a peer-reviewed paper with Dr. Deepali Ujalambkar as Lead Technical Architect; placed 3rd in the department; accepted for oral presentation at IEEE TechnicoKnockdown 2024 and published in <i>Journal of Technology</i> (Vol. 12(5), May 2024)."),
    Paragraph("<b>Khetirental</b> &#8212; Internal Smart India Hackathon 2023 (AISSMS COE)&#8194;—&#8194;Sep 2023", S["sub"]),
    L("Developed a location-based rental platform with proximity search and booking, enabling farmers to find nearby agricultural equipment and reduce upfront machinery-access costs."),
    L("Led end-to-end development from ideation and UI design to backend architecture and API integration; placed 2nd in the Computer Engineering Department at Internal SIH 2023."),

    Paragraph("EDUCATION", S["h"]),
    Paragraph("<b>AISSMS College of Engineering, Pune</b>&#8194;—&#8194;Jul 2020 &#8211; May 2024", S["sub"]),
    Paragraph("B.E. in Computer Engineering&#8194;(<b>First Class with Distinction</b>), CGPA 8.5/10", S["line"]),

    Paragraph("LEADERSHIP &amp; ENTREPRENEURIAL EXPERIENCE", S["h"]),
    Paragraph("<b>Founder &amp; Operations Lead, Gambit Chess Club</b>&#8194;—&#8194;Feb 2026 &#8211; Present", S["sub"]),
    L("Founded and scaled a multi-city chess venture across 4 cities (Nagpur, Pune, Nashik and Jaipur), generating INR 3.45 lakh+ in gross revenue across 30+ events with a 30%+ net profit margin."),
    L("Managed P&amp;L, pricing strategies, resource allocation, vendor contracts and customer acquisition budgets, achieving a 40% ticket yield premium in Pune and ~49% gross contribution margin across 30+ events."),
    L("Scaled an active community of 10,000+ members, led operations for 1,300+ paying clients, secured brand sponsorships, and negotiated revenue-sharing partnerships with 25+ premium commercial venues in an asset-light model."),
    Paragraph("<b>Founder and Lead, Niv Manch Initiative</b> (Aadarsh Gramin Bahuuddeshiya Sanstha)&#8194;—&#8194;Jan 2026 &#8191; Present".replace("&#8191;", "&#8211;"), S["sub"]),
    L("Founded an educational outreach initiative delivering free AI awareness and career guidance to 350+ students across rural schools in Nagpur and Umred through three on-ground seminar programs."),
    L("Trained 15+ school teachers to integrate free AI tools into secondary-school lesson planning through practical, hands-on sessions."),
    L("Delivered an AI education seminar and workshop for 120+ students at MIT-WPU, demonstrating practical AI tools and explaining academic and professional pathways in technology."),
    Paragraph("<b>Collegiate Leadership &amp; Sports</b>", S["sub"]),
    L("Chess: FIDE-rated player with a 1470 international rating (2026); won a DSO competition and captained the college team."),
    L("Football: Captained college team (2023&#8211;2024) in DSO competitions and won the inter-department competition."),
    L("Resonance Racing Team (Financial Management Lead): led budget planning and sponsorship negotiations while mentoring a junior finance subcommittee."),
    L("Junior Mentoring: ran after-hours sessions for juniors preparing for hackathons and coding contests; 6 new junior teams entered and 2 reached the podium, contributing to the department&#8217;s 2024 Interdepartment Trophy."),

    Paragraph("ADDITIONAL INFORMATION", S["h"]),
    Paragraph("<b>Languages:</b>&#8194;English (Fluent), Hindi (Native), Marathi (Native), Japanese (Basic)", S["line"]),
    Paragraph("<b>Technical Skills:</b>&#8194;Python (NumPy, Pandas, SciPy, Statsmodels), SQL (PostgreSQL), Advanced Excel, Risk Analytics, Fraud Detection Systems, Large Scale Data Analytics, Process Automation, Workflow Mapping, React, Spring Boot, VPS Deployment", S["line"]),
    Paragraph("<b>Certifications:</b>&#8194;AWS Certified Machine Learning Engineer, Associate (MLA-C01, Jun 2026) | AWS Certified Data Engineer, Associate (DEA-C01, Jun 2026) | IBM Python for Data Science, AI &amp; Development Professional Certificate (Jul 2024) | Google AI Professional Certificate (Apr 2026) | Business Foundations Specialization, University of Pennsylvania (Oct 2026)", S["line"]),
]
doc.build(story)
print("CV written")
