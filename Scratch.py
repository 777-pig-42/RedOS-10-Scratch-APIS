import requests
import scratchattach as sa
from requests import HTTPError


class specialScratchClasses:
    def __init__(self):
        self.index = None
        self.i = None
        self.char_decode = None
        self.char_encode = None
        self.cloud = None
        self.session = None
        self.CHARS = "abcdefghijklmnopqrstuvwxyz1234567890°FC "
        self.letter = ""

    def encode_to_cloud(self, string):
        self.char_encode = ""

        for self.letter in string:
            if self.letter not in self.CHARS:
                raise ValueError(f"Unsupported character: {self.letter}")

            self.char_encode += str(int(self.CHARS.index(self.letter.lower())) + 10)

        if len(self.char_encode) > 256:
            raise Exception("Scratch variables can only hold a maximum of 256 characters")

        return self.char_encode

    def decode_to_cloud(self, string):
        char_decode = ""
        i = 0
        while i < len(string):
            index_str = f"{string[i]}{string[i + 1]}"
            index = int(index_str) - 10
            if index < 0 or index >= len(self.CHARS):
                raise ValueError(f"Invalid encoded value: {index_str}")
            char_decode += self.CHARS[index]
            i += 2

        return char_decode

    def login_and_connect(self, username, password, projectID):
        self.session = sa.login(username, password)
        self.cloud = self.session.connect_cloud(projectID)

    def get_weather(self, city_input):
        city = city_input
        url = f"http://wttr.in/{city}?format=j1"
        response = requests.get(url)
        if not response.ok:
            raise HTTPError("Response crashed.")
        data = response.json()
        current_temp = data['current_condition'][0]['temp_F']
        return f"Current temperature in {city}: {current_temp}°F"

