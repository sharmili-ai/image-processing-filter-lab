import numpy as np

OPERATORS = {
    "Mean Filter": {
        "purpose": "Smooths the image by replacing each pixel with the average of its 3×3 neighborhood.",
        "working": "A 3×3 averaging kernel gives equal weight to every pixel in the neighborhood.",
        "result": "A smoother image with reduced small-scale intensity variations.",
        "kernel": np.ones((3, 3), dtype=np.float32) / 9.0,
        "kernel_label": "1/9 × [[1,1,1],[1,1,1],[1,1,1]]",
        "type": "kernel",
    },
    "Gaussian Filter": {
        "purpose": "Performs weighted smoothing, giving larger weights to pixels near the center.",
        "working": "A Gaussian-shaped 3×3 kernel performs weighted local averaging.",
        "result": "A smoother image with less high-frequency noise.",
        "kernel": np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]], dtype=np.float32) / 16.0,
        "kernel_label": "1/16 × [[1,2,1],[2,4,2],[1,2,1]]",
        "type": "kernel",
    },
    "Median Filter": {
        "purpose": "Reduces impulse (salt-and-pepper) noise while preserving many edges.",
        "working": "The center pixel is replaced by the median of the values in its 3×3 neighborhood.",
        "result": "A denoised image with less sensitivity to extreme outlier pixels.",
        "kernel": None,
        "kernel_label": "No convolution kernel — median operation",
        "type": "median",
    },
    "Sobel X": {
        "purpose": "Detects vertical edges using the horizontal intensity gradient.",
        "working": "Measures intensity change in the x direction using a weighted 3×3 gradient kernel.",
        "result": "Bright regions indicate strong vertical intensity changes.",
        "kernel": np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32),
        "kernel_label": "[[-1,0,1],[-2,0,2],[-1,0,1]]",
        "type": "gradient",
    },
    "Sobel Y": {
        "purpose": "Detects horizontal edges using the vertical intensity gradient.",
        "working": "Measures intensity change in the y direction using a weighted 3×3 gradient kernel.",
        "result": "Bright regions indicate strong horizontal intensity changes.",
        "kernel": np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float32),
        "kernel_label": "[[-1,-2,-1],[0,0,0],[1,2,1]]",
        "type": "gradient",
    },
    "Sobel Magnitude": {
        "purpose": "Combines horizontal and vertical Sobel gradients into one edge-strength image.",
        "working": "Computes G = sqrt(Gx² + Gy²) from the two Sobel responses.",
        "result": "Bright pixels represent stronger overall gradient magnitude.",
        "kernel": None,
        "kernel_label": "G = √(Gx² + Gy²) — uses Sobel X and Sobel Y",
        "type": "magnitude",
    },
    "Prewitt X": {
        "purpose": "Detects vertical edges using the Prewitt operator.",
        "working": "Computes the horizontal intensity gradient with equal vertical weights.",
        "result": "Bright regions indicate strong vertical intensity changes.",
        "kernel": np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=np.float32),
        "kernel_label": "[[-1,0,1],[-1,0,1],[-1,0,1]]",
        "type": "gradient",
    },
    "Prewitt Y": {
        "purpose": "Detects horizontal edges using the Prewitt operator.",
        "working": "Computes the vertical intensity gradient with equal horizontal weights.",
        "result": "Bright regions indicate strong horizontal intensity changes.",
        "kernel": np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]], dtype=np.float32),
        "kernel_label": "[[-1,-1,-1],[0,0,0],[1,1,1]]",
        "type": "gradient",
    },
    "Roberts Cross": {
        "purpose": "Detects diagonal intensity changes using compact 2×2 gradient kernels.",
        "working": "Computes two diagonal gradients and combines them as an edge magnitude.",
        "result": "A compact edge map emphasizing rapid diagonal changes.",
        "kernel": None,
        "kernel_label": "Gx = [[1,0],[0,-1]],  Gy = [[0,1],[-1,0]]",
        "type": "roberts",
    },
    "Laplacian": {
        "purpose": "Detects rapid changes in intensity and can emphasize fine image detail.",
        "working": "Applies a second-order derivative kernel to the grayscale image.",
        "result": "Bright regions represent strong second-order intensity changes.",
        "kernel": np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]], dtype=np.float32),
        "kernel_label": "[[0,-1,0],[-1,4,-1],[0,-1,0]]",
        "type": "gradient",
    },
    "Canny Edge Detection": {
        "purpose": "Detects edges using a multi-stage edge detection pipeline.",
        "working": "Gaussian smoothing → gradient calculation → non-maximum suppression → double threshold → hysteresis.",
        "result": "A binary edge map showing pixels identified as edges.",
        "kernel": None,
        "kernel_label": "No single standard kernel",
        "type": "canny",
    },
}

ROBERTS_GX = np.array([[1, 0], [0, -1]], dtype=np.float32)
ROBERTS_GY = np.array([[0, 1], [-1, 0]], dtype=np.float32)

CANNY_STAGES = [
    "Gaussian Smoothing",
    "Gradient Calculation",
    "Non-Maximum Suppression",
    "Double Threshold",
    "Edge Tracking by Hysteresis",
]
