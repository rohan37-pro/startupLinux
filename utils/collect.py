import os
import subprocess
import json
import hashlib
from utils import icon_search_algo
from tqdm import tqdm

def Collect_app_info():
    USER, HOME = get_current_user_info()
    with open("database/app_info.json", 'r') as file:
        app_info = json.load( file)
    if len(app_info)==0:
        desktops = os.listdir("/usr/share/applications/")
        applications = {}
        key = 0
        for apps in tqdm(desktops):
            if apps.endswith(".desktop")==False:
                print("unknown formate --> ",apps)
                continue
            applications[key] = {}
            desktop_file_name = apps
            applications[key]["file_name"] = desktop_file_name
            with open(f"/usr/share/applications/{apps}", 'r') as file:
                commands = file.readlines()
                sha256 = hashlib.sha256("".join(commands).encode()).hexdigest()
            section = ""
            for c in commands:
                if c.strip().startswith('[') and c.strip().endswith(']'):
                    section = c.strip()
                if section=="[Desktop Entry]":
                    c = c.split("=")
                    if c[0].strip() in ["Name","Terminal", "Icon", "Exec", "GenericName", "Type", "NoDisplay"]:
                        applications[key][c[0].strip()] = "".join(c[1:]).strip()
                    if c[0].strip()=="Icon":
                        icon = icon_search_algo.search("".join(c[1:]).strip())
                        applications[key]['icon_path'] = icon

            applications[key]["hasha256"] = sha256

            key+=1

        sort_application(applications)
        
        with open("database/app_info.json", 'w') as file:
            json.dump(applications, file, indent=4)
    
    else:
        i = "0"
        while int(i) < len(app_info):
            if i in app_info:
                if os.path.exists(f"/usr/share/applications/{app_info[i]['file_name']}"):
                    with open(f"/usr/share/applications/{app_info[i]['file_name']}", 'r') as file:
                        commands = file.readlines()
                        sha256 = hashlib.sha256("".join(commands).encode()).hexdigest()
                    if app_info[i]['hasha256'] != sha256:
                        print("file changed sha256 didn't match -->", app_info[i]['file_name'])
                        section = ""
                        for c in commands:
                            if c.strip().startswith('[') and c.strip().endswith(']'):
                                section = c.strip()
                            if section=="[Desktop Entry]":
                                c = c.split("=")
                                if c[0].strip() in ["Name","Terminal", "Icon", "Exec", "GenericName", "Type", "NoDisplay"]:
                                    app_info[i][c[0].strip()] = "".join(c[1:]).strip()
                                if c[0].strip()=="Icon":
                                    icon = icon_search_algo.search("".join(c[1:]).strip())
                                    app_info[i]['icon_path'] = icon

                        app_info[i]["hasha256"] = sha256
                else:
                    print("uninstalled", app_info[i]['file_name'])
                    with open(f"database/{USER}-startup_onned.json", 'r') as file:
                        info = json.load(file)
                    if app_info[i]['file_name'] in info:
                        del info[app_info[i]['file_name']]
                    with open(f"database/{USER}-startup_onned.json", 'w') as file:
                        json.dump(info, file, indent=4)
                    if os.path.exists(f"{HOME}.config/autostart/startup.{app_info[i]['file_name']}"):
                        os.remove(f"{HOME}.config/autostart/startup.{app_info[i]['file_name']}")
                    delete_application(app_info, i)
                    i=str(int(i)-1)
            i=str(int(i)+1)

        desktops = os.listdir("/usr/share/applications/")
        filenames = []
        for i in app_info:
            filenames.append(app_info[i]['file_name'])
        
        for d in desktops:
            if d not in filenames and d.endswith('.desktop'):
                print("new app installed --> ", d)
                key = len(app_info)
                key = str(key)
                app_info[key] = {}
                app_info[key]["file_name"] = d
                with open(f"/usr/share/applications/{d}", 'r') as file:
                    commands = file.readlines()
                    sha256 = hashlib.sha256("".join(commands).encode()).hexdigest()
                section = ""
                for c in commands:
                    if c.strip().startswith('[') and c.strip().endswith(']'):
                        section = c.strip()
                    if section=="[Desktop Entry]":
                        c = c.split("=")
                        if c[0].strip() in ["Name","Terminal", "Icon", "Exec", "GenericName", "Type", "NoDisplay"]:
                            app_info[key][c[0].strip()] = "".join(c[1:]).strip()
                        if c[0].strip()=="Icon":
                            icon = icon_search_algo.search("".join(c[1:]).strip())
                            app_info[key]['icon_path'] = icon
                app_info[key]["hasha256"] = sha256

        
        sort_application(app_info)
        with open("database/app_info.json", 'w') as file:
            json.dump(app_info, file, indent=4)


def sort_application(app):
    if "0" in app or '1' in app or '2' in app:
        for i in range(len(app)):
            for j in range(i+1, len(app)):
                if "Name" not in app[str(i)]:
                    print(app[str(i)])
                if "Name" not in app[str(j)]:
                    print(app[str(j)])
                if app[str(i)]['Name'].lower() > app[str(j)]['Name'].lower():
                    app[str(i)], app[str(j)] = app[str(j)], app[str(i)]
    elif 0 in app or 1 in app or 2 in app:
        for i in range(len(app)):
            for j in range(i+1, len(app)):
                if app[i]['Name'].lower() > app[j]['Name'].lower():
                    app[i], app[j] = app[j], app[i]


def delete_application(app, key):
    if '0' in app or '1' in app or '2' in app:
        key = str(key)
        del app[key]
        while int(key) < len(app):
            if str(int(key)+1) in app:
                app[key] = app[str(int(key)+1)]
            key=str(int(key)+1)
        del app[str(len(app)-1)]
    if 1 in app or 2 in app or 0 in app:
        key = int(key)
        del app[key]
        while key < len(app):
            if key in app:
                app[key] = app[key+1]
            key+=1
        del app[len(app)-1]
    


def load_current_user_info():
    USER = subprocess.run("echo $USER", shell=True, stdout=subprocess.PIPE).stdout.decode().strip()
    HOME = subprocess.run("echo $HOME", shell=True, stdout=subprocess.PIPE).stdout.decode().strip()
    if HOME.endswith('/')==False:
        HOME += '/'
    cur_usr = {}
    cur_usr['USER'] = USER
    cur_usr['HOME'] = HOME
    if os.path.exists(f'database/{USER}-added_sh.json')==False:
        with open(f'database/{USER}-added_sh.json', 'w') as file:
            json.dump({}, file)
    if os.path.exists(f'database/{USER}-startup_onned.json')==False:
        with open(f'database/{USER}-startup_onned.json', 'w') as file:
            json.dump({}, file)

    with open("database/current_user.json", 'w') as file:
        json.dump(cur_usr, file, indent=4)


def get_current_user_info() -> tuple:
    with open('database/current_user.json') as file:
        current_user = json.load(file)
    return current_user['USER'], current_user['HOME']



if __name__=="__main__":
    Collect_app_info()