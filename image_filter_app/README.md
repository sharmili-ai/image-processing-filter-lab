# 🖼️ Image Processing Filter Visualization Lab

An interactive **Image Processing Filter Visualization Lab** developed using **Python, Streamlit, OpenCV, NumPy, Pandas, and Matplotlib**.

This application is designed to demonstrate fundamental image-processing operations in an interactive and easy-to-understand way. Users can upload an image, inspect its pixel values, convert it to grayscale, select different image-processing filters, visualize the corresponding kernels, apply the filters, and compare the processed results.

## 🚀 Live Demo

👉 **[Open the Streamlit App](YOUR_STREAMLIT_APP_LINK)**

---

## 📌 Project Overview

Image processing is an important area of computer vision that involves manipulating and analyzing digital images to enhance their quality, extract useful information, and identify important features.

This project provides an interactive interface for understanding how different spatial-domain image-processing filters operate on an input image.

The application provides information about:

- Input image
- Grayscale image
- Pixel values
- Filter kernels
- Filter operations
- Processed image
- Edge detection results
- Pixel-level calculations

The project is intended for **academic and laboratory learning purposes**.

---

## 🎯 Objectives

The main objectives of this project are:

1. To understand the fundamentals of digital image processing.
2. To convert color images into grayscale images.
3. To visualize image pixel values.
4. To understand spatial filtering operations.
5. To visualize different filter kernels.
6. To apply filters to images.
7. To understand edge detection techniques.
8. To compare the effects of different filters.
9. To provide an interactive learning environment using Streamlit.
10. To understand how convolution-based image processing works.

---

## ✨ Features

### 1. Image Upload
The application allows the user to upload an image through the Streamlit interface.

Supported image formats include:

- JPG
- JPEG
- PNG

### 2. Image Preview
After uploading an image, the application displays the original image for visualization and comparison.

### 3. Grayscale Conversion
The application converts the input RGB image into a grayscale image.

### 4. Pixel Matrix Visualization
The grayscale image can be represented as a matrix of pixel intensity values.

Each pixel contains an intensity value generally ranging from:

```text
0 → Black
255 → White
```

### 5. Pixel Inspection
The application provides pixel-level inspection functionality so users can examine individual pixel values and understand how filters affect surrounding pixels.

---

## 🔬 Image Processing Operators

The application demonstrates the following image-processing operators.

### 1. Mean Filter
The Mean Filter replaces each pixel with the average value of neighboring pixels.

Used for:
- Smoothing
- Noise reduction
- Blurring

### 2. Gaussian Filter
The Gaussian Filter performs smoothing using a Gaussian-weighted kernel.

Used for:
- Image smoothing
- Noise reduction
- Pre-processing before edge detection

### 3. Median Filter
The Median Filter replaces a pixel with the median value of its neighboring pixels.

Useful for:
- Salt-and-pepper noise removal
- Impulse noise removal

### 4. Sobel X Filter
The Sobel X operator detects intensity changes primarily in the horizontal direction and highlights vertical edges.

### 5. Sobel Y Filter
The Sobel Y operator detects intensity changes primarily in the vertical direction and highlights horizontal edges.

### 6. Sobel Magnitude
Sobel Magnitude combines the Sobel X and Sobel Y responses to represent overall edge strength.

### 7. Prewitt X Filter
The Prewitt X operator detects edges in one direction using a predefined convolution kernel.

### 8. Prewitt Y Filter
The Prewitt Y operator detects edges in the opposite spatial direction and highlights corresponding image boundaries.

### 9. Roberts Cross Operator
The Roberts Cross operator is an edge-detection technique that uses small kernels to detect rapid changes in image intensity. It is useful for detecting diagonal edges.

### 10. Laplacian Filter
The Laplacian filter is a second-order derivative operator used to detect rapid intensity changes.

Applications:
- Edge detection
- Image sharpening
- Feature extraction

### 11. Canny Edge Detection
Canny Edge Detection is a multi-stage edge detection technique used to identify strong and meaningful edges in an image.

The application allows threshold values to be adjusted for controlling the edge detection process.

---

## 🧮 Kernel Visualization

A major feature of this application is the ability to visualize the kernel associated with each filtering operation.

A kernel is a small matrix used to process an image by moving across its pixels.

Example of a simple smoothing kernel:

```text
1  1  1
1  1  1
1  1  1
```

The kernel is applied to neighboring pixels to calculate a new pixel value.

---

## 🔄 Application Workflow

```text
          Upload Image
                ↓
         Preview Image
                ↓
       Convert to Grayscale
                ↓
        Display Pixel Matrix
                ↓
        Select Image Filter
                ↓
        Display Filter Kernel
                ↓
          Apply Filter
                ↓
       Generate Processed Image
                ↓
      Inspect Pixel Calculations
                ↓
        Compare Input & Output
                ↓
         Download Result
```

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Core programming language |
| Streamlit | Interactive web interface |
| OpenCV | Image processing |
| NumPy | Numerical and matrix operations |
| Pandas | Pixel data handling |
| Matplotlib | Visualization |

---

## 📂 Project Structure

```text
image-processing-filter-lab/
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

### `app.py`
Contains the main Streamlit application and user interface.

### `kernels.py`
Contains image-processing kernels and filter-related operations.

### `utils.py`
Contains supporting utility functions used by the application.

### `requirements.txt`
Contains the Python packages required to run the project.

### `static/custom.css`
Contains custom styling for the Streamlit interface.

---

## ⚙️ Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/sharmili-ai/image-processing-filter-lab.git
```

Move into the project directory:

```bash
cd image-processing-filter-lab
```

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 3: Activate the Virtual Environment

#### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

#### Windows Command Prompt

```cmd
venv\Scripts\activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

Start the Streamlit application using:

```bash
python -m streamlit run app.py
```

After starting the application, Streamlit will provide a local URL.

Usually:

```text
http://localhost:8501
```

Open this URL in a web browser to access the application.

---

## 🖥️ Application Interface

The application provides an interactive interface containing:

- Image upload section
- Original image preview
- Grayscale conversion
- Pixel matrix display
- Filter selection
- Kernel visualization
- Filter output
- Pixel calculation details
- Download functionality

---

## 📊 Filter Comparison

| Filter | Main Purpose |
|--------|--------------|
| Mean | Smoothing and noise reduction |
| Gaussian | Smoothening with weighted averaging |
| Median | Salt-and-pepper noise removal |
| Sobel X | Edge detection |
| Sobel Y | Edge detection |
| Sobel Magnitude | Overall edge strength |
| Prewitt X | Edge detection |
| Prewitt Y | Edge detection |
| Roberts Cross | Diagonal edge detection |
| Laplacian | Second-order edge detection |
| Canny | Advanced edge detection |

---

## 🧪 Experimental Procedure

1. Launch the Streamlit application.
2. Upload an image.
3. Preview the uploaded image.
4. Convert the image to grayscale.
5. Examine the grayscale pixel matrix.
6. Select an image-processing filter.
7. View the corresponding kernel.
8. Apply the selected filter.
9. Observe the processed image.
10. Inspect pixel-level calculations.
11. Compare the original and processed images.
12. Download the resulting image if required.
13. Repeat the process with different filters.

---

## 📚 Learning Outcomes

After completing this project, the user can understand:

- Digital image representation
- RGB and grayscale images
- Pixel intensity values
- Image matrices
- Spatial filtering
- Convolution
- Smoothing filters
- Noise reduction
- Edge detection
- Image kernels
- Sobel operators
- Prewitt operators
- Roberts Cross operator
- Laplacian filtering
- Canny edge detection
- Interactive image-processing applications

---

## 🚀 Future Enhancements

The project can be extended with additional features such as:

- Histogram visualization
- Histogram equalization
- Thresholding
- Adaptive thresholding
- Morphological operations
- Erosion and dilation
- Image sharpening
- Contrast enhancement
- Color-space conversion
- Real-time webcam processing
- Side-by-side filter comparison
- Additional convolution kernels
- Batch image processing

---

## 🎓 Academic Use

This project can be used as an **Image Processing Laboratory assignment/project** to demonstrate practical implementation of spatial filtering and edge detection techniques.

It provides both theoretical understanding and practical visualization of image-processing operations.

---

## 📌 Conclusion

The **Image Processing Filter Visualization Lab** provides an interactive platform for studying fundamental image-processing techniques.

By combining Python, OpenCV, NumPy, Pandas, Matplotlib, and Streamlit, the application allows users to visualize image pixels, understand filtering kernels, apply different spatial filters, and observe their effects on an image.

The project demonstrates how fundamental image-processing concepts can be implemented and visualized through an interactive application.

---

## 👩‍💻 Author

**Sharmili**

**B.Tech Artificial Intelligence and Data Science**

---

## 📄 License

This project is developed for **educational and academic purposes**.
