import numpy as np

class ForensicClassifier:
    """
    Rule-based classifier for image forgery detection
    Combines statistical features and manipulation indicators
    """
    
    def __init__(self):
        """Initialize classifier with thresholds"""
        # Statistical thresholds
        self.thresholds = {
            'mean_intensity': 10.0,      # Changed from 15 → detects earlier
    'variance': 200.0,            # Changed from 300 → detects earlier
    'std_deviation': 12.0,        # Changed from 17 → detects earlier
    'high_intensity_ratio': 0.08, # Changed from 0.1 → detects earlier
    'edge_intensity': 15.0,       # Changed from 20 → detects earlier
    'local_variance': 70.0
        }
        
        # AI-generation indicators (for future enhancement)
        self.ai_indicators = {
            'texture_uniformity_threshold': 0.85,
            'frequency_anomaly_threshold': 0.7
        }
    
    def classify(self, statistical_features, manipulation_results):
        """
        Classify image based on statistical features and manipulation indicators
        
        Args:
            statistical_features (dict): Statistical features from ELA
            manipulation_results (dict): Manipulation detection results
            
        Returns:
            dict: Classification result with label, confidence, and explanation
        """
        # Count statistical anomalies
        stat_anomalies = self._count_statistical_anomalies(statistical_features)
        
        # Count manipulation indicators
        manip_count = self._count_manipulation_indicators(manipulation_results)
        
        # Calculate total anomaly score
        total_score = stat_anomalies + manip_count
        
        # Determine classification
        if total_score >= 3:
            label = "Manipulated/Edited"
            confidence = min(0.95, 0.70 + (total_score * 0.10))
        elif total_score == 2:
            label = "Likely Manipulated"
            confidence = 0.65
        elif total_score == 1:
            label = "Possibly Manipulated"
            confidence = 0.55
        else:
            label = "Authentic"
            confidence = 0.90
        
        # Generate explanation
        explanation = self._generate_explanation(
            stat_anomalies, 
            manipulation_results,
            statistical_features,
            label
        )
        
        return {
            'label': label,
            'confidence': round(confidence, 2),
            'explanation': explanation,
            'anomaly_count': total_score,
            'statistical_anomalies': stat_anomalies,
            'manipulation_indicators': manip_count
        }
    
    def _count_statistical_anomalies(self, features):
        """
        Count number of statistical features exceeding thresholds
        
        Args:
            features (dict): Statistical features
            
        Returns:
            int: Number of anomalies detected
        """
        count = 0
        
        if features['mean_intensity'] > self.thresholds['mean_intensity']:
            count += 1
        
        if features['variance'] > self.thresholds['variance']:
            count += 1
        
        if features['std_deviation'] > self.thresholds['std_deviation']:
            count += 1
        
        if features['high_intensity_ratio'] > self.thresholds['high_intensity_ratio']:
            count += 1
        
        if features['edge_intensity'] > self.thresholds['edge_intensity']:
            count += 1
        
        if features['local_variance'] > self.thresholds['local_variance']:
            count += 1
        
        return count
    
    def _count_manipulation_indicators(self, manipulation_results):
        """
        Count detected manipulation indicators
        
        Args:
            manipulation_results (dict): Manipulation detection results
            
        Returns:
            int: Number of manipulation indicators detected
        """
        count = 0
        
        if manipulation_results['noise_inconsistency']['detected']:
            count += 1
        
        if manipulation_results['cloning_detected']['detected']:
            count += 1
        
        if manipulation_results['edge_anomalies']['detected']:
            count += 1
        
        if manipulation_results['color_blending']['detected']:
            count += 1
        
        return count
    
    def _generate_explanation(self, stat_count, manip_results, features, label):
        """
        Generate human-readable explanation of classification
        
        Args:
            stat_count (int): Number of statistical anomalies
            manip_results (dict): Manipulation detection results
            features (dict): Statistical features
            label (str): Classification label
            
        Returns:
            str: Detailed explanation
        """
        explanation_parts = []
        
        # Header
        if label == "Authentic":
            explanation_parts.append("Analysis indicates this image is likely authentic.")
            explanation_parts.append("No significant compression inconsistencies or manipulation artifacts detected.")
        else:
            explanation_parts.append(f"Analysis indicates this image is {label.lower()}.")
        
        # Statistical findings
        if stat_count > 0:
            explanation_parts.append(f"\n**Statistical Analysis:** {stat_count} anomalies detected")
            
            if features['mean_intensity'] > self.thresholds['mean_intensity']:
                explanation_parts.append(f"- High compression inconsistency (ELA mean: {features['mean_intensity']:.2f})")
            
            if features['variance'] > self.thresholds['variance']:
                explanation_parts.append(f"- Irregular compression variance detected ({features['variance']:.2f})")
            
            if features['high_intensity_ratio'] > self.thresholds['high_intensity_ratio']:
                explanation_parts.append(f"- {features['high_intensity_ratio']*100:.1f}% of pixels show high error levels")
        
        # Manipulation findings
        manip_detected = []
        
        if manip_results['noise_inconsistency']['detected']:
            manip_detected.append("Noise inconsistency")
        
        if manip_results['cloning_detected']['detected']:
            manip_detected.append("Clone/copy-move regions")
        
        if manip_results['edge_anomalies']['detected']:
            manip_detected.append("Sharp edge transitions")
        
        if manip_results['color_blending']['detected']:
            manip_detected.append("Color blending anomalies")
        
        if manip_detected:
            explanation_parts.append(f"\n**Manipulation Indicators:** {', '.join(manip_detected)}")
        
        # Recommendations
        if label != "Authentic":
            explanation_parts.append("\n**Recommendation:** Further forensic examination recommended.")
        
        return "\n".join(explanation_parts)
    
    def classify_with_ai_detection(self, statistical_features, manipulation_results, ai_features=None):
        """
        Enhanced classification including AI-generated image detection
        (Placeholder for future neural forensic integration)
        
        Args:
            statistical_features (dict): Statistical features
            manipulation_results (dict): Manipulation results
            ai_features (dict, optional): Neural forensic features
            
        Returns:
            dict: Classification result
        """
        # Base classification
        base_result = self.classify(statistical_features, manipulation_results)
        
        # If AI features are provided, check for AI-generation indicators
        if ai_features:
            if ai_features.get('texture_uniformity', 0) > self.ai_indicators['texture_uniformity_threshold']:
                base_result['label'] = "AI-Generated"
                base_result['confidence'] = 0.75
                base_result['explanation'] += "\n\n**AI Detection:** High texture uniformity suggests possible AI generation."
        
        return base_result
