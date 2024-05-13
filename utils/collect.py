import os
import subprocess
import json
import hashlib
from utils import icon_search_algo

def Collect_app_info():
    desktops = os.listdir("/usr/share/applications/")
    applications = {}
    key = 0
    for apps in desktops:
        applications[key] = {}
        with open(f"/usr/share/applications/{apps}", 'r') as file:
            commands = file.readlines()
            sha256 = hashlib.sha256("".join(commands).encode()).hexdigest()
        section = ""
        for c in commands:
            if c.strip().startswith('[') and c.strip().endswith(']'):
                section = c.strip()
            if section=="[Desktop Entry]":
                c = c.split("=")
                if c[0].strip() in ["Name","Terminal", "Icon", "Exec", "GenericName", "Type"]:
                    applications[key][c[0].strip()] = "".join(c[1:]).strip()
                if c[0].strip()=="Icon":
                    icon = icon_search_algo.search("".join(c[1:]))
        applications[key]["hasha256"] = sha256
        key+=1
    
    with open("database/app_info.json", 'w') as file:
        json.dump(applications, file, indent=4)





if __name__=="__main__":
    Collect_app_info()