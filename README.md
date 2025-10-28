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