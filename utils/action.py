import os
import subprocess
import json
import h5py
import random
from utils import collect



def startup_on_off(id, act):
    USER, HOME = collect.get_current_user_info()
    if not os.path.exists(f"{HOME}.config/autostart"):
        subprocess.run("mkdir ~/.config/autostart", shell=True)
    with open("database/app_info.json", 'r') as file:
        apps = json.load(file)

    if act==True:
        startup_on(apps[id])

    
    if act==False:
        startup_off(apps[id])


def startup_on(app):
    USER, HOME = collect.get_current_user_info()
    file_name = app["file_name"]
    with open(f"{HOME}.config/autostart/startup.{file_name}", 'w') as file:
        file.write("[Desktop Entry]\n")
        file.write(f"Name={app['Name']}\n")
        file.write(f"Type={app['Type']}\n")
        file.write(f"Exec={app['Exec']}\n")
        file.write(f"Terminal=false\n")
    with open(f"database/{USER}-startup_onned.json", 'r') as file:
        startup_apps = json.load(file)
    startup_apps[file_name]=True
    with open(f"database/{USER}-startup_onned.json", 'w') as file:
        json.dump(startup_apps, file, indent=4)


def startup_off(app):
    USER, HOME = collect.get_current_user_info()
    file_name = app["file_name"]
    if os.path.exists(f"{HOME}.config/autostart/startup.{file_name}"):
        os.remove(f"{HOME}.config/autostart/startup.{file_name}")

    with open(f"database/{USER}-startup_onned.json", 'r') as file:
        startup_apps = json.load(file)
    startup_apps[file_name]=False
    with open(f"database/{USER}-startup_onned.json", 'w') as file:
        json.dump(startup_apps, file, indent=4)






def startup_on_off_sh(name, act):
    USER, HOME = collect.get_current_user_info()
    if not os.path.exists(f"{HOME}.config/autostart"):
        subprocess.run("mkdir ~/.config/autostart", shell=True)
    with open(f"database/{USER}-added_sh.json", 'r') as file:
        sh_files = json.load(file)
    if act==True:
        startup_on_for_sh(sh_files, name)
    if act==False:
        startup_off_for_sh(sh_files, name)


def startup_on_for_sh(sh_files, name):
    USER, HOME = collect.get_current_user_info()
    filename = name.replace('/', '_') + ".desktop"
    terminals = subprocess.run("ls /usr/bin/ | grep terminal", shell=True, stdout=subprocess.PIPE).stdout.decode().strip().split("\n")
    term_found = ["", ""]
    for t in terminals:
        if "gnome-terminal" == t:
            term_found[0] = "gnome-terminal"
        if "qterminal" == t:
            term_found[1] = "qterminal"
    for i in term_found:
        if i != "":
            terminal = i
            break
    print(term_found)
    if os.path.exists(name):
        subprocess.run(f"chmod +x {name}", shell=True)
        with open(f"{HOME}.config/autostart/startup.{filename}", 'w') as file:
            file.write("[Desktop Entry]\n")
            file.write(f"Name=Startup Sh file\n")
            file.write(f"Type=Application\n")
            file.write(f"Exec={terminal} -- {name}\n")
            file.write(f"Terminal=true\n")
        sh_files[name]=True
        with open(f"database/{USER}-added_sh.json", 'w') as file:
            json.dump(sh_files, file, indent=4)


def startup_off_for_sh(shfiles, name):
    USER, HOME = collect.get_current_user_info()
    file_name = name.replace('/', '_') + ".desktop"
    if os.path.exists(f"{HOME}.config/autostart/startup.{file_name}"):
        os.remove(f"{HOME}.config/autostart/startup.{file_name}")
    shfiles[name]=False
    with open(f"database/{USER}-added_sh.json", 'w') as file:
        json.dump(shfiles, file, indent=4)

def startup_delete_sh(name):
    USER, HOME = collect.get_current_user_info()
    file_name = name.replace('/', '_') + ".desktop"
    if os.path.exists(f"{HOME}.config/autostart/startup.{file_name}"):
        os.remove(f"{HOME}.config/autostart/startup.{file_name}")
    with open(f"database/{USER}-added_sh.json", 'r') as file:
        sh_files = json.load(file)
    del sh_files[name]
    with open(f"database/{USER}-added_sh.json", 'w') as file:
        json.dump(sh_files, file, indent=4)


def get_needEmptyNumber():
    lis_dir = os.listdir('database')
    for i in lis_dir:
        if i.startswith('needEmpty'):
            num = i.split('.')[1]
    return int(num)

def chattr_needEmpty():
    os.path
    with h5py.File("database/needEmpty.txt", 'r') as meta:
        metadata = dict(meta.attrs.items())
    r = random.randint(1, 10000)
    while r==metadata['emptyattr']:
        r = random.randint(1, 10000)
    with h5py.File("database/needEmpty.txt", 'w') as meta:
        meta.attrs['emptyattr'] = r

def setattr_needEmpty0():
    with h5py.File("database/needEmpty.txt", 'w') as meta:
        meta.attrs['emptyattr'] = 0

