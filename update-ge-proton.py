from glob import glob
import json
import requests
import wget
import tarfile
import os
import glob
import shutil

# get user profile
user_profile = os.path.expanduser("~")
proton_path = f"{user_profile}/.steam/root/compatibilitytools.d/"
print(f"proton-ge will be installed in{proton_path}")


api_url = "https://api.github.com/repos/GloriousEggroll/proton-ge-custom/releases/latest"
json_load = json.loads(requests.get(api_url).text)

# find current latest local version:
proton_all_current = glob.glob(proton_path + "*")
proton_all_current_version = []
# remove all but digits from that list of string
for element in proton_all_current:
    proton_all_current_version.append(element.split("-")[-1])
# convert to int
proton_all_current_version = [int(x) for x in proton_all_current_version]
# sort
proton_all_current_version.sort()
# take last element
proton_current = proton_all_current_version[-1]
print("Current version:", proton_current)


print("Getting latest proton-ge release...")
for download in json_load["assets"]:
    if "tar.gz" in download["name"]:
        download_url = download["browser_download_url"]
        latest_bin = download["name"]
        version = latest_bin.split("-")[-1].split(".")[0]
        break
if int(version) > proton_current:
    print(f"Downloading {latest_bin}...")
    if os.path.isfile(latest_bin):
        print("This version is  already downloaded")
    else:
        wget.download(download_url, latest_bin)
    # open file
    file = tarfile.open(latest_bin)

    # extracting file
    print("Extracting file to ", proton_path)
    file.extractall(proton_path)

    file.close()
    # remove latest_bin
    os.remove(latest_bin)
    print("proton-ge has been installed")
else:
    print("proton-ge is already up to date")

# ask user wich directory versions to remove
print("Do you want to remove old versions of proton-ge?")
print("Current version:", proton_current)
print("All versions:", proton_all_current_version)
print("Type the version you want to remove or type 'all' to remove all versions")
print("Type 'exit' to exit")
while True:
    user_input = input()
    if user_input == "exit":
        break
    elif user_input == "all":
        for version in proton_all_current_version:
            shutil.rmtree(f"{proton_path}/GE-Proton7-{version}")
        break
    elif int(user_input) in proton_all_current_version:
        shutil.rmtree(f"{proton_path}/GE-Proton7-{user_input}")
        break
    else:
        print("Invalid input")
