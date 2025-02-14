import requests
# Public API base URL
base_url = "https://pokeapi.co/api/v2"

# Defining a function to get the required data
def get_pokemon_info(name):
    url = f"{base_url}/pokemon/{name}"
    response = requests.get(url)
    print(response)
    # Giving conditions and accessing data if response is successful
    if response.status_code == 200:
        pokemon_data = response.json()
        return pokemon_data
    else:
        print(f"Failed to retrieve the data. Status code: {response.status_code}")

pokemon_name = "pikachu"
pokemon_info = get_pokemon_info(pokemon_name)

# If name exists, give the below details as follows
if pokemon_info:
    print(f"{pokemon_info['name']}")
    print(f"{pokemon_info['id']}")
    print(f"{pokemon_info['height']}")
    print(f"{pokemon_info['weight']}")
