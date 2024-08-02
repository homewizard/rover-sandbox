import subprocess
import argparse

parser = argparse.ArgumentParser(
    description="Move all images from 'image_list.txt' to gcr.io/hw-cloud-service using gcrane.")
parser.add_argument('-d', '--dry', 
                    action="store_true",
                    help="run process without executing gcrane commands")
parser.add_argument('-t', '--test',
                    action="store_true",
                    help="run process with test data in 'images_test_list.txt'")

def execute_commands_from_file(file_path, args):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            print(f"File read")

            if args.dry:
                print("Dry-run only returning commands and not executing them:")
            
            for line in lines:
                image = line.strip()
                if image:  # Make sure it's not an empty line
                    try:
                        # Execute the command
                        new_image = 'gcr.io/hw-cloud-service/' + "/".join(image.split("/")[1:])
                        command = f'gcrane copy {image} {new_image}'
                        if args.dry:
                            print(f"Command '{command}'")
                        else:
                            result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
                            print(f"Command '{command}' executed successfully.")
                            print(f"Output: {result.stderr}\n{result.stdout}")
                    except subprocess.CalledProcessError as e:
                        print(f"Command '{command}' failed with error:\n{e.stderr}")
                    except Exception as e:
                        print(f"An error occurred while executing command '{command}': {e}")

    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred while reading the file '{file_path}': {e}")

if __name__ == "__main__":
    args = parser.parse_args()
    if args.test:
        print("Executing test file")
        file_path = './images_test_list.txt'
    else: 
        print("Executing prod file")
        file_path = './images_list.txt'
    execute_commands_from_file(file_path, args)
