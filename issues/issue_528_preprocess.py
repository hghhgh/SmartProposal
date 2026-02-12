import json

def load_raw_feedback(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def convert_to_training_format(raw_data):
    training_data = []

    for item in raw_data:
        training_data.append({
            "input": item["proposal_text"],
            "output": item["feedback"]
        })

    return training_data

def save_as_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    raw_data = load_raw_feedback("raw_feedback.json")
    training_data = convert_to_training_format(raw_data)
    save_as_json(training_data, "training_data.json")

    print("Training data generated successfully.")
