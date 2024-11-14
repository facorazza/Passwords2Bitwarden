import re

def parse_custom_fields(fields):
    custom_fields = []
    pattern = re.compile(r"(\S+), (\w+): (.+)")

    for field in pattern.findall(fields):
        match field[1]:
            case "text" | "email" | "file" | "website":
                field_type = 0 # Text field
            case "secret":
                field_type = 1 # Hidden field
            case _:
                field_type = 0 # Defaults to text field

        custom_fields.append({
            "name": field[0],
            "value": field[2],
            "type": field_type,
        })

    return custom_fields
