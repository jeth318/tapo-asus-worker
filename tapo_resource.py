from dotenv import dotenv_values, load_dotenv
import os

load_dotenv()

config = dotenv_values(".env")
password = os.environ['TAPO_PASS']
username = os.environ['TAPO_USER']
cam2Ip = os.environ['CAM_1_IP']
cam1Ip = os.environ['CAM_2_IP']
triggerDeviceIp = os.environ['TRIGGER_DEVICE_IP']


def togglePrivacy(state):
    return {
        "method": "multipleRequest",
        "params": {
            "requests": [
                {
                    "method": "setLensMaskConfig",
                    "params": {
                        "lens_mask": {
                            "lens_mask_info": {
                                "enabled": state
                            }
                        }
                    }
                }
            ]
        }
    }


# Livingroom
camera_1 = Tapo(cam1Ip, username, password)
# Kitchen
camera_2 = Tapo(cam2Ip, username, password)


def dispatchPrivacyToggle(state):
    camera_1.performRequest(togglePrivacy(state))
    camera_2.performRequest(togglePrivacy(state))

