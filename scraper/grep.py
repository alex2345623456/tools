import subprocess
import argparse

def run_grep_command(query, output_file):
    # Define the commands to run
    grep_commands = [
        f"grep -i -o '{query}[a-z]\\+' output.txt",
        f"grep -i -o '{query}[a-z0-9]*[0-9][a-z0-9]*' output.txt",
        f"grep -i -o '{query}[a-z0-9-]*-[a-z0-9-]*' output.txt",
        f"grep -i -o '{query}[a-z0-9_]*\\_+[a-z0-9_]*' output.txt",
        f"grep -i -o '/{query}[a-z]\\+' output.txt | sed 's/\\///g'",
        f"grep -i -o '/{query}[a-z0-9]*[0-9][a-z0-9]*' output.txt | sed 's/\\///g'",
        f"grep -i -o '/{query}[a-z0-9-]*-[a-z0-9-]\\+' output.txt | sed 's/\\///g'",
        f"grep -i -o '/{query}[a-z0-9]*\\_+[a-z0-9_]*' output.txt | sed 's/\\///g'"
    ]
    
    # Open the output file to write the results
    with open(output_file, 'w') as f:
        # Run each command and capture the output
        for command in grep_commands:
            print(f"Running command: {command}")
            try:
                # Run the command and capture output
                result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                # Write the result to the file (no modifications)
                f.write(result.decode())
            except subprocess.CalledProcessError as e:
                print(f"Error executing command: {e.cmd}")
                print(f"Error output: {e.output.decode()}")

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Run a series of grep commands based on the provided query.")
    parser.add_argument("-k", "--query", required=True, help="The query string to search for in the output.txt file")
    args = parser.parse_args()

    # Define output file name based on the query
    output_file = f"{args.query}.txt"
    
    # Run the grep commands and save the output
    run_grep_command(args.query, output_file)
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    main()
