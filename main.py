import click
import csv
import json
import re
import zipfile


def parse_custom_fields(fields):
    custom_fields = list()
    pattern = re.compile(r"(\S+), (\w+): (.+)")
    
    for field in pattern.findall(fields):
        match field[1]:
            case "text" | "email" | "file" | "website":
                field_type = 0 # Text field
            case "secret":
                field_type = 1 # Hidden field
            case _:
                field_type = 0 # Default to text field
    
        custom_fields.append({
            "name": field[0],
            "value": field[2],
            "type": field_type,
        })
    
    return custom_fields


@click.command()
@click.argument("zip_filepath", type=click.Path(exists=True))
def cli(zip_filepath):
    
    with zipfile.ZipFile(zip_filepath, "r") as zf:
        zf.extractall()
    
    dump = dict()
    dump["folders"] = list()
    dump["items"] = list()
    
    
    with open("Folders.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            dump["folders"].append({
                "id": row["Id"],
                "name": row["Label"]
            })
    
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
