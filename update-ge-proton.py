from glob import glob
import json
from cupshelpers import Printer
import requests
from sympy import false, true
import wget
import tarfile
import os
import glob
import shutil

# get user profile
user_profile = os.path.expanduser("~")
proton_path = f"{user_profile}/.steam/root/compatibilitytools.d/"
print(f"proton-ge will be installed in{proton_path}")

# check if proton_path exists
if not os.path.exists(proton_path):
    print("the standard proton path does not exist")
    print("please enter the path where you want to install proton-ge")
    proton_path = input("path: ")
    print(f"proton-ge will be installed in{proton_path}")

api_url = "https://api.github.com/repos/GloriousEggroll/proton-ge-custom/releases"
json_load = json.loads(requests.get(api_url).text)

# find current latest local version:
proton_all_current = glob.glob(proton_path + "*")
# if no local version, go to install
if len(proton_all_current) > 0:
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
else:
    proton_current = 0
    print("No local version found")

# ask user input if he wants the latest version


print("Getting latest proton-ge release...")
found = false
for version in json_load:
    if found == true:
        break
    for asset in version["assets"]:
        if "tar.gz" in asset["name"]:
            latest_bin = asset["name"]
            latest_version = latest_bin.split("-")[-1].split(".")[0]
            found = true
            break
# print latest version
print("Latest version:", latest_version)

# ask user if he wants a different version


version = input("Enter version number you wish to download (default: latest): ")
if version == "":
    version = int(latest_version)
    print("Using latest version")
else:
    version = int(version)
    print("Using version", version)


found = false

for release in json_load:
    if found == true:
        break
    for asset in release["assets"]:
        if f"-{version}.tar.gz" in asset["name"]:
            latest_bin = asset["name"]
            latest_version = latest_bin.split("-")[-1].split(".")[0]
            download_url = asset["browser_download_url"]
            found = true
            break

if int(version) != proton_current:
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
    print("{latest_bin} has been installed")
else:
    print("proton-ge is already up to date")
if proton_current > 0:
    # ask user wich directory versions to remove
    print("Do you want to remove old versions of proton-ge?")
    print("Current version:", proton_current)
    print("All versions:", proton_all_current_version)
    print("Type the version you want to remove or type 'all' to remove all versions")
    print("Type '0' to exit")
    while True:
        user_input = input()
        if user_input == "0":
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
