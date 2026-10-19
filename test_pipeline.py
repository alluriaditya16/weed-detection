from pipeline import analyze_image

stage, advice = analyze_image("test.jpg")

print("Weed Stage:", stage)
print("Control Method:", advice["method"])
print("Reason:", advice["reason"])
print("Chemical:", advice["chemical"])
