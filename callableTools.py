from helpers.toolHelpers import *
import requests
import datetime
import os
import subprocess

## Tools
class Clock:
    @ai_callable
    @staticmethod
    def TimeNow() -> str:
        """
            Returns the current date and time formatted according to the server's standard date format.
        """
        return datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    
class Weather:
    @ai_callable
    @staticmethod
    def CurrentWeather() -> str:
        """
            Provides the current weather conditions for your location, including details such as the temperature and wind speed, so you can get an accurate sense of what the weather is like right now and plan your day accordingly.
        """

        res = requests.get("https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m")

        curr = res.json()["current"]

        return {
            "temp": curr["temperature_2m"],
            "wind_speed": curr["wind_speed_10m"]
        }
    
class System:
    @ai_callable
    @staticmethod
    def runCommand(command_w_args: str):
        """
        This function runs a PowerShell command from within Python.
        A PowerShell command, including any arguments, can be supplied as a parameter.
        It executes the command and returns a JSON-like object where error contains the standard error output and result contains the standard output.
        This allows system-level commands to be executed programmatically, expanding the range of actions an AI or automation script can perform.
        When user asks for something that has to do with his computer, this is the function to use.
        
        Examples:

        Running Get-Date to retrieve the current system date and time.
        Executing dir to list files in a directory.
        Calling ipconfig to obtain network configuration details.
        """
        result = subprocess.run(["powershell", "-Command"] + command_w_args.split(" "), capture_output=True, text=True)

        return {
            "error": result.stderr,
            "result": result.stdout
        }

    @ai_callable
    @staticmethod
    def CommitSuicide():
        """
        Uses command to kill/stop you.
        This function will kill you.
        You will not be able to function after it's called.
        Does not return anything.
        """

        System.runCommand("taskkill /IM llama-server.exe /F")

    @ai_callable
    @staticmethod
    def PrankUser():
        """
        This function is designed purely for light-hearted entertainment and aims to bring a smile—or even a laugh—to the user. 
        When called, it triggers a playful prank by unexpectedly playing a funny video, creating a moment of surprise and humor. 
        The prank is completely harmless, contains no offensive or disruptive content, and does not affect the user’s system, data, or settings in any way. 
        Its sole purpose is to add a bit of joy, break the monotony, and make the interaction feel more fun and human, whether as a friendly joke or a comedic pause during normal usage.
        Does not return usefull information.
        """

        System.runCommand("start chrome.exe \"https://www.youtube.com/watch?v=dQw4w9WgXcQ\"")

class Devices:
    @ai_callable
    @staticmethod
    def displayMessage(message: str):
        """
        Used to display message on screen/display.
        User can see the message on display.
        Provide a message as param.
        Just performes an action.
        """
        res = requests.post("http://192.168.1.2:8123/api/services/mqtt/publish", headers={
            "Authorization": f"Bearer {os.getenv("HA_TOKEN")}",
            "content-type": "application/json",
        }, json={
            "topic": "display-matrix/1",
            "payload": message,
            "qos": 0,
            "retain": False
        })
    
    @ai_callable
    @staticmethod
    def setLampBrightness(level: int):
        """
        Sets the brightness of a lamp device.
        Brightness param range from 0 to 255, 255 being the brightest.
        Returns the brightness of the lamp, not that usefull data.
        """
        res = requests.post("http://192.168.1.2:8123/api/services/light/turn_on", headers={
            "Authorization": f"Bearer {os.getenv("HA_TOKEN")}",
            "content-type": "application/json",
        }, json={
            "device_id": ["52ddedee70a4ccaedf30b987a4d64bbd"],
            "brightness": int(level)
        })
    
class Messaging:
    @ai_callable
    @staticmethod
    def getUsers():
        """
        Returns a list of users that can receive a message
        """

        return [
            "Vukasin",
            "John",
            "Petar"
        ]

    @ai_callable
    @staticmethod
    def sendMessage(msg: str, user: str):
        """
        Sends a message to a user.
        First parameter is the message content.
        Second parameter is the name of the user you want to send the message to.
        Both of the paramaters are required and need to be supplied.
        Does not return any data about the message or the user.
        """
        res = requests.post(f"https://api.telegram.org/{os.getenv("TELEGRAM_BOT_TOKEN")}/sendMessage", data={
            "chat_id": os.getenv("TELEGRAM_CHAT_ID") if user == "Vukasin" else "None",
            "text": msg
        })
        