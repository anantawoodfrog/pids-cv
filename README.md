Text Metadata Extraction

This script extracts text from a PDF file along with its position (x, y, width, height) and the orientation angle of each detected text block.
It also creates an annotated image showing bounding boxes around detected text and saves everything in a JSON file.

What It Does

1. Converts PDF to Image:
The PDF is first converted into images using pdf2image.

2. Extracts Text Using Tesseract:
Tesseract OCR is used to detect text and get their bounding box coordinates.

3. Finds Text Orientation:
For each detected word, it calculates the text’s angle based on its bounding box.

4. Draws Bounding Boxes:
It highlights each detected text region in green on the image and labels it.

5. Saves Results:

Annotated image → annotated_output_test.png

Extracted data (text, coordinates, orientation) → extracted_text_orientation.json


Requirements

Make sure these libraries are installed:

 > pip install opencv-python pytesseract pdf2image


Also, you need:

- Tesseract OCR installed on your system

- Poppler installed (required by pdf2image)


How to Use

Put your PDF file in the same folder as this script.

Update the PDF path and run:
> Python
    obj = text_metadata_extraction("your_file.pdf")
    obj.extract_text_with_coordinates_orientation()


Once done, you’ll get:

1. The converted image

2. Annotated output

3. A JSON file with all text details

Code Logic

1. PDF to Image Conversion

The extract_image() method uses convert_from_path() to convert every page of the PDF into a .png image.

Each image is saved with the format filename_page_1.png, filename_page_2.png, etc.

2. Text Detection

The pytesseract.image_to_data() function extracts all words and their bounding boxes (x, y, width, height).

This helps in identifying where each word is located in the image.

3. Orientation Calculation

The function get_text_orientation_bbox3() takes the bounding box corners of a text.

It calculates edge lengths and finds the longest one — assuming it represents the direction of the text line.

Then it computes the angle using:

math.degrees(math.atan2(delta_y, delta_x))


which gives the text’s tilt in degrees.

4. Annotation

For every detected text, the script draws:

A green bounding box (cv2.rectangle)

The detected text label (cv2.putText)

5. Saving Outputs

Annotated image → saved as annotated_output_test.png


All text metadata (text, coordinates, angle) → stored in extracted_text_orientation.json

------------------------

# Image Preprocessing & Line Detection Script
Overview

This Python script performs image preprocessing and line detection on Piping and Instrumentation Diagram (P&ID) or similar engineering drawings.
It aims to:

Clean the image by removing unwanted elements such as text, symbols, and legends.

Detect lines in the cleaned image using the Probabilistic Hough Transform.

Dependencies

Make sure you have the following Python libraries installed:

pip install opencv-python pytesseract numpy

Input

Both functions take an image file path (.png, .jpg, etc.) as input.

Function	Input Parameter	Type	Description
image_preprocessing(image_path)	image_path	str	Path to the raw input image
line_detection(image_path)	image_path	str	Path to the cleaned image (output of preprocessing step)
Output
1. image_preprocessing(image_path)
Output	Type	Description
Returns	str	File path of the final cleaned image (*_cleaned.png)
Generates	.png files	Intermediate outputs for debugging and inspection
Saves	.png files	- *_cropped.png: Image after removing outer borders and legends.
- *_no_text.png: Image after text removal.
- *_cleaned.png: Final cleaned image after removing text and symbols.
2. line_detection(image_path)
Output	Type	Description
Returns	list[dict]	Metadata of detected lines with their start and end coordinates
Generates	.json file	*_line_metadata.json: Stores line coordinates and unique line IDs
Saves	.png file	*_line_detected1.2.png: Image with detected lines drawn in blue
Function Details
### image_preprocessing(image_path)

This function prepares the image for analysis by cleaning it step by step.

Steps & Logic:

Load and Grayscale Conversion

Reads the input image.

Converts it to grayscale for easier processing.

Noise Reduction & Thresholding

Applies Gaussian blur to reduce noise.

Uses Otsu’s thresholding to separate foreground from background.

Crop to Main Drawing

Finds the largest contour to crop the main drawing region and removes unnecessary white borders.

Legend Removal (Right Side)

Identifies and removes the right-side legend or notes area by checking mean pixel intensity.

Text Detection and Removal

Uses pytesseract to detect text regions.

Creates a text mask and dilates it to include surrounding pixels.

Uses inpainting (TELEA method) to remove text areas.

Symbol Detection and Removal

Thresholds and finds contours in the text-free image.

Detects shapes/symbols within a defined area and aspect ratio range.

Removes them using another inpainting process.

Save Outputs

Saves cropped, text-removed, and fully cleaned images for inspection.

Returns the final cleaned image path.

Example Output Files:
image_cropped.png
image_no_text.png
image_cleaned.png

### line_detection(image_path)

Detects straight lines in the cleaned image.

Steps & Logic:

Read and Convert to Grayscale

Loads the cleaned image and converts it to grayscale.

Edge Detection

Uses Canny edge detection to identify edges for line detection.

Line Detection

Applies Probabilistic Hough Line Transform to detect line segments.

Each detected line is assigned:

A unique line ID (L1, L2, …)

Start and end point coordinates.

Draw and Save

Draws the detected lines on the image.

Saves the annotated image and metadata as JSON.

Example Output:

image_line_metadata.json

[
    {
        "line_id": "L1",
        "start_point": [150, 320],
        "end_point": [480, 320]
    },
    {
        "line_id": "L2",
        "start_point": [200, 100],
        "end_point": [200, 400]
    }
]


image_line_detected1.2.png
→ Image with detected blue lines drawn over it.

Example Usage
# Step 1: Preprocess image
cleaned_image_path = image_preprocessing("diagram.png")

# Step 2: Detect lines on cleaned image
line_metadata = line_detection(cleaned_image_path)

print("Detected Lines Metadata:", line_metadata)
