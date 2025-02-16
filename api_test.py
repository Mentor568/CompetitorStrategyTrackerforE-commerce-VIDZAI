import requests

response = requests.get("https://api.github.com")  # GitHub API example
print("Status Code:", response.status_code)
print("Response:", response.json())  # Print API response
response = requests.get("https://api.github.com/repositories")
repos = response.json()

# Print the first 3 repository names
for repo in repos[:3]:
    print("Repo Name:", repo["name"], "| Owner:", repo["owner"]["login"])
