from flask import Flask, request, render_template, jsonify, send_file
import os
import logging
from PIL import Image
import numpy as np
from fpdf import FPDF

app = Flask(__name__)


# Function to predict anemia using the image and CBC parameters
def predict_anemia(img_array, hemoglobin, age, gender, mcv, rbc_count):
    # Predict using the image model
    image_prediction = model.predict(img_array)
    class_index = np.argmax(image_prediction, axis=1)[0]
    classes = ['Dimorphic Anemia', 'Sickle Cell Anemia', 'Iron Deficiency Anemia', 'Vitamin B12 Deficiency (Megaloblastic)', 'Thalassemia']
    predicted_class = classes[class_index]
    
    # Incorporate CBC data for refining the diagnosis
    hemoglobin = float(hemoglobin)
    mcv = float(mcv)  # Mean Corpuscular Volume (MCV)
    rbc_count = float(rbc_count)  # RBC count
    
    # Iron Deficiency Anemia
    if predicted_class == 'Iron Deficiency Anemia' and hemoglobin < 12 and mcv < 80:
        predicted_class = 'Iron Deficiency Anemia'
    
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

    # You can add more conditions for other types of anemia based on CBC data

    return predicted_class, np.max(image_prediction) * 100


# Preprocess image function
def preprocess_image(img_path):
    img = Image.open(img_path)
    img = img.resize((224, 224))
    img_array = np.array(img)
    img_array = img_array / 255.0  # Normalize
    img_array = np.expand_dims(img_array, axis=0)  # Batch size 1
    return img_array

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

            # Preprocess the image
            img_array = preprocess_image(filepath)

            # Make prediction using the image and CBC parameters
            predicted_class, class_prob = predict_anemia(img_array, hemoglobin, age, gender, mcv, rbc_count)

            # Render the template with the result
            return render_template('index.html', result=predicted_class, probability=f"{class_prob:.2f}%")

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    app.run(debug=True)
