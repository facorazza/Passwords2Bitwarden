# Passwords2Bitwarden

Vault converter from Nextcloud Passwords to Bitwarden or Vaultwarden.

## Requirements

The script requires at least Python 3.10. Otherwise, you can run the script in a container.

If you're using an older version, you can work around it by using the code mentioned [here](https://github.com/facorazza/Passwords2Bitwarden/issues/8) even though I have not tested it.

## How to...

### Nextcloud Passwords

> :warning: Before exporting your passwords, you must change your Nextcloud language to English. Got to `Settings > Personal info > Language`. You can revert the change once downloaded the archive.

Enter your Nextcloud instance go to `Passwords > More > Backup & Restore`. Select `Backup or export` and then fill the following fields:

1. Choose Format: `Predefined CSV`
2. Select Options: Select at least `Passwords` and `Folders`
3. Run Export
4. Download CSV

### Conversion

There are two options to run the conversion: the first one is using Docker or Podman, the second one is to run the script by directly cloning the repository.

The former is more robust in terms of dependencies and you don't need to install anything if you already have a container runtime installed. However, it is yet to be tested. Please open an issue if you find problems with this method or if it worked and the instructions were clear enough.

The latter method requires you to install a few Python dependencies, but it's been tested and is fairly consistent.

#### Docker

> You can use the automatically built container image on GitHub or you can build your own using the Dockerfile contained in the repository.

```shell
docker run --name passwords2bitwarden --rm -v ./<path-to-archive>/<archive-name>.zip:/app/archive.zip -v ./passwords2bitwarden:/app/output facorazza/passwords2bitwarden
```

You'll find the exported dump under `passwords2bitwarden`.

#### Bare-Metal

Clone the repo locally:

```shell
git clone https://github.com/facorazza/Passwords2Bitwarden.git
cd Passwords2Bitwarden
```

Install Python requirements:

```shell
python -m pip install -r requirements.txt
```

To convert the zip archive call the script like so:

```shell
python main.py ~/Downloads/.../path/to/zip/archive.zip
```

The converted file will be stored inside the folder repo under the name `dump.json`.

### Bitwarden (Vaultwarden) Import

Go to your Bitwarden or Vaultwarden instance `Tools > Import Data`. Select `Bitwarden (json)`. Upload the `dump.json` file and click on `Import Data`.
