import requests

def searchlocation(city=None, country=None, state=None):
    """
    Queries the Nominatim API for a specific city.
    
    Args:
        city (str): The name of the city.
        country (str): The name of the country.
        state (str, optional): The name of the state/province. Defaults to None.
        
    Returns:
        dict: A dictionary containing the location data, or None if not found.
    """
    url = "https://nominatim.openstreetmap.org/search"
    
    # Define the search parameters
    params = {
        "city": city,
        "country": country,
        "format": "json",
        "limit": 1,  # We only need the top result
        "accept-language": "en"
    }
    
    # Add state to parameters only if it was provided
    if state:
        params["state"] = state
        
    # IMPORTANT: Nominatim requires a descriptive User-Agent. 
    # Replace the email below with your actual contact email.
    headers = {
        "User-Agent": "MyGeocodingScript/1.0 (bingusfartballs@wakanda.gov)" # TODO: Change email logic
    }
    
    try:
        # Make the GET request
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Check for HTTP errors (e.g., 404, 403)
        
        # Parse the JSON response
        data = response.json()
        
        # Nominatim returns a list of matches. Return the first one if it exists.
        if data:
            return data[0]
        else:
            print("No results found for the specified location.")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")
        return None

# --- Example Usage ---
if __name__ == "__main__":

    # Example 2: City, State, and Country
    print("Searching for Tucson, Arizona, USA...")
    result2 = searchlocation(city="Tucson", state="Arizona", country="USA")
    if result2:
        print(f"Found: {result2.get('display_name')}")
        print(f"Latitude: {result2.get('lat')}, Longitude: {result2.get('lon')}\n")

    print("Searching for Pukalani, HI")
    result2 = searchlocation(city="", state="", country="Congo_Brazzaville")
    if result2:
        print(f"Found: {result2.get('display_name')}")
        print(f"Latitude: {result2.get('lat')}, Longitude: {result2.get('lon')}\n")
        for i in result2:
            print(f"{i} : {result2[i]}")

    