import csv
import json
import zipfile

import click

from utils import parse_custom_fields

@click.command()
@click.argument("zip_filepath", type=click.Path(exists=True))
def cli(zip_filepath):

    with zipfile.ZipFile(zip_filepath, "r") as zf:
        zf.extractall()

    dump = {}
    dump["folders"] = []
    dump["items"] = []

    with open("Folders.csv", "r") as f:
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

    with open("Passwords.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            dump["items"].append({
                "id": row["Id"],
                "organizationId": None,
                "folderId": row["Folder Id"],
                "type": 1,
                "name": row["Label"],
                "notes": row["Notes"],
                "favorite": True if row["Favorite"] == "true" else False,
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

    with open("dump.json", "w") as f:
        f.write(json.dumps(dump))

    print("Done! Upload dump.json to Bitwarden or Vaultwarden.")


if __name__ == "__main__":
    cli()
