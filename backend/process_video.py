import os
import uuid
import cv2
import subprocess

from detector import detect
from blur import blur_box


def process_video(input_path, output_dir, blur_style="Gaussian Blur"):

    os.makedirs(output_dir, exist_ok=True)

    cap = cv2.VideoCapture(input_path)

    if not cap.isOpened():
        raise Exception(f"Cannot open video:\n{input_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 30

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if width <= 0 or height <= 0:
        raise Exception("Invalid video size")

    print("=" * 60)
    print("Video Loaded")
    print("FPS:", fps)
    print("Width:", width)
    print("Height:", height)
    print("=" * 60)

    temp_name = f"{uuid.uuid4()}_temp.avi"
    temp_path = os.path.join(output_dir, temp_name)

    output_name = f"{uuid.uuid4()}.mp4"
    output_path = os.path.join(output_dir, output_name)

    fourcc = cv2.VideoWriter_fourcc(*"XVID")

    writer = cv2.VideoWriter(
        temp_path,
        fourcc,
        fps,
        (width, height)
    )

    if not writer.isOpened():
        raise Exception("Cannot create output video")

    frame_count = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        try:

            results = detect(frame)

            if results:

                for result in results:

                    if result.boxes is None:
                        continue

                    for box in result.boxes.xyxy.cpu().numpy():
                        frame = blur_box(frame, box)

        except Exception as e:
            print("Detection Error:", e)

        writer.write(frame)

        frame_count += 1

        if frame_count % 30 == 0:
            print(f"Processed {frame_count} frames")

    cap.release()
    writer.release()
    cv2.destroyAllWindows()

    print("\nConverting video to browser compatible MP4...\n")

    # -------------------------------------------------
    # FFMPEG PATH
    # -------------------------------------------------
    ffmpeg_path = os.path.join(
        os.path.dirname(__file__),
        "bin",
        "ffmpeg.exe"
    )

    print("FFmpeg Path :", ffmpeg_path)
    print("Exists      :", os.path.exists(ffmpeg_path))

    if not os.path.exists(ffmpeg_path):
        raise Exception(
            f"FFmpeg not found:\n{ffmpeg_path}\n\nCopy ffmpeg.exe into backend/bin"
        )

    command = [
        ffmpeg_path,
        "-y",
        "-i",
        temp_path,
        "-vcodec",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-acodec",
        "aac",
        output_path
    ]

    print("\nRunning FFmpeg...\n")

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    print("============== FFMPEG OUTPUT ==============")
    print(result.stdout)
    print(result.stderr)
    print("===========================================")

    if result.returncode != 0:
        raise Exception("FFmpeg conversion failed")

    if os.path.exists(temp_path):
        os.remove(temp_path)

    if not os.path.exists(output_path):
        raise Exception("Output video not created")

    size = os.path.getsize(output_path)

    print("=" * 60)
    print("Frames Written :", frame_count)
    print("Output File    :", output_path)
    print("File Size      :", size)
    print("=" * 60)

    return output_name