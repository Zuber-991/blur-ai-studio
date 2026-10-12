import cv2


def blur_box(frame, box):
    """
    Apply Gaussian blur to a detected bounding box.
    """

    try:
        x1, y1, x2, y2 = map(int, box)

        h, w = frame.shape[:2]

        # Keep coordinates inside the frame
        x1 = max(0, min(x1, w - 1))
        y1 = max(0, min(y1, h - 1))
        x2 = max(0, min(x2, w))
        y2 = max(0, min(y2, h))

        # Invalid box
        if x2 <= x1 or y2 <= y1:
            return frame

        roi = frame[y1:y2, x1:x2]

        if roi.size == 0:
            return frame

        # Kernel size must be odd
        blurred = cv2.GaussianBlur(
            roi,
            (51, 51),
            30
        )

        frame[y1:y2, x1:x2] = blurred

        return frame

    except Exception as e:
        print("Blur Error:", e)
        return frame