import re

def parse_custom_fields(fields):
    custom_fields = []
    pattern = re.compile(r"(\S+), (\w+): (.+)")

    for field in pattern.findall(fields):
        field_type = 0 # Default to text field
        if field[1] in ["text", "email", "file", "website"]:
            field_type = 0 # Text field
        elif field[1] == "secret":
            field_type = 1 # Hidden field

        custom_fields.append({
            "name": field[0],
            "value": field[2],
            "type": field_type,
        })

    return custom_fields

