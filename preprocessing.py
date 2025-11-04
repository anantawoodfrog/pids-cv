import cv2
import numpy as np

class Preprocessing:
    def __init__(self, image_path):
        self.image_path = image_path
        

    def image_prep_text_extrcation(self):
        image = cv2.imread(self.image_path)
        # 1. Coverting t o gray Scale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        #Contrast Stretching
        gray = cv2.normalize(gray, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)

        #Removing noise
        denoised = cv2.medianBlur(gray, 3)

        # Adaptive Thresholding
        binary = cv2.adaptiveThreshold(
            denoised, 
            255, 
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 
            31,  
            10   
        )
        #Small Noise Removal 
        kernel = np.ones((1, 1), np.uint8)
        cleaned = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
        
        preprocessed_path = self.image_path.replace(".png", "_preprocessed.png")
        cv2.imwrite(preprocessed_path, cleaned)
        return preprocessed_path
