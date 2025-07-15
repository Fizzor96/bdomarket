import requests
from bs4 import BeautifulSoup
import json
from enum import Enum

class Server(Enum):
    EU = "eu"
    NA = "na"
    ASIAPS = "ps4-asia"
    JP = "jp"
    KR = "kr"
    MENA = "mena"
    NAPS = "ps4-xbox-na"
    RU = "ru"
    SA = "sa"
    SEA = "sea"
    TH = "th"
    TW = "tw"

class Boss():
    def __init__(self, server: Server = Server.EU):
        self.__url = f"https://mmotimer.com/bdo/?server={server.value}"
        self.__data = []
            
    def Scrape(self) -> "Boss":
        """Scrape the boss timer data from the website."""
        self.__content = requests.get(self.__url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Connection": "keep-alive",
        }).content
        soup = BeautifulSoup(self.__content, 'html.parser')
        
        table = soup.find('table', class_='main-table')
        thead = table.find('thead') # type: ignore
        # time_headers = [th.text.strip() for th in thead.find_all('th')]
        time_headers = [th.text.strip() for th in thead.find_all('th')][1:] # type: ignore
        self.__data = []

        # Iterate rows (days) in <tbody>
        tbody = table.find('tbody') # type: ignore
        for row in tbody.find_all('tr'): # type: ignore
            cells = row.find_all(['th', 'td']) # type: ignore
            day = cells[0].text.strip()  # first cell is day

            for i, cell in enumerate(cells[1:]):  # skip day column
                time = time_headers[i]

                if cell.text.strip() == "-":
                    continue  # skip empty slots

                bosses = [span.text.strip() for span in cell.find_all('span')] # type: ignore

                if bosses:
                    self.__data.append([f"{day} {time}", ', '.join(bosses)])
        return self
            
    def GetTimer(self):
        """Get the scraped boss timer data.

        Returns:
            list: A list of lists containing the boss timer data, where each sublist contains the time and the bosses.
        """
        return self.__data
    
    def GetTimerJSON(self, indent=2):
        """Convert the boss timer data to a JSON string.

        Args:
            indent (int, optional): The number of spaces to use for indentation in the JSON output. Defaults to 2.

        Returns:
            str: A JSON string representation of the boss timer data.
        """
        return json.dumps(self.__data, indent=indent)