import sys
import json
import os
import subprocess
import zipfile
import requests
from os.path import basename
import cProfile
import re
import fasteners
import socket
import xml.etree.ElementTree
import plistlib
import urllib.request
from shutil import copyfile
from shutil import rmtree

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ipAddress = s.getsockname()[0]
s.close()

print("=======================  Updating file details ======================= ")
print('\n | Checking for File Name')
name : str = "testAPK"
commandResult = ""
gotten = False;
androidPath = '/Users/rasheenruwisha/final-year-proj/mobilestorecopy/android/app/src/main/res/values/strings.xml';
iosPath = '/Users/rasheenruwisha/final-year-proj/mobilestorecopy/ios/mobilestore/Info.plist';
appid = '';
"""
Check for the arguments that has been passed when the script was executed
If the arguments are greater than 3 the script executes and the display name and name of the application is set to the
business name which is the first argument that is passed.
"""

try:
    if(len(sys.argv) >= 8):
        """
            Run a while loop till the gotten == False which means try till the script locking the file has released
            the lock and lock it for this instance of the script. once the script has the  file locked in the
            rest of the script will be exceuted.
        """
        while gotten == False:
            a_lock = fasteners.InterProcessLock('/tmp/temp_lock_file')
            gotten = a_lock.acquire(blocking=False)

            if(gotten):
                print(len(sys.argv))
            
                try:
                    rmtree('/Users/rasheenruwisha/final-year-proj/mobilestorecopy/android/build');
                    rmtree('/Users/rasheenruwisha/final-year-proj/mobilestorecopy/android/app/build');
                except:
                    print("Directories not found")
                
                
                print("Locked by" + sys.argv[1])
                businessName = sys.argv[1]
                businessName = businessName.replace("-","")
                packageName = 'com.'+ businessName.lower()
                LOGO_URL = sys.argv[5];
                STARTER_URL = sys.argv[4]
                ICON_URL = sys.argv[7]
                
                LOGO_URL = LOGO_URL.replace("api.appezite.com",ipAddress)
                print(LOGO_URL)
                STARTER_URL = STARTER_URL.replace("api.appezite.com",ipAddress)
                ICON_URL = ICON_URL.replace("api.appezite.com",ipAddress)
                
                urllib.request.urlretrieve(ICON_URL, "/Users/rasheenruwisha/final-year-proj/mobilestorecopy/android/app/src/main/res/mipmap-hdpi/ic_launcher.png")
                copyfile( "/Users/rasheenruwisha/final-year-proj/mobilestorecopy/android/app/src/main/res/mipmap-hdpi/ic_launcher.png","/Users/rasheenruwisha/final-year-proj/mobilestorecopy/android/app/src/main/res/mipmap-hdpi/ic_launcher_round.png")

                copyfile( "/Users/rasheenruwisha/final-year-proj/mobilestorecopy/android/app/src/main/res/mipmap-hdpi/ic_launcher.png","/Users/rasheenruwisha/final-year-proj/mobilestorecopy/android/app/src/main/res/mipmap-mdpi/ic_launcher_round.png")

                copyfile( "/Users/rasheenruwisha/final-year-proj/mobilestorecopy/android/app/src/main/res/mipmap-hdpi/ic_launcher.png",
                "/Users/rasheenruwisha/final-year-proj/mobilestorecopy/android/app/src/main/res/mipmap-mdpi/ic_launcher.png")


                copyfile( "/Users/rasheenruwisha/final-year-proj/mobilestorecopy/android/app/src/main/res/mipmap-hdpi/ic_launcher.png","/Users/rasheenruwisha/final-year-proj/mobilestorecopy/android/app/src/main/res/mipmap-xhdpi/ic_launcher_round.png")

                copyfile( "/Users/rasheenruwisha/final-year-proj/mobilestorecopy/android/app/src/main/res/mipmap-hdpi/ic_launcher.png","/Users/rasheenruwisha/final-year-proj/mobilestorecopy/android/app/src/main/res/mipmap-xhdpi/ic_launcher.png")


                copyfile( "/Users/rasheenruwisha/final-year-proj/mobilestorecopy/android/app/src/main/res/mipmap-hdpi/ic_launcher.png","/Users/rasheenruwisha/final-year-proj/mobilestorecopy/android/app/src/main/res/mipmap-xxhdpi/ic_launcher_round.png")

                copyfile( "/Users/rasheenruwisha/final-year-proj/mobilestorecopy/android/app/src/main/res/mipmap-hdpi/ic_launcher.png","/Users/rasheenruwisha/final-year-proj/mobilestorecopy/android/app/src/main/res/mipmap-xxhdpi/ic_launcher.png")

                copyfile( "/Users/rasheenruwisha/final-year-proj/mobilestorecopy/android/app/src/main/res/mipmap-hdpi/ic_launcher.png","/Users/rasheenruwisha/final-year-proj/mobilestorecopy/android/app/src/main/res/mipmap-xxxhdpi/ic_launcher_round.png")

                copyfile( "/Users/rasheenruwisha/final-year-proj/mobilestorecopy/android/app/src/main/res/mipmap-hdpi/ic_launcher.png","/Users/rasheenruwisha/final-year-proj/mobilestorecopy/android/app/src/main/res/mipmap-xxxhdpi/ic_launcher.png")
                
                
                appData = {'package': packageName,
                        'name': businessName}
                if(len(sys.argv) >= 9):
                    print(sys.argv[8])
                    appid = sys.argv[8]
                else:
                    url = requests.get('http://localhost:5005/firebase/addApp', json = appData)
                    appid = url.json()['appid']
                
                # The app.json file is opened and the JSON is updated with the display name and the name.

                print('\n | Dumping new details')
                       
                print('\n | Updating Display Name')

                # Read strings.xml file
                et = xml.etree.ElementTree.parse(androidPath)
                root = et.getroot()

                # Loop through the xml elements
                for strings in root.findall('string'):
                    name = strings.get('name');
                    # Check wether name attribute of the xml element = 'app_name'
                    if(name == 'app_name'):
                        # set new name to the tag
                        strings.text = businessName
                # Write the updated file
                et.write(androidPath)
                
                info  = '';
                # Open Info.plist file
                with open(iosPath, 'rb') as iosRead:
                    info = plistlib.load(iosRead)
                    # Check wether CFBundleDisplayName is available
                    if info.get('CFBundleDisplayName'):
                        # Change name to the new name
                        info['CFBundleDisplayName'] = businessName
                        # close the file
                        iosRead.close();
                # Open the file in write mode
                with open(iosPath, 'wb') as iosFile:
                    # Dump the new details to the file
                    plistlib.dump(info, iosFile)
                    iosFile.close()

                print('\n | Dumping new details')

                """
                The properties.js file is searched within the mobilestore folder and if it exists the file is deleted.
                If the file is not found the exceptions is handled and a error is printed in the console.
                """
                try:
                    os.remove('/Users/rasheenruwisha/final-year-proj/mobilestorecopy/properties.js')
                except:
                    print("File not found")


                """
                A new file is created with write permissions and the required details are written to the file which is
                later used by the application to render the application properly.
                """

                with open('/Users/rasheenruwisha/final-year-proj/mobilestorecopy/properties.js', 'w') as file:

                    file.write('export const BUSINESS_ID = "'+sys.argv[3]+'";')
                    file.write('export const STARTER_URL = "'+STARTER_URL+'";')
                    file.write('export const LOGO_URL = "'+LOGO_URL+'";')
                    file.write('export const BASE_URL = "http://'+ipAddress+':5005/client";')
                    file.write('export const THEME_COLOR = "'+sys.argv[6]+'";')
                    file.write('export const BUSINESS_NAME = "'+sys.argv[1]+'";')
                    file.write('export const IP_ADR = "'+ipAddress+'"')
                    file.close()
                # Write the file out again



                print('\n=======================  File details update complete ======================= ')
                print('\n\n======================= Starting gradle build build process ======================= ')
                
                os.chdir("/Users/rasheenruwisha/final-year-proj/mobilestorecopy")
                print(os.getcwd())
                print(businessName)
                print(packageName)
                newBusinessName = businessName.replace("-"," ")
                command = 'react-native-rename "%s" -b %s' % (newBusinessName, packageName)
                print(command)
                os.system('react-native-rename "%s" -b %s' % ("test", packageName))
                os.system(command)
                
                os.chdir("/Users/rasheenruwisha/final-year-proj/mobilestorecopy/android")
                print(os.getcwd())
                # os.system('./gradlew assembleRelease')
                
                with open("/Users/rasheenruwisha/final-year-proj/mobilestorecopy/android/app/google-services.json", "r+") as appJs:
                    data = json.load(appJs)
                    data['client'][0]['client_info']['mobilesdk_app_id'] = appid
                    data['client'][0]['client_info']['android_client_info']['package_name'] = packageName
                
                os.remove("/Users/rasheenruwisha/final-year-proj/mobilestorecopy/android/app/google-services.json")
                with open("/Users/rasheenruwisha/final-year-proj/mobilestorecopy/android/app/google-services.json", 'w') as f:
                    json.dump(data, f, indent=4)
                
                cleanProc = subprocess.Popen('./gradlew clean', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                while cleanProc.poll() is None:
                    print(cleanProc.stdout.readline())
                    commandResult = cleanProc.wait()
                    
                os.chdir("/Users/rasheenruwisha/final-year-proj/mobilestorecopy")
                print(os.getcwd())
                os.system('react-native bundle --platform android --dev false --entry-file index.js --bundle-output android/app/src/main/assets/index.android.bundle --assets-dest android/app/src/main/res')
                    
                os.chdir("/Users/rasheenruwisha/final-year-proj/mobilestorecopy/android")
                print(os.getcwd())
                                   
                proc = subprocess.Popen('./gradlew assembleRelease', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                while proc.poll() is None:
                    print(proc.stdout.readline())
                    commandResult = proc.wait()

                if commandResult == 1:
                    print('\n======================= Gradle Build Failed ======================= ')
                elif commandResult == 0:
                        directory = "/Users/rasheenruwisha/final-year-proj/mobilestorecopy/android/app/build/outputs/apk/release/"
                        outZipFile = zipfile.ZipFile(sys.argv[1]+'.zip', "w", zipfile.ZIP_DEFLATED)
                        rootdir = os.path.basename(directory)
                        abs_src = os.path.abspath("/Users/rasheenruwisha/final-year-proj/mobilestorecopy/android/app/build/outputs/apk/release/app-release.apk")
                        for dirpath, dirnames, filenames in os.walk(directory):
                            for filename in filenames:
                                # Write the file named filename to the archive,
                                # giving it the archive name 'arcname'.
                                filepath = os.path.join(dirpath, filename)
                                parentpath = os.path.relpath(filepath, directory)
                                arcname = os.path.join(rootdir, parentpath)

                                outZipFile.write(filepath, arcname)

                        outZipFile.close()
                        with open(sys.argv[1]+'.zip',
                                  'rb') as f:
                            r = requests.post('http://localhost:5005/ipfs/uploadapk', files={'apk': f})
                            try:
                                rJson = r.json()['data']['link'];
                                print(rJson)
                                data = {'email': sys.argv[2],
                                        'businessId': sys.argv[3],
                                        'appid':appid,
                                        'apkurl': rJson}
                                url = requests.post('http://localhost:5005/merchant/updateAPKURL', json = data)
                                print(url.json())
                                print('\n======================= Application Uploaded to IPFS ======================= ')
                                if gotten:
                                    a_lock.release()
                            except:
                                print("Application could not be uploaded. IPFS connection refused")

            else:
                print("No lock for " +sys.argv[1])
    else:
        raise ValueError('Program cannot be exectued as arguments are missing.')
except ValueError as exp:
    print ("Error", exp)

