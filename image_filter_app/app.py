import os
import streamlit as st
import numpy as np
import cv2

from kernels import OPERATORS, ROBERTS_GX, ROBERTS_GY, CANNY_STAGES
from utils import (
    decode_uploaded_image,
    bgr_to_rgb,
    to_grayscale,
    matrix_dataframe,
    apply_operator,
    convolution_demo,
    image_to_png_bytes,
    image_to_jpg_bytes,
    format_matrix,
    format_expression,
)

st.set_page_config(
    page_title="Image Processing Filter Visualization Lab",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded",
)

css_path = os.path.join(os.path.dirname(__file__), "static", "custom.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f.read(), unsafe_allow_html=True)


def reset_app():
    for key in ["uploaded_name", "image_bgr", "gray", "processed", "processed_operator"]:
        st.session_state.pop(key, None)


def kernel_table(kernel):
    if kernel is None:
        return
    import pandas as pd
    arr = np.asarray(kernel)
    rows = []
    for row in arr:
        formatted = []
        for value in row:
            v = float(value)
            if abs(v - round(v)) < 1e-8:
                formatted.append(str(int(round(v))))
            else:
                formatted.append(f"{v:.4f}")
        rows.append(formatted)
    df = pd.DataFrame(rows, columns=[f"C{i+1}" for i in range(arr.shape[1])])
    st.dataframe(df, hide_index=True, use_container_width=True)


def show_matrix(name, matrix):
    st.markdown(f"**{name}**")
    st.code(format_matrix(matrix), language="text")


def display_kernel_visual(operator):
    info = OPERATORS[operator]
    st.markdown("### Kernel / Mathematical Operation")

    if operator == "Median Filter":
        st.info("Median filtering does not use a normal convolution kernel.")
        example = np.array([[12, 15, 18], [14, 255, 20], [16, 17, 19]])
        st.markdown("**Example neighborhood**")
        kernel_table(example)
        sorted_values = sorted(example.flatten().tolist())
        st.markdown(f"**Sorted values:** `{', '.join(map(str, sorted_values))}`")
        st.markdown("**Median:** `17`")
        return

    if operator == "Canny Edge Detection":
        st.info("Canny does not have one single standard convolution kernel.")
        for i, stage in enumerate(CANNY_STAGES, 1):
            st.markdown(f"**{i}. {stage}**")
        return

    if operator == "Sobel Magnitude":
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Sobel X — Gx**")
            kernel_table(OPERATORS["Sobel X"]["kernel"])
        with c2:
            st.markdown("**Sobel Y — Gy**")
            kernel_table(OPERATORS["Sobel Y"]["kernel"])
        st.latex(r"G = \sqrt{G_x^2 + G_y^2}")
        return

    if operator == "Roberts Cross":
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Roberts Gx**")
            kernel_table(ROBERTS_GX)
        with c2:
            st.markdown("**Roberts Gy**")
            kernel_table(ROBERTS_GY)
        st.latex(r"G = \sqrt{G_x^2 + G_y^2}")
        return

    kernel_table(info["kernel"])
    st.markdown(f"<div class='kernel-caption'>{info['kernel_label']}</div>", unsafe_allow_html=True)


def show_convolution_demo(gray, operator, x, y):
    st.markdown("### 🔍 Step-by-Step Pixel Convolution Demo")
    try:
        result = convolution_demo(gray, x, y, operator)
    except ValueError as e:
        st.warning(str(e))
        return

    st.write(f"**Coordinates:** ({x}, {y})")
    st.write(f"**Original pixel intensity:** {result['original']}")

    if result["kind"] == "canny":
        st.info(
            "Canny is a multi-stage algorithm rather than a single convolution. "
            "The selected pixel therefore cannot be represented by one kernel multiplication."
        )
        st.markdown("**Canny stages:**")
        for i, stage in enumerate(CANNY_STAGES, 1):
            st.write(f"{i}. {stage}")
        return

    if result["kind"] == "median":
        c1, c2 = st.columns(2)
        with c1:
            show_matrix("Step 2 — 3×3 Neighborhood", result["neighborhood"])
        with c2:
            st.markdown("**Step 3 — Sort the neighborhood**")
            st.code(", ".join(map(str, result["sorted_values"])), language="text")
            st.markdown(f"**Step 4 — Median = `{result['result']}`**")
        st.success(f"Final output value for the median calculation: {result['result']}")
        return

    if result["kind"] == "roberts":
        show_matrix("Step 2 — 2×2 Roberts Neighborhood", result["neighborhood"])
        c1, c2 = st.columns(2)
        with c1:
            show_matrix("Roberts Gx Kernel", result["gx_kernel"])
            show_matrix("Gx Element-wise Products", result["gx_terms"])
            st.code(f"Gx = {result['gx']:.3f}", language="text")
        with c2:
            show_matrix("Roberts Gy Kernel", result["gy_kernel"])
            show_matrix("Gy Element-wise Products", result["gy_terms"])
            st.code(f"Gy = {result['gy']:.3f}", language="text")
        st.latex(
            rf"G = \sqrt{{({result['gx']:.3f})^2 + ({result['gy']:.3f})^2}}"
            rf" = {result['result']:.3f}"
        )
        return

    if result["kind"] == "magnitude":
        show_matrix("Step 2 — 3×3 Neighborhood", result["neighborhood"])
        c1, c2 = st.columns(2)
        with c1:
            show_matrix("Sobel X Kernel", result["gx_kernel"])
            show_matrix("Gx Products", result["gx_terms"])
            st.code(f"Gx = {result['gx']:.3f}", language="text")
        with c2:
            show_matrix("Sobel Y Kernel", result["gy_kernel"])
            show_matrix("Gy Products", result["gy_terms"])
            st.code(f"Gy = {result['gy']:.3f}", language="text")
        st.latex(
            rf"G = \sqrt{{({result['gx']:.3f})^2 + ({result['gy']:.3f})^2}}"
            rf" = {result['result']:.3f}"
        )
        return

    show_matrix("Step 2 — Neighborhood", result["neighborhood"])
    show_matrix("Step 3 — Kernel", result["kernel"])
    show_matrix("Step 4 — Element-wise Products", result["terms"])
    expression = format_expression(result["terms"])
    st.markdown(f"**Step 5 — Sum:**")
    st.code(f"{expression} = {result['sum']:.3f}", language="text")
    st.success(
        f"Step 6 — Calculated output value: {result['sum']:.3f} "
        "(the displayed processed image may normalize signed edge responses for visualization)."
    )


# Header
st.markdown(
    """
<div class="hero">
    <h1>Image Processing Filter Visualization Lab</h1>
    <p>Explore Pixels • Kernels • Convolution • Edge Detection</p>
    <p>Upload an image, inspect its pixel representation, choose an operator,
    visualize its kernel or mathematical procedure, and observe the transformation.</p>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="workflow">
<span class="workflow-step">📤 Upload</span><span class="workflow-arrow">→</span>
<span class="workflow-step">🖼️ Original</span><span class="workflow-arrow">→</span>
<span class="workflow-step">⚫ Grayscale</span><span class="workflow-arrow">→</span>
<span class="workflow-step">🔢 Pixels</span><span class="workflow-arrow">→</span>
<span class="workflow-step">⚙️ Operator</span><span class="workflow-arrow">→</span>
<span class="workflow-step">🧮 Kernel</span><span class="workflow-arrow">→</span>
<span class="workflow-step">✨ Output</span><span class="workflow-arrow">→</span>
<span class="workflow-step">🔍 Pixel Demo</span>
</div>
""",
    unsafe_allow_html=True,
)

# Sidebar
with st.sidebar:
    st.markdown("## 🧪 Image Processing Lab")
    st.markdown(
        """
        **Navigation / Learning Path**

        📷 Upload Image  
        🔢 Pixel Matrix  
        ⚙️ Select Operator  
        🧮 Kernel / Algorithm  
        🖼️ Processed Output  
        🔍 Pixel Analysis
        """
    )
    st.divider()
    st.markdown("### Lab Information")
    st.markdown(
        """
        <span class="info-chip">11 Operators</span>
        <span class="info-chip">Streamlit</span>
        <span class="info-chip">OpenCV</span>
        <span class="info-chip">NumPy</span>
        """,
        unsafe_allow_html=True,
    )
    st.caption("Designed for college Image Processing laboratory learning.")
    if st.button("↺ Reset / Clear", use_container_width=True):
        reset_app()
        st.rerun()

# Upload
st.markdown("## 📤 1. Upload Image")
uploaded = st.file_uploader(
    "Choose a PNG, JPG, or JPEG image",
    type=["png", "jpg", "jpeg"],
    help="Upload a normal image for filtering and pixel-level analysis.",
)

if uploaded is None:
    st.info("⚠️ Please upload an image first. Supported formats: PNG, JPG, JPEG.")
    st.stop()

try:
    image_bgr = decode_uploaded_image(uploaded)
except ValueError as e:
    st.error(f"⚠️ {e}")
    st.stop()
except Exception:
    st.error("⚠️ The image could not be processed. Please upload a valid PNG/JPG/JPEG file.")
    st.stop()

gray = to_grayscale(image_bgr)
h, w = gray.shape
channels = 1 if image_bgr.ndim == 2 else image_bgr.shape[2]

st.session_state["uploaded_name"] = uploaded.name
st.session_state["image_bgr"] = image_bgr
st.session_state["gray"] = gray

# Image information
c1, c2, c3, c4 = st.columns(4)
c1.metric("Width", f"{w} px")
c2.metric("Height", f"{h} px")
c3.metric("Channels", channels)
c4.metric("Format", uploaded.name.split(".")[-1].upper())

st.caption(f"File: **{uploaded.name}**")

# Original + grayscale
st.markdown("## 🖼️ 2. Original & Grayscale")
c1, c2 = st.columns(2)
with c1:
    st.markdown("### Original Image")
    st.image(bgr_to_rgb(image_bgr), use_container_width=True)
with c2:
    st.markdown("### Grayscale Image")
    st.image(gray, use_container_width=True, clamp=True)
    st.caption("Grayscale represents each pixel using one intensity value from 0 (black) to 255 (white).")

# Pixel matrix
st.markdown("## 🔢 3. Pixel / Matrix Representation")
matrix_size = st.select_slider(
    "Displayed matrix size (selected top-left portion of the complete image)",
    options=[5, 10, 20, 50],
    value=10,
)
st.dataframe(
    matrix_dataframe(gray, matrix_size),
    use_container_width=True,
    height=min(650, 100 + matrix_size * 30),
)
st.caption(
    f"Showing at most {matrix_size} × {matrix_size} pixels from the top-left portion. "
    "The full image matrix is much larger."
)

# Operator
st.markdown("## ⚙️ 4. Select Image Processing Operator")
operator = st.selectbox(
    "Choose an operator",
    list(OPERATORS.keys()),
    index=0,
)

info = OPERATORS[operator]

if operator == "Canny Edge Detection":
    canny_low = st.slider("Lower Threshold", 0, 254, 50)
    canny_high = st.slider("Upper Threshold", canny_low + 1, 255, max(150, canny_low + 1))
else:
    canny_low, canny_high = 50, 150

# Selected operator information
st.markdown("## 🧮 5. Selected Operator")
st.markdown(f"<div class='operator-title'>{operator}</div>", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    st.markdown("### Definition / Purpose")
    st.write(info["purpose"])
    st.markdown("### Working Principle")
    st.write(info["working"])
with c2:
    st.markdown("### Result")
    st.write(info["result"])
    st.markdown("### Kernel / Algorithm")
    display_kernel_visual(operator)

# Apply
st.markdown("## ✨ 6. Apply Operator")
if st.button("▶ Apply Operator", use_container_width=True, type="primary"):
    try:
        processed = apply_operator(gray, operator, canny_low, canny_high)
        st.session_state["processed"] = processed
        st.session_state["processed_operator"] = operator
    except Exception as e:
        st.error(f"⚠️ Image processing failed: {e}")

processed = st.session_state.get("processed")
processed_operator = st.session_state.get("processed_operator")

if processed is not None:
    st.markdown("## 🖼️ 7. Before / After Comparison")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### Before Processing")
        st.image(gray, use_container_width=True, clamp=True)
    with c2:
        st.markdown(f"### After Processing — {processed_operator}")
        st.image(processed, use_container_width=True, clamp=True)

    kernel_size_text = "3 × 3"
    if processed_operator == "Roberts Cross":
        kernel_size_text = "2 × 2"
    elif processed_operator in ("Median Filter", "Canny Edge Detection", "Sobel Magnitude"):
        kernel_size_text = "3 × 3 / multi-stage"

    c1, c2, c3 = st.columns(3)
    c1.metric("Operator Applied", processed_operator)
    c2.metric("Kernel / Procedure", kernel_size_text)
    c3.metric("Output Type", "Edge Map" if processed_operator in {
        "Sobel X", "Sobel Y", "Sobel Magnitude", "Prewitt X",
        "Prewitt Y", "Roberts Cross", "Laplacian", "Canny Edge Detection"
    } else "Filtered Image")

    st.markdown("## 📥 8. Download Processed Image")
    d1, d2 = st.columns(2)
    with d1:
        st.download_button(
            "⬇ Download PNG",
            data=image_to_png_bytes(processed),
            file_name=f"{os.path.splitext(uploaded.name)[0]}_{processed_operator.lower().replace(' ', '_')}.png",
            mime="image/png",
            use_container_width=True,
        )
    with d2:
        st.download_button(
            "⬇ Download JPG",
            data=image_to_jpg_bytes(processed),
            file_name=f"{os.path.splitext(uploaded.name)[0]}_{processed_operator.lower().replace(' ', '_')}.jpg",
            mime="image/jpeg",
            use_container_width=True,
        )

# Pixel inspection
st.markdown("## 🔍 9. Pixel Inspection")
st.caption("Choose an interior pixel for a local neighborhood demonstration.")
px1, px2 = st.columns(2)
with px1:
    x = st.number_input("X coordinate", min_value=0, max_value=max(0, w - 1), value=min(w // 2, max(0, w - 1)), step=1)
with px2:
    y = st.number_input("Y coordinate", min_value=0, max_value=max(0, h - 1), value=min(h // 2, max(0, h - 1)), step=1)

x, y = int(x), int(y)
original_value = int(gray[y, x])

if processed is not None:
    processed_value = int(processed[y, x])
else:
    processed_value = None

c1, c2, c3 = st.columns(3)
c1.metric("Pixel Coordinates", f"({x}, {y})")
c2.metric("Original Intensity", original_value)
c3.metric("Processed Intensity", processed_value if processed_value is not None else "Apply filter")

if x in (0, w - 1) or y in (0, h - 1):
    st.warning("⚠️ This pixel is on an image boundary. A full neighborhood demonstration may not be available.")

with st.expander("🔍 Step-by-Step Pixel Convolution Demo", expanded=False):
    if operator == "Canny Edge Detection":
        show_convolution_demo(gray, operator, x, y)
    elif operator == "Median Filter":
        show_convolution_demo(gray, operator, x, y)
    else:
        show_convolution_demo(gray, operator, x, y)

# Educational summary
st.markdown("## 🎓 10. Learning Summary")
st.markdown(
    """
<div class="section-card">
<b>Input → Grayscale → Pixels → Kernel/Algorithm → Filter → Output</b><br><br>
The application is designed to make the image-processing pipeline visible:
you can see the actual grayscale intensities, inspect the selected operator,
follow the local pixel calculation, and compare the input with the processed result.
For signed gradient operators, the internal response is calculated before
normalization so negative gradients are not discarded prematurely.
</div>
""",
    unsafe_allow_html=True,
)

st.caption("Image Processing Filter Visualization Lab • Python + Streamlit + OpenCV + NumPy")
