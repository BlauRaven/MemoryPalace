import csv
import json

def generate_experiences(csv_path="melbourne_cultural_dataset.csv", output_path="experiences.json"):
    experiences = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            experiences.append({
                "lat": float(row["latitude"]),
                "lng": float(row["longitude"]),
                "year": int(row["year"]),
                "comment": row["comment_message"],
            })
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(experiences, f)

if __name__ == "__main__":
    generate_experiences()
    print("experiences.json generated")
