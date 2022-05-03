#This is for standalone use without the automator. Inactive by default.

import os
import time
from dotenv import dotenv_values, load_dotenv
from pytapo import Tapo
from tapo_integration import dispatchPrivacyToggle
from rt_ax58u import RouterInfo


load_dotenv()

config = dotenv_values(".env")
routerIp = os.environ['ROUTER_IP']
routerUser = os.environ['ROUTER_USER']
routerPass = os.environ['ROUTER_PASS']
password = os.environ['TAPO_PASS']
username = os.environ['TAPO_USER']
cam2Ip = os.environ['CAM_1_IP']
cam1Ip = os.environ['CAM_2_IP']
triggerDeviceIp = os.environ['TRIGGER_DEVICE_IP']
macTrigger = os.environ['TRIGGER_DEVICE_MAC']

camera_1 = Tapo(cam1Ip, username, password)
camera_2 = Tapo(cam2Ip, username, password)
router = RouterInfo(routerIp, routerUser, routerPass)

try:
    privacyMode = camera_1.getPrivacyMode()['enabled']
except Exception as e:
    privacyMode = "on"
    print("Could not get initial privacyMode. Will set to enabled.")

print(privacyMode)


def privacyWorker():
    global privacyMode
    global macTrigger
    isConnected = router.findConnectedDevice(macTrigger)

    if isConnected and privacyMode != "on":
        print("Will toggle privace on")
        privacyMode = "on"
        dispatchPrivacyToggle("on")
    elif not isConnected and privacyMode != "off":
        print("Will toggle privace off")
        privacyMode = "off"
        dispatchPrivacyToggle("off")
    time.sleep(60)
    #privacyWorker()


# Initialize
#privacyWorker()
