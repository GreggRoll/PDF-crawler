import fitz  # PyMuPDF
import cv2
import numpy as np
from skimage.metrics import structural_similarity as compare_ssim
from PIL import Image

def convert_pdf_to_images(pdf_path, dpi=300):
    doc = fitz.open(pdf_path)
    images = []
    for page in doc:
        pix = page.get_pixmap(dpi=dpi)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)
    doc.close()
    return images

def compare_images(image1, image2):
    # Convert images to grayscale
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # Calculate Structural Similarity Index (SSI)
    score, diff = compare_ssim(gray1, gray2, full=True)
    diff = (diff * 255).astype("uint8")

    # Thresholding to get binary image
    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    # Use morphological operations to clean up the noise
    kernel = np.ones((5,5),np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    return thresh

def overlay_differences(base_image, diff):
    # Find contours in the difference image
    contours, _ = cv2.findContours(diff, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Overlay semi-transparent boxes on the base image
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        
        # Create a yellow rectangle
        rectangle = np.full((h, w, 3), (255, 255, 0), dtype=np.uint8)

        # Blend the rectangle with the base image
        roi = base_image[y:y+h, x:x+w]
        cv2.addWeighted(rectangle, 0.5, roi, 0.5, 0, roi)

    return base_image


def highlight_differences(pdf1, pdf2, output_path):
    images1 = convert_pdf_to_images(pdf1)
    images2 = convert_pdf_to_images(pdf2)

    result_images = []
    min_len = min(len(images1), len(images2))

    for i in range(min_len):
        diff = compare_images(np.array(images1[i]), np.array(images2[i]))
        result_image = overlay_differences(np.array(images2[i]), diff)
        result_images.append(Image.fromarray(result_image))

    # Save as a single PDF
    result_images[0].save(output_path, "PDF", resolution=100.0, save_all=True, append_images=result_images[1:])

file1 = 'version1.0.pdf'
file2 = 'version1.1.pdf'
new_file_name = f"{file1[:-4]}-{file2[:-4]}_differences.pdf" #should come out to version1.0-version1.1_differences.pdf
highlight_differences(file1, file2, new_file_name)
