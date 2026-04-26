import sqlite3 as sql
import nominatim as n
import time

conn = sql.connect('data/database.db')
c = conn.cursor()

# Initialization
c.execute("CREATE TABLE IF NOT EXISTS countries (countryid INTEGER PRIMARY KEY, dname TEXT, lat REAL, lon REAL, UNIQUE(dname))")
c.execute("CREATE TABLE IF NOT EXISTS cities (cid INTEGER PRIMARY KEY, cname TEXT, cstate TEXT, countryid INTEGER REFERENCES countries (countryid), lat REAL, lon REAL, UNIQUE(cname, cstate, countryid))")
c.execute("CREATE TABLE IF NOT EXISTS responses (rid INTEGER PRIMARY KEY, cid INTEGER REFERENCES cities (cid), \
age INTEGER,\
sex TEXT,\
email TEXT,\
unique_id TEXT,\
occupation TEXT,\
date_of_report TEXT,\
postal_code TEXT,\
phone_number TEXT,\
household_member_id TEXT,\
geographical_coordinates TEXT,\
no_symptoms INTEGER,\
symptoms TEXT,\
date_of_illness TEXT,\
cough_congestion INTEGER,\
nausea_vomiting INTEGER,\
difficulty_breathing INTEGER,\
sore_throat INTEGER,\
rash INTEGER,\
fever INTEGER,\
chills INTEGER,\
diarrhea INTEGER,\
bleeding_from_body_openings INTEGER,\
red_eyes INTEGER,\
muscle_or_body_aches_and_pains INTEGER,\
discolored_or_bloody_urine INTEGER,\
loss_of_smell_or_taste INTEGER,\
yellow_skin_yellow_eyes INTEGER,\
absent_from_work INTEGER,\
absent_from_school INTEGER,\
did_you_seek_health_care_or_treatment INTEGER,\
attending_a_recent_mass_gathering INTEGER,\
tick_or_insect_bite INTEGER,\
animal_bite INTEGER,\
history_of_travel INTEGER)")

# Add countries


# Adds a city into the database
def add_city(cname, cstate, countryid):
    result = n.searchlocation(city=cname, cstate=cstate, country=countryid)
    if (result):
        c.execute(f"INSERT INTO cities (cname, cstate, countryid)")
    else:
        print(f"ERROR: API call failed for searchlocation({cname}, {cstate}, {countryid}).")
        return False
    return True

def insert_city_to_db(result):
    # Sanitize input
    vals = result["display_name"].split(",").strip()
    if len(vals) == 2:
        cname = vals[0]
        cstate = ""
        countryid = get_country_id()

    if (result):
        c.execute(f"INSERT INTO cities (cname, cstate, countryid) VALUES ")
    else:
        print(f"ERROR: API call failed for searchlocation({cname}, {cstate}, {countryid}).")
        return False
    return True

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
    c.execute()

# Initialize countries
build_countries()




