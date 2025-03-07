# Secret Message to Girlfriend 💌

This project uses **LSB Steganography** to hide secret messages in images. Using the Least Significant Bit (LSB) method, we can store text, images, or binary data inside an image without noticeable distortion.

## Features:
✅ Hide text messages in images  
✅ Extract hidden messages  
✅ Supports image and binary file steganography  
✅ Uses OpenCV for image processing  

## Installation:
First, install dependencies:
```bash
pip install -r requirements.txt
```

##Encoding a Secret Message:

```
python LSBSteg.py encode -i input.png -o output.png -f secret.txt

```

##Decoding a Secret Message:
```
python LSBSteg.py decode -i output.png -o extracted_secret.txt
```
