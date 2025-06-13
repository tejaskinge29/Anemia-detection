from fpdf import FPDF
import os

# Make sure the reports folder exists
os.makedirs("reports", exist_ok=True)

def generate_pdf_report(patient_name, age, gender, predicted_class, class_prob, rbc_count, blood_type,hemoglobin,mch,mcv):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

     # 📌 Add logo (left side)
    pdf.image('static/logo.png', 8, 1, 40)  # (path, x, y, width)

    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Anemia Detection Report', ln=True, align='C')

    
     # 🏥 Address (below title in smaller font)
    pdf.set_font('Arial', '', 10)
    pdf.set_text_color(100)  # Grey color
    pdf.set_y(18)  # Below the title
    pdf.cell(0, 10, 'PathLabs Diagnostic Center, Pune, Maharashtra - 411001', border=0, ln=True, align='C')
    


    pdf.ln(10)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'Name: {patient_name}', ln=True)
    pdf.cell(0, 10, f'Age: {age}', ln=True)
    pdf.cell(0, 10, f'Gender: {gender}', ln=True)
    pdf.cell(0, 10, f'Predicted Anemia Type: {predicted_class}', ln=True)
    pdf.cell(0, 10, f'RBC Count: {rbc_count}', ln=True)
    pdf.cell(0, 10, f'Blood Group: {blood_type}', ln=True)
    pdf.cell(0, 10, f'Hemoglobin Level: {hemoglobin}', ln=True)
    pdf.cell(0, 10, f'Mean Corpuscular Hemoglobin (MCH): {mch}', ln=True)
    pdf.cell(0, 10, f'Mean Corpuscular Volume (MCV): {mcv}', ln=True)



    # pdf.cell(0, 10, f'Probability: {class_prob:.2f}%', ln=True)

    # pdf_output_path = f"reports/{patient_name}_report.pdf"
    # pdf.output(pdf_output_path)
    
    # return pdf_output_path  # Returns the path to the generated PDF
    
    pdf_output_path = f"reports/{patient_name}_report.pdf"
    pdf.output(pdf_output_path)
    
    return pdf_output_path



# from fpdf import FPDF

# # Generate PDF report
# def generate_pdf_report(patient_name, age, gender, predicted_class, class_prob):
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font('Arial', 'B', 16)
#     pdf.cell(40, 10, 'Anemia Detection Report')
#     pdf.ln(10)
#     pdf.set_font('Arial', '', 12)
#     pdf.cell(40, 10, f'Name: {patient_name}')
#     pdf.ln(10)
#     pdf.cell(40, 10, f'Age: {age}')
#     pdf.ln(10)
#     pdf.cell(40, 10, f'Gender: {gender}')
#     pdf.ln(10)
#     pdf.cell(40, 10, f'Predicted Anemia Type: {predicted_class}')
#     pdf.ln(10)
#     pdf.cell(40, 10, f'Probability: {class_prob:.2f}%')
#     pdf_output = f"reports/{patient_name}_report.pdf"
#     pdf.output(pdf_output)
#     return pdf_output
