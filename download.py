import requests

def download_file(url, destination):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        with open(destination, 'wb') as file:
            file.write(response.content)

        print(f"Downloaded successfully to {destination}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")

