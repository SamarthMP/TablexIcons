# This file will grab the icons and map them into the KDE formatted icon theme in dist/

import json
import os
import shutil
import tarfile
import os.path

def GenerateTar(variantPath):
    with tarfile.open(variantPath + ".tar.gz", "w:gz") as tar:
        tar.add(variantPath, arcname=os.path.basename(variantPath))

def ReadIcon(iconName):
    iconPath = "./tabler-icons/" + iconName + ".svg"
    f = open(iconPath, "r")
    data = f.read()
    f.close()
    print("Mapping Icon " + iconName)
    return data

def WriteIcon(icon, scale, path, append):
    newPath = path.replace("__scale__", scale) + append + ".svg";
    os.makedirs(os.path.dirname(newPath), exist_ok=True)
    iconFile = open(newPath, "w")
    iconFile.write(icon)
    iconFile.close()

def GenerateVariant(variantName):
    # Parse Icon Map
    mapData = open("./generate.json", "r")
    variantData = open("./variants/" + variantName + ".json", "r")
    map = json.loads(mapData.read())
    variant = json.loads(variantData.read())

    # Copy All Icons
    for i in map:
        path = "./dist/" + variantName + "/__scale__/" + i
        icon = ApplyVariant(variant, ReadIcon(map[i]))
        WriteIcon(icon, "scalable", path, "")
        WriteIcon(icon, "scalable", path, "-symbolic")
        WriteIcon(icon, "16", path, "")
        WriteIcon(icon, "16", path, "-symbolic")

    mapData.close()

    # Copy Extra Stuff
    shutil.copy("./index.theme", "./dist/" + variantName)

    # Convert to tar.gz
    GenerateTar("./dist/" + variantName)

def ApplyVariant(variant, icon):
    appliedIcon = icon

    # Apply Primary Color
    appliedIcon = appliedIcon.replace("currentColor", variant["primaryColor"])

    return appliedIcon

def Main():
    for variant in os.listdir("./variants"):
        GenerateVariant(variant.split(".")[0])

if (__name__ == "__main__"):
    Main()