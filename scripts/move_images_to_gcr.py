import subprocess

def execute_commands_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        print(f"File read")
        for line in lines:
            image = line.strip()
            if image:  # Make sure it's not an empty line
                try:
                    # Execute the command
                    new_image = 'gcr.io/hw-cloud-service/' + "/".join(image.split("/")[1:])
                    command = f'gcrane copy {image} {new_image}'
                    result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
                    print(f"Result {result}")
                    print(f"Command '{command}' executed successfully.")
                    print(f"Output:\n{result.stdout}")
                except subprocess.CalledProcessError as e:
                    print(f"Command '{command}' failed with error:\n{e.stderr}")
                except Exception as e:
                    print(f"An error occurred while executing command '{command}': {e}")

    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred while reading the file '{file_path}': {e}")

if __name__ == "__main__":
    file_path = './images_list.txt'  # Replace this with your file path
    execute_commands_from_file(file_path)
