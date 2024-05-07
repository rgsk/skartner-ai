def read_text_file(url: str):
    import requests
    response = requests.get(url)
    if response.status_code == 200:
        file_contents = response.text
        return file_contents
    else:
        raise Exception(
            f"Failed to retrieve file contents. Status code: {response.status_code}")
