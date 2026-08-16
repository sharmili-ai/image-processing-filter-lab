# Image Processing Filter Visualization Lab

An interactive college-level Image Processing laboratory application built with **Python, Streamlit, OpenCV, NumPy, Pandas, and custom CSS**.

## Project Description

The application demonstrates the complete educational workflow:

**Upload Image → Original Image → Grayscale → Pixel Matrix → Select Operator → Kernel/Algorithm → Apply Operator → Processed Output → Pixel-Level Demonstration**

It is designed to show not only the final filtered image but also the underlying image-processing concepts.

## Features

- Upload PNG, JPG, and JPEG images
- Display original image and image information
- Convert the image to grayscale
- Display a configurable pixel matrix (5×5, 10×10, 20×20, 50×50)
- Select from 11 image-processing operators
- Display numerical kernels as tables
- Explain the definition, purpose, working principle, and result of each operator
- Apply filters without re-uploading the image
- Before/after comparison
- Pixel coordinate inspection
- Step-by-step pixel-level calculation
- Median sorting demonstration
- Sobel magnitude calculation
- Roberts Cross magnitude calculation
- Canny threshold controls
- PNG and JPG download
- Reset/Clear
- Modern dark educational interface
- Friendly error handling

## Supported Operators

1. Mean Filter
2. Gaussian Filter
3. Median Filter
4. Sobel X
5. Sobel Y
6. Sobel Magnitude
7. Prewitt X
8. Prewitt Y
9. Roberts Cross
10. Laplacian
11. Canny Edge Detection

## Technologies

- Python
- Streamlit
- OpenCV
- NumPy
- Pandas
- Matplotlib (included as an optional visualization dependency)
- Custom CSS

## Project Structure

```text
image_filter_app/
│
├── app.py
├── kernels.py
├── utils.py
├── requirements.txt
├── README.md
│
└── static/
    └── custom.css
```

## Installation

Open a terminal in the project folder.

```bash
python -m venv venv
```

### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution for the current session, use:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal.

## Example Workflow

1. Upload an image.
2. View its dimensions, channels, and original appearance.
3. Compare the original image with its grayscale version.
4. Inspect a selected portion of the grayscale pixel matrix.
5. Select an operator such as Sobel X.
6. Inspect the corresponding kernel.
7. Click **Apply Operator**.
8. Compare the grayscale input and processed output.
9. Select an interior pixel.
10. Open **Step-by-Step Pixel Convolution Demo**.
11. Inspect the neighborhood, kernel, products, sum, and calculated output.
12. Download the processed image as PNG or JPG.

## Educational Notes

### Mean Filter

Uses:

```text
1/9 ×
[ 1 1 1
  1 1 1
  1 1 1 ]
```

It smooths an image by averaging neighboring pixels.

### Gaussian Filter

Uses:

```text
1/16 ×
[ 1 2 1
  2 4 2
  1 2 1 ]
```

It performs weighted smoothing.

### Median Filter

Median filtering is not a normal convolution. It sorts the neighborhood values and selects the middle value.

### Sobel

Sobel X and Sobel Y estimate directional gradients. Sobel Magnitude combines them:

```text
G = sqrt(Gx² + Gy²)
```

### Prewitt

Prewitt X and Prewitt Y are directional gradient operators with simple 3×3 kernels.

### Roberts Cross

Uses two 2×2 kernels:

```text
Gx = [ 1  0
       0 -1 ]

Gy = [ 0  1
      -1  0 ]
```

### Laplacian

Uses a second-order derivative kernel:

```text
[ 0 -1  0
 -1  4 -1
  0 -1  0 ]
```

### Canny

Canny does not have one single standard kernel. It is a multi-stage edge detector:

```text
Gaussian Smoothing
        ↓
Gradient Calculation
        ↓
Non-Maximum Suppression
        ↓
Double Threshold
        ↓
Edge Tracking by Hysteresis
```

## Technical Correctness

- Processing starts from grayscale data.
- Signed gradient responses are calculated in floating point before visualization normalization.
- Gradient magnitudes are calculated before normalization.
- Borders are handled with reflected border conditions for kernel operations.
- Median filtering is treated separately from convolution.
- Canny is treated as a multi-stage algorithm rather than being assigned a fake kernel.
- Pixel-level demonstrations use actual pixel values from the uploaded image.
- Large matrices are limited to configurable visible portions to avoid browser overload.

## Requirements

Recommended Python version: **3.10–3.13**.

## Educational Purpose

This project is suitable for a college Image Processing laboratory, mini-project demonstration, viva, or practical record because it connects the visual output of a filter with the pixel-level mathematical operation that produces it.
