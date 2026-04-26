import sqlite3 as sql
import nominatim as n
import time

conn = sql.connect('data/database.db')
c = conn.cursor()

# Initialization
c.execute("CREATE TABLE IF NOT EXISTS countries (countryid INTEGER PRIMARY KEY, dname TEXT, lat REAL, lon REAL, UNIQUE(dname))")
c.execute("CREATE TABLE IF NOT EXISTS cities (cid INTEGER PRIMARY KEY, cname TEXT, cstate TEXT, countryid INTEGER REFERENCES countries (countryid), lat REAL, lon REAL, UNIQUE(cname, cstate, countryid))")
c.execute("CREATE TABLE IF NOT EXISTS responses (rid INTEGER PRIMARY KEY, cid INTEGER REFERENCES cities (cid), \
date_of_report TEXT,\
cough_congestion INTEGER,\
nausea_vomiting INTEGER,\
difficulty_breathing INTEGER,\
sore_throat INTEGER,\
rash INTEGER,\
fever INTEGER,\
chills INTEGER,\
diarrhea INTEGER,\
red_eyes INTEGER,\
attending_a_recent_mass_gathering INTEGER,\
history_of_travel INTEGER)")

# Add countries


# Adds a city into the database
def add_city(cname, state, country): 
    time.sleep(1.5)
    result = n.searchlocation(city=cname, state=state, country=country)
    if (result):
        return insert_city_to_db(result)
    else:
        print(f"ERROR: API call failed for searchlocation({cname}, {state}, {country}).")
        return False

def insert_city_to_db(result):
    # Sanitize input
    vals = result["display_name"].split(",")
    if len(vals) == 2:
        cname = vals[0].strip()
        cstate = "".strip()
        countryid = get_country_id(vals[-1])
    elif len(vals) > 2:
        cname = vals[0].strip()
        cstate = vals[-2].strip()
        countryid = get_country_id(vals[-1])
    else:
        print("City isn't part of a country?")
        return False
    lon = float(result["lon"])
    lat = float(result["lat"])
    

    if (result):
        c.execute(f"INSERT OR IGNORE INTO cities (cname, cstate, countryid, lon, lat) VALUES (?, ?, ?, ?, ?)", (cname, cstate, countryid, lon, lat))
        conn.commit()
    else:
        print(f"ERROR: API call failed for searchlocation({cname}, {cstate}, {countryid}, {lon}, {lat}).")
        return False
    return True

def add_response(city, state, country, date, values):
    # Query the nominatim API to create a city entry if it doesn't exist, and get the cityid for the response
    time.sleep(1.5)
    result = n.searchlocation(city=city, state=state, country=country)

    if result:
        city = result.get('display_name').split(",")[0].strip()
        state = result.get('display_name').split(",")[-2].strip() if len(result.get('display_name').split(",")) > 2 else ""
        country = result.get('display_name').split(",")[-1].strip()
        insert_city_to_db(result)
        cityid = c.execute("SELECT cid FROM cities WHERE cname = ? AND cstate = ? AND countryid = ?", (city.strip(), state.strip(), get_country_id(country))).fetchone()[0]
    else:
        print(f"ERROR: API call failed for searchlocation({city}, {state}, {country}). Cannot add response.")
        return False

    # Define the exact column names as they appear in the database schema
    valid_parameters = [
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
    
    # Initialize a dictionary mapping every parameter to 0 (False)
    param_states = {param: 0 for param in valid_parameters}
    
    # Loop through the provided list and set present parameters to 1 (True)
    for val in values:
        if val in param_states:
            param_states[val] = 1
        else:
            print(f"WARNING: '{val}' is not a recognized parameter and will be ignored.")
            
    try:
        # Build the final tuple to insert, keeping the strict order of valid_parameters
        # We start with cityid and date, then append the 11 parameter values
        insert_values = (cityid, date) + tuple(param_states[param] for param in valid_parameters)
        
        c.execute('''
            INSERT INTO responses (
                cid, 
                date_of_report, 
                cough_congestion, 
                nausea_vomiting, 
                difficulty_breathing, 
                sore_throat, 
                rash, 
                fever, 
                chills, 
                diarrhea, 
                red_eyes, 
                attending_a_recent_mass_gathering, 
                history_of_travel
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', insert_values)
        
        conn.commit()
        return True
        
    except sql.Error as e:
        print(f"ERROR: Database error when adding response: {e}")
        return False

def build_countries():
    # Check if the countries have been populated
    c.execute("SELECT COUNT(*) FROM countries")
    row_count = c.fetchone()[0]
    if row_count >= 195:
        return

    countrylist = ["Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo_Brazzaville", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czechia", "Democratic Republic of the Congo", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Ivory Coast", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea", "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Korea", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"]
    for country in countrylist:
        result = n.searchlocation(country=country)
        if result:
            c.execute(
                "INSERT OR IGNORE INTO countries (dname, lat, lon) VALUES (?, ?, ?)", 
                (result.get('display_name'), result.get('lat'), result.get('lon'))
            )
            print(f"Inserted {country}")
        else:
            print(f"Error for country {country}")
        time.sleep(1.5)
    conn.commit()


def get_country_id(dname):
    # Query nominatim for the proper country name and insert it into the database if it doesn't exist, then return the countryid
    time.sleep(1.5)
    result = n.searchlocation(country=dname)
    if result:
        c.execute("INSERT OR IGNORE INTO countries (dname, lat, lon) VALUES (?, ?, ?)", (result.get('display_name'), result.get('lat'), result.get('lon')))
        conn.commit()
    else:        
        print(f"ERROR: API call failed for searchlocation({dname}). Cannot get country ID.")
        return None
    
    # Now that we are sure the country is in the database, query for its ID and return it
    dname = result.get('display_name')

    return c.execute("SELECT countryid FROM countries WHERE dname = ?", (dname.strip(),)).fetchone()[0]

# Initialize countries
build_countries()


if __name__ == "__main__":
    add_city(cname="Pukalani", country="US", state="HI")
    add_response(city="Pukalani", state="HI", country="US", date="2024-06-01", values=["cough_congestion", "fever", "diarrhea"])

