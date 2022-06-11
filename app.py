import os
import time
from dotenv import dotenv_values, load_dotenv
from tapo_integration import dispatchPrivacyToggle
from router_info import RouterInfo


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
    privacy = camera_1.getPrivacyMode()['enabled']
except Exception as e:
    print("Could not get the current privacy state. Will set to enabled.")
    privacy = "on"


def privacyWorker():
    global privacy
    global macTrigger
    isConnected = router.findConnectedDevice(macTrigger)

    if isConnected and privacy != "on":
        print("Will toggle privacy on")
        privacy = "on"
        dispatchPrivacyToggle("on")
    elif not isConnected and privacy != "off":
        print("Will toggle privace off")
        privacy = "off"
        dispatchPrivacyToggle("off")
    time.sleep(60)
    privacyWorker()


# Initialize
privacyWorker()
