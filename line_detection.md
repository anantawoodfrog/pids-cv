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