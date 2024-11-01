from flask import Flask, request, render_template, jsonify, send_file
import os
import logging
from fpdf import FPDF
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model

from PIL import ImageDraw, ImageFont
# pdf
from pdf import generate_pdf_report


app = Flask(__name__)

model = load_model('M_Anemia.h5')

# Function to predict anemia using the image and CBC parameters
def predict_anemia(img_array, hemoglobin, age, gender, mcv, rbc_count):
    # Predict using the image model
    image_prediction = model.predict(img_array)
    class_index = np.argmax(image_prediction, axis=1)[0]
    classes = ['Dimorphic Anemia', 'Sickle Cell Anemia', 'Iron Deficiency Anemia', 'Thalassemia', 'Vitamin B12 Deficiency (Megaloblastic)']
    predicted_class = classes[class_index]
    
    # Incorporate CBC data for refining the diagnosis
    try:
        hemoglobin = float(hemoglobin)
        mcv = float(mcv)  # Mean Corpuscular Volume (MCV)
        rbc_count = float(rbc_count)  # RBC count
    except ValueError:
        return "Invalid input for CBC data", 0

    # Iron Deficiency Anemia
    if predicted_class == 'Iron Deficiency Anemia':
        if hemoglobin < 12 and mcv < 80:
            predicted_class = 'Iron Deficiency Anemia'
        else:
            return "CBC values do not support Iron Deficiency Anemia diagnosis", 0
    
    # Vitamin B12 Deficiency (Megaloblastic Anemia)
    elif predicted_class == 'Vitamin B12 Deficiency (Megaloblastic)' and hemoglobin < 9 and mcv > 100:
        predicted_class = 'Vitamin B12 Deficiency (Megaloblastic)'
    
    # Sickle Cell Anemia (based on low hemoglobin and genetic markers, but approximating here)
    elif predicted_class == 'Sickle Cell Anemia' and hemoglobin < 10 and rbc_count < 3.5:
        predicted_class = 'Sickle Cell Anemia'
    
    # Dimorphic Anemia (a combination of iron and B12 deficiency)
    elif predicted_class == 'Dimorphic Anemia' and hemoglobin < 10 and (mcv > 100 or mcv < 80):
        predicted_class = 'Dimorphic Anemia'
    
    # Thalassemia (low hemoglobin with high RBC count, and very low MCV)
    elif predicted_class == 'Thalassemia' and hemoglobin < 10 and rbc_count > 5 and mcv < 75:
        predicted_class = 'Thalassemia'
    
    return predicted_class, np.max(image_prediction) * 100


# # Function to predict anemia using the image and CBC parameters
# def predict_anemia(img_array, hemoglobin, age, gender, mcv, rbc_count):
#     # Predict using the image model
#     image_prediction = model.predict(img_array)
#     class_index = np.argmax(image_prediction, axis=1)[0]
#     classes = ['Dimorphic Anemia', 'Sickle Cell Anemia', 'Iron Deficiency Anemia', 'Vitamin B12 Deficiency (Megaloblastic)', 'Thalassemia']
#     predicted_class = classes[class_index]
    
#     # Incorporate CBC data for refining the diagnosis
#     hemoglobin = float(hemoglobin)
#     mcv = float(mcv)  # Mean Corpuscular Volume (MCV)
#     rbc_count = float(rbc_count)  # RBC count
    
#     # Iron Deficiency Anemia
#     if predicted_class == 'Iron Deficiency Anemia' and hemoglobin < 12 and mcv < 80:
#         predicted_class = 'Iron Deficiency Anemia'
    
#     # Vitamin B12 Deficiency (Megaloblastic Anemia)
#     elif predicted_class == 'Vitamin B12 Deficiency (Megaloblastic)' and hemoglobin < 9 and mcv > 100:
#         predicted_class = 'Vitamin B12 Deficiency (Megaloblastic)'
    
#     # Sickle Cell Anemia (based on low hemoglobin and genetic markers, but approximating here)
#     elif predicted_class == 'Sickle Cell Anemia' and hemoglobin < 10 and rbc_count < 3.5:
#         predicted_class = 'Sickle Cell Anemia'
    
#     # Dimorphic Anemia (a combination of iron and B12 deficiency)
#     elif predicted_class == 'Dimorphic Anemia' and hemoglobin < 10 and (mcv > 100 or mcv < 80):
#         predicted_class = 'Dimorphic Anemia'
    
#     # Thalassemia (low hemoglobin with high RBC count, and very low MCV)
#     elif predicted_class == 'Thalassemia' and hemoglobin < 10 and rbc_count > 5 and mcv < 75:
#         predicted_class = 'Thalassemia'

#     # You can add more conditions for other types of anemia based on CBC data

#     return predicted_class, np.max(image_prediction) * 100


# Preprocess image function
def preprocess_image(img_path):
    try:
        img = Image.open(img_path)
        img = img.convert("RGB")  # Ensure the image is RGB
        if img.size != (224, 224):
            img = img.resize((224, 224))  # Resize if necessary
        img_array = np.array(img)
        img_array = img_array / 255.0  # Normalize
        img_array = np.expand_dims(img_array, axis=0)  # Batch size 1
        return img_array
    except Exception as e:
        raise ValueError("Invalid image format or the image is not related to anemia.")

# prev code
# def preprocess_image(img_path):
#     img = Image.open(img_path)
#     img = img.resize((224, 224))
#     img_array = np.array(img)
#     img_array = img_array / 255.0  # Normalize
#     img_array = np.expand_dims(img_array, axis=0)  # Batch size 1
#     return img_array

def validate_image_size(img):
    width, height = img.size
    # Assuming blood smear images should have a minimum resolution and be roughly square
    if width >= 300 and height >= 300 and 0.75 < width / height < 1.33:  # Aspect ratio between 3:4 and 4:3
        return True
    return False

#warning popup
def add_warning_to_image(img_path, message):
    # Open the original image
    img = Image.open(img_path)
    draw = ImageDraw.Draw(img)

    # Set up the font and message position
    try:
        # Load a TTF font file if available, else use the default font
        font = ImageFont.truetype("arial.ttf", 36)
    except IOError:
        font = ImageFont.load_default()
    
    # Use a safer way to calculate text size
    text_width, text_height = draw.textsize(message, font=font)

    # Calculate text position (centered)
    text_x = (img.width - text_width) / 2
    text_y = 10  # Positioning the text at the top of the image

    # Draw a semi-transparent rectangle behind the text
    draw.rectangle([text_x - 10, text_y - 10, text_x + text_width + 10, text_y + text_height + 10], fill=(255, 0, 0, 128))  # Red background
    draw.text((text_x, text_y), message, fill="white", font=font)

    # Save the new image
    warning_image_path = os.path.join("uploads", "warning_" + os.path.basename(img_path))
    img.save(warning_image_path)
    
    return warning_image_path


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        hemoglobin = request.form['hemoglobin']
        mcv = request.form['mcv']
        rbc_count = request.form['rbc_count']

        # Get the uploaded image
        file = request.files['image']
        if file:
            filepath = os.path.join("uploads", file.filename)
            file.save(filepath)

            # # Validate the image size and aspect ratio
            # img = Image.open(filepath)
            # if not validate_image_size(img):
            #     return jsonify({"error": "Invalid image size or aspect ratio. Please upload a valid blood smear image."})

            # Validate the image size and aspect ratio
            img = Image.open(filepath)
            if not validate_image_size(img):
                warning_message = "Invalid image size or format!"
                return render_template('index.html', warning=warning_message)
            # if not validate_image_size(img):
            #     warning_image_path = add_warning_to_image(filepath, "Invalid image size or format!")
            #     return render_template('index.html', warning_image=warning_image_path)


            # Preprocess the image
            img_array = preprocess_image(filepath)

            # Make prediction using the image and CBC parameters
            predicted_class, class_prob = predict_anemia(img_array, hemoglobin, age, gender, mcv, rbc_count)


             #Generate PDF report
            patient_name = request.form['name']
            pdf_path = generate_pdf_report(patient_name, age, gender, predicted_class, class_prob)

            # Render the template with the result and provide a link to download the PDF report
            return render_template('index.html', result=predicted_class, probability=f"{class_prob:.2f}%", pdf_path=pdf_path)

            # # Render the template with the result
            # return render_template('index.html', result=predicted_class, probability=f"{class_prob:.2f}%")

    except Exception as e:
        return jsonify({"error": str(e)})
    
@app.route('/download_report', methods=['GET'])
def download_report():
    patient_name = request.args.get('name')
    file_path = generate_pdf_report(patient_name, ...)
    return send_file(file_path, as_attachment=True)


if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    app.run(debug=True)
