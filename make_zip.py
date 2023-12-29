import os
import zipfile


def zip_folder(src_folder: str, output_zip: str) -> None:
    """Zip a folder
    Args:
        src_folder (str): The folder to zip
        output_zip (str): The output zip file
    """
    # Remove the existing zip file if it exists
    if os.path.exists(output_zip):
        os.remove(output_zip)

    # Create a zip file
    added = []
    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(src_folder):
            # Exclude certain directories and hidden files
            dirs[:] = [d for d in dirs if not d.startswith(".") and d != "__pycache__" and d != "build"]
            files = [f for f in files if not f.startswith(".")]
            for file in files:
                print(f"Adding... {file}")
                zipf.write(
                    os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(src_folder, ".."))
                )
                added.append(file)
    if not added:
        print("No files added to zip.")
    else:
        print(f"Added {len(added)} files to zip.")


if __name__ == "__main__":
    # Usage
    zip_folder("./src/", "./ai_shell/fish_tank.zip")
