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

Here's your Python program for **Secret Message to Girlfriend** using LSB Steganography. I'll provide the full implementation, including encoding and decoding functions, and a script to run it.

### Instructions:
1. **Encoding a Message**  
   ```bash
   python script.py encode input.png "I love you 💖" output.png
   ```
   This hides the message inside `input.png` and saves the result as `output.png`.

2. **Decoding a Message**  
   ```bash
   python script.py decode output.png
   ```
   This extracts the hidden message from `output.png`.

##Decoding a Secret Message:
```
python LSBSteg.py decode -i output.png -o extracted_secret.txt
```
