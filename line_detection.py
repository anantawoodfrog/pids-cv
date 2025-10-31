import cv2
import numpy as np
import pytesseract
from pytesseract import Output
import os
import json


class LineDetector:
    def __init__(self, image_path):
        self.image_path = image_path

    def image_preprocessing(self, image_path):
        print("In Image Preprocessing")
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        inverted= cv2.bitwise_not(thresh)   

        contours, _ = cv2.findContours(inverted, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            x,y,w,h = cv2.boundingRect(largest_contour)
            cropped = image[y:y+h, x:x+w]
        else:
            cropped = image.copy()

        #Removing "Text Regions"
        rgb = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
        data = pytesseract.image_to_data(rgb, output_type=Output.DICT)
        text_mask = np.zeros(cropped.shape[:2], dtype=np.uint8)

        for i, text in enumerate(data['text']):
            if text.strip():
                x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                cv2.rectangle(text_mask, (x, y), (x + w, y + h), 255, -1)

        #Dlating text mask to cover surrounding areas
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        text_mask = cv2.dilate(text_mask, kernel, iterations=2)

        #Removing text regions from cropped image
        no_text = cv2.inpaint(cropped, text_mask, 3, cv2.INPAINT_TELEA)

        #Removing "Symbol Regions"
        gray_nt = cv2.cvtColor(no_text, cv2.COLOR_BGR2GRAY)

        _, binary = cv2.threshold(gray_nt, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        contours, _  = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        symbol_mask = np.zeros(gray_nt.shape, dtype=np.uint8)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if 300 < area < 5000: 
                x, y, w, h = cv2.boundingRect(cnt)
                aspect_ratio = w / float(h)
                if 0.5 < aspect_ratio < 2:  
                    cv2.rectangle(symbol_mask, (x, y), (x + w, y + h), 255, -1)

        no_symbols = cv2.inpaint(no_text, symbol_mask, 3, cv2.INPAINT_TELEA)
        
        cleaned_image = no_symbols
        imagename = os.path.basename(image_path).split(".")[0]
        outputpath =f"{imagename}cleaned.png"
        cv2.imwrite(f"{imagename}_cropped.png", cropped)
        cv2.imwrite(f"{imagename}_no_text.png", no_text)
        # cv2.imwrite(f"{imagename}_symbol_mask.png", symbol_mask)
        cv2.imwrite(outputpath, cleaned_image)

        return outputpath
    
    def line_detection(image_path):
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        #Converting to gray scale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray,50, 200)

        #Detecting Lines using Probabilistic Hough Transform
        lines  = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=120, lines=np.array([]), minLineLength=100, maxLineGap=100)
        #Drawing detected lines on the Original image
        line_metadata = []
        for idx,line in enumerate(lines, start=1):
            x1,y1,x2,y2 = line[0]
            cv2.line(image,(x1,y1), (x2,y2), (255,0,0), 3)
            line_metadata.append({
                "line_id": f"L{idx}",
                "start_point": (int(x1), int(y1)),
                "end_point": (int(x2), int(y2))
            })
        imagename = os.path.basename(image_path).split(".")[0]
        outputpath = f"{imagename}_line_detected1.2.png"
        cv2.imwrite(outputpath, image)

        with open(f"{imagename}_line_metadata.json", "w") as f:
            json.dump(line_metadata, f, indent=4)
        return line_metadata
    
    def process(self):
        cleaned_image_path = self.image_preprocessing(self.image_path)
        line_metadata = self.line_detection(cleaned_image_path)
        return line_metadata