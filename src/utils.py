def read_file(path):
    with open(path, 'r') as file:
        # Read the entire contents of the file
        file_contents = file.read()
        return file_contents
