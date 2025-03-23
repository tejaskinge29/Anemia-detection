# Anemia Detection Using Image Processing - 2025

## Overview
The Anemia Detection project leverages machine learning and image processing techniques to identify different types of anemia from blood smear images. This solution is designed to assist medical professionals in making quicker and more accurate diagnoses. Built using Python with a Flask-based interface, the system processes input images, runs predictions, and generates comprehensive reports, providing a user-friendly experience for non-experts.

## Key Features

- **Anemia Classification**: The system can detect and classify different types of anemia (e.g., Dimorphic Anemia) by analyzing blood smear images using a trained deep learning model.
- **Image Processing**: Enhanced with data augmentation and transfer learning techniques for improved accuracy and reliability in predictions.
- **Report Generation**: Automatically generates a PDF lab report for each diagnosis, containing patient details, predicted anemia type, and probability scores.
- **User-Friendly Interface**: Developed using Flask, the web app allows users to upload blood smear images, view results, and download professional PDF reports.

## Technologies Used

- **Python**: Core language for image processing, machine learning, and backend logic.
- **TensorFlow & Keras**: For building and training the deep learning model.
- **Flask**: For developing the web-based user interface.
- **OpenCV**: For image preprocessing and augmentation.
- **FPDF**: For generating professional PDF reports containing diagnosis results.
