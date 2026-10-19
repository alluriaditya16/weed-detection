def get_weed_stage(weed_boxes):
    """
    weed_boxes: list of [x1, y1, x2, y2]
    """
    if len(weed_boxes) == 0:
        return "No Weeds Detected"

    areas = []
    for box in weed_boxes:
        x1, y1, x2, y2 = box
        areas.append((x2 - x1) * (y2 - y1))

    avg_area = sum(areas) / len(areas)

    if avg_area < 1500:
        return "Early Stage"
    elif avg_area < 5000:
        return "Vegetative Stage"
    else:
        return "Mature Stage"
