import pandas as pd
import random

# -------- CONFIG --------
N = 500

# Locations with real coordinates
locations = [
    {"name": "Federation Square", "lat": -37.817979, "lon": 144.969057},
    {"name": "Flinders Street Station", "lat": -37.818271, "lon": 144.967061},
    {"name": "Queen Victoria Market", "lat": -37.8076, "lon": 144.9568},
    {"name": "St Kilda Beach", "lat": -37.8676, "lon": 144.9806},
    {"name": "Royal Botanic Gardens", "lat": -37.8304, "lon": 144.9796},
    {"name": "Melbourne Central", "lat": -37.8102, "lon": 144.9623},
    {"name": "Chapel Street", "lat": -37.8430, "lon": 144.9930},
    {"name": "Hosier Lane", "lat": -37.8163, "lon": 144.9690},
    {"name": "Southbank Promenade", "lat": -37.8206, "lon": 144.9653},
    {"name": "Carlton Gardens", "lat": -37.8060, "lon": 144.9717}
]

# Cultural + memory-focused templates
cultural_food = [
    "I remember sharing traditional food here with friends, it felt like a celebration of culture",
    "The mix of cultural cuisines here reminds me of Melbourne’s diversity",
    "Tried a dish that reflected authentic heritage and family traditions",
    "The food here connects deeply to cultural roots and history",
    "Every meal here feels like experiencing a different culture"
]

memories = [
    "I used to come here as a child, it holds a lot of personal memories",
    "This place reminds me of family gatherings and special moments",
    "I have vivid memories of spending weekends here with loved ones",
    "Being here feels nostalgic, like revisiting an important part of my life",
    "This location has always been meaningful in my personal journey"
]

culture_general = [
    "You can really feel the cultural diversity and artistic energy here",
    "This place represents the multicultural identity of Melbourne",
    "There’s a strong sense of community and cultural expression here",
    "Art, music, and people come together to create a cultural hub",
    "It’s a place where different cultures blend seamlessly"
]

# Combine all comment pools
comment_pool = cultural_food + memories + culture_general

# -------- GENERATE DATA --------
data = []

for _ in range(N):
    loc = random.choice(locations)
    year = random.randint(2000, 2026)
    comment = random.choice(comment_pool)
    
    data.append({
        "latitude": loc["lat"],
        "longitude": loc["lon"],
        "year": year,
        "comment_message": comment
    })

# -------- CREATE DATAFRAME --------
df = pd.DataFrame(data)

# -------- SAVE CSV --------
df.to_csv("melbourne_cultural_dataset.csv", index=False)

print(df.head())
print(f"\nGenerated {len(df)} rows.")