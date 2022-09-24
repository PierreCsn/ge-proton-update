import json
import requests
import wget
import tarfile
import os

api_url = "https://api.github.com/repos/GloriousEggroll/proton-ge-custom/releases/latest"
json_load = json.loads(requests.get(api_url).text)
proton_path="/home/pierre/.steam/root/compatibilitytools.d/"
for download in json_load["assets"]:
        if "tar.gz" in download["name"]:
            download_url = download["browser_download_url"]
            latest_bin = download["name"]
            break
if not os.path.isfile():
    wget.download(download_url,latest_bin)
    # open file
    file = tarfile.open(latest_bin)
    
    # extracting file
    file.extractall(proton_path)
    
    file.close()
