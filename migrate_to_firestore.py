"""
Script to migrate experiences from experiences.json to Firebase Firestore
"""
import json
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Initialize Firebase Admin SDK
# Download your service account key from Firebase Console:
# Project Settings > Service Accounts > Generate New Private Key > Save as credentials.json
cred = credentials.Certificate('credentials.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

def migrate_experiences():
    """Load experiences from JSON and add to Firestore"""
    try:
        # Read the JSON file
        with open('experiences.json', 'r') as f:
            experiences = json.load(f)
        
        print(f"Found {len(experiences)} experiences to migrate")
        
        # Add each experience to Firestore
        for i, exp in enumerate(experiences, 1):
            doc_data = {
                'lat': exp['lat'],
                'lng': exp['lng'],
                'year': exp['year'],
                'month': exp['month'],
                'comment': exp['comment'],
                'likes': exp.get('likes', 0),
                'timestamp': datetime.now()
            }
            
            # Add to Firestore 'experiences' collection
            db.collection('experiences').add(doc_data)
            
            if i % 50 == 0:
                print(f"  ... migrated {i} experiences")
        
        print(f"✓ Successfully migrated all {len(experiences)} experiences to Firestore!")
        
    except FileNotFoundError:
        print("Error: experiences.json file not found")
    except json.JSONDecodeError:
        print("Error: experiences.json is not valid JSON")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    migrate_experiences()
