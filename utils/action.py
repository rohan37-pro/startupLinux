import os
import subprocess
import json

HOME_DIR = os.path.expanduser("~/")


def startup_on_off(id, act):
    print(f"act in statup_on_off = {act}")
    print(f"id = {id}")
    if not os.path.exists(f"{HOME_DIR}.config/autostart"):
        subprocess.run("mkdir ~/.config/autostart", shell=True)
    with open("database/app_info.json", 'r') as file:
        apps = json.load(file)

    if act==True:
        startup_on(apps[id])

    
    if act==False:
        startup_off(apps[id])


def startup_on(app):
    file_name = app["file_name"]
    with open(f"{HOME_DIR}.config/autostart/startup.{file_name}", 'w') as file:
        file.write("[Desktop Entry]\n")
        file.write(f"Name={app['Name']}\n")
        file.write(f"Type={app['Type']}\n")
        file.write(f"Exec={app['Exec']}\n")
        file.write(f"Terminal=false\n")
    with open("database/startup_onned.json", 'r') as file:
        startup_apps = json.load(file)
    startup_apps[file_name]=True
    with open("database/startup_onned.json", 'w') as file:
        json.dump(startup_apps, file, indent=4)


def startup_off(app):
    file_name = app["file_name"]
    if os.path.exists(f"{HOME_DIR}.config/autostart/startup.{file_name}"):
        os.remove(f"{HOME_DIR}.config/autostart/startup.{file_name}")

    with open("database/startup_onned.json", 'r') as file:
        startup_apps = json.load(file)
    startup_apps[file_name]=False
    with open("database/startup_onned.json", 'w') as file:
        json.dump(startup_apps, file, indent=4)