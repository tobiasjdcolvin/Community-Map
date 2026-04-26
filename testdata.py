import database as db
import random

# A list of tuples, containing cities, states, and countries from around the world to be used for testing the database functions
# (States are optional, but should be included for US/Canadian cities to ensure accurate geocoding results from the Nominatim API)
test_cities = [
    ("Pukalani", "HI", "US"),
    ("Honolulu", "HI", "US"),
    ("Seattle", "WA", "US"),
    ("New York", "NY", "US"),
    ("Los Angeles", "CA", "US"),
    ("Chicago", "IL", "US"),
    ("Houston", "TX", "US"),
    ("Phoenix", "AZ", "US"),
    ("Philadelphia", "PA", "US"),
    ("San Antonio", "TX", "US"),
    ("San Diego", "CA", "US"),
    ("Dallas", "TX", "US"),
    ("San Jose", "CA", "US"),
    ("Austin", "TX", "US"),
    ("Jacksonville", "FL", "US"),
    ("Fort Worth", "TX", "US"),
    ("Columbus", "OH", "US"),
    ("Charlotte", "NC", "US"),
    ("San Francisco", "CA", "US"),
    ("Indianapolis", "IN", "US"),
    ("Tokyo", "", "Japan"),
    ("London", "", "UK"),
    ("Paris", "", "France"),
    ("Berlin", "", "Germany"),
    ("Madrid", "", "Spain"),
    ("Rome", "", "Italy"),
    ("Toronto", "ON", "Canada"),
    ("Vancouver", "BC", "Canada"),
    ("Montreal", "QC", "Canada"),
    ("Pukalani", "Hawaii", "USA"),
    ("Cape Town", "", "South Africa"),
]

# Random dates from 2000 to 2026 for testing the date handling functions in the database
test_dates = [
    "2024-06-01",
    "2024-06-02",
    "2024-06-03",
    "2024-06-04",
    "2024-06-05",
    "2024-06-06",
    "2024-06-07",
    "2024-06-08",
    "2024-06-09",
    "2024-06-10",
    "2024-06-11",
    "2024-06-12",
    "2024-06-13",
    "2024-06-14",
    "2024-06-15",
    "2024-06-16",
    "2024-06-17",
    "2024-06-18",
    "2024-06-19",
    "2024-06-20",
    "2024-06-21",
    "2024-06-22",
    "2024-06-23",
    "2024-06-24",
    "2024-06-25",
    "2024-06-26",
    "2024-06-27",
    "2024-06-28",
    "2024-06-29",
    "2024-06-30"
]

valid_symptoms = [
    "cough_congestion",
    "nausea_vomiting",
    "difficulty_breathing",
    "sore_throat",
    "rash",
    "fever",
    "chills",
    "diarrhea",
    "red_eyes",
    "attending_a_recent_mass_gathering",
    "history_of_travel"
]

if __name__ == "__main__":
    # Insert 100 random responses
    for _ in range(100):
        city, state, country = test_cities[random.randint(0, len(test_cities)-1)]
        date = test_dates[random.randint(0, len(test_dates)-1)]
        num_symptoms = random.randint(1, len(valid_symptoms))
        # Randomly select a subset of unique symptoms for this response (do not just call a function)
        symptoms = []
        while len(symptoms) < num_symptoms:
            symptom = valid_symptoms[random.randint(0, len(valid_symptoms)-1)]
            if symptom not in symptoms:
                symptoms.append(symptom)
        
        success = db.add_response(city=city, state=state, country=country, date=date, values=symptoms)
        if success:
            print(f"Successfully added response for {city}, {state}, {country} on {date} with symptoms: {symptoms}")
        else:
            print(f"Failed to add response for {city}, {state}, {country} on {date} with symptoms: {symptoms}")