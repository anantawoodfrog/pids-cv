import cv2
import pytesseract
from pytesseract import Output
import os
import math
import json
from pdf2image import convert_from_path


class text_metadata_extraction:

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extract_image(self):
        print("In Extracting pdf content as image")
        images = convert_from_path(self.pdf_path, dpi=300)
        filename = os.path.basename(self.pdf_path).split(".")[0]
        for i, image in enumerate(images):
            image_path = f'{filename}_page_{i+1}.png'
            image.save(image_path, 'PNG')
        return image_path

    
    def get_text_orientation_bbox3(self,bbox):
        print("Inside getting oritentation")
        # Calculating Lenghts of edges
        edge_lengths = [
            math.hypot(bbox[i][0] - bbox[(i+1)%4][0], bbox[i][1] - bbox[(i+1)%4][1])
            for i in range(4)
        ]
        # Finding the longest edge which is main text direction
        max_edge_index = edge_lengths.index(max(edge_lengths))
        pt1 = bbox[max_edge_index]
        pt2 = bbox[(max_edge_index+1)%4]
        
        # getting angle across x-axis
        delta_x, delta_y = pt2[0] - pt1[0], pt2[1] - pt1[1]
        angle = math.degrees(math.atan2(delta_y, delta_x))
        return angle

    def extract_text_with_coordinates_orientation(self):
        print("In Text and Coordinate extraction")
        # ENsuring is file exists
        image_path = self.extract_image()
        if not os.path.isfile(image_path):
            print(f"Error: File '{image_path}' not found.")
            return []

        # Read the image
        image = cv2.imread(image_path)
        if image is None:
            print("Error: Unable to read the image. Check file format.")
            return []

        # Converting to RGB 
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Detecting and correct image rotation
        osd = pytesseract.image_to_osd(rgb_image)
        rotation_angle = int(osd.split("Rotate:")[1].split("\n")[0])
        print(f"Detected rotation angle: {rotation_angle}°")

        if rotation_angle != 0:
            (h, w) = rgb_image.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, -rotation_angle, 1.0)
            rgb_image = cv2.warpAffine(rgb_image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

        # Geting bounding boxes
        data = pytesseract.image_to_data(rgb_image, output_type=Output.DICT)


        results = []
        for i in range(len(data['text'])):
            text = data['text'][i].strip()
            # removing empty strings
            if text:  
                x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                # Defining bbox corners
                x1, y1 = x, y
                x2, y2 = x + w, y
                x3, y3 = x + w, y + h
                x4, y4 = x, y + h

                bbox = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
                angle = self.get_text_orientation_bbox3(bbox)
                results.append({
                    "text": text,
                    "coordinates": (x, y, w, h),
                    "orientation": angle
                })
                # Draw bounding boxes on the image
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

        # Save and display the annotated image
        output_path = "annotated_output_test.png"
        cv2.imwrite(output_path, image)
        print(f"Annotated image saved as '{output_path}'")

        with open('extracted_text_orientation.json', 'w') as f:
            json.dump(results, f, indent=4)
        print(f"JSON file saved as '{output_path}'")

        return results

