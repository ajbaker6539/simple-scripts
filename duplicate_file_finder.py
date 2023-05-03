import hashlib
import os
import shutil

# Get the current directory
dir_path = os.getcwd()

# Create a subdirectory called "Duplicates" to store duplicate files
duplicates_dir = os.path.join(dir_path, "Duplicates")
if not os.path.exists(duplicates_dir):
    os.mkdir(duplicates_dir)

# Dictionary to store file hashes
hashes = {}

# Loop over every file in the directory, in batches of 1000
batch_size = 1000
files = os.listdir(dir_path)
num_files = len(files)
for i in range(0, num_files, batch_size):
    batch = files[i:i+batch_size]
    num_files_processed = i + len(batch)

    print(f"Processing files {i+1}-{num_files_processed} of {num_files}...")

    for filename in batch:
        # Check if the file is a directory
        if os.path.isdir(os.path.join(dir_path, filename)):
            print(f"Skipping directory: {filename}")
            continue

        # Calculate the hash value of the file
        hasher = hashlib.sha256()
        try:
            with open(os.path.join(dir_path, filename), 'rb') as file:
                data = file.read()
                hasher.update(data)
            file_hash = hasher.hexdigest()

            # Check if the hash value has already been seen
            if file_hash in hashes:
                print(f"Duplicate file detected: {filename} is identical to {hashes[file_hash]}")
                # Create a folder named after the hash value in the "Duplicates" directory, if it doesn't exist
                folder_path = os.path.join(duplicates_dir, file_hash)
                if not os.path.exists(folder_path):
                    os.mkdir(folder_path)
                # Move the duplicate file to the folder
                dest_filename = filename
                dest_path = os.path.join(folder_path, dest_filename)
                i = 1
                while os.path.exists(dest_path):
                    # If file already exists in the destination folder, iterate the filename
                    dest_filename = f"{os.path.splitext(filename)[0]}_{i}{os.path.splitext(filename)[1]}"
                    dest_path = os.path.join(folder_path, dest_filename)
                    i += 1
                shutil.move(os.path.join(dir_path, filename), dest_path)
                print(f"Moved {filename} to {dest_path}")
            else:
                hashes[file_hash] = filename

        except PermissionError:
            print(f"Skipping file due to permission error: {filename}")
            continue

# Write the results to the hashlist.txt file
with open("hashlist.txt", "w") as f:
    for file_hash, filename in hashes.items():
        f.write(f"{filename}: {file_hash}\n")

print("Done.")
