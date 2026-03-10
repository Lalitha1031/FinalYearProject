import cv2
import numpy as np
from skimage.feature import match_template
from scipy import ndimage

class ManipulationDetector:
    """
    Detects common image manipulation artifacts:
    - Noise inconsistencies
    - Clone/copy-move regions
    - Edge transitions
    - Color blending anomalies
    """
    
    def detect_artifacts(self, image_path, ela_array):
        """
        Perform comprehensive manipulation detection
        
        Args:
            image_path (str): Path to original image
            ela_array (numpy.ndarray): ELA output array
            
        Returns:
            dict: Detected manipulation indicators
        """
        # Load original image
        original = cv2.imread(image_path)
        
        results = {
            'noise_inconsistency': self._detect_noise_inconsistency(original),
            'cloning_detected': self._detect_cloning(original),
            'edge_anomalies': self._detect_edge_anomalies(original, ela_array),
            'color_blending': self._detect_color_blending(original)
        }
        
        return results
    
    def _detect_noise_inconsistency(self, image):
        """
        Detect inconsistent noise patterns across image regions
        Edited areas often have different noise characteristics
        
        Args:
            image (numpy.ndarray): Original image
            
        Returns:
            dict: Noise analysis results
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Divide into blocks and analyze noise
        block_size = 64
        h, w = gray.shape
        noise_levels = []
        
        for i in range(0, h - block_size, block_size):
            for j in range(0, w - block_size, block_size):
                block = gray[i:i+block_size, j:j+block_size]
                
                # Estimate noise using high-pass filter
                blurred = cv2.GaussianBlur(block, (5, 5), 0)
                noise = np.abs(block.astype(float) - blurred.astype(float))
                noise_level = np.std(noise)
                noise_levels.append(noise_level)
        
        if not noise_levels:
            return {'detected': False, 'score': 0.0}
        
        # Calculate variation in noise levels
        noise_variance = np.var(noise_levels)
        noise_std = np.std(noise_levels)
        
        # High variance indicates inconsistent noise (potential editing)
        detected = noise_variance > 50 or noise_std > 7
        
        return {
            'detected': bool(detected),
            'score': float(noise_variance),
            'description': 'Inconsistent noise patterns detected' if detected else 'Noise patterns appear uniform'
        }
    
    def _detect_cloning(self, image, block_size=32, threshold=0.9):
        """
        Detect copy-move/cloning artifacts
        Uses template matching to find duplicated regions
        
        Args:
            image (numpy.ndarray): Original image
            block_size (int): Size of blocks to compare
            threshold (float): Similarity threshold
            
        Returns:
            dict: Cloning detection results
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape
        
        # Reduce image size for faster processing
        scale_factor = 0.5
        small_gray = cv2.resize(gray, None, fx=scale_factor, fy=scale_factor)
        small_h, small_w = small_gray.shape
        small_block = int(block_size * scale_factor)
        
        # Sample blocks and check for matches
        matches_found = 0
        max_similarity = 0.0
        
        # Sample fewer blocks for performance
        step = small_block
        for i in range(0, small_h - small_block, step):
            for j in range(0, small_w - small_block, step):
                template = small_gray[i:i+small_block, j:j+small_block]
                
                # Skip if template is too uniform
                if np.std(template) < 10:
                    continue
                
                # Match template in the image
                result = match_template(small_gray, template)
                
                # Find peaks (excluding the template location itself)
                result[i:i+small_block, j:j+small_block] = 0
                max_val = np.max(result)
                
                if max_val > threshold:
                    matches_found += 1
                    max_similarity = max(max_similarity, max_val)
                
                # Early termination if cloning detected
                if matches_found > 0:
                    break
            
            if matches_found > 0:
                break
        
        detected = matches_found > 0
        
        return {
            'detected': bool(detected),
            'score': float(max_similarity),
            'description': 'Duplicated regions detected (copy-move)' if detected else 'No obvious cloning detected'
        }
    
    def _detect_edge_anomalies(self, image, ela_array):
        """
        Detect unnatural edge transitions
        Cut-paste operations create sharp boundaries
        
        Args:
            image (numpy.ndarray): Original image
            ela_array (numpy.ndarray): ELA output
            
        Returns:
            dict: Edge anomaly results
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detect edges using Canny
        edges = cv2.Canny(gray, 50, 150)
        
        # Convert ELA to grayscale if needed
        if len(ela_array.shape) == 3:
            ela_gray = cv2.cvtColor(ela_array, cv2.COLOR_RGB2GRAY)
        else:
            ela_gray = ela_array
        
        # Resize ELA to match edge image if needed
        if ela_gray.shape != edges.shape:
            ela_gray = cv2.resize(ela_gray, (edges.shape[1], edges.shape[0]))
        
        # Check ELA intensity at edge locations
        edge_ela_values = ela_gray[edges > 0]
        
        if len(edge_ela_values) > 0:
            edge_ela_mean = np.mean(edge_ela_values)
            edge_ela_std = np.std(edge_ela_values)
        else:
            edge_ela_mean = 0
            edge_ela_std = 0
        
        # High ELA values at edges indicate potential manipulation
        detected = edge_ela_mean > 30 or edge_ela_std > 25
        
        return {
            'detected': bool(detected),
            'score': float(edge_ela_mean),
            'description': 'Sharp edge transitions detected' if detected else 'Edge transitions appear natural'
        }
    
    def _detect_color_blending(self, image):
        """
        Detect color blending anomalies
        Pasted objects often have halo effects or color mismatches
        
        Args:
            image (numpy.ndarray): Original image
            
        Returns:
            dict: Color blending results
        """
        # Convert to LAB color space (better for perceptual differences)
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        
        # Split channels
        l_channel, a_channel, b_channel = cv2.split(lab)
        
        # Detect sudden color transitions using gradient
        grad_a = np.abs(cv2.Sobel(a_channel, cv2.CV_64F, 1, 0, ksize=3))
        grad_b = np.abs(cv2.Sobel(b_channel, cv2.CV_64F, 0, 1, ksize=3))
        
        # Calculate average gradient magnitude
        color_gradient = np.sqrt(grad_a**2 + grad_b**2)
        mean_gradient = np.mean(color_gradient)
        
        # High gradient indicates abrupt color changes
        detected = mean_gradient > 15
        
        return {
            'detected': bool(detected),
            'score': float(mean_gradient),
            'description': 'Color blending anomalies detected' if detected else 'Color transitions appear smooth'
        }
