def reformat_http_history(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        lines = infile.readlines()

        method, endpoint, http_version = None, None, None

        for line in lines:
            line = line.strip()  # Remove leading and trailing whitespace

            # Extract Method, Endpoint, and HTTP Version
            if line.startswith("https://") or line.startswith("http://"):
                endpoint = line.split("/")[-1].strip('{}')
            elif line.startswith("Method:"):
                method = line.split(":")[1].strip('{}')
            elif line.startswith("HTTP Version:"):
                http_version = line.split(":")[1].strip('{}')

            # Write reformatted header if complete
            if method and endpoint and http_version:
                outfile.write(f"{method} /{endpoint} {http_version}\n")
                method, endpoint, http_version = None, None, None
            elif line and not (line.startswith("Method:") or line.startswith("HTTP Version:") or line.startswith("https://") or line.startswith("http://")):
                outfile.write(line + "\n")
            elif not line:
                outfile.write("\n")

# Specify input and output file paths
input_file = 'filtered_httphistory.txt'
output_file = 'formatted_httphistory.txt'

# Call the function
reformat_http_history(input_file, output_file)
