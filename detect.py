import os
from pathlib import Path

def detect_victims(video_path):
    # YOLOv5 detection script
    weights = "yolov5/yolov5s.pt"  # Pre-trained weights
    output_dir = "runs/detect"  # Save output here

    # Run YOLOv5 detection
    os.system(f"python yolov5/detect.py --source {video_path} --weights {weights} --save-txt --project {output_dir}")

    # Check if results exist
    result_path = Path(output_dir) / "exp"
    if result_path.exists():
        print(f"Detection complete. Results saved in: {result_path}")
        return result_path
    else:
        print("Detection failed. Check your setup.")
        return None
