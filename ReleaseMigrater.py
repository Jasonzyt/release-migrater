import os
from time import sleep
from github import Github, Auth
import requests

with open("token.txt", "r") as f:
    TOKEN = f.readlines()[0].strip()

g = Github(auth=Auth.Token(TOKEN))

old_repo = g.get_repo("LiteLDev/LiteLoaderBDS")
new_repo = g.get_repo("LiteLDev/LiteLoaderBDS2")

def download(url, name):
    with open("tmp/" + name, "wb") as f:
        f.write(requests.get(url).content)

if not os.path.exists("tmp"):
    os.mkdir("tmp")

for release in old_repo.get_releases():
    print("[INFO] Migrating release: " + release.title)
    assets = []
    raw_info = f"Release: {release.raw_data}\nAssets:\n"
    for asset in release.get_assets():
        raw_info += "- " + str(asset.raw_data) + "\n"
        download(asset.browser_download_url, asset.name)
        assets.append(asset)
    print(raw_info)
    new_msg = release.body + "\n\n<!--\nMigrated from LiteLDev/LiteLoaderBDS. Raw information:\n" + raw_info + "-->"
    new_release = new_repo.create_git_release(tag=release.tag_name, name=release.title, message=new_msg, draft=release.draft, prerelease=release.prerelease)
    for asset in assets:
        new_release.upload_asset("tmp/" + asset.name, asset.label, asset.content_type, asset.name)
        os.remove("tmp/" + asset.name)
    sleep(30)