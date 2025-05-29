# Fingerprint OTP System

A secure authentication system that combines fingerprint verification with OTP (One-Time Password) delivery through WhatsApp. The system uses advanced computer vision techniques for fingerprint matching and provides a user-friendly interface for authentication.

## Features

- **Advanced Fingerprint Processing:**
  - CLAHE (Contrast Limited Adaptive Histogram Equalization) for image enhancement
  - SIFT (Scale-Invariant Feature Transform) for robust feature extraction
  - FLANN (Fast Library for Approximate Nearest Neighbors) for efficient matching
  - Adaptive thresholding for better ridge detection

- **Secure OTP System:**
  - WhatsApp-based OTP delivery
  - 5-minute OTP expiration
  - Secure template storage in JSON format

- **User Interface:**
  - Modern Tkinter-based GUI
  - Real-time status updates
  - Easy fingerprint image selection
  - Clear verification feedback

## Technologies Used

- **Core Technologies:**
  - Python 3.11
  - OpenCV 4.9.0 (cv2)
  - NumPy
  - Tkinter (GUI)

- **Fingerprint Processing:**
  - SIFT for feature extraction
  - FLANN for feature matching
  - CLAHE for image enhancement
  - Adaptive thresholding

- **OTP Delivery:**
  - pywhatkit for WhatsApp integration
  - Secure random number generation

## Prerequisites

- Python 3.7 or higher
- WhatsApp Web (for WhatsApp OTP)
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd fingerprint-otp-system
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up WhatsApp Web:
   - Open WhatsApp Web in your browser
   - Scan the QR code with your phone
   - Keep WhatsApp Web open while using the system

## Usage

1. Run the application:
```bash
python src/main.py
```

2. Using the system:
   - Enter your User ID
   - Provide your WhatsApp number (with country code)
   - Browse and select a fingerprint image
   - The system will send an OTP through WhatsApp
   - Enter the OTP to complete authentication

## Project Structure

```
fingerprint-otp-system/
├── config/
│   └── settings.py          # Configuration settings
├── data/
│   ├── datasets/           # Fingerprint datasets
│   └── templates.json      # Stored fingerprint templates
├── src/
│   ├── fingerprint.py      # Fingerprint processing and matching
│   ├── otp.py             # OTP generation and delivery
│   └── main.py            # Main application and GUI
├── requirements.txt        # Project dependencies
└── README.md              # Project documentation
```

## Implementation Details

### Fingerprint Matching Process
1. **Image Preprocessing:**
   - Grayscale conversion
   - CLAHE enhancement
   - Gaussian blur
   - Adaptive thresholding

2. **Feature Extraction:**
   - SIFT keypoint detection
   - Descriptor computation
   - Feature vector generation

3. **Matching Algorithm:**
   - FLANN-based feature matching
   - Ratio test for match filtering
   - Score calculation and threshold comparison

### Security Features
- Secure template storage using JSON
- NumPy arrays for efficient processing
- Type checking and validation
- Error handling and logging

## Troubleshooting

1. **WhatsApp OTP Issues:**
   - Ensure WhatsApp Web is open and logged in
   - Check your internet connection
   - Verify the phone number format (include country code)
   - Wait for the WhatsApp Web tab to open automatically

2. **Fingerprint Matching Issues:**
   - Ensure the fingerprint image is clear and well-lit
   - Try using a different fingerprint image
   - Check if the image format is supported (BMP, PNG, JPG)
   - Verify that the same finger is used for enrollment and verification

## Contributing

Feel free to submit issues and enhancement requests! 
