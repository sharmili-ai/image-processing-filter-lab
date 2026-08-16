import io
import cv2
import numpy as np
import pandas as pd


def decode_uploaded_image(uploaded_file):
    data = uploaded_file.getvalue()
    if not data:
        raise ValueError("The uploaded file is empty.")
    array = np.frombuffer(data, dtype=np.uint8)
    image = cv2.imdecode(array, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("The file could not be decoded as a valid image.")
    return image


def bgr_to_rgb(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def to_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def matrix_dataframe(gray, size):
    h, w = gray.shape
    nrows = min(size, h)
    ncols = min(size, w)
    crop = gray[:nrows, :ncols]
    df = pd.DataFrame(crop)
    df.index.name = "Y"
    df.columns = [f"X={i}" for i in range(ncols)]
    return df


def normalize_to_uint8(image):
    image = np.asarray(image, dtype=np.float32)
    if image.size == 0:
        return np.zeros((1, 1), dtype=np.uint8)
    min_v = float(np.min(image))
    max_v = float(np.max(image))
    if max_v - min_v < 1e-12:
        if min_v > 0:
            return np.full(image.shape, np.clip(min_v, 0, 255), dtype=np.uint8)
        return np.zeros(image.shape, dtype=np.uint8)
    return cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)


def apply_operator(gray, operator, canny_low=50, canny_high=150):
    gray_f = gray.astype(np.float32)

    if operator == "Mean Filter":
        kernel = np.ones((3, 3), np.float32) / 9.0
        return cv2.filter2D(gray, -1, kernel, borderType=cv2.BORDER_REFLECT)

    if operator == "Gaussian Filter":
        return cv2.GaussianBlur(gray, (3, 3), 0, borderType=cv2.BORDER_REFLECT)

    if operator == "Median Filter":
        return cv2.medianBlur(gray, 3)

    if operator == "Sobel X":
        gx = cv2.Sobel(gray_f, cv2.CV_32F, 1, 0, ksize=3, borderType=cv2.BORDER_REFLECT)
        return normalize_to_uint8(np.abs(gx))

    if operator == "Sobel Y":
        gy = cv2.Sobel(gray_f, cv2.CV_32F, 0, 1, ksize=3, borderType=cv2.BORDER_REFLECT)
        return normalize_to_uint8(np.abs(gy))

    if operator == "Sobel Magnitude":
        gx = cv2.Sobel(gray_f, cv2.CV_32F, 1, 0, ksize=3, borderType=cv2.BORDER_REFLECT)
        gy = cv2.Sobel(gray_f, cv2.CV_32F, 0, 1, ksize=3, borderType=cv2.BORDER_REFLECT)
        magnitude = cv2.magnitude(gx, gy)
        return normalize_to_uint8(magnitude)

    if operator == "Prewitt X":
        kernel = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=np.float32)
        response = cv2.filter2D(gray_f, cv2.CV_32F, kernel, borderType=cv2.BORDER_REFLECT)
        return normalize_to_uint8(np.abs(response))

    if operator == "Prewitt Y":
        kernel = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]], dtype=np.float32)
        response = cv2.filter2D(gray_f, cv2.CV_32F, kernel, borderType=cv2.BORDER_REFLECT)
        return normalize_to_uint8(np.abs(response))

    if operator == "Roberts Cross":
        gx_kernel = np.array([[1, 0], [0, -1]], dtype=np.float32)
        gy_kernel = np.array([[0, 1], [-1, 0]], dtype=np.float32)
        gx = cv2.filter2D(gray_f, cv2.CV_32F, gx_kernel, borderType=cv2.BORDER_REFLECT)
        gy = cv2.filter2D(gray_f, cv2.CV_32F, gy_kernel, borderType=cv2.BORDER_REFLECT)
        magnitude = cv2.magnitude(gx, gy)
        return normalize_to_uint8(magnitude)

    if operator == "Laplacian":
        response = cv2.Laplacian(gray_f, cv2.CV_32F, ksize=3, borderType=cv2.BORDER_REFLECT)
        return normalize_to_uint8(np.abs(response))

    if operator == "Canny Edge Detection":
        if not (0 <= canny_low < canny_high <= 255):
            raise ValueError("Canny thresholds must satisfy 0 ≤ lower < upper ≤ 255.")
        return cv2.Canny(gray, int(canny_low), int(canny_high))

    raise ValueError(f"Unsupported operator: {operator}")


def get_kernel_for_demo(operator):
    from kernels import OPERATORS, ROBERTS_GX, ROBERTS_GY
    info = OPERATORS[operator]
    if info["kernel"] is not None:
        return info["kernel"]
    if operator == "Roberts Cross":
        return ROBERTS_GX
    return None


def get_pixel_neighborhood(gray, x, y, radius=1):
    h, w = gray.shape
    if not (0 <= x < w and 0 <= y < h):
        raise ValueError(f"Coordinates must be within x=0..{w-1}, y=0..{h-1}.")
    if x - radius < 0 or y - radius < 0 or x + radius >= w or y + radius >= h:
        raise ValueError(
            f"Pixel ({x}, {y}) is too close to an image boundary for a "
            f"{2*radius+1}×{2*radius+1} neighborhood. Choose an interior pixel."
        )
    return gray[y-radius:y+radius+1, x-radius:x+radius+1]


def convolution_demo(gray, x, y, operator):
    from kernels import OPERATORS, ROBERTS_GX, ROBERTS_GY

    if operator == "Median Filter":
        n = get_pixel_neighborhood(gray, x, y, 1)
        values = n.flatten().tolist()
        sorted_values = sorted(values)
        median = sorted_values[len(sorted_values)//2]
        return {
            "kind": "median",
            "neighborhood": n,
            "sorted_values": sorted_values,
            "result": median,
            "original": int(gray[y, x]),
        }

    if operator == "Canny Edge Detection":
        return {"kind": "canny", "original": int(gray[y, x])}

    if operator == "Sobel Magnitude":
        n = get_pixel_neighborhood(gray, x, y, 1).astype(np.float32)
        kx = OPERATORS["Sobel X"]["kernel"]
        ky = OPERATORS["Sobel Y"]["kernel"]
        gx_terms = n * kx
        gy_terms = n * ky
        gx = float(gx_terms.sum())
        gy = float(gy_terms.sum())
        magnitude = float(np.sqrt(gx * gx + gy * gy))
        return {
            "kind": "magnitude",
            "neighborhood": n,
            "gx_kernel": kx,
            "gy_kernel": ky,
            "gx_terms": gx_terms,
            "gy_terms": gy_terms,
            "gx": gx,
            "gy": gy,
            "result": magnitude,
            "original": int(gray[y, x]),
        }

    if operator == "Roberts Cross":
        n = get_pixel_neighborhood(gray, x, y, 1).astype(np.float32)
        # Demonstrate the upper-left 2×2 neighborhood for the Roberts kernels.
        n2 = n[:2, :2]
        gx_terms = n2 * ROBERTS_GX
        gy_terms = n2 * ROBERTS_GY
        gx = float(gx_terms.sum())
        gy = float(gy_terms.sum())
        magnitude = float(np.sqrt(gx * gx + gy * gy))
        return {
            "kind": "roberts",
            "neighborhood": n2,
            "gx_kernel": ROBERTS_GX,
            "gy_kernel": ROBERTS_GY,
            "gx_terms": gx_terms,
            "gy_terms": gy_terms,
            "gx": gx,
            "gy": gy,
            "result": magnitude,
            "original": int(gray[y, x]),
        }

    kernel = get_kernel_for_demo(operator)
    if kernel is None:
        raise ValueError("No single kernel is available for this operation.")

    size = kernel.shape[0]
    radius = size // 2
    n = get_pixel_neighborhood(gray, x, y, radius).astype(np.float32)
    terms = n * kernel
    total = float(terms.sum())
    return {
        "kind": "kernel",
        "neighborhood": n,
        "kernel": kernel,
        "terms": terms,
        "sum": total,
        "original": int(gray[y, x]),
    }


def image_to_png_bytes(image):
    ok, encoded = cv2.imencode(".png", image)
    if not ok:
        raise ValueError("Could not encode output as PNG.")
    return encoded.tobytes()


def image_to_jpg_bytes(image):
    ok, encoded = cv2.imencode(".jpg", image, [cv2.IMWRITE_JPEG_QUALITY, 95])
    if not ok:
        raise ValueError("Could not encode output as JPG.")
    return encoded.tobytes()


def format_matrix(matrix, decimals=3):
    arr = np.asarray(matrix)
    rows = []
    for row in arr:
        vals = []
        for value in row:
            if abs(float(value) - round(float(value))) < 1e-8:
                vals.append(str(int(round(float(value)))))
            else:
                vals.append(f"{float(value):.{decimals}f}")
        rows.append("[ " + "  ".join(vals) + " ]")
    return "\n".join(rows)


def format_expression(terms):
    pieces = []
    for value in np.asarray(terms).flatten():
        pieces.append(f"{float(value):.2f}")
    return " + ".join(pieces)
