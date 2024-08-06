import qrcode
from io import BytesIO

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
    img.save('test.png')
    return img

# import cv2
# from pyzbar import pyzbar
# import json

# def decode_qr_code(image_path):
#     # Load the image
#     image = cv2.imread(image_path)
    
#     # Decode the QR code
#     decoded_objects = pyzbar.decode(image)
    
#     for obj in decoded_objects:
#         # Print the decoded text
#         qr_data = obj.data.decode("utf-8")
#         print("Decoded QR Code Data:", qr_data)
        
#         # Parse the JSON data
#         try:
#             json_data = json.loads(qr_data)
#             print("Parsed JSON Data:", json_data)
#         except json.JSONDecodeError:
#             print("Error: Decoded data is not valid JSON")

# # Path to the image containing the QR code
# image_path = 'qrcode_json.png'
# decode_qr_code(image_path)


if __name__ == '__main__':
    print(generate_qr_code({'name': "Yoseph", 'order': 'done'}))