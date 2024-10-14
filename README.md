# Passwords2Bitwarden

Vault converter from Nextcloud Passwords to Bitwarden or Vaultwarden.

## Requirements

The script requires at least Python 3.10.

If you're using an older version, you can work around it by using the code mentioned [here](https://github.com/facorazza/Passwords2Bitwarden/issues/8) even though I have not tested it. 

## How to...

Clone the repo locally:

```
git clone https://github.com/facorazza/Passwords2Bitwarden.git
cd Passwords2Bitwarden
```

### Requirements

Install Python requirements:

```
python -m pip install -r requirements.txt
```

### Nextcloud Passwords

> :warning: Before exporting your passwords, you must change your Nextcloud language to English. Got to `Settings > Personal info > Language`. You can revert the change once downloaded the archive.

Enter your Nextcloud instance go to `Passwords > More > Backup & Restore`. Select `Backup or export` and then fill the following fields:

1. Choose Format: `Predefined CSV`
2. Select Options: Select at least `Passwords` and `Folders`
3. Run Export
4. Download CSV

## Conversion

To convert the zip archive call the script like so:

```
python main.py ~/Downloads/.../path/to/zip/archive.zip
```

The converted file will be stored inside the folder repo under the name `dump.json`.

### Bitwarden (Vaultwarden) Import

Go to your Bitwarden or Vaultwarden instance `Tools > Import Data`. Select `Bitwarden (json)`. Upload the `dump.json` file and click on `Import Data`.



# Docker

`docker build -t passwords2bitwarden .`

Rename the "predefined csv" downloaded zip to `archive.zip`

`docker run --rm -v ./archive.zip:/app/archive.zip -v ./output:/app/output passwords2bitwarden /app/archive.zip /app/output`

#check `./output` dir and import in bitwarden using bitwarden-json format.
