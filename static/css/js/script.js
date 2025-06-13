// Anemia Detection System - Vanilla JavaScript Implementation

// Constants for anemia types and descriptions
const ANEMIA_TYPES = [
    'Dimorphic Anemia',
    'Sickle Cell Anemia',
    'Thalassemia',
    'Vitamin B12 Deficiency',
    'Iron Deficiency Anemia'
  ];
  
  const ANEMIA_DESCRIPTIONS = {
    'Dimorphic Anemia': 'Characterized by the presence of two distinct populations of red blood cells: normocytic normochromic and microcytic hypochromic cells.',
    'Sickle Cell Anemia': 'A genetic disorder causing red blood cells to become sickle-shaped, leading to blocked blood flow and oxygen delivery issues.',
    'Thalassemia': 'An inherited blood disorder characterized by abnormal hemoglobin production, resulting in destruction of red blood cells.',
    'Vitamin B12 Deficiency': 'Results in the formation of abnormally large red blood cells that cannot function properly, often due to dietary deficiency or absorption issues.',
    'Iron Deficiency Anemia': 'The most common type of anemia, caused by insufficient iron to produce hemoglobin, resulting in small, pale red blood cells.'
  };
  
  // DOM Elements
  const tabButtons = document.querySelectorAll('.tab');
  const tabPanes = document.querySelectorAll('.tab-pane');
  const patientForm = document.getElementById('patient-form');
  const resetFormButton = document.getElementById('reset-form');
  const processImageButton = document.getElementById('process-image');
  const newAnalysisButton = document.getElementById('new-analysis');
  const downloadReportButton = document.getElementById('download-report');
  const imageInput = document.getElementById('image');
  const imagePreviewContainer = document.getElementById('image-preview-container');
  const imagePreview = document.getElementById('image-preview');
  const removeImageButton = document.getElementById('remove-image');
  const uploadContainer = document.getElementById('upload-container');
  const loadingOverlay = document.getElementById('loading-overlay');
  
  // Patient data and selected image state
  let patientData = {};
  let selectedImage = null;
  
  // Initialize the application
  document.addEventListener('DOMContentLoaded', () => {
    setupTabNavigation();
    setupFormHandling();
    setupImageUpload();
  });
  
  // Tab Navigation
  function setupTabNavigation() {
    tabButtons.forEach(button => {
      button.addEventListener('click', () => {
        const tabName = button.getAttribute('data-tab');
        
        // Only allow switching to results tab if we have results
        if (tabName === 'results' && !document.getElementById('result-anemiaType').textContent.trim()) {
          return;
        }
        
        // Update active tab button
        tabButtons.forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');
        
        // Show the selected tab pane
        tabPanes.forEach(pane => pane.classList.remove('active'));
        document.getElementById(`${tabName}-tab`).classList.add('active');
      });
    });
  }
  
  // Form Handling
  function setupFormHandling() {
    // Form submission
    patientForm.addEventListener('submit', handleFormSubmit);
    
    // Reset form
    resetFormButton.addEventListener('click', resetForm);
    
    // New analysis button
    newAnalysisButton.addEventListener('click', () => {
      // Switch to patient data tab
      tabButtons[0].click();
    });
    
    // Download report button
    downloadReportButton.addEventListener('click', () => {
      alert('In a real application, this would generate a PDF report with the analysis results.');
    });
  }
  
  // Image Upload
  function setupImageUpload() {
    // File input change
    imageInput.addEventListener('change', handleImageChange);
    
    // Remove image button
    removeImageButton.addEventListener('click', removeImage);
    
    // Drag and drop functionality
    uploadContainer.addEventListener('dragover', (e) => {
      e.preventDefault();
      uploadContainer.classList.add('border-indigo-500');
    });
    
    uploadContainer.addEventListener('dragleave', () => {
      uploadContainer.classList.remove('border-indigo-500');
    });
    
    uploadContainer.addEventListener('drop', (e) => {
      e.preventDefault();
      uploadContainer.classList.remove('border-indigo-500');
      
      if (e.dataTransfer.files.length) {
        const file = e.dataTransfer.files[0];
        if (file.type.startsWith('image/')) {
          imageInput.files = e.dataTransfer.files;
          handleImageChange({ target: { files: e.dataTransfer.files } });
        }
      }
    });
  }
  
  // Handle image selection
  function handleImageChange(e) {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      selectedImage = file;
      
      const reader = new FileReader();
      reader.onload = (event) => {
        imagePreview.src = event.target.result;
        imagePreviewContainer.style.display = 'block';
        
        // Hide the upload elements
        document.querySelector('.upload-icon').style.display = 'none';
        document.querySelector('.upload-text').style.display = 'none';
        document.querySelector('.upload-hint').style.display = 'none';
        imageInput.style.display = 'none';
      };
      reader.readAsDataURL(file);
    }
  }
  
  // Remove selected image
  function removeImage() {
    selectedImage = null;
    imagePreview.src = '';
    imagePreviewContainer.style.display = 'none';
    imageInput.value = '';
    
    // Show the upload elements again
    document.querySelector('.upload-icon').style.display = 'block';
    document.querySelector('.upload-text').style.display = 'block';
    document.querySelector('.upload-hint').style.display = 'block';
    imageInput.style.display = 'block';
  }
  
  // Handle form submission
  async function handleFormSubmit(e) {
    e.preventDefault();
    
    if (!selectedImage) {
      alert('Please upload a blood smear image');
      return;
    }
    
    // Collect form data
    const formData = new FormData(patientForm);
    patientData = Object.fromEntries(formData.entries());

    formData.append('image', selectedImage);

    // Show loading overlay
    loadingOverlay.style.display = 'flex';

    try {
    const response = await fetch('/predict', {
      method: 'POST',
      body: formData
    });

    const result = await response.json();

    if (result.error) {
      alert(result.error);
      return;
    }
    // ✅ This is where we use the real result from Flask!
    updateResults({
      anemiaType: result.anemiaType,
      confidence: result.confidence,
      description: result.description,
      // patientData: patientData
      // patientData: result.patientData,
      imageUrl: result.imageUrl
    });

    tabButtons[1].click(); // Switch to Results tab

  } catch (error) {
    console.error('Error:', error);
    alert('Failed to process image');
  } finally {
    loadingOverlay.style.display = 'none';
  }
}

//   fetch('/predict', {
//   method: 'POST',
//   body: formData
// })
  // Process the image (simulation)
  function processImage() {
    // Randomly select an anemia type for demonstration
    const randomType = ANEMIA_TYPES[Math.floor(Math.random() * ANEMIA_TYPES.length)];
    const randomConfidence = Math.round((0.7 + Math.random() * 0.29) * 100) / 100;
    
    // Update results
    updateResults({
      anemiaType: randomType,
      confidence: randomConfidence,
      description: ANEMIA_DESCRIPTIONS[randomType]
    });
    
    // Hide loading overlay
    loadingOverlay.style.display = 'none';
    
    // Switch to results tab
    tabButtons[1].click();
  }
  
  // Update the results view with data
  function updateResults(results) {
    // Use patient data from results object
    const data = results.patientData;

    document.getElementById('result-name').textContent = data.name || '-';
    document.getElementById('result-age').textContent = data.age || '-';
    document.getElementById('result-sex').textContent = data.sex || '-';
    document.getElementById('result-bloodType').textContent = data.bloodType || '-';

    document.getElementById('result-rbcCount').textContent = data.rbcCount ? `${data.rbcCount} 10^6/μL` : '-';
    document.getElementById('result-hemoglobin').textContent = data.hemoglobin ? `${data.hemoglobin} g/dL` : '-';
    document.getElementById('result-hematocrit').textContent = data.hematocrit ? `${data.hematocrit}%` : '-';
    document.getElementById('result-mcv').textContent = data.mcv ? `${data.mcv} fL` : '-';
    document.getElementById('result-mch').textContent = data.mch ? `${data.mch} pg` : '-';
    document.getElementById('result-mchc').textContent = data.mchc ? `${data.mchc} g/dL` : '-';
    document.getElementById('result-rdw').textContent = data.rdw ? `${data.rdw}%` : '-';
    document.getElementById('result-plateletCount').textContent = data.plateletCount ? `${data.plateletCount} 10^3/μL` : '-';

    // Analysis result
    document.getElementById('result-anemiaType').textContent = results.anemiaType;
    document.getElementById('result-confidence').textContent = `${(results.confidence * 100).toFixed(1)}%`;
    document.getElementById('result-description').textContent = results.description;

    // Image
    document.getElementById('result-image').src = results.imageUrl;
}
  
  // Reset the form
  function resetForm() {
    patientForm.reset();
    removeImage();
  }