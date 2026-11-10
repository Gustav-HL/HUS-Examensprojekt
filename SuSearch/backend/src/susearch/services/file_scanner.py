import os
from pathlib import Path
import json
from datetime import datetime

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
                except (ValueError, TypeError):
                    pass
        return highest_id

    def scan_and_track(self, target_dir, json_file=current_directory / "file_tracker.json"):
        target_path = Path(target_dir).resolve()
        if not target_path.exists():
            print(f"Error: Directory '{target_path}' does not exist.")
            return

        data = {"folders": {}, "files": {}}
        if os.path.exists(json_file):
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)

        highest_document_idF = self.create_id("f", data["folders"])
        highest_document_idD = self.create_id("d", data["files"])

        current_folders = {}
        current_files = {}
        
        for root, dirs, files in os.walk(target_path):
            root_path = Path(root).relative_to(target_path)

            for d in dirs:
                directory_path = str(Path(root_path) / d) if root_path != Path(".") else d
                current_folders[directory_path] = d

            for f in files:
                if Path(root) == target_path and f == json_file:
                    continue
                file_path = str(Path(root_path) / f) if root_path != Path(".") else f
                current_files[file_path] = f

        add_new_folders = {}
        for folder_pathway, folder_name in current_folders.items():
            if folder_pathway in data["folders"]:
                add_new_folders[folder_pathway] = data["folders"][folder_pathway]
            else:
                highest_document_idF += 1
                add_new_folders[folder_pathway] = {"id": f"f{highest_document_idF}", "name": folder_name}

        add_new_files = {}
        for file_pathway, file_name in current_files.items():
            full_file_path = target_path / file_pathway
            
            if not full_file_path.exists():
                continue

            current_modification_date = self.get_modification_date(full_file_path)

            if file_pathway in data["files"]:
                file_tracker = data["files"][file_pathway]
                stored_modification_date = file_tracker.get("modification date")

                if stored_modification_date == current_modification_date:
                    add_new_files[file_pathway] = file_tracker
                else:
                    file_tracker["modification date"] = current_modification_date
                    
                    add_new_files[file_pathway] = file_tracker
            else:
                highest_document_idD += 1
                
                add_new_files[file_pathway] = {"id": f"d{highest_document_idD}", "name": file_name, "modification date": current_modification_date}

        updated_data = {
            "folders": add_new_folders,
            "files": add_new_files
        }
        
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(updated_data, f, indent=4, ensure_ascii=False)

        return target_path

    def fetch_data(self, json_file=current_directory / "file_tracker.json"):
        if os.path.exists(json_file):
            with open(json_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"folders": {}, "files": {}}

    def get_modification_date(self, path):
        timestamp = os.path.getmtime(path)
        formatted_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')
        return formatted_date

if __name__ == "__main__":
    path = (r"C:\Users\leona\OneDrive")
    document = DocumentScanner()
    document.scan_and_track(path)