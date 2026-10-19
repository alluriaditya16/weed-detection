import torch
from weed_stage import get_weed_stage
from weed_control import weed_control_advice

# Load trained model
model = torch.hub.load(
    'ultralytics/yolov5',
    'custom',
    path='runs/train/maize_weed_v1/weights/best.pt',
    force_reload=True
)

def analyze_image(image_path):
    results = model(image_path)

    weed_boxes = []
    for *box, conf, cls in results.xyxy[0]:
        if int(cls) == 1:  # Weed class
            weed_boxes.append(box)

    stage = get_weed_stage(weed_boxes)
    advice = weed_control_advice(stage)

    return stage, advice
