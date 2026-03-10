"""
Test Script for Image Forgery Detection System
Verifies that all components are properly installed and working
"""

import sys
import os

def test_imports():
    """Test all required imports"""
    print("Testing imports...")
    
    try:
        import cv2
        print("✓ OpenCV imported successfully")
    except ImportError as e:
        print(f"✗ OpenCV import failed: {e}")
        return False
    
    try:
        import numpy as np
        print("✓ NumPy imported successfully")
    except ImportError as e:
        print(f"✗ NumPy import failed: {e}")
        return False
    
    try:
        from PIL import Image
        print("✓ Pillow imported successfully")
    except ImportError as e:
        print(f"✗ Pillow import failed: {e}")
        return False
    
    try:
        from flask import Flask
        print("✓ Flask imported successfully")
    except ImportError as e:
        print(f"✗ Flask import failed: {e}")
        return False
    
    try:
        from scipy import stats
        print("✓ SciPy imported successfully")
    except ImportError as e:
        print(f"✗ SciPy import failed: {e}")
        return False
    
    try:
        from skimage.feature import match_template
        print("✓ scikit-image imported successfully")
    except ImportError as e:
        print(f"✗ scikit-image import failed: {e}")
        return False
    
    return True

def test_analysis_modules():
    """Test analysis modules"""
    print("\nTesting analysis modules...")
    
    try:
        from analysis.ela_analyzer import ELAAnalyzer
        print("✓ ELAAnalyzer imported successfully")
    except ImportError as e:
        print(f"✗ ELAAnalyzer import failed: {e}")
        return False
    
    try:
        from analysis.statistical_analyzer import StatisticalAnalyzer
        print("✓ StatisticalAnalyzer imported successfully")
    except ImportError as e:
        print(f"✗ StatisticalAnalyzer import failed: {e}")
        return False
    
    try:
        from analysis.manipulation_detector import ManipulationDetector
        print("✓ ManipulationDetector imported successfully")
    except ImportError as e:
        print(f"✗ ManipulationDetector import failed: {e}")
        return False
    
    try:
        from analysis.classifier import ForensicClassifier
        print("✓ ForensicClassifier imported successfully")
    except ImportError as e:
        print(f"✗ ForensicClassifier import failed: {e}")
        return False
    
    return True

def test_directories():
    """Test required directories"""
    print("\nTesting directories...")
    
    required_dirs = ['uploads', 'results', 'templates', 'static', 'analysis']
    
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"✓ Directory '{directory}' exists")
        else:
            print(f"✗ Directory '{directory}' missing")
            return False
    
    return True

def test_template_files():
    """Test template files"""
    print("\nTesting template files...")
    
    template_files = ['index.html', 'about.html', 'how_it_works.html']
    
    for template in template_files:
        path = os.path.join('templates', template)
        if os.path.exists(path):
            print(f"✓ Template '{template}' exists")
        else:
            print(f"✗ Template '{template}' missing")
            return False
    
    return True

def test_static_files():
    """Test static files"""
    print("\nTesting static files...")
    
    static_files = [
        'static/css/style.css',
        'static/js/main.js'
    ]
    
    for static_file in static_files:
        if os.path.exists(static_file):
            print(f"✓ Static file '{static_file}' exists")
        else:
            print(f"✗ Static file '{static_file}' missing")
            return False
    
    return True

def test_analysis_workflow():
    """Test analysis workflow with dummy data"""
    print("\nTesting analysis workflow...")
    
    try:
        import numpy as np
        from analysis.ela_analyzer import ELAAnalyzer
        from analysis.statistical_analyzer import StatisticalAnalyzer
        from analysis.classifier import ForensicClassifier
        
        # Create dummy ELA array
        dummy_ela = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        
        # Test statistical analyzer
        stat_analyzer = StatisticalAnalyzer()
        features = stat_analyzer.extract_features(dummy_ela)
        print("✓ Statistical feature extraction working")
        
        # Test classifier
        classifier = ForensicClassifier()
        dummy_manip = {
            'noise_inconsistency': {'detected': False, 'score': 0},
            'cloning_detected': {'detected': False, 'score': 0},
            'edge_anomalies': {'detected': False, 'score': 0},
            'color_blending': {'detected': False, 'score': 0}
        }
        result = classifier.classify(features, dummy_manip)
        print("✓ Classification working")
        
        return True
    except Exception as e:
        print(f"✗ Analysis workflow test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("Image Forgery Detection System - Test Suite")
    print("="*60)
    
    all_passed = True
    
    # Run tests
    all_passed &= test_imports()
    all_passed &= test_analysis_modules()
    all_passed &= test_directories()
    all_passed &= test_template_files()
    all_passed &= test_static_files()
    all_passed &= test_analysis_workflow()
    
    print("\n" + "="*60)
    if all_passed:
        print("✓ ALL TESTS PASSED")
        print("="*60)
        print("\nYour system is ready to use!")
        print("Run 'python app.py' to start the application")
        return 0
    else:
        print("✗ SOME TESTS FAILED")
        print("="*60)
        print("\nPlease fix the issues above before running the application")
        return 1

if __name__ == "__main__":
    sys.exit(main())
