import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timezone
import os
from .identifiers import Server, ItemProp, PigCave
from .response import ApiResponse
import aiohttp
from typing import Optional
from collections import defaultdict


def timestamp_to_datetime(timestamp: float) -> datetime:
    return datetime.fromtimestamp(timestamp, tz=timezone.utc)


def datetime_to_timestamp(dt: datetime) -> float:
    return dt.timestamp()


def get_items_by_name_from_db(db, name: str = ""):
    name_index = defaultdict(list)
    for item in db:
        name_index[item["name"]].append(item)
    return name_index.get(name, [])


def get_items_by_id_from_db(db, id: int = 0):
    id_index = defaultdict(list)
    for item in db:
        id_index[item["id"]].append(item)
    return id_index.get(id, [])

def search_items_by_name(file_path, search_string):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    matches = [item for item in data['content']
               if search_string.lower() in item['name'].lower()]
    return matches

def search_items_by_id(file_path, search_id):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    matches = [item for item in data['content'] if item['id'] == search_id]
    return matches


class Pig:
    def __init__(self, region: PigCave = PigCave.EU):
        """Initialize Pig with a region.

        Args:
            region (PigCave, optional): Region for Pig Cave API. Defaults to PigCave.EU.
        """
        self._region = region
        self._status: Optional[str] = None

    async def get_status(self) -> ApiResponse:
        """Fetch Pig Cave status (garmoth data).

        Returns:
            ApiResponse: Contains success status, status code, message, and response content.

        Raises:
            aiohttp.ClientError: If the HTTP request fails.
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"http://node70.lunes.host:3030/{self._region.value}") as response:
                    content = await response.text()
                    self._status = content
                    return ApiResponse(
                        success=200 <= response.status <= 299,
                        status_code=response.status,
                        message=self._region.value,
                        content=content
                    )
        except aiohttp.ClientError as e:
            return ApiResponse(
                success=False,
                status_code=0,
                message=f"Request failed: {str(e)}",
            )


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
        thead = table.find('thead')  # type: ignore
        # time_headers = [th.text.strip() for th in thead.find_all('th')]
        time_headers = [th.text.strip()
                        for th in thead.find_all('th')][1:]  # type: ignore
        self.__data = []

        # Iterate rows (days) in <tbody>
        tbody = table.find('tbody')  # type: ignore
        for row in tbody.find_all('tr'):  # type: ignore
            cells = row.find_all(['th', 'td'])  # type: ignore
            day = cells[0].text.strip()  # first cell is day

            for i, cell in enumerate(cells[1:]):  # skip day column
                time = time_headers[i]

                if cell.text.strip() == "-":
                    continue  # skip empty slots

                bosses = [span.text.strip()
                          for span in cell.find_all('span')]  # type: ignore

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


class Item:
    def __init__(self, id: str = "735008", name: str = ""):
        """Initialize an Item object.

        Args:
            id (str, optional): The unique identifier for the item. Defaults to "735008".
            name (str, optional): The name of the item. Defaults to "Blackstar Shuriken".
            sid (str, optional): The sidentifier for the item can be the enchancement level. Defaults to "0".
        """
        self.id = id
        self.name = name  # TODO: implement query by name
        self.sid = 0
        self.grade = 0

    def __repr__(self):
        """Representation of the Item object.

        Returns:
            str: A string representation of the item including its id, name, and sid.
        """
        return f"Item(id={self.id}, name='{self.name}', sid={self.sid})"

    def __str__(self):
        """String representation of the Item object.

        Returns:
            str: A string describing the item with its name, id, and sid.
        """
        return f"Item: {self.name} (ID: {self.id}, SID: {self.sid})"

    def to_dict(self):
        """Convert the item to a dictionary representation.

        Returns:
            dict: A dictionary containing the item's id, name, and sid.
        """
        return {
            "item_id": self.id,
            "name": self.name,
            "sid": self.sid,
            "grade": self.grade
        }

    def GetIcon(self, folderpath: str = "icons", isrelative: bool = True, filenameprop: ItemProp = ItemProp.ID):
        """Download the icon for the item and save it to the specified folder.

        Args:
            folderpath (str, optional): The path to the folder where the icon will be saved. Defaults to "icons".
            isrelative (bool, optional): If True, the folderpath is treated as relative to the current file. If False, it is treated as absolute. Defaults to True.
            filenameprop (ItemProp, optional): Determines whether to use the item's ID or name for the filename. Defaults to ItemProp.ID.
        """
        if not folderpath:
            folderpath = "icons"

        # Determine the folder path based on whether it is relative or absolute
        if isrelative:
            folder = folderpath
        else:
            folder = os.path.join(os.path.dirname(__file__), folderpath)

        # Check if the folder exists
        if not os.path.exists(folder):
            os.makedirs(folder)

        # Check if file already exists with id
        if os.path.exists(os.path.join(folder, f"{self.id}.png")) and filenameprop == ItemProp.ID:
            return

        # Check if file already exists with name
        if os.path.exists(os.path.join(folder, f"{self.name}.png")) and filenameprop == ItemProp.NAME:
            return

        # If folder exist but file does not, we can download the icon
        response = requests.get(
            f"https://s1.pearlcdn.com/NAEU/TradeMarket/Common/img/BDO/item/{self.id}.png")
        if 199 < response.status_code < 300:
            with open(f"{folder}/{self.id if filenameprop == ItemProp.ID else self.name}.png", "wb") as file:
                file.write(response.content)
