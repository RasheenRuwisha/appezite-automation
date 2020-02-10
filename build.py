import sys
import json
import os
import subprocess
import zipfile
import requests
from os.path import basename

print("=======================  Updating file details ======================= ")
print('\n | Checking for File Name')
print('\n | Checking for Display Name')

displayName : str = "testAPK"
name : str = "testAPK"
commandResult = ""

if(len(sys.argv) >= 3):
    displayName = sys.argv[1]
    name = sys.argv[2]

print('\n | Updating for Display Name')
print('\n | Updating for Display Name')
with open("/Users/rasheenruwisha/Projects/rn-fs/testbuild/App.json", "r+") as appJs:
    data = json.load(appJs)
    data['displayName'] = displayName
    data['name'] = name
    appJs.seek(0)
    json.dump(data,appJs,indent=4)

print('\n | Dumping new details')


try:
    os.remove('/Users/rasheenruwisha/Projects/rn-fs/testbuild/properties.js')
except:
    print("File not found")

with open('/Users/rasheenruwisha/Projects/rn-fs/testbuild/properties.js', 'w') as file:

    file.write('export const BUSINESS_ID = "'+sys.argv[3]+'";')
    file.write('export const STARTER_URL = "'+sys.argv[4]+'";')
    file.write('export const LOGO_URL = "'+sys.argv[5]+'";')
    file.write('export const BASE_URL = "http://localhost:8082/";')
    file.write('export const THEME_COLOR = "'+sys.argv[6]+'";')
    file.write('export const BUSINESS_NAME = "'+sys.argv[1]+'"')

    file.close()
# Write the file out again



print('\n=======================  File details update complete ======================= ')
print('\n\n======================= Starting gradle build build process ======================= ')


os.chdir("/Users/rasheenruwisha/Projects/rn-fs/testbuild/android")
print(os.getcwd())
# os.system('./gradlew assembleRelease')
proc = subprocess.Popen('./gradlew assembleRelease', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
while proc.poll() is None:
    print(proc.stdout.readline())
    commandResult = proc.wait()  

if commandResult == 1:
    print('\n======================= Gradle Build Failed ======================= ')
elif commandResult == 0:
        directory = "/Users/rasheenruwisha/Projects/rn-fs/testbuild/android/app/build/outputs/apk/debug/"
        outZipFile = zipfile.ZipFile(sys.argv[4]+'.zip', "w", zipfile.ZIP_DEFLATED)
        rootdir = os.path.basename(directory)
        abs_src = os.path.abspath("/Users/rasheenruwisha/Projects/rn-fs/testbuild/android/app/build/outputs/apk/debug/app-debug.apk")
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                # Write the file named filename to the archive,
                # giving it the archive name 'arcname'.
                filepath = os.path.join(dirpath, filename)
                parentpath = os.path.relpath(filepath, directory)
                arcname = os.path.join(rootdir, parentpath)

                outZipFile.write(filepath, arcname)

        outZipFile.close()
        with open(sys.argv[4]+'.zip',
                  'rb') as f:
            r = requests.post('http://localhost:5005/uploadapk', files={'apk': f})
            rJson = r.json()['data']['link'];
            print(sys.argv[3])
            data = {'email': sys.argv[3],
                    'businessId': sys.argv[4],
                    'apkurl': rJson}
            url = requests.post('http://localhost:8081/updateAPKURL', json = data)
            print(url.json())
            print('\n======================= Gradle Build Completed ======================= ')

