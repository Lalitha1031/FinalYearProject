import numpy as np
import cv2
from scipy import stats

class StatisticalAnalyzer:
    """
    Statistical Feature Extractor for Forensic Analysis
    Analyzes ELA output to identify anomalies
    """
    
    def extract_features(self, ela_array):
        """
        Extract comprehensive statistical features from ELA image
        
        Args:
            ela_array (numpy.ndarray): ELA image array
            
        Returns:
            dict: Statistical features
        """
        # Convert to grayscale for analysis
        if len(ela_array.shape) == 3:
            ela_gray = cv2.cvtColor(ela_array, cv2.COLOR_RGB2GRAY)
        else:
            ela_gray = ela_array
        
        features = {}
        
        # Basic statistics
        features['mean_intensity'] = float(np.mean(ela_gray))
        features['std_deviation'] = float(np.std(ela_gray))
        features['variance'] = float(np.var(ela_gray))
        features['max_intensity'] = float(np.max(ela_gray))
        features['min_intensity'] = float(np.min(ela_gray))
        
        # Distribution statistics
        features['median'] = float(np.median(ela_gray))
        features['skewness'] = float(stats.skew(ela_gray.flatten()))
        features['kurtosis'] = float(stats.kurtosis(ela_gray.flatten()))
        
        # Percentile analysis
        features['percentile_75'] = float(np.percentile(ela_gray, 75))
        features['percentile_90'] = float(np.percentile(ela_gray, 90))
        features['percentile_95'] = float(np.percentile(ela_gray, 95))
        
        # High-intensity pixel ratio (potential tampering indicator)
        high_intensity_threshold = 50
        high_intensity_pixels = np.sum(ela_gray > high_intensity_threshold)
        total_pixels = ela_gray.size
        features['high_intensity_ratio'] = float(high_intensity_pixels / total_pixels)
        
        # Local variance (checks for inconsistent regions)
        features['local_variance'] = self._calculate_local_variance(ela_gray)
        
        # Edge intensity
        features['edge_intensity'] = self._calculate_edge_intensity(ela_gray)
        
        return features
    
    def _calculate_local_variance(self, image, block_size=16):
        """
        Calculate variance across local blocks
        High variance indicates inconsistent compression
        
        Args:
            image (numpy.ndarray): Grayscale ELA image
            block_size (int): Size of blocks for analysis
            
        Returns:
            float: Average local variance
        """
        h, w = image.shape
        variances = []
        
        for i in range(0, h - block_size, block_size):
            for j in range(0, w - block_size, block_size):
                block = image[i:i+block_size, j:j+block_size]
                variances.append(np.var(block))
        
        return float(np.mean(variances)) if variances else 0.0
    
    def _calculate_edge_intensity(self, image):
        """
        Calculate average edge intensity using Sobel operator
        
        Args:
            image (numpy.ndarray): Grayscale ELA image
            
        Returns:
            float: Average edge intensity
        """
        # Calculate gradients
        sobelx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
        
        # Calculate magnitude
        magnitude = np.sqrt(sobelx**2 + sobely**2)
        
        return float(np.mean(magnitude))
    
    def interpret_features(self, features):
        """
        Provide human-readable interpretation of features
        
        Args:
            features (dict): Statistical features
            
        Returns:
            dict: Interpretation results
        """
        interpretation = {
            'compression_anomaly': 'High' if features['mean_intensity'] > 15 else 'Low',
            'variance_level': 'High' if features['variance'] > 300 else 'Normal',
            'edge_artifacts': 'Detected' if features['edge_intensity'] > 20 else 'None',
            'intensity_distribution': 'Irregular' if features['high_intensity_ratio'] > 0.1 else 'Normal'
        }
        
        return interpretation
