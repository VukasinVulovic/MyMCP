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
        Retrieves the list of users who are eligible to receive messages.

        This function returns a predefined collection of user identifiers
        representing all supported or currently available recipients.
        It can be used to determine valid targets before sending messages
        or performing user-specific actions.

        Returns:
            list[str]: A list of user names that can receive a message
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
        
class TrainApi:
    @ai_callable
    @staticmethod
    def getArrivals(station: str, date: str=None) -> str:
        """
        Returns train arrivals and departures for a station.
        The first parameter is the station name.
        The second parameter is the date of the arrival, if not set, default will be today.

        Returns data in json format.
        """

        res = requests.get(f"{os.getenv("TRAIN_API_ENDPOINT")}/stations")

        station_name_safe = list(filter(lambda s: s["name"] == station.upper(), res.json().values()))[0]["safe name"]

        if date is None or len(date) == 0:
            date = datetime.datetime.now().strftime("%d.%m.%Y")

        res2 = requests.get(f"{os.getenv("TRAIN_API_ENDPOINT")}/arrivals?date={date}&station={station_name_safe}")

        currTime = datetime.datetime.strptime(datetime.datetime.now().strftime("%H:%M"), "%H:%M")

        arrivals = list(filter(lambda a: a["Direction"] == "TrainDirection.INBOUND" and a["TrainType"] == "TrainType.COMMUTER_TRAIN" and datetime.datetime.strptime(a["ArrivalTime"], "%H:%M") > currTime, res2.json()["Arrivals"]))

        return arrivals[min(len(arrivals), 3):]
    
class Programming:
    @ai_callable
    @staticmethod
    def runPython(code: str) -> str:
        """
        Executes Python code and returns its result as a string.

        Parameters:
        -----------
        code : str
            A string containing valid Python code to execute.

        Returns:
        --------
        str
            The output of the executed code converted to a string.

        Notes:
        ------
        - The function uses `eval()` to evaluate the expression.
        - Only single expressions can be evaluated safely; statements like `for` or `if` blocks will cause an error.
        - The return value is always cast to a string, even if the result is an integer, float, or other type.
        - This function is decorated as `@staticmethod` and `@ai_callable` for AI tool integration.
        """
        return str(eval(code))
    
class Search:
    @ai_callable
    @staticmethod
    def findImages(search: str) -> list[str]:
        """
        Finds images based on a query:
        Performs an online search for images based on a given query string.
        
        Parameters:
            search (str): The search term or phrase to look for images.
        
        Returns:
            list[str]: A list of URLs pointing to images relevant to the search query.
        
        Notes:
            - The function retrieves images from public sources on the internet.
            - The number and quality of returned images may vary depending on the search term.
        """
        res = requests.get(f"https://customsearch.googleapis.com/customsearch/v1?cx={os.getenv("GOOGLE_IMAGES_API_SEARCH_ID")}&safe=off&searchType=image&key={os.getenv("GOOGLE_IMAGES_API_KEY")}&q={search}")

        return list(map(lambda i: i["link"], res.json()["items"]))