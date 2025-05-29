import cv2
import numpy as np
import os
import json

class FingerprintProcessor:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.template_db = {}
        self.match_threshold = 0.5  # Further lowered threshold
        self.load_templates()
        
    def load_templates(self):
        """Load fingerprint templates from file and convert descriptors back to numpy arrays"""
        template_path = os.path.join(self.data_dir, 'templates.json')
        if os.path.exists(template_path):
            try:
                with open(template_path, 'r') as f:
                    loaded_data = json.load(f)
                    self.template_db = {}
                    for user_id, template_list in loaded_data.items():
                        # Ensure template_list is not None and is a list before converting
                        if isinstance(template_list, list) and template_list:
                            self.template_db[user_id] = np.array(template_list, dtype=np.float32)
                        else:
                            self.template_db[user_id] = None # Store None if data is invalid or empty list
                print("Templates loaded successfully.")
            except Exception as e:
                print(f"Error loading templates: {e}")
                self.template_db = {}
        else:
            print(f"No templates file found at {template_path}.") # Debugging print
                
    def save_templates(self):
        """Save fingerprint templates to file (convert numpy arrays to lists)"""
        # Ensure data directory exists before saving
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            print(f"Created data directory at {self.data_dir}") # Debugging print
            
        template_path = os.path.join(self.data_dir, 'templates.json')
        try:
            with open(template_path, 'w') as f:
                # Convert numpy array descriptors to list for JSON serialization
                serializable_template_db = {}
                for user_id, template in self.template_db.items():
                    if template is not None:
                        # Ensure it's a numpy array before converting to list
                        if isinstance(template, np.ndarray):
                             serializable_template_db[user_id] = template.tolist()
                        else:
                             # If somehow not a numpy array, store as None or handle appropriately
                             serializable_template_db[user_id] = None 
                             print(f"Warning: Template for user {user_id} is not a numpy array before saving.")
                    else:
                        serializable_template_db[user_id] = None
                        
                json.dump(serializable_template_db, f, indent=4)
            print("Templates saved successfully.")
        except Exception as e:
            print(f"Error saving templates: {e}")
            
    def preprocess_fingerprint(self, image):
        """Preprocess fingerprint image for better matching"""
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
        # Apply CLAHE
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(image)
        
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(enhanced, (5, 5), 0)
        
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY, 11, 2)
        
        return thresh
        
    def extract_features(self, image):
        """Extract fingerprint features using SIFT"""
        # Ensure image is in correct format (CV_8U) for SIFT
        if image is None:
            print("Warning: Input image for feature extraction is None.")
            return None, None

        if image.dtype != np.uint8:
            image = image.astype(np.uint8)
            
        sift = cv2.SIFT_create()
        keypoints, descriptors = sift.detectAndCompute(image, None)
        
        # Return descriptors as float32 numpy array
        return keypoints, descriptors.astype(np.float32) if descriptors is not None else None
        
    def match_fingerprints(self, template1, template2):
        """Match two fingerprint templates"""
        if template1 is None or template2 is None:
            print("Warning: One of the templates is None for matching.")
            return 0
            
        # template1 is from the current image (already float32 from extract_features)
        # template2 is the stored one (should be float32 numpy array from load_templates)

        # Use FLANN matcher
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        
        try:
            # Ensure there are enough descriptors to match (SIFT usually needs at least 2)
            if template1.shape[0] < 2 or template2.shape[0] < 2:
                 print(f"Warning: Not enough descriptors for matching. Template1 count: {template1.shape[0]}, Template2 count: {template2.shape[0]}")
                 return 0

            matches = flann.knnMatch(template1, template2, k=2)
            
            # Apply ratio test
            good_matches = []
            # Ensure match has at least 2 results before ratio test
            if len(matches) > 0 and len(matches[0]) == 2:
                 for m, n in matches:
                    if m.distance < 0.75 * n.distance:
                        good_matches.append(m)
            else:
                 print("Warning: knnMatch returned fewer than 2 matches, skipping ratio test.")

            # Calculate match score
            # Avoid division by zero if one template has no descriptors (though checked above)
            max_len = max(template1.shape[0], template2.shape[0])
            if max_len == 0:
                return 0
            match_score = len(good_matches) / max_len
            print(f"Calculated Match Score: {match_score}")
            return match_score
        except Exception as e:
            print(f"Error during matching: {e}")
            return 0
            
    def process_image(self, image_path):
        """Process a fingerprint image and return features"""
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Could not read image from {image_path}")
            return None, None
            
        processed = self.preprocess_fingerprint(image)
        return self.extract_features(processed)
        
    def store_template(self, user_id, descriptors):
        """Store fingerprint template for a user"""
        # Ensure descriptors is a numpy array before storing
        if descriptors is not None and isinstance(descriptors, np.ndarray):
            self.template_db[user_id] = descriptors
            self.save_templates()
        else:
            self.template_db[user_id] = None # Store None if descriptors are invalid
            print(f"Warning: Attempted to store invalid descriptors for user {user_id}")

        
    def verify_fingerprint(self, user_id, image_path):
        """Verify a fingerprint against stored template"""
        if user_id not in self.template_db or self.template_db[user_id] is None:
            print(f"Error: No template found for user {user_id}")
            return False
            
        keypoints, descriptors = self.process_image(image_path)
        if descriptors is None:
            print(f"Error: Could not extract descriptors from verification image {image_path}")
            return False
            
        # Retrieve stored template (should be a numpy array)
        stored_template = self.template_db[user_id]

        # Double-check if stored_template is indeed a numpy array before matching
        if not isinstance(stored_template, np.ndarray):
             print(f"Error: Stored template for user {user_id} is not a numpy array, it is {type(stored_template)}.")
             # Attempt to convert here as a fallback, though it should be handled in load_templates
             if isinstance(stored_template, list):
                  print("Attempting fallback conversion from list to numpy array...")
                  stored_template = np.array(stored_template, dtype=np.float32)
                  # Update the template in the db to prevent future errors?
                  self.template_db[user_id] = stored_template
             else:
                 return False # Cannot proceed if template is not a valid type

        # Ensure both descriptors are float32 and numpy arrays before passing to match_fingerprints
        if descriptors.dtype != np.float32:
             descriptors = descriptors.astype(np.float32)
             print("Warning: Descriptors from current image not float32, converting.")
             
        if stored_template.dtype != np.float32:
             stored_template = stored_template.astype(np.float32)
             print("Warning: Stored template not float32, converting.")


        match_score = self.match_fingerprints(descriptors, stored_template)
        
        # Check if the match score exceeds the threshold
        is_match = match_score > self.match_threshold
        print(f"Verification result for user {user_id} (Image: {os.path.basename(image_path)}) - Score: {match_score}, Threshold: {self.match_threshold}, Match: {is_match}")
        
        return is_match 