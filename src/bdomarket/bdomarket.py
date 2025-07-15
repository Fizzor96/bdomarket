import requests
import json
from enum import Enum
import json
from datetime import datetime
import os

# source: https://www.postman.com/bdomarket/arsha-io-bdo-market-api/overview

class AvailableApiVersions(Enum):
    V1 = "v1"
    V2 = "v2"

class AvailableRegions(Enum):
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
    
class SupportedLanguages(Enum):
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
        
class ApiResponse:
    def __init__(self, success: bool = False, statuscode: int = -1, message: str = "", content: str = ""):
        self.success = success
        self.statuscode = statuscode
        self.message: str = message
        self.content: str = content if content else ""
        
    def __str__(self):
        return f"success: {self.success}\nstatuscode: {self.statuscode}\nmessage: {self.message}\ncontent: {self.content}"
    
    def Deserialize(self):
        try:
            return json.loads(self.content)
        except:
            raise Exception("Could not get IterableObject!")
        
    def SaveToFile(self, path: str):
        folder = os.path.dirname(path)
        os.makedirs(folder, exist_ok=True)
        data = {
            "success": self.success,
            "statuscode": self.statuscode,
            "message": self.message,
            "content": json.loads(self.content)
        }
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

def ConvertTimestamp(timestamp_ms:float):
    return datetime.utcfromtimestamp(timestamp_ms / 1000).strftime("%Y-%m-%d")

class Market:
    def __init__(self, region: AvailableRegions = AvailableRegions.EU, apiversion: AvailableApiVersions = AvailableApiVersions.V2, language: SupportedLanguages = SupportedLanguages.English):
        self.__baseurl = "https://api.arsha.io"
        self.__apiversion = apiversion.value
        self.__apiregion = region.value
        self.__apilang = language.value
        
    def __makerequest(self, method, endpoint, jsondata = None, data = None, headers = None, params = None,) -> ApiResponse:
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
            VeliaInnResponse: standardized response.
        """
        return self.__makerequest("GET", "GetWorldMarketWaitList")
    
    def PostGetWorldMarketWaitList(self) -> ApiResponse:
        """Returns a parsed variant of the current items waiting to be listed on the central market.  

        Returns:
            VeliaInnResponse: standardized response.
        """
        return self.__makerequest("POST", "GetWorldMarketWaitList") 
    
    def GetWorldMarketHotList(self) -> ApiResponse:
        """Get current market hotlist.

        Returns:
            VeliaInnResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items currently on market hotlist.
        """
        return self.__makerequest("GET", "GetWorldMarketHotList")
    
    def PostGetWorldMarketHotList(self) -> ApiResponse:
        """Get current market hotlist

        Returns:
            VeliaInnResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items currently on market hotlist.
        """
        return self.__makerequest("POST", "GetWorldMarketHotList")
    
    def GetMarketPriceInfo(self, id:list[str], sid:list[str]) -> ApiResponse:
        """Get price history for an item or list of items. If multiple ids are given, returns a JsonArray of JsonObject of the items' price history. If only one id is given, returns a JsonObject of the item's price history.

        Args:
            id (list[str]): itemid(s)
            sid (list[str]): subid(s) like enhancement level

        Returns:
            VeliaInnResponse: standardized response. Returned values in content.history: key (eg. "1745193600000"): Unix timestamps in milliseconds (from utils use ConvertTimestamp), value (eg. 75000000000): item silver value
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
            VeliaInnResponse: standardized response. Returned values in content.history: key (eg. "1745193600000"): Unix timestamps in milliseconds (from utils use ConvertTimestamp), value (eg. 75000000000): item silver value
        """
        # ! Not working: can get valid response, but it makes no sense.
        return self.__makerequest("POST", "GetMarketPriceInfo", params={"lang": self.__apilang}, jsondata=[{"id": id, "sid": sid}])
    
    def GetWorldMarketSearchList(self, ids:list[str]) -> ApiResponse:
        """Search for items by their id(s).

        Args:
            ids (str): itemid(s).

        Returns:
            VeliaInnResponse: Standardized response.
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
            VeliaInnResponse: Standardized response.
        """
        return self.__makerequest("POST", "GetWorldMarketSearchList", jsondata=ids, params={"lang": self.__apilang})
    
    def GetWorldMarketList(self, maincategory:str, subcategory:str) -> ApiResponse:
        """Get items from a specific category or subcategory.

        Args:
            maincategory (str): maincategory
            subcategory (str): subcategory

        Returns:
            VeliaInnResponse: Standardized response.
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
            VeliaInnResponse: Standardized response.
        """
        return self.__makerequest("POST", "GetWorldMarketList", jsondata={"mainCategory":maincategory, "subCategory": subcategory}, params={"lang":self.__apilang})
    
    def GetWorldMarketSubList(self, id:list[str]) -> ApiResponse:
        """Get parsed item or items from min to max enhance (if available).

        Args:
            id (list[str]): itemid(s)

        Returns:
            VeliaInnResponse: Standardized response.
        """
        return self.__makerequest("GET", "GetWorldMarketSubList", params={"id":id, "lang":self.__apilang})
    
    def PostGetWorldMarketSubList(self, id:list[str]) -> ApiResponse:
        """Get parsed item or items from min to max enhance (if available).

        Args:
            id (str): itemid(s)

        Returns:
            VeliaInnResponse: Standardized response.
        """
        return self.__makerequest("POST", "GetWorldMarketSubList", jsondata=id, params={"lang":self.__apilang})
    
    def GetBiddingInfo(self, id:list[str], sid:list[str]) -> ApiResponse:
        """Get orders of an item or list of items

        Args:
            id (list[str]): itemid(s)
            sid (list[str]): subid(s)

        Returns:
            VeliaInnResponse: Standardized response.
        """
        return self.__makerequest("GET", "GetBiddingInfoList", params={"id": id, "sid":sid, "lang":self.__apilang})
    
    def PostGetBiddingInfo(self, id:list[str], sid:list[str]) -> ApiResponse:
        """Get orders of an item or list of items

        Args:
            id (list[str]): itemid(s)
            sid (list[str]): subid(s)

        Returns:
            VeliaInnResponse: Standardized response.
        """
        # ! Not working: An unexpected error occurred
        return self.__makerequest("POST", "GetBiddingInfoList", jsondata=[{"id":id, "sid":sid}], params={"lang":self.__apilang})
    
    def GetPearlItems(self) -> ApiResponse:
        """Convenience method for getting all pearl items.

        Returns:
            VeliaInnResponse: Standardized response.
        """
        return self.__makerequest("GET", "pearlItems", params={"lang":self.__apilang})
    
    def PostGetPearlItems(self) -> ApiResponse:
        """Convenience method for getting all pearl items.

        Returns:
            VeliaInnResponse: Standardized response.
        """
        return self.__makerequest("POST", "pearlItems", params={"lang":self.__apilang})
    
    def GetMarket(self) -> ApiResponse:
        """Convenience method for getting all items currently available on the market.

        Returns:
            VeliaInnResponse: Standardized response.
        """
        # ! Not working: One or more requests returned invalid data (probably blocked by Imperva). Try again later.
        return self.__makerequest("GET", "market", params={"lang":self.__apilang})
    
    def PostGetMarket(self) -> ApiResponse:
        """Convenience method for getting all items currently available on the market.

        Returns:
            VeliaInnResponse: Standardized response.
        """
        # ! Not working: One or more requests returned invalid data (probably blocked by Imperva). Try again later.
        return self.__makerequest("POST", "market", params={"lang":self.__apilang})