# Image Processing Filter Visualization Lab

An interactive **Image Processing Filter Visualization Lab** built using **Python, Streamlit, OpenCV, NumPy, and Pandas**. The application allows users to upload an image, convert it to grayscale, inspect pixel values, select image-processing operators, visualize kernels, apply filters, and compare the results.

## Features

- Upload and preview an input image
- Convert RGB images to grayscale
- Display grayscale pixel values as a matrix
- Inspect individual pixel values
- Select and apply image-processing operators
- Visualize the kernel used by an operator
- Show step-by-step pixel/convolution calculations
- Compare original and processed images
- Download processed images
- Canny edge detection with adjustable thresholds
- Reset the application
- Error handling for invalid inputs

## Image Processing Operators

The application demonstrates the following operators:

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

## Technologies Used

- **Python**
- **Streamlit** – interactive web interface
- **OpenCV** – image processing and edge detection
- **NumPy** – numerical and pixel-level operations
- **Pandas** – pixel matrix/data handling
- **Matplotlib** – visualization

## Project Structure

```text
image-processing-filter-lab/
│
├── app.py
├── kernels.py
├── utils.py
├── requirements.txt
├── README.md
│
├── static/
│   └── custom.css
│
└── output/
    ├── original_input.png
    ├── grayscale.png
    ├── mean_filter.png
    ├── gaussian_filter.png
    ├── median_filter.png
    ├── sobel_x.png
    ├── sobel_y.png
    ├── sobel_magnitude.png
    ├── prewitt_x.png
    ├── prewitt_y.png
    ├── roberts_cross.png
    ├── laplacian.png
    └── canny_edge_detection.png
```

## Installation

Clone or download this repository.

Create and activate a virtual environment:

```bash
python -m venv venv
```

### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Run the Application

Start the Streamlit application using:

```bash
python -m streamlit run app.py
```

Then open the local URL displayed in the terminal, usually:

```text
http://localhost:8501
```

## Application Workflow

```text
Upload Image
     ↓
Preview Image
     ↓
Convert to Grayscale
     ↓
View Pixel Matrix
     ↓
Select Operator
     ↓
View Kernel / Algorithm
     ↓
Apply Filter
     ↓
View Output
     ↓
Inspect Pixel / Calculation
     ↓
Download Result
```

## Output Results

### Original Image
![Original Image](image_filter_app/image_processing_outputs_my_model/output/original_input.png)

### Grayscale
![Grayscale](image_filter_app/image_processing_outputs_my_model/output/grayscale.png)

### Mean Filter
![Mean Filter](image_filter_app/image_processing_outputs_my_model/output/mean_filter.png)

### Gaussian Filter
![Gaussian Filter](image_filter_app/image_processing_outputs_my_model/output/gaussian_filter.png)

### Median Filter
![Median Filter](image_filter_app/image_processing_outputs_my_model/output/median_filter.png)

### Sobel X
![Sobel X](image_filter_app/image_processing_outputs_my_model/output/sobel_x.png)

### Sobel Y
![Sobel Y](image_filter_app/image_processing_outputs_my_model/output/sobel_y.png)

### Sobel Magnitude
![Sobel Magnitude](image_filter_app/image_processing_outputs_my_model/output/sobel_magnitude.png)

### Prewitt X
![Prewitt X](image_filter_app/image_processing_outputs_my_model/output/prewitt_x.png)

### Prewitt Y
![Prewitt Y](image_filter_app/image_processing_outputs_my_model/output/prewitt_y.png)

### Roberts Cross
![Roberts Cross](image_filter_app/image_processing_outputs_my_model/output/roberts_cross.png)

### Laplacian
![Laplacian](image_filter_app/image_processing_outputs_my_model/output/laplacian.png)

### Canny Edge Detection
![Canny Edge Detection](image_filter_app/image_processing_outputs_my_model/output/canny_edge_detection.png)

## Result

The application provides a visual and interactive way to understand how different spatial-domain image-processing filters affect an image. It combines filter output visualization with kernel information and pixel-level analysis, making it suitable for an academic image-processing laboratory assignment.

## Author

**Sharmili**

B.Tech Artificial Intelligence and Data Science
