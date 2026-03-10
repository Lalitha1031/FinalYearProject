// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const filePreview = document.getElementById('filePreview');
const previewImage = document.getElementById('previewImage');
const fileName = document.getElementById('fileName');
const uploadForm = document.getElementById('uploadForm');
const analyzeBtn = document.getElementById('analyzeBtn');
const loadingSpinner = document.getElementById('loadingSpinner');
const resultsSection = document.getElementById('resultsSection');

let selectedFile = null;

// Upload area click handler
uploadArea.addEventListener('click', () => {
    fileInput.click();
});

// Drag and drop handlers
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = '#0a58ca';
    uploadArea.style.background = '#e7f1ff';
});

uploadArea.addEventListener('dragleave', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = '#0d6efd';
    uploadArea.style.background = '#f8f9fa';
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = '#0d6efd';
    uploadArea.style.background = '#f8f9fa';
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileSelect(files[0]);
    }
});

// File input change handler
fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileSelect(e.target.files[0]);
    }
});

// Handle file selection
function handleFileSelect(file) {
    // Validate file type
    if (!file.type.match('image/jpeg') && !file.type.match('image/jpg')) {
        alert('Please select a JPEG or JPG image file.');
        return;
    }
    
    // Validate file size (16MB)
    if (file.size > 16 * 1024 * 1024) {
        alert('File size must be less than 16MB.');
        return;
    }
    
    selectedFile = file;
    
    // Display preview
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
        fileName.textContent = file.name;
        filePreview.style.display = 'block';
        uploadArea.style.display = 'none';
        analyzeBtn.disabled = false;
    };
    reader.readAsDataURL(file);
}

// Form submission handler
uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    if (!selectedFile) {
        alert('Please select an image first.');
        return;
    }
    
    // Show loading state
    analyzeBtn.disabled = true;
    loadingSpinner.style.display = 'block';
    resultsSection.style.display = 'none';
    
    // Prepare form data
    const formData = new FormData();
    formData.append('file', selectedFile);
    
    try {
        // Send request to server
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            // Display results
            displayResults(data);
        } else {
            alert('Error: ' + (data.error || 'Analysis failed'));
            analyzeBtn.disabled = false;
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred during analysis. Please try again.');
        analyzeBtn.disabled = false;
    } finally {
        loadingSpinner.style.display = 'none';
    }
});

// Display analysis results
function displayResults(data) {
    // Scroll to results
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    
    // Display classification result
    displayClassification(data.classification, data.confidence);
    
    // Display images
    document.getElementById('originalImage').src = '/uploads/' + data.filename;
    document.getElementById('elaImage').src = data.ela_image;
    
    // Display statistical features
    displayStatisticalFeatures(data.statistical_features);
    
    // Display manipulation indicators
    displayManipulationIndicators(data.manipulation_indicators);
    
    // Display explanation
    document.getElementById('explanation').textContent = data.explanation;
}

// Display classification result
function displayClassification(label, confidence) {
    const resultLabel = document.getElementById('resultLabel');
    const resultIcon = document.getElementById('resultIcon');
    const confidenceBar = document.getElementById('confidenceBar');
    const confidenceText = document.getElementById('confidenceText');
    
    resultLabel.textContent = label;
    confidenceText.textContent = (confidence * 100).toFixed(0) + '%';
    
    // Set icon based on classification
    let iconHTML = '';
    let barClass = '';
    
    if (label === 'Authentic') {
        iconHTML = '<i class="fas fa-check-circle text-success" style="font-size: 4rem;"></i>';
        barClass = 'bg-success';
    } else if (label.includes('Manipulated') || label.includes('Edited')) {
        iconHTML = '<i class="fas fa-exclamation-triangle text-warning" style="font-size: 4rem;"></i>';
        barClass = 'bg-danger';
    } else {
        iconHTML = '<i class="fas fa-question-circle text-info" style="font-size: 4rem;"></i>';
        barClass = 'bg-warning';
    }
    
    resultIcon.innerHTML = iconHTML;
    confidenceBar.className = 'progress-bar ' + barClass;
    confidenceBar.style.width = (confidence * 100) + '%';
    confidenceBar.textContent = (confidence * 100).toFixed(0) + '%';
}

// Display statistical features
function displayStatisticalFeatures(features) {
    const container = document.getElementById('statisticalFeatures');
    
    const featuresList = [
        { label: 'Mean Intensity', value: features.mean_intensity.toFixed(2), unit: '' },
        { label: 'Variance', value: features.variance.toFixed(2), unit: '' },
        { label: 'Standard Deviation', value: features.std_deviation.toFixed(2), unit: '' },
        { label: 'High Intensity Ratio', value: (features.high_intensity_ratio * 100).toFixed(1), unit: '%' },
        { label: 'Edge Intensity', value: features.edge_intensity.toFixed(2), unit: '' },
        { label: 'Local Variance', value: features.local_variance.toFixed(2), unit: '' }
    ];
    
    let html = '';
    featuresList.forEach(feature => {
        html += `
            <div class="stat-item">
                <span class="stat-label">${feature.label}</span>
                <span class="stat-value">${feature.value}${feature.unit}</span>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

// Display manipulation indicators
function displayManipulationIndicators(indicators) {
    const container = document.getElementById('manipulationIndicators');
    
    const indicatorsList = [
        { 
            label: 'Noise Inconsistency', 
            data: indicators.noise_inconsistency,
            icon: 'fa-wave-square'
        },
        { 
            label: 'Clone Detection', 
            data: indicators.cloning_detected,
            icon: 'fa-copy'
        },
        { 
            label: 'Edge Anomalies', 
            data: indicators.edge_anomalies,
            icon: 'fa-border-style'
        },
        { 
            label: 'Color Blending', 
            data: indicators.color_blending,
            icon: 'fa-palette'
        }
    ];
    
    let html = '';
    indicatorsList.forEach(indicator => {
        const isDetected = indicator.data.detected;
        const itemClass = isDetected ? 'detected' : 'not-detected';
        const iconClass = isDetected ? 'fa-exclamation-circle text-warning' : 'fa-check-circle text-success';
        
        html += `
            <div class="indicator-item ${itemClass}">
                <div>
                    <i class="fas ${iconClass} indicator-icon"></i>
                    <strong>${indicator.label}</strong>
                    <p class="mb-0 small text-muted">${indicator.data.description}</p>
                </div>
                <div>
                    ${isDetected ? 
                        '<span class="badge bg-warning">Detected</span>' : 
                        '<span class="badge bg-success">Not Detected</span>'}
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}
