Overview

This module provides a preprocessing pipeline designed to enhance image quality for accurate text extraction OCR.

OCR systems, perform best on images with high contrast, minimal noise, and well-defined text boundaries.
This function optimizes the image for those conditions by applying a sequence of OpenCV-based transformations.

Function Definition
def image_prep_text_extrcation(image_path):
    image = cv2.imread(image_path)

    # 1. Convert to Grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 2. Contrast Stretching
    gray = cv2.normalize(gray, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)

    # 3. Denoising
    denoised = cv2.medianBlur(gray, 3)

    # 4. Adaptive Thresholding
    binary = cv2.adaptiveThreshold(
        denoised, 
        255, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 
        31,  
        10   
    )

    # 5. Small Noise Removal
    kernel = np.ones((1, 1), np.uint8)
    cleaned = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    
    # 6. Save and Return Preprocessed Image Path
    preprocessed_path = image_path.replace(".png", "_preprocessed.png")
    cv2.imwrite(preprocessed_path, cleaned)
    return preprocessed_path

Step-by-Step Explanation
1. Convert to Grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


Reduces the image to a single intensity channel.

Simplifies the image for text recognition by removing color information.

Makes further image enhancement operations computationally efficient.

2. Contrast Stretching
gray = cv2.normalize(gray, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)


Improves visibility of text against the background.

Expands the pixel intensity range to cover the full 0–255 scale.

Helps Azure OCR detect faint or low-contrast text.

3. Denoising
denoised = cv2.medianBlur(gray, 3)


Removes salt-and-pepper noise while preserving edges (important for text).

Median filtering is ideal for documents and scanned images where fine lines should remain sharp.

4. Adaptive Thresholding
binary = cv2.adaptiveThreshold(
    denoised, 
    255, 
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
    cv2.THRESH_BINARY, 
    31,  
    10
)


Converts the image into a binary format (black text on white background).

Adaptive thresholding dynamically adjusts the threshold for different regions, making it robust for images with uneven lighting or shadows.

cv2.ADAPTIVE_THRESH_GAUSSIAN_C uses a weighted mean for local regions, improving text clarity.

5. Small Noise Removal
kernel = np.ones((1, 1), np.uint8)
cleaned = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)


Performs morphological opening (erosion followed by dilation).

Removes isolated white noise or artifacts not part of the text.

Ensures cleaner text edges for better OCR segmentation.

6. Save Preprocessed Image
preprocessed_path = image_path.replace(".png", "_preprocessed.png")
cv2.imwrite(preprocessed_path, cleaned)
return preprocessed_path


Saves the preprocessed image with a _preprocessed suffix.

Returns the new path for direct use with Azure OCR or any other text extraction pipeline.


Benefits 
| Step                       | Enhancement                          | Benefit to OCR                    |
| -------------------------- | ------------------------------------ | --------------------------------- |
| **Grayscale Conversion**   | Simplifies image                     | Reduces processing complexity     |
| **Contrast Stretching**    | Increases text-background separation | Improves OCR text segmentation    |
| **Median Blur**            | Reduces noise while preserving edges | Avoids false character detections |
| **Adaptive Threshold**     | Handles uneven lighting              | Improves binarization accuracy    |
| **Morphological Cleaning** | Removes specks and distortions       | Produces cleaner text shapes      |


Dependencies

Python 3.x

OpenCV (cv2)

NumPy

Install via:

pip install opencv-python-headless numpy

Notes

The preprocessing works best for scanned documents, invoices, forms, or P&ID drawings where text clarity varies.

Adjust adaptive threshold parameters (blockSize, C) for specific document types if needed.

Supports .png, .jpg, and .jpeg images (you can modify the file extension replacement logic accordingly).