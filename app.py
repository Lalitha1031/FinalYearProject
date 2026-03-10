from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
import json
from datetime import datetime
from analysis.ela_analyzer import ELAAnalyzer
from analysis.statistical_analyzer import StatisticalAnalyzer
from analysis.manipulation_detector import ManipulationDetector
from analysis.classifier import ForensicClassifier

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
RESULTS_FOLDER = 'results'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create necessary directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if uploaded file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')

@app.route('/about')
def about():
    """Render about page"""
    return render_template('about.html')

@app.route('/how-it-works')
def how_it_works():
    """Render how it works page"""
    return render_template('how_it_works.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle image upload and perform forensic analysis"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file type
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only JPEG/JPG files are allowed'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        # Initialize analyzers
        ela_analyzer = ELAAnalyzer()
        stat_analyzer = StatisticalAnalyzer()
        manip_detector = ManipulationDetector()
        classifier = ForensicClassifier()
        
        # Step 1: Perform ELA
        ela_output_path = os.path.join(app.config['RESULTS_FOLDER'], f"ela_{unique_filename}")
        ela_image = ela_analyzer.perform_ela(filepath, ela_output_path)
        
        # Step 2: Extract statistical features
        statistical_features = stat_analyzer.extract_features(ela_image)
        
        # Step 3: Detect manipulation artifacts
        manipulation_results = manip_detector.detect_artifacts(filepath, ela_image)
        
        # Step 4: Classify image
        classification_result = classifier.classify(
            statistical_features, 
            manipulation_results
        )
        
        # Prepare response
        response = {
            'success': True,
            'filename': unique_filename,
            'ela_image': f"/results/ela_{unique_filename}",
            'classification': classification_result['label'],
            'confidence': classification_result['confidence'],
            'statistical_features': statistical_features,
            'manipulation_indicators': manipulation_results,
            'explanation': classification_result['explanation'],
            'timestamp': timestamp
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/results/<filename>')
def get_result(filename):
    """Serve result images"""
    return send_from_directory(app.config['RESULTS_FOLDER'], filename)

@app.route('/uploads/<filename>')
def get_upload(filename):
    """Serve uploaded images"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    return jsonify({'error': 'File too large. Maximum size is 16MB'}), 413

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
