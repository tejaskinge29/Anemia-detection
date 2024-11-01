from fpdf import FPDF

# Generate PDF report
def generate_pdf_report(patient_name, age, gender, predicted_class, class_prob):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(40, 10, 'Anemia Detection Report')
    pdf.ln(10)
    pdf.set_font('Arial', '', 12)
    pdf.cell(40, 10, f'Name: {patient_name}')
    pdf.ln(10)
    pdf.cell(40, 10, f'Age: {age}')
    pdf.ln(10)
    pdf.cell(40, 10, f'Gender: {gender}')
    pdf.ln(10)
    pdf.cell(40, 10, f'Predicted Anemia Type: {predicted_class}')
    pdf.ln(10)
    pdf.cell(40, 10, f'Probability: {class_prob:.2f}%')
    pdf_output = f"reports/{patient_name}_report.pdf"
    pdf.output(pdf_output)
    return pdf_output
