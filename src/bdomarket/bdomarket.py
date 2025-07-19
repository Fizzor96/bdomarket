import requests
import json
import os
import aiohttp
import asyncio
from typing import List, Optional, Dict, Any
from .identifiers import ApiVersion, Locale, MarketRegion
from .utils import timestamp_to_datetime

class ApiResponse:
    def __init__(self, success: bool = False, status_code: int = -1, message: str = "", content: str = ""):
        self.success = success
        self.status_code = status_code
        self.message = message
        self.content = content

    def __str__(self) -> str:
        """String representation of the ApiResponse object.

        Returns:
            str: A string containing the success status, status code, message, and content of the response.
        """
        return f"success: {self.success}\nstatus_code: {self.status_code}\nmessage: {self.message}\ncontent: {json.dumps(self.content, indent=2, ensure_ascii=False)}"

    # def deserialize(self) -> Dict[str, Any]:
    #     try:
    #         return json.loads(self.content) if self.content else {}
    #     except json.JSONDecodeError:
    #         raise ValueError("Failed to deserialize content")

    def save_to_file(self, path: str, mode: str = "w") -> None:
        """Save the ApiResponse content to a file in JSON format.

        Args:
            path (str): The file path where the content should be saved.
        """
        os.makedirs(os.path.dirname(path), exist_ok=True)
        data = {
            "success": self.success,
            "status_code": self.status_code,
            "message": self.message,
            "content": self.content
        }
        with open(path, mode, encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

class Market:
    def __init__(self, region: MarketRegion = MarketRegion.EU, api_version: ApiVersion = ApiVersion.V2, language: Locale = Locale.English):
        """ Initializes the Market object with the specified region, API version, and language.

        Args:
            region (AvailableRegions, optional): The region to use for the API requests. Defaults to AvailableRegions.EU.
            apiversion (AvailableApiVersions, optional): The API version to use for the requests. Defaults to AvailableApiVersions.V2.
            language (SupportedLanguages, optional): The language to use for the API responses. Defaults to SupportedLanguages.English.
        """
        self._base_url = "https://api.arsha.io"
        self._api_version = api_version.value
        self._api_region = region.value
        self._api_lang = language.value
        self._session = requests.Session()

    async def _make_request_async(self, method: str, endpoint: str, json_data: Optional[Any] = None,
                                data: Optional[Any] = None, headers: Optional[Dict] = None,
                                params: Optional[Dict] = None) -> ApiResponse:
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method=method,
                url=f"{self._base_url}/{self._api_version}/{self._api_region}/{endpoint}",
                params=params,
                json=json_data,
                data=data,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                # try:
                #     content = await response.json()
                # except aiohttp.ContentTypeError:
                #     content = await response.text()
                return ApiResponse(
                    success=response.status >= 200 and response.status <= 299,
                    status_code=response.status,
                    message=response.reason or "No message provided",
                    # content=content if isinstance(content, dict) else {"message": content}
                    content=json.loads(json.dumps(await response.json(), indent=2))
                )

    def _make_request_sync(self, method: str, endpoint: str, json_data: Optional[Any] = None,
                          data: Optional[Any] = None, headers: Optional[Dict] = None,
                          params: Optional[Dict] = None) -> ApiResponse:
        try:
            # Reinitialize session if None
            if self._session is None:
                self._session = requests.Session()
            response = self._session.request(
                method=method,
                url=f"{self._base_url}/{self._api_version}/{self._api_region}/{endpoint}",
                params=params,
                json=json_data,
                data=data,
                headers=headers,
                timeout=10
            )
            content = response.json() if response.content else {}
            return ApiResponse(
                success=response.status_code >= 200 and response.status_code <= 299,
                status_code=response.status_code,
                message=response.reason or "No message provided",
                content=json.dumps(content, indent=2, ensure_ascii=False)
            )
        except requests.RequestException as e:
            return ApiResponse(message=str(e))
        
    def close(self):
        """Close the synchronous requests session."""
        if self._session is not None:
            self._session.close()
            self._session = None
        
    async def get_world_market_wait_list(self) -> ApiResponse:
        """Returns a parsed variant of the current items waiting to be listed on the central market.  

        Returns:
            ApiResponse: An ApiResponse object containing the success status, status code, message, and content of the response.
        """
        return await self._make_request_async("GET", "GetWorldMarketWaitList")
    
    def get_world_market_wait_list_sync(self) -> ApiResponse:
        """Returns a parsed variant of the current items waiting to be listed on the central market.  

        Returns:
            ApiResponse: An ApiResponse object containing the success status, status code, message, and content of the response.
        """
        return self._make_request_sync("GET", "GetWorldMarketWaitList")

    async def post_world_market_wait_list(self) -> ApiResponse:
        """Returns a parsed variant of the current items waiting to be listed on the central market.  

        Returns:
            ApiResponse: An ApiResponse object containing the success status, status code, message, and content of the response.
        """
        return await self._make_request_async("POST", "GetWorldMarketWaitList")
    
    def post_world_market_wait_list_sync(self) -> ApiResponse:
        """Returns a parsed variant of the current items waiting to be listed on the central market.  

        Returns:
            ApiResponse: An ApiResponse object containing the success status, status code, message, and content of the response.
        """
        return self._make_request_sync("POST", "GetWorldMarketWaitList")

    async def get_world_market_hot_list(self) -> ApiResponse:
        """Get current market hotlist.

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items currently on market hotlist.
        """
        return await self._make_request_async("GET", "GetWorldMarketHotList")
    
    def get_world_market_hot_list_sync(self) -> ApiResponse:
        """Get current market hotlist.

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items currently on market hotlist.
        """
        return self._make_request_sync("GET", "GetWorldMarketHotList")

    async def post_world_market_hot_list(self) -> ApiResponse:
        """Get current market hotlist

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items currently on market hotlist.
        """
        return await self._make_request_async("POST", "GetWorldMarketHotList")
    
    def post_world_market_hot_list_sync(self) -> ApiResponse:
        """Get current market hotlist

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items currently on market hotlist.
        """
        return self._make_request_sync("POST", "GetWorldMarketHotList")

    async def get_market_price_info(self, ids: List[str], sids: List[str], convertdate: bool = True, formatprice: bool = False) -> ApiResponse:
        """Get price history for an item or list of items. If multiple ids are given, returns a JsonArray of JsonObject of the items' price history. If only one id is given, returns a JsonObject of the item's price history.

        Args:
            id (List[str]): itemid(s)
            sid (List[str]): subid(s) like enhancement level
            convertdate (bool): Convert unix-like timestamp to UTC datetime. Defaults to True.
            formatprice (bool): Format price, adding separator (,). Defaults to False.

        Returns:
            ApiResponse: standardized response. Returned values in content.history: key (eg. "1745193600000"): Unix timestamps in milliseconds (from utils use ConvertTimestamp), value (eg. 75000000000): item silver value
        """
        params = {"id": ids, "sid": sids, "lang": self._api_lang}
        result = await self._make_request_async("GET", "GetMarketPriceInfo", params=params)
        if convertdate or formatprice:
            # Handle both list and dict cases
            content_list = [result.content] if isinstance(result.content, dict) else result.content
            for item in content_list:
                if "history" in item:
                    new_history = {}
                    for k, v in item["history"].items(): # type: ignore
                        # Convert date if needed
                        new_key = timestamp_to_datetime(float(k) / 1000).strftime("%Y-%m-%d") if convertdate else k
                        # Format price if needed
                        new_value = f"{v:,}" if formatprice else v
                        new_history[new_key] = new_value
                    item["history"] = new_history # type: ignore
            result.content = content_list # type: ignore
        return result
    
    def get_market_price_info_sync(self, ids: List[str], sids: List[str], convertdate: bool = True, formatprice: bool = False) -> ApiResponse:
        """Get price history for an item or list of items. If multiple ids are given, returns a JsonArray of JsonObject of the items' price history. If only one id is given, returns a JsonObject of the item's price history.

        Args:
            id (List[str]): itemid(s)
            sid (List[str]): subid(s) like enhancement level
            convertdate (bool): Convert unix-like timestamp to UTC datetime. Defaults to True.
            formatprice (bool): Format price, adding separator (,). Defaults to False.

        Returns:
            ApiResponse: standardized response. Returned values in content.history: key (eg. "1745193600000"): Unix timestamps in milliseconds (from utils use ConvertTimestamp), value (eg. 75000000000): item silver value
        """
        params = {"id": ids, "sid": sids, "lang": self._api_lang}
        result = self._make_request_sync("GET", "GetMarketPriceInfo", params=params)
        if convertdate or formatprice:
            # Handle both list and dict cases
            content_list = [result.content] if isinstance(result.content, dict) else result.content
            for item in content_list:
                if "history" in item:
                    new_history = {}
                    for k, v in item["history"].items(): # type: ignore
                        # Convert date if needed
                        new_key = timestamp_to_datetime(float(k) / 1000).strftime("%Y-%m-%d") if convertdate else k
                        # Format price if needed
                        new_value = f"{v:,}" if formatprice else v
                        new_history[new_key] = new_value
                    item["history"] = new_history # type: ignore
            result.content = content_list # type: ignore
        return result

    async def post_market_price_info(self, ids: List[str], sids: List[str], convertdate: bool = True, formatprice: bool = False) -> ApiResponse:
        """Get price history for an item or list of items. If multiple ids are given, returns a JsonArray of JsonObject of the items' price history. If only one id is given, returns a JsonObject of the item's price history.

        Args:
            id (List[str]): itemid(s)
            sid (List[str]): subid(s) like enhancement level
            convertdate (bool): Convert unix-like timestamp to UTC datetime. Defaults to True.
            formatprice (bool): Format price, adding separator (,). Defaults to False.

        Returns:
            ApiResponse: standardized response. Returned values in content.history: key (eg. "1745193600000"): Unix timestamps in milliseconds (from utils use ConvertTimestamp), value (eg. 75000000000): item silver value
        """
        result = await self._make_request_async("POST", "GetMarketPriceInfo", params={"lang": self._api_lang},
                                            json_data = [{"id": int(id_), "sid": int(sid)} for id_, sid in zip(ids, sids)])
        if convertdate or formatprice:
            # Handle both list and dict cases
            content_list = [result.content] if isinstance(result.content, dict) else result.content
            for item in content_list:
                if "history" in item:
                    new_history = {}
                    for k, v in item["history"].items(): # type: ignore
                        # Convert date if needed
                        new_key = timestamp_to_datetime(float(k) / 1000).strftime("%Y-%m-%d") if convertdate else k
                        # Format price if needed
                        new_value = f"{v:,}" if formatprice else v
                        new_history[new_key] = new_value
                    item["history"] = new_history # type: ignore
            result.content = content_list # type: ignore
        return result
    
    def post_market_price_info_sync(self, ids: List[str], sids: List[str], convertdate: bool = True, formatprice: bool = False) -> ApiResponse:
        """Get price history for an item or list of items. If multiple ids are given, returns a JsonArray of JsonObject of the items' price history. If only one id is given, returns a JsonObject of the item's price history.

        Args:
            id (List[str]): itemid(s)
            sid (List[str]): subid(s) like enhancement level
            convertdate (bool): Convert unix-like timestamp to UTC datetime. Defaults to True.
            formatprice (bool): Format price, adding separator (,). Defaults to False.

        Returns:
            ApiResponse: standardized response. Returned values in content.history: key (eg. "1745193600000"): Unix timestamps in milliseconds (from utils use ConvertTimestamp), value (eg. 75000000000): item silver value
        """
        result = self._make_request_sync("POST", "GetMarketPriceInfo", params={"lang": self._api_lang},
                                            json_data = [{"id": int(id_), "sid": int(sid)} for id_, sid in zip(ids, sids)])
        if convertdate or formatprice:
            # Handle both list and dict cases
            content_list = [result.content] if isinstance(result.content, dict) else result.content
            for item in content_list:
                if "history" in item:
                    new_history = {}
                    for k, v in item["history"].items(): # type: ignore
                        # Convert date if needed
                        new_key = timestamp_to_datetime(float(k) / 1000).strftime("%Y-%m-%d") if convertdate else k
                        # Format price if needed
                        new_value = f"{v:,}" if formatprice else v
                        new_history[new_key] = new_value
                    item["history"] = new_history # type: ignore
            result.content = content_list # type: ignore
        return result

    async def get_world_market_search_list(self, ids: List[str]) -> ApiResponse:
        """Search for items by their id(s).

        Args:
            ids (str): itemid(s).

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items matching the search criteria.
        """
        return await self._make_request_async("GET", "GetWorldMarketSearchList", params={"ids": ids, "lang": self._api_lang})
    
    def get_world_market_search_list_sync(self, ids: List[str]) -> ApiResponse:
        """Search for items by their id(s).

        Args:
            ids (str): itemid(s).

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items matching the search criteria.
        """
        return self._make_request_sync("GET", "GetWorldMarketSearchList", params={"ids": ids, "lang": self._api_lang})

    async def post_world_market_search_list(self, ids: List[str]) -> ApiResponse:
        """Search for items by their id(s).

        Args:
            ids (str): itemid(s).

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items matching the search criteria.
        """
        return await self._make_request_async("POST", "GetWorldMarketSearchList", json_data=ids, params={"lang": self._api_lang})
    
    def post_world_market_search_list_sync(self, ids: List[str]) -> ApiResponse:
        """Search for items by their id(s).

        Args:
            ids (str): itemid(s).

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items matching the search criteria.
        """
        return self._make_request_sync("POST", "GetWorldMarketSearchList", json_data=ids, params={"lang": self._api_lang})

    async def get_world_market_list(self, main_category: str, sub_category: str) -> ApiResponse:
        """Get items from a specific category or subcategory.

        Args:
            maincategory (str): maincategory
            subcategory (str): subcategory

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items in the specified category or subcategory.
        """
        params = {"mainCategory": main_category, "subCategory": sub_category, "lang": self._api_lang}
        return await self._make_request_async("GET", "GetWorldMarketList", params=params)
    
    def get_world_market_list_sync(self, main_category: str, sub_category: str) -> ApiResponse:
        """Get items from a specific category or subcategory.

        Args:
            maincategory (str): maincategory
            subcategory (str): subcategory

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items in the specified category or subcategory.
        """
        params = {"mainCategory": main_category, "subCategory": sub_category, "lang": self._api_lang}
        return self._make_request_sync("GET", "GetWorldMarketList", params=params)

    async def post_world_market_list(self, main_category: str, sub_category: str) -> ApiResponse:
        """Get items from a specific category or subcategory.

        Args:
            maincategory (str): maincategory
            subcategory (str): subcategory

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items in the specified category or subcategory.
        """
        json_data = {"mainCategory": main_category, "subCategory": sub_category}
        return await self._make_request_async("POST", "GetWorldMarketList", json_data=json_data, params={"lang": self._api_lang})
    
    def post_world_market_list_sync(self, main_category: str, sub_category: str) -> ApiResponse:
        """Get items from a specific category or subcategory.

        Args:
            maincategory (str): maincategory
            subcategory (str): subcategory

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items in the specified category or subcategory.
        """
        json_data = {"mainCategory": main_category, "subCategory": sub_category}
        return self._make_request_sync("POST", "GetWorldMarketList", json_data=json_data, params={"lang": self._api_lang})

    async def get_world_market_sub_list(self, ids: List[str]) -> ApiResponse:
        """Get parsed item or items from min to max enhance (if available).

        Args:
            id (list[str]): itemid(s)

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items with their subid(s) (enhancement level).
        """
        return await self._make_request_async("GET", "GetWorldMarketSubList", params={"id": ids, "lang": self._api_lang})
    
    def get_world_market_sub_list_sync(self, ids: List[str]) -> ApiResponse:
        """Get parsed item or items from min to max enhance (if available).

        Args:
            id (list[str]): itemid(s)

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items with their subid(s) (enhancement level).
        """
        return self._make_request_sync("GET", "GetWorldMarketSubList", params={"id": ids, "lang": self._api_lang})

    async def post_world_market_sub_list(self, ids: List[str]) -> ApiResponse:
        """Get parsed item or items from min to max enhance (if available).

        Args:
            id (list[str]): itemid(s)

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items with their subid(s) (enhancement level).
        """
        return await self._make_request_async("POST", "GetWorldMarketSubList", json_data=ids, params={"lang": self._api_lang})
    
    def post_world_market_sub_list_sync(self, ids: List[str]) -> ApiResponse:
        """Get parsed item or items from min to max enhance (if available).

        Args:
            id (list[str]): itemid(s)

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items with their subid(s) (enhancement level).
        """
        return self._make_request_sync("POST", "GetWorldMarketSubList", json_data=ids, params={"lang": self._api_lang})

    async def get_bidding_info(self, ids: List[str], sids: List[str]) -> ApiResponse:
        """Get orders of an item or list of items

        Args:
            id (list[str]): itemid(s)
            sid (list[str]): subid(s)

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items' bidding information.
        """
        params = {"id": ids, "sid": sids, "lang": self._api_lang}
        return await self._make_request_async("GET", "GetBiddingInfoList", params=params)
    
    def get_bidding_info_sync(self, ids: List[str], sids: List[str]) -> ApiResponse:
        """Get orders of an item or list of items

        Args:
            id (list[str]): itemid(s)
            sid (list[str]): subid(s)

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items' bidding information.
        """
        params = {"id": ids, "sid": sids, "lang": self._api_lang}
        return self._make_request_sync("GET", "GetBiddingInfoList", params=params)

    async def post_bidding_info(self, ids: List[str], sids: List[str]) -> ApiResponse:
        """Get orders of an item or list of items

        Args:
            id (list[str]): itemid(s)
            sid (list[str]): subid(s)

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items' bidding information.
        """
        return await self._make_request_async("POST", "GetBiddingInfoList", json_data = [{"id": int(id_), "sid": int(sid)} for id_, sid in zip(ids, sids)],
                                            params={"lang": self._api_lang})
        
    
    def post_bidding_info_sync(self, ids: List[str], sids: List[str]) -> ApiResponse:
        """Get orders of an item or list of items

        Args:
            id (list[str]): itemid(s)
            sid (list[str]): subid(s)

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items' bidding information.
        """
        return self._make_request_sync("POST", "GetBiddingInfoList", json_data = [{"id": int(id_), "sid": int(sid)} for id_, sid in zip(ids, sids)],
                                            params={"lang": self._api_lang})

    async def get_pearl_items(self) -> ApiResponse:
        """Convenience method for getting all pearl items.

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of pearl items.
        """
        return await self._make_request_async("GET", "pearlItems", params={"lang": self._api_lang})
    
    def get_pearl_items_sync(self) -> ApiResponse:
        """Convenience method for getting all pearl items.

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of pearl items.
        """
        return self._make_request_sync("GET", "pearlItems", params={"lang": self._api_lang})


    async def post_pearl_items(self) -> ApiResponse:
        """Convenience method for getting all pearl items.

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of pearl items.
        """
        return await self._make_request_async("POST", "pearlItems", params={"lang": self._api_lang})
    
    def post_pearl_items_sync(self) -> ApiResponse:
        """Convenience method for getting all pearl items.

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of pearl items.
        """
        return self._make_request_sync("POST", "pearlItems", params={"lang": self._api_lang})

    # ! Not working
    async def get_market(self) -> ApiResponse:
        """NOT WORKING! Convenience method for getting all items currently available on the market.
        

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items currently available on the market.
        """
        return await self._make_request_async("GET", "market", params={"lang": self._api_lang})
    
    # ! Not working
    def get_market_sync(self) -> ApiResponse:
        """NOT WORKING! Convenience method for getting all items currently available on the market.
        

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items currently available on the market.
        """
        return self._make_request_sync("GET", "market", params={"lang": self._api_lang})

    # ! Not working
    async def post_market(self) -> ApiResponse:
        """NOT WORKING! Convenience method for getting all items currently available on the market.
        

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items currently available on the market.
        """
        return await self._make_request_async("POST", "market", params={"lang": self._api_lang})
    
    def post_market_sync(self) -> ApiResponse:
        """NOT WORKING! Convenience method for getting all items currently available on the market.
        

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items currently available on the market.
        """
        return self._make_request_sync("POST", "market", params={"lang": self._api_lang})

    async def get_item(self, ids: List[str] = []) -> ApiResponse:
        """Get item information by its id(s).

        Args:
            ids (list[str], optional): A list of item ids to retrieve information for. Defaults to an empty list.

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items with their id, name, and sid.
        If no ids are provided, returns an empty ApiResponse.
        """
        if not ids:
            return ApiResponse()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self._base_url}/util/db",
                    params={"id": ids, "lang": self._api_lang},
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    return ApiResponse(
                        success=response.status >= 200 and response.status <= 299,
                        status_code=response.status,
                        message=response.reason or "No message provided",
                        content=json.loads(await response.text())
                    )
        except aiohttp.ClientError as e:
            return ApiResponse(message=str(e))
        
    def get_item_sync(self, ids: List[str] = []) -> ApiResponse:
        """Get item information by its id(s).

        Args:
            ids (list[str], optional): A list of item ids to retrieve information for. Defaults to an empty list.

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items with their id, name, and sid.
        If no ids are provided, returns an empty ApiResponse.
        """
        if not ids:
            return ApiResponse()
        try:
            response = self._make_request_sync(
                            method="GET",
                            endpoint=f"{self._base_url}/util/db",
                            params={"id": ids, "lang": self._api_lang}
                        )
            return ApiResponse(
                success=response.status_code >= 200 and response.status_code <= 299,
                status_code=response.status_code,
                message=response.message or "No message provided",
                content=json.loads(response.content)
            )
        except aiohttp.ClientError as e:
            return ApiResponse(message=str(e))

    # NOTE: No point making sync for this function
    async def item_database_dump(self, start_id: int, end_id: int, chunk_size: int = 100) -> ApiResponse:
        """Dump the item database from startid to endid in chunks of chunksize.

        Args:
            startid (int): _description_
            endid (int): _description_
            chunksize (int, optional): The number of items to fetch in each request. Defaults to 100.

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items with their id, name, and sid.
        """
        chunk_size = min(chunk_size, 100)  # API limit
        items = []
        tasks = []

        for i in range(start_id, end_id + 1, chunk_size):
            ids = [str(j) for j in range(i, min(i + chunk_size, end_id + 1))]
            tasks.append(self.get_item(ids))

        responses = await asyncio.gather(*tasks, return_exceptions=True)
        for response in responses:
            if isinstance(response, ApiResponse) and response.success:
                # items.extend(response.deserialize() or [])
                items.extend(response.content or [])
            else:
                print(f"Error fetching items: {response.message if isinstance(response, ApiResponse) else str(response)}")

        return ApiResponse(
            # content=json.dumps(items, indent=2, ensure_ascii=False),
            content=json.loads(json.dumps(items, indent=2)),
            success=True,
            status_code=200,
            message="Item database dump completed successfully."
        )

    # # NOTE: moved, have to test it!
    # async def get_pig_cave_status(self, region: PigCave = PigCave.EU) -> ApiResponse:
    #     """Get Pig Cave status by region (garmoth.com data)

    #     Args:
    #         region (PigCave, optional): Region and endpoint at the same time. Defaults to PigCave.EU.

    #     Returns:
    #         ApiResponse: An ApiResponse object containing the success status, status code, message, and content of the response.
    #     """
    #     async with aiohttp.ClientSession() as session:
    #         async with session.get(f"http://node63.lunes.host:3132/{region.value}") as response:
    #             content = await response.text()
    #             return ApiResponse(
    #                 success=response.status >= 200 and response.status <= 299,
    #                 status_code=response.status,
    #                 message=f"{region.value}" or "No message provided",
    #                 content=content
    #             )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._session is not None:
            self._session.close()
            self._session = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.close()