import cv2
import os
import qrcode
from io import BytesIO
from pyzbar import pyzbar
import json
from ExpressYourself.settings import BASE_DIR

def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer)
    return buffer



def decode_qr_code(image_path):
    # Load the image
    image = cv2.imread(image_path)
    
    # Decode the QR code
    decoded_objects = pyzbar.decode(image)
    
    for obj in decoded_objects:
        # Print the decoded text
        qr_data = obj.data.decode("utf-8")

    return qr_data
