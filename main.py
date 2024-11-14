import csv
import json
import zipfile
import os

import click

from utils import parse_custom_fields

@click.command()
@click.argument("zip_filepath", type=click.Path(exists=True))
@click.argument("output_dir", type=click.Path(exists=False), default=".")
def cli(zip_filepath, output_dir):
    # Extract the ZIP archive
    with zipfile.ZipFile(zip_filepath, "r") as zf:
        zf.extractall()

    dump = {}
    dump["folders"] = []
    dump["items"] = []

    # Process Folders.csv
    with open("Folders.csv", "r", encoding="utf-8") as f:
        folder_structure = {}
        folders = []

        reader = csv.DictReader(f)
        for row in reader:
            if row["ParentLabel"] == "Home":
                folder_structure[row["Id"]] = row["Label"]
                dump["folders"].append({"id": row["Id"], "name": row["Label"]})
            elif row["ParentId"] in folder_structure:
                path = row["ParentLabel"] + "/" + row["Label"]
                folder_structure[row["Id"]] = path
                dump["folders"].append({"id": row["Id"], "name": path})
            else:
                folders.append({
                    "parent_id": row["ParentId"],
                    "id": row["Id"],
                    "name": row["Label"]
                })

        while len(folders):
            for index, folder in enumerate(folders):
                if folder["parent_id"] in folder_structure:
                    path = folder_structure[folder["parent_id"]] + "/" + folder["name"]
                    folder_structure[folder["id"]] = path
                    dump["folders"].append({"id": folder["id"], "name": path})
                    folders.pop(index)

    # Process Passwords.csv
    with open("Passwords.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            dump["items"].append({
                "id": row["Id"],
                "organizationId": None,
                "folderId": row["Folder Id"],
                "type": 1,
                "name": row["Label"],
                "notes": row["Notes"],
                "favorite": True if "Favorite" in row and row["Favorite"] == "true" else False,
                "login": {
                    "username": row["Username"],
                    "password": row["Password"],
                    "totp": None,
                    "uris": [{
                        "match": None,
                        "uri": row["Url"],
                    }],
                },
                "fields": parse_custom_fields(row["Custom Fields"]),
                "collectionIds": [],
            })

    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save to the output directory
    output_file = os.path.join(output_dir, "dump.json")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(json.dumps(dump, indent=4))

    print(f"Done! Upload {output_file} to Bitwarden or Vaultwarden.")


if __name__ == "__main__":
    cli()
