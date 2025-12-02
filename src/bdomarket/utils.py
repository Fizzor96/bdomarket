# pylint: disable=missing-module-docstring, line-too-long
import json
import os
from functools import wraps
from collections import defaultdict
from datetime import datetime, timezone
from importlib.metadata import PackageNotFoundError, version
from typing import Optional

import aiohttp
import requests
from bs4 import BeautifulSoup

from .identifiers import ItemProp, PigCave, Server
from .response import ApiResponse

def experimental(stage="experimental"):
    """Decorator to mark a function as experimental, printing a warning when it is called.

    Args:
        stage (str, optional): The experimental stage label to display. Defaults to "experimental".
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"⚠️  {func.__name__} is {stage}.")
            return func(*args, **kwargs)
        return wrapper
    return decorator

def check_for_updates():
    """Check if a package has an update available on PyPI.
    """
    package = "bdomarket"
    try:
        installed_version = version(package)
    except PackageNotFoundError:
        installed_version = None
    latest_version = None
    try:
        url = f"https://pypi.org/pypi/{package}/json"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            latest_version = response.json()["info"]["version"]
    except requests.RequestException as e:
        print(f"Update check failed: {e}")
        return

    if latest_version and latest_version != installed_version:
        print(f"🔔 Update available for {package}: {installed_version or 'Not installed'} → {latest_version}")
    else:
        print(f"✅ {package} is up to date ({installed_version})")
    print("Stay Updated!")
    print("Join our Discord community for the latest updates, news, and exclusive information:")
    print("https://discord.gg/hSWHfhSpDe")

def timestamp_to_datetime(timestamp: float) -> datetime:
    """Convert a timestamp to a UTC datetime object.

    Args:
        timestamp (float): Unix timestamp.

    Returns:
        datetime: Datetime object in UTC timezone.
    """
    return datetime.fromtimestamp(timestamp, tz=timezone.utc)

def datetime_to_timestamp(dt: datetime) -> float:
    """Convert a datetime object to a Unix timestamp.

    Args:
        dt (datetime): Datetime object.

    Returns:
        float: Unix timestamp.
    """
    return dt.timestamp()

def get_items_by_name_from_db(db: str, name: str = "") -> list:
    """Retrieve items from a database by name.

    Args:
        db (str): Database containing items with 'name' keys.
        name (str, optional): Name to search for. Defaults to "".

    Returns:
        list: List of items matching the given name.
    """
    name_index = defaultdict(list)
    for item in db:
        name_index[item["name"]].append(item) # type: ignore
    return name_index.get(name, [])

def get_items_by_id_from_db(db: str, item_id: int = 0) -> list:
    """Retrieve items from a database by ID.

    Args:
        db (str): Database containing items with 'id' keys.
        id (int, optional): ID to search for. Defaults to 0.

    Returns:
        list: List of items matching the given ID.
    """
    id_index = defaultdict(list)
    for item in db:
        id_index[item["id"]].append(item) # type: ignore
    return id_index.get(item_id, [])

def search_items_by_name(file_path, search_string) -> list:
    """Search items by name in a JSON file.

    Args:
        file_path (str): Path to the JSON file.
        search_string (str): String to search in item names.

    Returns:
        list: List of items with names containing the search string (case-insensitive).
    """
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    matches = [item for item in data['content']
               if search_string.lower() in item['name'].lower()]
    return matches

def search_items_by_id(file_path, search_id) -> list:
    """Search items by ID in a JSON file.

    Args:
        file_path (str): Path to the JSON file.
        search_id (int): ID to search for.

    Returns:
        list: List of items with the specified ID.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    matches = [item for item in data['content'] if item['id'] == search_id]
    return matches

@experimental("beta")
class Pig:
    """Handles interactions with the Pig Cave API to fetch status data for a specified region.
    """
    def __init__(self, region: PigCave = PigCave.EU):
        """Initialize Pig with a region.

        Args:
            region (PigCave, optional): Region for Pig Cave API. Defaults to PigCave.EU.
        """
        self._region = region
        self._status: Optional[str] = None

    @experimental("beta")
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

@experimental("beta")
class Boss:
    """Scrapes and provides boss timer data from mmotimer.com for a specified server region.
    """
    def __init__(self, server: Server = Server.EU):
        """Initialize a Boss object with a server region.

        Args:
            server (Server, optional): Server region for boss timer data. Defaults to Server.EU.
        """
        self.__url = f"https://mmotimer.com/bdo/?server={server.value}"
        self.__data = []
        self.__content = ""

    @experimental("beta")
    def scrape(self) -> "Boss":
        """Scrape the boss timer data from the website.

        Returns:
            Boss: The instance itself for method chaining.
        """
        self.__content = requests.get(self.__url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Connection": "keep-alive",
        }, timeout=5).content

        soup = BeautifulSoup(self.__content, 'html.parser')

        table = soup.find('table', class_='main-table')
        thead = table.find('thead')  # type: ignore
        time_headers = [th.text.strip() for th in thead.find_all('th')][1:]  # type: ignore
        self.__data = []

        tbody = table.find('tbody')  # type: ignore
        for row in tbody.find_all('tr'):  # type: ignore
            cells = row.find_all(['th', 'td'])  # type: ignore
            day = cells[0].text.strip()

            for i, cell in enumerate(cells[1:]):
                time = time_headers[i]

                if cell.text.strip() == "-":
                    continue

                bosses = [span.text.strip() for span in cell.find_all('span')]  # type: ignore

                if bosses:
                    self.__data.append([f"{day} {time}", ', '.join(bosses)])
        return self

    @experimental("beta")
    def get_timer(self) -> list:
        """Get the scraped boss timer data.

        Returns:
            list: A list of lists containing the boss timer data, where each sublist contains the time and the bosses.
        """
        return self.__data

    @experimental("beta")
    def get_timer_json(self, indent=2) -> str:
        """Convert the boss timer data to a JSON string.

        Args:
            indent (int, optional): Number of spaces for JSON indentation. Defaults to 2.

        Returns:
            str: JSON string of the boss timer data.
        """
        return json.dumps(self.__data, indent=indent)

@experimental("beta")
class Item:
    """Represents an item with its ID, name, SID, and grade, and provides methods for icon retrieval and serialization.
    """
    def __init__(self, item_id: str = "735008", name: str = ""):
        """Initialize an Item object.

        Args:
            id (str, optional): Unique identifier for the item. Defaults to "735008".
            name (str, optional): Name of the item. Defaults to "".
        """
        self.id = item_id
        self.name = name
        self.sid = 0
        self.grade = 0

    @experimental("beta")
    def __repr__(self) -> str:
        """Representation of the Item object.

        Returns:
            str: String representation with id, name, and sid.
        """
        return f"Item(id={self.id}, name='{self.name}', sid={self.sid})"

    @experimental("beta")
    def __str__(self) -> str:
        """String representation of the Item object.

        Returns:
            str: Descriptive string with name, id, and sid.
        """
        return f"Item: {self.name} (ID: {self.id}, SID: {self.sid})"

    @experimental("beta")
    def to_dict(self) -> dict:
        """Convert the item to a dictionary.

        Returns:
            dict: Dictionary with item’s id, name, sid, and grade.
        """
        return {
            "item_id": self.id,
            "name": self.name,
            "sid": self.sid,
            "grade": self.grade
        }

    @experimental("beta")
    def get_icon(self, folderpath: str = "icons", isrelative: bool = True, filenameprop: ItemProp = ItemProp.ID):
        """Download and save the item’s icon to a specified folder.

        Args:
            folderpath (str, optional): Path to save the icon. Defaults to "icons".
            isrelative (bool, optional): If True, folderpath is relative to the current file. If False, it’s absolute. Defaults to True.
            filenameprop (ItemProp, optional): Use item’s ID or name for the filename. Defaults to ItemProp.ID.
        """
        if not folderpath:
            folderpath = "icons"

        if isrelative:
            folder = folderpath
        else:
            folder = os.path.join(os.path.dirname(__file__), folderpath)

        if not os.path.exists(folder):
            os.makedirs(folder)

        if os.path.exists(os.path.join(folder, f"{self.id}.png")) and filenameprop == ItemProp.ID:
            return

        if os.path.exists(os.path.join(folder, f"{self.name}.png")) and filenameprop == ItemProp.NAME:
            return

        response = requests.get(
            f"https://s1.pearlcdn.com/NAEU/TradeMarket/Common/img/BDO/item/{self.id}.png", timeout=5)
        if 199 < response.status_code < 300:
            with open(f"{folder}/{self.id if filenameprop == ItemProp.ID else self.name}.png", "wb") as file:
                file.write(response.content)
