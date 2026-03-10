import cv2
import numpy as np
from PIL import Image
import os

class ELAAnalyzer:
    """
    Error Level Analysis (ELA) Analyzer
    Detects compression inconsistencies in JPEG images
    """
    
    def __init__(self, quality=95, scale=10):
        """
        Initialize ELA Analyzer
        
        Args:
            quality (int): JPEG recompression quality (default: 95)
            scale (int): Amplification factor for visualization (default: 10)
        """
        self.quality = quality
        self.scale = scale
    
    def perform_ela(self, image_path, output_path):
        """
        Perform Error Level Analysis on an image
        
        Args:
            image_path (str): Path to input image
            output_path (str): Path to save ELA output
            
        Returns:
            numpy.ndarray: ELA image array
        """
        try:
            # Load original image
            original = Image.open(image_path)
            
            # Convert to RGB if needed
            if original.mode != 'RGB':
                original = original.convert('RGB')
            
            # Create temporary path for recompressed image
            temp_path = output_path.replace('.jpg', '_temp.jpg').replace('.jpeg', '_temp.jpg')
            
            # Resave image at specified quality
            original.save(temp_path, 'JPEG', quality=self.quality)
            
            # Load recompressed image
            recompressed = Image.open(temp_path)
            
            # Convert both images to numpy arrays
            original_array = np.array(original, dtype=np.float32)
            recompressed_array = np.array(recompressed, dtype=np.float32)
            
            # Calculate absolute difference
            ela_array = np.abs(original_array - recompressed_array)
            
            # Scale for visualization
            ela_array = ela_array * self.scale
            
            # Clip values to valid range
            ela_array = np.clip(ela_array, 0, 255).astype(np.uint8)
            
            # Save ELA image
            ela_image = Image.fromarray(ela_array)
            ela_image.save(output_path)

            # Clean up temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            return ela_array
            
        except Exception as e:
            raise Exception(f"ELA analysis failed: {str(e)}")
    
    def get_ela_statistics(self, ela_array):
        """
        Calculate basic statistics from ELA output
        
        Args:
            ela_array (numpy.ndarray): ELA image array
            
        Returns:
            dict: Statistical measures
        """
        return {
            'mean': float(np.mean(ela_array)),
            'std': float(np.std(ela_array)),
            'max': float(np.max(ela_array)),
            'min': float(np.min(ela_array))
        }
    
    def visualize_ela_heatmap(self, ela_array, output_path):
        """
        Create color heatmap visualization of ELA
        
        Args:
            ela_array (numpy.ndarray): ELA image array
            output_path (str): Path to save heatmap
        """
        # Convert to grayscale if needed
        if len(ela_array.shape) == 3:
            ela_gray = cv2.cvtColor(ela_array, cv2.COLOR_RGB2GRAY)
        else:
            ela_gray = ela_array
        
        # Apply colormap
        heatmap = cv2.applyColorMap(ela_gray, cv2.COLORMAP_JET)
        
        # Save heatmap
        cv2.imwrite(output_path, heatmap)
        

    
        return heatmap
