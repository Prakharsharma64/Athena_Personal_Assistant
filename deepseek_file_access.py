import os
import subprocess

def read_file(file_path):
    """Read the contents of a file."""
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            # Fallback to a different encoding if UTF-8 fails
            with open(file_path, 'r', encoding='ISO-8859-1') as file:
                return file.read()
    else:
        return "File not found."

def query_model(prompt):
    """Send a prompt to the Ollama model and get the response."""
    # Ensure the prompt is properly formatted and does not contain null characters
    prompt = prompt.replace('\0', '')  # Remove any null characters
    
    # Limit the length of the prompt to avoid Windows command length issues
    max_length = 200  # Set a reasonable maximum length for the prompt
    if len(prompt) > max_length:
        prompt = prompt[:max_length] + "..."  # Truncate and indicate truncation
    
    command = f'ollama run deepseek-r1 "{prompt}"'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout

def analyze_repository(repo_path):
    """Analyze all files in the repository."""
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_content = read_file(file_path)
            
            if file_content != "File not found.":
                prompt = f"Analyze this file content: {file_content}"
                response = query_model(prompt)
                print(f"Model Response for {file_path}:\n{response}\n")
            else:
                print(f"File not found: {file_path}")

# Set the absolute path to your local repository
repo_path = r"C:\Users\HP\Desktop\Jarvis Python 2.0"  # Update with your actual repository path

# Ensure the path is correct, or specify the absolute path
if os.path.isdir(repo_path):
    analyze_repository(repo_path)
else:
    print(f"The specified path {repo_path} does not exist.")
