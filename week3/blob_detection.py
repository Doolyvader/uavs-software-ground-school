import cv2
from pathlib import Path

# Path to this Week 3 folder
week3_dir = Path(__file__).parent

# Output folder
output_dir = week3_dir / "output"
output_dir.mkdir(exist_ok=True)

# Input image
image_path = week3_dir / "images" / "polka_dots_1.png"

# Read image
image = cv2.imread(str(image_path))

if image is None:
    raise FileNotFoundError(f"Could not load image: {image_path}")

print("Image shape:", image.shape)

# Convert BGR image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

print("Grayscale shape:", gray.shape)

# Save grayscale image for inspection
output_path = week3_dir / "output" / "polka_dots_1_gray.png"
cv2.imwrite(str(output_path), gray)

print("Saved grayscale image to:", output_path)

# Convert BGR image to HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Extract saturation channel
saturation = hsv[:, :, 1]

# Save saturation image for inspection
saturation_output_path = (
    week3_dir / "output" / "polka_dots_1_saturation.png"
)

cv2.imwrite(
    str(saturation_output_path),
    saturation
)

print(
    "Saved saturation image to:",
    saturation_output_path
)     

# Configure the blob detector
params = cv2.SimpleBlobDetector_Params()

# Filter blobs by area
params.filterByArea = True
params.minArea = 100
params.maxArea = 10000

# Filter blobs by circularity
params.filterByCircularity = True
params.minCircularity = 0.7

# Keep other filters off for the first test
params.filterByConvexity = False
params.filterByInertia = False
params.filterByColor = False

# Create detector
detector = cv2.SimpleBlobDetector_create(params)

# Detect blobs in the grayscale image
keypoints = detector.detect(gray)

hsv_params = cv2.SimpleBlobDetector_Params()

hsv_params.filterByArea = True
hsv_params.minArea = 100
hsv_params.maxArea = 10000

hsv_params.filterByCircularity = True
hsv_params.minCircularity = 0.7

hsv_params.filterByConvexity = False
hsv_params.filterByInertia = False

# In saturation, colored blobs are bright
hsv_params.filterByColor = True
hsv_params.blobColor = 255

hsv_detector = cv2.SimpleBlobDetector_create(hsv_params)

hsv_keypoints = hsv_detector.detect(saturation)

print("HSV/Saturation detected blobs:", len(hsv_keypoints))

hsv_detected_image = cv2.drawKeypoints(
    image,
    hsv_keypoints,
    None,
    flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
)

hsv_detection_output_path = (
    week3_dir / "output" / "polka_dots_1_hsv_detected.png"
)

cv2.imwrite(
    str(hsv_detection_output_path),
    hsv_detected_image
)

print(
    "Saved HSV detection result to:",
    hsv_detection_output_path
)

print("Detected blobs:", len(keypoints))

# Convert detections into measurements
for i, kp in enumerate(keypoints):
    x, y = kp.pt
    size = kp.size

    print(
        f"Blob {i}: x={x:.1f}, y={y:.1f}, size={size:.1f}"
    )


# Draw detected blobs on the original image
detected_image = cv2.drawKeypoints(
    image,
    keypoints,
    None,
    flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
)

# Save visualization
detection_output_path = (
    week3_dir / "output" / "polka_dots_1_detected.png"
)

cv2.imwrite(
    str(detection_output_path),
    detected_image
)

print("Saved detection result to:", detection_output_path)

# ============================================================
# Circularity sensitivity test
# ============================================================

print("\n===================================")
print("Circularity sensitivity test")
print("===================================")

circularity_values = [0.9, 0.7, 0.5]

for min_circularity in circularity_values:

    test_params = cv2.SimpleBlobDetector_Params()

    # Same area settings as before
    test_params.filterByArea = True
    test_params.minArea = 100
    test_params.maxArea = 10000

    # Change only circularity
    test_params.filterByCircularity = True
    test_params.minCircularity = min_circularity

    test_params.filterByConvexity = False
    test_params.filterByInertia = False

    # Colored blobs are bright in saturation channel
    test_params.filterByColor = True
    test_params.blobColor = 255

    # Create detector
    test_detector = cv2.SimpleBlobDetector_create(test_params)

    # Detect using HSV saturation image
    test_keypoints = test_detector.detect(saturation)

    print(
        f"minCircularity = {min_circularity}: "
        f"{len(test_keypoints)} blobs"
    )

    # Draw detections
    test_image = cv2.drawKeypoints(
        image,
        test_keypoints,
        None,
        flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
    )

    # Save separate image for each setting
    test_output_path = (
        output_dir
        / f"polka_dots_1_circularity_{min_circularity}.png"
    )

    cv2.imwrite(
        str(test_output_path),
        test_image
    )

print("===================================")