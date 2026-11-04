import os
from pathlib import Path
import json

current_directory = Path(__file__).resolve().parent

class DocumentScanner:

    def create_id(self, prefix, f_dict):
        highest_id = 0
        for f in f_dict.values():
            f_id = f.get("id", "")
            if f_id.startswith(prefix):
                try:
                    id = int(f_id[len(prefix):])
                    if id > highest_id:
                        highest_id = id
                except(ValueError, TypeError):
                    pass
        return highest_id

    def scan_and_track(self, target_dir, json_file= current_directory/"file_tracker.json"):

        target_path = Path(target_dir).resolve()
        if not target_path.exists():
            print(f"Error: Directory '{target_path}' does not exist.")
            return

        data = {"folders": {}, "files": {} }
        if os.path.exists(json_file):
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)

        highest_document_idF = self.create_id("f", data["folders"])
        highest_document_idD = self.create_id("d", data["files"])

        current_folders = {}
        current_files = {}
        
        for root, dirs, files in os.walk(target_path):
            root_path = Path(root).relative_to(target_path)
            #print(f"Root:{root_path}")
            #print(f"Check what root is:{root}")
            #print(f"What is target_path:{target_path}")

            for d in dirs:
                directory_path = str(Path(root_path) / d) if root_path != Path(".") else d
                current_folders[directory_path] = d
                #print(f"Folder:{directory_path}")
                #print(f"What is d:{d}")

            for f in files:
                if Path(root) == target_path and f == json_file:
                    continue
                file_path = str(Path(root_path) / f) if root_path != Path(".") else f
                current_files[file_path] = f
                #print(f"File:{file_path}")
                #print(f"What is f:{f}")

        add_new_folders = {}
        for folder_pathway, folder_name in current_folders.items():
            if folder_pathway in data["folders"]:
                
                add_new_folders[folder_pathway] = data["folders"][folder_pathway]
            else:
                
                highest_document_idF += 1
                add_new_folders[folder_pathway] = {"id": f"f{highest_document_idF}", "name": folder_name}

        add_new_files = {}
        for file_pathway, file_name in current_files.items():
            if file_pathway in data["files"]:
        
                add_new_files[file_pathway] = data["files"][file_pathway]
            else:
                
                highest_document_idD += 1
                add_new_files[file_pathway] = {"id": f"d{highest_document_idD}", "name": file_name}

        updated_data = {
            "folders": add_new_folders,
            "files": add_new_files
        }
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(updated_data, f, indent=4, ensure_ascii=False)

        # if missing_folders or missing_files:
        #     for folder in missing_folders:
        #         print(f"{folder}")
        #     for file in missing_files:
        #         print(f"{file}")

        # if added_folders or added_files:
        #     for folder in added_folders:
        #         print(f"{folder}")
        #     for file in added_files:
        #         print(f"{file}")

        return target_path

    def fetch_data(self, json_file= current_directory/"file_tracker.json"):
        if os.path.exists(json_file):
            with open(json_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"folders": {}, "files": {}}

    # def fetch_data(self, target_dir):
    #     # Combine the directory path with your json filename
    #     json_path = Path(target_dir) / "file_tracker.json"
        
    #     if json_path.exists():
    #         with open(json_path, "r", encoding="utf-8") as f:
    #             return json.load(f)
        
    #     # Return empty structure if the file doesn't exist there yet
    #     return {"folders": {}, "files": {}}

if __name__ == "__main__":
    path = (r"C:\Users\leona\OneDrive")
    document = DocumentScanner()
    document.scan_and_track(path)