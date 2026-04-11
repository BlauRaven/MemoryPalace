import csv
import json
import random

def generate_experiences(csv_path="melbourne_cultural_dataset.csv", output_path="experiences.json"):
    experiences = []
    
    # Read existing Melbourne dataset with month field
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            experiences.append({
                "lat": float(row["latitude"]),
                "lng": float(row["longitude"]),
                "year": int(row["year"]),
                "month": random.randint(1, 12),
                "comment": row["comment_message"],
            })
    
    # Add global experiences from various countries
    global_experiences = [
        # Japan
        {"lat": 35.6762, "lng": 139.6503, "year": 2019, "month": 4, "comment": "Witnessed a cherry blossom festival in Tokyo, felt timeless beauty"},
        {"lat": 34.6901, "lng": 135.1955, "year": 2018, "month": 7, "comment": "Collaborated with local artisans at a pottery workshop in Kyoto"},
        {"lat": 34.6901, "lng": 135.1955, "year": 2022, "month": 11, "comment": "Experienced zen gardens and traditional tea ceremony in Kyoto"},
        
        # Italy
        {"lat": 41.9028, "lng": 12.4964, "year": 2015, "month": 9, "comment": "Walking through Roman ruins at the Colosseum felt like stepping into history"},
        {"lat": 43.7696, "lng": 11.2558, "year": 2017, "month": 5, "comment": "Tasted authentic Tuscan wine and met generations of vintners"},
        {"lat": 45.4408, "lng": 12.3155, "year": 2019, "month": 6, "comment": "Gondola ride through Venice canals, pure magic"},
        
        # Mexico
        {"lat": 19.4326, "lng": -99.1332, "year": 2016, "month": 10, "comment": "Día de Muertos celebrations in Mexico City were spiritually profound"},
        {"lat": 20.6296, "lng": -87.0739, "year": 2018, "month": 3, "comment": "Explored Mayan ruins and met indigenous communities in Tulum"},
        
        # India
        {"lat": 28.6139, "lng": 77.2090, "year": 2014, "month": 12, "comment": "Diwali lights filled Delhi with warmth and unity"},
        {"lat": 19.0760, "lng": 72.8777, "year": 2020, "month": 2, "comment": "Street food markets in Mumbai pulse with energy and culture"},
        {"lat": 31.6340, "lng": 74.8711, "year": 2017, "month": 5, "comment": "Golden Temple in Amritsar provided spiritual sanctuary"},
        
        # Brazil
        {"lat": -22.9068, "lng": -43.1729, "year": 2019, "month": 2, "comment": "Rio Carnival danced into my heart forever"},
        {"lat": -23.5505, "lng": -46.6333, "year": 2018, "month": 8, "comment": "São Paulo's street art tells stories of resilience and hope"},
        
        # South Korea
        {"lat": 37.5665, "lng": 126.9780, "year": 2021, "month": 10, "comment": "Seoul's blend of ancient temples and modern technology mesmerized me"},
        {"lat": 35.1596, "lng": 129.0496, "year": 2019, "month": 7, "comment": "K-culture workshops in Busan connected me with passionate artists"},
        
        # Egypt
        {"lat": 30.0444, "lng": 31.2357, "year": 2015, "month": 11, "comment": "Standing before the pyramids awakened ancestral memories"},
        {"lat": 25.2854, "lng": 55.3604, "year": 2017, "month": 3, "comment": "Nile River cruises and Luxor temples were transcendent"},
        
        # Thailand
        {"lat": 13.7563, "lng": 100.5018, "year": 2016, "month": 4, "comment": "Songkran festival in Bangkok was joyful chaos and connection"},
        {"lat": 18.7883, "lng": 98.9853, "year": 2020, "month": 1, "comment": "Buddhist temples in Chiang Mai offered deep meditation experiences"},
        
        # Portugal
        {"lat": 38.7223, "lng": -9.1393, "year": 2018, "month": 9, "comment": "Lisbon's fado music stirred my soul with melancholy beauty"},
        {"lat": 41.1579, "lng": -8.6291, "year": 2019, "month": 6, "comment": "Porto's ancient streets and local wine bars felt like home"},
        
        # Turkey
        {"lat": 41.0082, "lng": 28.9784, "year": 2017, "month": 5, "comment": "Istanbul's bazaars were sensory feasts of color and spice"},
        {"lat": 37.8852, "lng": 27.2871, "year": 2019, "month": 8, "comment": "Ephesus ruins connected me to ancient philosophical traditions"},
        
        # Peru
        {"lat": -12.0464, "lng": -77.0428, "year": 2016, "month": 6, "comment": "Lima's food scene celebrates indigenous and global fusion"},
        {"lat": -13.1631, "lng": -72.5450, "year": 2018, "month": 9, "comment": "Machu Picchu trek deepened my respect for Incan heritage"},
        
        # Greece
        {"lat": 37.9838, "lng": 23.7275, "year": 2015, "month": 7, "comment": "Athens mythology came alive walking through ancient agoras"},
        {"lat": 36.4069, "lng": 25.4615, "year": 2017, "month": 8, "comment": "Santorini sunsets and local wine validated romantic notions"},
        
        # Morocco
        {"lat": 31.6295, "lng": -8.0088, "year": 2016, "month": 3, "comment": "Marrakech medinas were labyrinths of craft and tradition"},
        {"lat": 34.0209, "lng": -6.8416, "year": 2018, "month": 4, "comment": "Fes tanneries and artisanal leather work honored centuries-old methods"},
        
        # Vietnam
        {"lat": 21.0285, "lng": 105.8542, "year": 2017, "month": 2, "comment": "Hanoi's street food and motorbike chaos felt authentically alive"},
        {"lat": 10.7769, "lng": 106.6965, "year": 2019, "month": 12, "comment": "Ho Chi Minh City's history museums moved me deeply"},
        
        # Colombia
        {"lat": 4.7110, "lng": -74.0721, "year": 2018, "month": 7, "comment": "Bogotá's coffee culture and street art revival inspire resilience"},
        {"lat": 10.3932, "lng": -75.4830, "year": 2020, "month": 3, "comment": "Cartagena's colonial beauty and warm people left lasting impressions"},
        
        # Indonesia
        {"lat": -6.2088, "lng": 106.8456, "year": 2016, "month": 5, "comment": "Jakarta's diverse neighborhoods reflect multicultural harmony"},
        {"lat": -8.6705, "lng": 115.2126, "year": 2019, "month": 10, "comment": "Balinese temples and rice terraces explored spiritual dimensions"},
        
        # Philippines
        {"lat": 14.5994, "lng": 120.9842, "year": 2017, "month": 11, "comment": "Manila's vibrant street culture and bayanihan spirit uplifted me"},
        {"lat": 10.3157, "lng": 123.8854, "year": 2021, "month": 1, "comment": "Cebu's indigenous heritage workshops deepened cultural knowledge"},
        
        # South Africa
        {"lat": -33.9249, "lng": 18.4241, "year": 2015, "month": 10, "comment": "Cape Town's melting pot of African, Dutch, and global influences"},
        {"lat": -25.7482, "lng": 28.2293, "year": 2018, "month": 9, "comment": "Johannesburg townships taught lessons in community and survival"},
        
        # Canada
        {"lat": 43.2557, "lng": -79.8711, "year": 2016, "month": 8, "comment": "Niagara Falls reminded me of nature's overwhelming power"},
        {"lat": 49.2827, "lng": -123.1207, "year": 2017, "month": 7, "comment": "Vancouver's First Nations art honored indigenous perspectives"},
        
        # USA (non-local)
        {"lat": 40.7128, "lng": -74.0060, "year": 2014, "month": 5, "comment": "NYC's museums and street performances capture human creativity"},
        {"lat": 34.0522, "lng": -118.2437, "year": 2016, "month": 9, "comment": "LA's diverse neighborhoods span continents of culture"},
        {"lat": 41.8781, "lng": -87.6298, "year": 2018, "month": 6, "comment": "Chicago's architecture and blues clubs celebrate innovation"},
    ]
    
    experiences.extend(global_experiences)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(experiences, f)

if __name__ == "__main__":
    generate_experiences()
    print("experiences.json generated")
