import requests
import json
from enum import Enum
import json
from datetime import datetime, timezone
import os

# source: https://www.postman.com/bdomarket/arsha-io-bdo-market-api/overview

class ApiVersion(Enum):
    V1 = "v1"
    V2 = "v2"

class MarketRegion(Enum):
    NA = "na"
    EU = "eu"
    SEA = "sea"
    MENA = "mena"
    KR = "kr"
    RU = "ru"
    JP = "jp"
    TH = "th"
    TW = "tw"
    SA = "sa"
    CONSOLE_EU = "console_eu"
    CONSOLE_NA = "console_na"
    CONSOLE_ASIA = "console_asia"
    
class Locale(Enum):
    English = "en"
    German = "de"
    French = "fr"
    Russian = "ru"
    SpanishEU = "es"
    PortugueseRedFox = "sp"
    Portuguese = "pt"
    Japanese = "jp"
    Korean = "kr"
    Thai = "th"
    Turkish = "tr"
    ChineseTaiwan = "tw"
    ChineseMainland = "cn"
    
class PigCave(Enum):
    EU = "eupig"
    JP = "jpig"
    KR = "krpig"
    RU = "rupig"
    SA = "sapig"
    TW = "twpig"
    ASIA = "asiapig"
    MENA = "menapig"
    
def ConvertTimestamp(timestamp_ms:float, format: str = "%Y-%m-%d") -> str:
    """Convert a timestamp in milliseconds to a formatted date string.

    Args:
        timestamp_ms (float): The timestamp in milliseconds to convert.
        format (str, optional): The format string for the output date. Defaults to "%Y-%m-%d".

    Returns:
        str: A formatted date string
    """
    return datetime.utcfromtimestamp(timestamp_ms / 1000).strftime(format)

def TimestampToDatetime(timestamp):
    return datetime.fromtimestamp(timestamp, timezone.utc)

def DatetimeToTimestamp(dt):
    return datetime.timestamp(dt)
        
class ApiResponse:
    def __init__(self, success: bool = False, statuscode: int = -1, message: str = "", content: str = ""):
        self.success = success
        self.statuscode = statuscode
        self.message: str = message
        self.content: str = content if content else ""
        
    def __str__(self):
        """String representation of the ApiResponse object.

        Returns:
            str: A string containing the success status, status code, message, and content of the response.
        """
        return f"success: {self.success}\nstatuscode: {self.statuscode}\nmessage: {self.message}\ncontent: {self.content}"
    
    def Deserialize(self):
        """Deserialize the content of the ApiResponse object from JSON format.

        Raises:
            Exception: If the content cannot be deserialized into a Python object.

        Returns:
            dict: The deserialized content as a Python dictionary.
        """
        try:
            return json.loads(self.content)
        except:
            raise Exception("Could not get IterableObject!")
        
    def SaveToFile(self, path: str, mode: str = "w"):
        """Save the ApiResponse content to a file in JSON format.

        Args:
            path (str): The file path where the content should be saved.
        """
        # TODO: improve this like in Item.GetIcon
        folder = os.path.dirname(path)
        os.makedirs(folder, exist_ok=True)
        data = {
            "success": self.success,
            "statuscode": self.statuscode,
            "message": self.message,
            "content": json.loads(self.content)
        }
        with open(path, mode, encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

class Market:
    def __init__(self, region: MarketRegion = MarketRegion.EU, apiversion: ApiVersion = ApiVersion.V2, language: Locale = Locale.English):
        """ Initializes the Market object with the specified region, API version, and language.

        Args:
            region (AvailableRegions, optional): The region to use for the API requests. Defaults to AvailableRegions.EU.
            apiversion (AvailableApiVersions, optional): The API version to use for the requests. Defaults to AvailableApiVersions.V2.
            language (SupportedLanguages, optional): The language to use for the API responses. Defaults to SupportedLanguages.English.
        """
        self.__baseurl = "https://api.arsha.io"
        self.__apiversion = apiversion.value
        self.__apiregion = region.value
        self.__apilang = language.value
        
    def __makerequest(self, method, endpoint, jsondata = None, data = None, headers = None, params = None,) -> ApiResponse:
        """Make a request to the API.

        Args:
            method (_type_): The HTTP method to use for the request (e.g., GET, POST).
            endpoint (_type_): The API endpoint to call.
            jsondata (_type_, optional): The JSON data to send in the request body. Defaults to None.
            data (_type_, optional): The form data to send in the request body. Defaults to None.
            headers (_type_, optional): The headers to include in the request. Defaults to None.
            params (_type_, optional): The query parameters to include in the request URL. Defaults to None.

        Returns:
            ApiResponse: An ApiResponse object containing the success status, status code, message, and content of the response.
        """
        response = requests.request(method=method, 
                                    url=f"{self.__baseurl}/{self.__apiversion}/{self.__apiregion}/{endpoint}", 
                                    params=params,
                                    json=jsondata, 
                                    data=data,
                                    headers=headers,
                                    timeout=10)
        return ApiResponse(success= True if 199 < response.status_code < 299 else False, 
                          statuscode=response.status_code, 
                          message=response.reason if response.reason else "No message provided",
                          content=json.dumps(response.json(), indent=2))
    
    def GetWorldMarketWaitList(self) -> ApiResponse:
        """Returns a parsed variant of the current items waiting to be listed on the central market.  

        Returns:
            ApiResponse: An ApiResponse object containing the success status, status code, message, and content of the response.
        """
        return self.__makerequest("GET", "GetWorldMarketWaitList")
    
    def PostGetWorldMarketWaitList(self) -> ApiResponse:
        """Returns a parsed variant of the current items waiting to be listed on the central market.  

        Returns:
            ApiResponse: An ApiResponse object containing the success status, status code, message, and content of the response.
        """
        return self.__makerequest("POST", "GetWorldMarketWaitList") 
    
    def GetWorldMarketHotList(self) -> ApiResponse:
        """Get current market hotlist.

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items currently on market hotlist.
        """
        return self.__makerequest("GET", "GetWorldMarketHotList")
    
    def PostGetWorldMarketHotList(self) -> ApiResponse:
        """Get current market hotlist

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items currently on market hotlist.
        """
        return self.__makerequest("POST", "GetWorldMarketHotList")
    
    def GetMarketPriceInfo(self, id:list[str], sid:list[str]) -> ApiResponse:
        """Get price history for an item or list of items. If multiple ids are given, returns a JsonArray of JsonObject of the items' price history. If only one id is given, returns a JsonObject of the item's price history.

        Args:
            id (list[str]): itemid(s)
            sid (list[str]): subid(s) like enhancement level

        Returns:
            ApiResponse: standardized response. Returned values in content.history: key (eg. "1745193600000"): Unix timestamps in milliseconds (from utils use ConvertTimestamp), value (eg. 75000000000): item silver value
        """
        query_params = {
            "id": id,
            "sid": sid,
            "lang": self.__apilang
        }
        return self.__makerequest("GET", "GetMarketPriceInfo", params=query_params)
    
    def PostGetMarketPriceInfo(self, id:list[str], sid:list[str]) -> ApiResponse:
        """Get price history for an item or list of items. If multiple ids are given, returns a JsonArray of JsonObject of the items' price history. If only one id is given, returns a JsonObject of the item's price history.

        Args:
            id (list[str]): itemid(s)
            sid (list[str]): subid(s) like enhancement level

        Returns:
            ApiResponse: standardized response. Returned values in content.history: key (eg. "1745193600000"): Unix timestamps in milliseconds (from utils use ConvertTimestamp), value (eg. 75000000000): item silver value
        """
        # ! Not working: can get valid response, but it makes no sense.
        return self.__makerequest("POST", "GetMarketPriceInfo", params={"lang": self.__apilang}, jsondata=[{"id": id, "sid": sid}])
    
    def GetWorldMarketSearchList(self, ids:list[str]) -> ApiResponse:
        """Search for items by their id(s).

        Args:
            ids (str): itemid(s).

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items matching the search criteria.
        """
        return self.__makerequest("GET", "GetWorldMarketSearchList", params={
            "ids": ids,
            "lang": self.__apilang
        })
    
    def PostGetWorldMarketSearchList(self, ids:list[str]) -> ApiResponse:
        """Search for items by their id(s).

        Args:
            ids (list[str]): itemid(s).

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items matching the search criteria.
        """
        return self.__makerequest("POST", "GetWorldMarketSearchList", jsondata=ids, params={"lang": self.__apilang})
    
    def GetWorldMarketList(self, maincategory:str, subcategory:str) -> ApiResponse:
        """Get items from a specific category or subcategory.

        Args:
            maincategory (str): maincategory
            subcategory (str): subcategory

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items in the specified category or subcategory.
        """
        return self.__makerequest("GET", "GetWorldMarketList", params={
            "mainCategory": maincategory,
            "subCategory": subcategory,
            "lang": self.__apilang
        })
    
    def PostGetWorldMarketList(self, maincategory:str, subcategory:str) -> ApiResponse:
        """Get items from a specific category or subcategory.

        Args:
            maincategory (str): maincategory
            subcategory (str): subcategory

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items in the specified category or subcategory.
        """
        return self.__makerequest("POST", "GetWorldMarketList", jsondata={"mainCategory":maincategory, "subCategory": subcategory}, params={"lang":self.__apilang})
    
    def GetWorldMarketSubList(self, id:list[str]) -> ApiResponse:
        """Get parsed item or items from min to max enhance (if available).

        Args:
            id (list[str]): itemid(s)

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items with their subid(s) (enhancement level).
        """
        return self.__makerequest("GET", "GetWorldMarketSubList", params={"id":id, "lang":self.__apilang})
    
    def PostGetWorldMarketSubList(self, id:list[str]) -> ApiResponse:
        """Get parsed item or items from min to max enhance (if available).

        Args:
            id (str): itemid(s)

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items with their subid(s) (enhancement level).
        """
        return self.__makerequest("POST", "GetWorldMarketSubList", jsondata=id, params={"lang":self.__apilang})
    
    def GetBiddingInfo(self, id:list[str], sid:list[str]) -> ApiResponse:
        """Get orders of an item or list of items

        Args:
            id (list[str]): itemid(s)
            sid (list[str]): subid(s)

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items' bidding information.
        """
        return self.__makerequest("GET", "GetBiddingInfoList", params={"id": id, "sid":sid, "lang":self.__apilang})
    
    def PostGetBiddingInfo(self, id:list[str], sid:list[str]) -> ApiResponse:
        """Get orders of an item or list of items

        Args:
            id (list[str]): itemid(s)
            sid (list[str]): subid(s)

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items' bidding information.
        """
        # ! Not working: An unexpected error occurred
        return self.__makerequest("POST", "GetBiddingInfoList", jsondata=[{"id":id, "sid":sid}], params={"lang":self.__apilang})
    
    def GetPearlItems(self) -> ApiResponse:
        """Convenience method for getting all pearl items.

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of pearl items.
        """
        return self.__makerequest("GET", "pearlItems", params={"lang":self.__apilang})
    
    def PostGetPearlItems(self) -> ApiResponse:
        """Convenience method for getting all pearl items.

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of pearl items.
        """
        return self.__makerequest("POST", "pearlItems", params={"lang":self.__apilang})
    
    def GetMarket(self) -> ApiResponse:
        """Convenience method for getting all items currently available on the market.

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items currently available on the market.
        """
        # ! Not working: One or more requests returned invalid data (probably blocked by Imperva). Try again later.
        return self.__makerequest("GET", "market", params={"lang":self.__apilang})
    
    def PostGetMarket(self) -> ApiResponse:
        """Convenience method for getting all items currently available on the market.

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items currently available on the market.
        """
        # ! Not working: One or more requests returned invalid data (probably blocked by Imperva). Try again later.
        return self.__makerequest("POST", "market", params={"lang":self.__apilang})
    
    def GetItem(self, ids:list[str] = []) -> ApiResponse:
        """Get item information by its id(s).

        Args:
            ids (list[str], optional): A list of item ids to retrieve information for. Defaults to an empty list.

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items with their id, name, and sid.
        If no ids are provided, returns an empty ApiResponse.
        """
        if not ids:
            return ApiResponse()
        response = requests.request(method="GET", 
                                    url=f"{self.__baseurl}/util/db", 
                                    params={"id":ids, "lang":self.__apilang},
                                    timeout=10)
        
        return ApiResponse(success= True if 199 < response.status_code < 299 else False, 
                          statuscode=response.status_code, 
                          message=response.reason if response.reason else "No message provided",
                          content=json.dumps(json.loads(response.content), indent=2, ensure_ascii=False))
    
        
    def ItemDatabaseDump(self, startid: int, endid: int, chunksize: int = 100) -> ApiResponse:
        """Dump the item database from startid to endid in chunks of chunksize.

        Args:
            startid (int): _description_
            endid (int): _description_
            chunksize (int, optional): The number of items to fetch in each request. Defaults to 100.

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items with their id, name, and sid.
        """
        chunksize = min(chunksize, 100)  # API limit

        items = []
        for i in range(startid, endid + 1, chunksize):
            ids = [str(j) for j in range(i, min(i + chunksize, endid + 1))]
            response = self.GetItem(ids)

            if response.success:
                deserialized = response.Deserialize() or []
                items.extend(item for item in deserialized if item is not None)
            else:
                print(f"Error fetching items {ids}: {response.message}")

        return ApiResponse(
            content=json.dumps(items, indent=2, ensure_ascii=False),
            success=True,
            statuscode=200,
            message="Item database dump completed successfully."
        )
        
    def GetPigCaveStatus(self, region: PigCave = PigCave.EU) -> ApiResponse:
        """Get Pig Cave status by region (garmoth.com data)

        Args:
            region (PigCave, optional): Region and endpoint at the same time. Defaults to PigCave.EU.

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items with their id, name, and sid.
        """
        response = requests.request("GET", f"http://node63.lunes.host:3132/{region.value}")
        return ApiResponse(
            success=True if 199 < response.status_code < 299 else False,
            statuscode=response.status_code,
            message=response.reason if response.reason else "No message provided",
            content=response.text
        )