def weed_control_advice(stage):
    advice = {
        "Early Stage": {
            "method": "Manual removal or shallow hoeing",
            "reason": "Weeds are small and easy to remove",
            "chemical": "Not required"
        },
        "Vegetative Stage": {
            "method": "Mechanical weeding or selective herbicide",
            "reason": "Weeds start competing with maize",
            "chemical": "Atrazine (pre/post-emergence)"
        },
        "Mature Stage": {
            "method": "Targeted herbicide or uprooting",
            "reason": "High competition and seed production risk",
            "chemical": "Glyphosate (directed spray)"
        }
    }
    return advice.get(stage, "No recommendation available")
