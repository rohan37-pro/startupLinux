import os
import subprocess

def search(icon):
    print(f"searching for {icon}")
    if (icon.endswith('.png') or icon.endswith('.svg')) or icon.startswith('/'):
        return icon
    try:
        icon_path = subprocess.run(f"find /usr/share/pixmaps -name {icon}.png 2>/dev/null", shell=True, stdout=subprocess.PIPE)
        if icon_path.stdout:
            return match_pix_map(icon_path)
        icon_path = subprocess.run(f"find /usr/share/pixmaps -name {icon}-symbolic.png 2>/dev/null", shell=True, stdout=subprocess.PIPE)
        if icon_path.stdout:
            return match_pix_map(icon_path)
        else:
            icon_path = subprocess.run(f"find /usr/share/pixmaps -name {icon}.svg 2>/dev/null", shell=True, stdout=subprocess.PIPE)
            if icon_path.stdout:
                return match_pix_map(icon_path)
            icon_path = subprocess.run(f"find /usr/share/pixmaps -name {icon}-symbolic.svg 2>/dev/null", shell=True, stdout=subprocess.PIPE)
            if icon_path.stdout:
                return match_pix_map(icon_path)
    except Exception as e:
        pass

    icon_directory_list = os.listdir("/usr/share/icons/")
    for icon_dir in icon_directory_list:
        if icon_dir.lower().startswith("yaru"):
            try:
                icon_path = subprocess.run(f"find /usr/share/icons/{icon_dir} -name {icon}.png 2>/dev/null", shell=True, stdout=subprocess.PIPE)
                if icon_path.stdout:
                    return match_pix_map(icon_path)
                icon_path = subprocess.run(f"find /usr/share/icons/{icon_dir} -name {icon}-symbolic.png 2>/dev/null", shell=True, stdout=subprocess.PIPE)
                if icon_path.stdout:
                    return match_pix_map(icon_path)
                else:
                    icon_path = subprocess.run(f"find /usr/share/icons/{icon_dir} -name {icon}.svg 2>/dev/null", shell=True, stdout=subprocess.PIPE)
                    if icon_path.stdout:
                        return match_pix_map(icon_path)
                    icon_path = subprocess.run(f"find /usr/share/icons/{icon_dir} -name {icon}-symbolic.svg 2>/dev/null", shell=True, stdout=subprocess.PIPE)
                    if icon_path.stdout:
                        return match_pix_map(icon_path)
            except:
                pass
    for icon_dir in icon_directory_list:
        if icon_dir.lower()=="hicolor":
            icon_path = subprocess.run(f"find /usr/share/icons/{icon_dir} -name {icon}.png 2>/dev/null", shell=True, stdout=subprocess.PIPE)
            if icon_path.stdout:
                return match_pix_map(icon_path)
            icon_path = subprocess.run(f"find /usr/share/icons/{icon_dir} -name {icon}-symbolic.png 2>/dev/null", shell=True, stdout=subprocess.PIPE)
            if icon_path.stdout:
                return match_pix_map(icon_path)
            else:
                icon_path = subprocess.run(f"find /usr/share/icons/{icon_dir} -name {icon}.svg 2>/dev/null", shell=True, stdout=subprocess.PIPE)
                if icon_path.stdout:
                    return match_pix_map(icon_path)
                icon_path = subprocess.run(f"find /usr/share/icons/{icon_dir} -name {icon}-symbolic.svg 2>/dev/null", shell=True, stdout=subprocess.PIPE)
                if icon_path.stdout:
                    return match_pix_map(icon_path)

    for icon_dir in icon_directory_list:
        if icon_dir.lower()=="highcontrast":
            icon_path = subprocess.run(f"find /usr/share/icons/{icon_dir} -name {icon}.png 2>/dev/null", shell=True, stdout=subprocess.PIPE)
            if icon_path.stdout:
                return match_pix_map(icon_path)
            icon_path = subprocess.run(f"find /usr/share/icons/{icon_dir} -name {icon}-symbolic.png 2>/dev/null", shell=True, stdout=subprocess.PIPE)
            if icon_path.stdout:
                return match_pix_map(icon_path)
            else:
                icon_path = subprocess.run(f"find /usr/share/icons/{icon_dir} -name {icon}.svg 2>/dev/null", shell=True, stdout=subprocess.PIPE)
                if icon_path.stdout:
                    return match_pix_map(icon_path)
                icon_path = subprocess.run(f"find /usr/share/icons/{icon_dir} -name {icon}-symbolic.svg 2>/dev/null", shell=True, stdout=subprocess.PIPE)
                if icon_path.stdout:
                    return match_pix_map(icon_path)

    for icon_dir in icon_directory_list:
        if icon_dir.lower().startswith('yaru') or icon_dir.lower()=="highcontrast" or icon_dir.lower()=="hicolor":
            continue
        else:
            icon_path = subprocess.run(f"find /usr/share/icons/{icon_dir} -name {icon}.png 2>/dev/null", shell=True, stdout=subprocess.PIPE)
            if icon_path.stdout:
                return match_pix_map(icon_path)
            icon_path = subprocess.run(f"find /usr/share/icons/{icon_dir} -name {icon}-symbolic.png 2>/dev/null", shell=True, stdout=subprocess.PIPE)
            if icon_path.stdout:
                return match_pix_map(icon_path)
            else:
                icon_path = subprocess.run(f"find /usr/share/icons/{icon_dir} -name {icon}.svg 2>/dev/null", shell=True, stdout=subprocess.PIPE)
                if icon_path.stdout:
                    return match_pix_map(icon_path)
                icon_path = subprocess.run(f"find /usr/share/icons/{icon_dir} -name {icon}-symbolic.svg 2>/dev/null", shell=True, stdout=subprocess.PIPE)
                if icon_path.stdout:
                    return match_pix_map(icon_path)
                    
            

def match_pix_map(icon_path):
    icon_path = icon_path.stdout.decode("utf-8").strip()
    icon_path = icon_path.split("\n")
    if len(icon_path)==1:
        return icon_path[0]
    icon_dictionary = {}
    for icon in icon_path:
        ic = icon.split('/')
        if '256x256@2x' in ic or '256X256@2X' in ic:
            icon_dictionary[0] = icon
        if "256x256" in ic or '256X256' in ic:
            icon_dictionary[1] = icon
        if '128x128@2x' in ic or '128X128@2X' in ic:
            icon_dictionary[2] = icon
        if '128x128' in ic or '128X128' in ic:
            icon_dictionary[3] = icon
        if '128x128@2x' in ic or '128X128@2X' in ic:
            icon_dictionary[4] = icon
        if '128x128' in ic or '128X128' in ic:
            icon_dictionary[5] = icon
        if '64x64@2x' in ic or '64X64@2X' in ic:
            icon_dictionary[6] = icon
        if '64x64' in ic or '64X64' in ic:
            icon_dictionary[7] = icon
        if '48x48@2x' in ic or '48X48@2X' in ic:
            icon_dictionary[8] = icon
        if '48x48' in ic or '48X48' in ic:
            icon_dictionary[9] = icon
        if '32x32@2x' in ic or '32X32@2X' in ic:
            icon_dictionary[10] = icon
        if '32x32' in ic or '32X32' in ic:
            icon_dictionary[11] = icon
        if '24x24@2x' in ic or '24X24@2X' in ic:
            icon_dictionary[12] = icon
        if '24x24' in ic or '24X24' in ic:
            icon_dictionary[13] = icon
        if '22x22@2x' in ic or '22X22@2X' in ic:
            icon_dictionary[14] = icon
        if '22x22' in ic or '22X22' in ic:
            icon_dictionary[15] = icon
        if '16x16@2x' in ic or '16X16@2X' in ic:
            icon_dictionary[16] = icon
        if '16x16' in ic or '16X16' in ic:
            icon_dictionary[17] = icon
    for i in range(18):
        if i in icon_dictionary:
            return icon_dictionary[i]
    else:
        return icon_path[0]

    

# import json
# with open("./database/app_info.json") as file:
#     data = json.load(file)
# i = 0
# for d in data:
#     if "Icon" in data[d]:
#         path = search(icon=data[d]['Icon'])
#         if path== None:
#             print()
#             print(f"{d}-->{data[d]['Name']}")
#             print(path)
#             print()
#         i+=1
# print(f"total {i} apps found")