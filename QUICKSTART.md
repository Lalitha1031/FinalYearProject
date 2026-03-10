# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Open Terminal/Command Prompt

**Windows**: Press `Win + R`, type `cmd`, press Enter  
**Mac**: Press `Cmd + Space`, type `terminal`, press Enter  
**Linux**: Press `Ctrl + Alt + T`

### Step 2: Navigate to Project Folder

```bash
cd path/to/image-forgery-detection
```

### Step 3: Install Requirements

```bash
# First, create a virtual environment (recommended)
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Test the System

```bash
python test_system.py
```

If all tests pass, proceed to Step 5.

### Step 5: Run the Application

```bash
python app.py
```

You should see:
```
* Running on http://127.0.0.1:5000
```

### Step 6: Open in Browser

Open your web browser and go to:
```
http://localhost:5000
```

## 🎯 Testing the System

### Get Test Images

1. **Authentic Images**: Use original photos from your phone/camera
2. **Edited Images**: 
   - Open an image in any photo editor
   - Copy and paste objects
   - Save as JPEG
3. **Download samples** from free image sites

### Try the Analysis

1. Click the upload area
2. Select a JPEG image
3. Click "Analyze Image"
4. Wait 2-5 seconds
5. Review the results

## ❓ Troubleshooting

### "Module not found" Error

```bash
# Make sure virtual environment is activated
# Then reinstall requirements
pip install -r requirements.txt
```

### "Port already in use" Error

```bash
# Change port in app.py (last line):
# Change from:
app.run(debug=True, host='0.0.0.0', port=5000)
# To:
app.run(debug=True, host='0.0.0.0', port=8000)
```

### Images Not Loading

1. Check that `uploads/` and `results/` folders exist
2. Try restarting the application
3. Clear browser cache (Ctrl+Shift+Delete)

## 📝 For Your Project Report

### Screenshots to Include

1. **Home Page**: Upload interface
2. **Analysis Results**: Classification result card
3. **ELA Visualization**: Original vs ELA comparison
4. **Statistical Features**: Feature values display
5. **Manipulation Indicators**: Detection results

### Key Points to Highlight

- **Technology Used**: Flask, OpenCV, NumPy
- **Techniques Applied**: ELA, Statistical Analysis, Manipulation Detection
- **Classification Method**: Rule-based decision making
- **Performance**: 2-5 seconds per image
- **Accuracy**: Depends on image quality and manipulation type

## 🎓 Demonstration Tips

1. **Start with authentic image**: Show it's classified as authentic
2. **Show edited image**: Demonstrate manipulation detection
3. **Explain ELA**: Point out bright regions in tampered areas
4. **Discuss features**: Explain what each statistical value means
5. **Show confidence**: Explain how confidence scores work

## 📊 Dataset Suggestions

For testing and evaluation:

1. **CASIA Dataset**: Research dataset for image forgery
2. **Your own images**: Edit photos yourself
3. **AI-generated**: Use Stable Diffusion or similar
4. **Internet sources**: Download from stock photo sites

## ✅ Final Checklist

Before submitting:

- [ ] All code files present
- [ ] Requirements.txt included
- [ ] README.md completed
- [ ] Screenshots taken
- [ ] Report written
- [ ] Code commented
- [ ] System tested with multiple images
- [ ] Results documented

## 🎉 You're Ready!

Your Image Forgery Detection System is now complete and ready for demonstration and submission!

Good luck with your project! 🚀
