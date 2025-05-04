from fpdf import FPDF
import datetime

def save_summary_to_pdf(summary_text):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="VibeNews Summary", ln=True, align="C")
        pdf.ln(10)

        for line in summary_text.split('\n'):
            pdf.multi_cell(0, 10, line)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"vibenews_summary_{timestamp}.pdf"
        pdf.output(filename)
        print(f"📄 PDF saved: {filename}")

    except Exception as e:
        print(f"PDF generation error: {e}")
