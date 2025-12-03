# pylint: disable=missing-module-docstring, line-too-long
import asyncio
import json
import threading
from typing import Any, Dict, List, Optional

import aiohttp
import requests
from tqdm import tqdm

from .identifiers import ApiVersion, Locale, MarketRegion
from .response import ApiResponse
from .utils import check_for_updates, timestamp_to_datetime, experimental
# pylint: enable=missing-module-docstring


class BaseMarket:
    def __init__(self, base_url: str):
        self._base_url = base_url
        self._session = requests.Session()
        self._async_session: Optional[aiohttp.ClientSession] = None

    async def _make_request_async(self, method: str, endpoint: str, json_data: Optional[Any] = None,
                                  data: Optional[Any] = None, headers: Optional[Dict] = None,
                                  params: Optional[Dict] = None) -> ApiResponse:
        if self._async_session is None:
            self._async_session = aiohttp.ClientSession()
        try:
            async with self._async_session.request(
                method=method,
                url=f"{self._base_url}/{endpoint}",
                params=params,
                json=json_data,
                data=data,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                url = str(response.url)
                status_code = response.status
                message = response.reason or "No message provided"
                success = 200 <= status_code <= 299
                content_type = response.headers.get("Content-Type", "").lower()
                headers = response.headers
                if "image/png" in content_type:
                    content = await response.read()
                elif "application/json" in content_type or response.content_length == 0:
                    content = await response.json() if response.content_length else None
                else:
                    content = await response.text()
                return ApiResponse(success, status_code, message, content, url, headers)
        except Exception as e:
            return ApiResponse(False, None, str(e), None, None)

    def _make_request_sync(self, method: str, endpoint: str, json_data: Optional[Any] = None,
                           data: Optional[Any] = None, headers: Optional[Dict] = None,
                           params: Optional[Dict] = None) -> ApiResponse:
        try:
            response = self._session.request(
                method=method,
                url=f"{self._base_url}/{endpoint}",
                params=params,
                json=json_data,
                data=data,
                headers=headers,
                timeout=10
            )
            url = str(response.url)
            status_code = response.status_code
            message = response.reason or "No message provided"
            success = 200 <= status_code <= 299
            content_type = response.headers.get("Content-Type", "").lower()
            headers = response.headers
            if "image/png" in content_type:
                content = response.content
            elif "application/json" in content_type or not response.content:
                content = response.json() if response.content else None
            else:
                content = response.text
            return ApiResponse(success, status_code, message, content, url, headers)
        except Exception as e:
            return ApiResponse(False, None, str(e), None, None)

    # TODO: automatic close for sessions
    # def __del__(self):
    #     if self._session:
    #         self.close()
    #     if self._async_session:
    #         await self.async_close()

    def close(self):
        if self._session:
            self._session.close()
            self._session = None
        if self._async_session:
            # Note: Cannot await in sync close; use async_close for async session
            pass

    async def async_close(self):
        if self._async_session:
            await self._async_session.close()
            self._async_session = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    async def __aenter__(self):
        self._async_session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.async_close()


class UnofficialMarket(BaseMarket):
    def __init__(self, region: MarketRegion = MarketRegion.EU, apiversion: ApiVersion = ApiVersion.V2, language: Locale = Locale.English):
        super().__init__("https://api.blackdesertmarket.com")
        self._api_version = apiversion.value
        self._api_region = "eu"
        self._api_lang = "en-US"
        threading.Thread(target=check_for_updates(), daemon=True).start()

    @experimental("broken")
    def get_list_hot_sync(self):
        return self._make_request_sync("GET", "list/hot", params={"region": self._api_region, "language": self._api_lang})

    @experimental("broken")
    async def get_list_hot(self):
        return await self._make_request_async("GET", "list/hot", params={"region": self._api_region, "language": self._api_lang})

    async def get_list_queue(self):
        return await self._make_request_async("GET", "list/queue", params={"region": self._api_region, "language": self._api_lang})

    def get_list_queue_sync(self):
        return self._make_request_sync("GET", "list/queue", params={"region": self._api_region, "language": self._api_lang})

    async def get_list_category(self, main_category: int, sub_category: int):
        return await self._make_request_async("GET", f"list/{main_category}/{sub_category}", params={"region": self._api_region, "language": self._api_lang})

    def get_list_category_sync(self, main_category: int, sub_category: int):
        return self._make_request_sync("GET", f"list/{main_category}/{sub_category}", params={"region": self._api_region, "language": self._api_lang})

    async def get_item_id(self, item_id: int):
        return await self._make_request_async("GET", f"item/{item_id}", params={"region": self._api_region, "language": self._api_lang})

    def get_item_id_sync(self, item_id: int):
        return self._make_request_sync("GET", f"item/{item_id}", params={"region": self._api_region, "language": self._api_lang})

    async def get_item_id_icon(self, item_id: int):
        return await self._make_request_async("GET", f"item/{item_id}/icon", params={"region": self._api_region, "language": self._api_lang})

    def get_item_id_icon_sync(self, item_id: int):
        return self._make_request_sync("GET", f"item/{item_id}/icon", params={"region": self._api_region, "language": self._api_lang})

    async def get_item_id_enhancement(self, item_id: int, enhancement: int):
        return await self._make_request_async("GET", f"item/{item_id}/{enhancement}", params={"region": self._api_region, "language": self._api_lang})

    def get_item_id_enhancement_sync(self, item_id: int, enhancement: int):
        return self._make_request_sync("GET", f"item/{item_id}/{enhancement}", params={"region": self._api_region, "language": self._api_lang})

    async def get_item_id_enhancement_tooltip(self, item_id: int, enhancement: int):
        return await self._make_request_async("GET", f"item/{item_id}/{enhancement}/tooltip", params={"region": self._api_region, "language": self._api_lang})

    def get_item_id_enhancement_tooltip_sync(self, item_id: int, enhancement: int):
        return self._make_request_sync("GET", f"item/{item_id}/{enhancement}/tooltip", params={"region": self._api_region, "language": self._api_lang})

    async def get_search(self, search_string: str):
        return await self._make_request_async("GET", f"search/{search_string}", params={"region": self._api_region, "language": self._api_lang})

    def get_search_sync(self, search_string: str):
        return self._make_request_sync("GET", f"search/{search_string}", params={"region": self._api_region, "language": self._api_lang})


class ArshaMarket(BaseMarket):
    """
    The Market class provides synchronous and asynchronous methods to interact with the Black Desert Online market API,
    allowing retrieval of item data, price history, bidding information, and other market-related endpoints for different regions and languages.
    Usage:
        market = Market(region=MarketRegion.EU, apiversion=ApiVersion.V2, language=Locale.English)
        response = market.get_market_price_info_sync(ids=["12345"], sids=["0"])
    """

    def __init__(self, region: MarketRegion = MarketRegion.EU, apiversion: ApiVersion = ApiVersion.V2, language: Locale = Locale.English):
        """Initializes the Market object with the specified region, API version, and language.

        Args:
            region (MarketRegion, optional): The region to use for the API requests. Defaults to AvailableRegions.EU.
            apiversion (ApiVersion, optional): The API version to use for the requests. Defaults to AvailableApiVersions.V2.
            language (Locale, optional): The language to use for the API responses. Defaults to SupportedLanguages.English.
        """
        super().__init__("https://api.arsha.io")
        self._api_version = apiversion.value
        self._api_region = region.value
        self._api_lang = language.value
        self._session = requests.Session()
        threading.Thread(target=check_for_updates(), daemon=True).start()

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
            ids (List[str]): itemid(s)
            sids (List[str]): subid(s) like enhancement level
            convertdate (bool): Convert unix-like timestamp to UTC datetime. Defaults to True.
            formatprice (bool): Format price, adding separator (,). Defaults to False.

        Returns:
            ApiResponse: standardized response. Returned values in content.history: key (eg. "1745193600000"): Unix timestamps in milliseconds (from utils use ConvertTimestamp), value (eg. 75000000000): item silver value
        """
        params = {"id": ids, "sid": sids, "lang": self._api_lang}
        result = await self._make_request_async("GET", "GetMarketPriceInfo", params=params)
        if convertdate or formatprice:
            # Handle both list and dict cases
            content_list = [result.content] if isinstance(
                result.content, dict) else result.content
            for item in content_list:
                if "history" in item:
                    new_history = {}
                    for k, v in item["history"].items():  # type: ignore
                        # Convert date if needed
                        new_key = timestamp_to_datetime(
                            float(k) / 1000).strftime("%Y-%m-%d") if convertdate else k
                        # Format price if needed
                        new_value = f"{v:,}" if formatprice else v
                        new_history[new_key] = new_value
                    item["history"] = new_history  # type: ignore
            result.content = content_list  # type: ignore
        return result

    def get_market_price_info_sync(self, ids: List[str], sids: List[str], convertdate: bool = True, formatprice: bool = False) -> ApiResponse:
        """Get price history for an item or list of items. If multiple ids are given, returns a JsonArray of JsonObject of the items' price history. If only one id is given, returns a JsonObject of the item's price history.

        Args:
            ids (List[str]): itemid(s)
            sids (List[str]): subid(s) like enhancement level
            convertdate (bool): Convert unix-like timestamp to UTC datetime. Defaults to True.
            formatprice (bool): Format price, adding separator (,). Defaults to False.

        Returns:
            ApiResponse: standardized response. Returned values in content.history: key (eg. "1745193600000"): Unix timestamps in milliseconds (from utils use ConvertTimestamp), value (eg. 75000000000): item silver value
        """
        params = {"id": ids, "sid": sids, "lang": self._api_lang}
        result = self._make_request_sync(
            "GET", "GetMarketPriceInfo", params=params)
        if convertdate or formatprice:
            # Handle both list and dict cases
            content_list = [result.content] if isinstance(
                result.content, dict) else result.content
            for item in content_list:
                if "history" in item:
                    new_history = {}
                    for k, v in item["history"].items():  # type: ignore
                        # Convert date if needed
                        new_key = timestamp_to_datetime(
                            float(k) / 1000).strftime("%Y-%m-%d") if convertdate else k
                        # Format price if needed
                        new_value = f"{v:,}" if formatprice else v
                        new_history[new_key] = new_value
                    item["history"] = new_history  # type: ignore
            result.content = content_list  # type: ignore
        return result

    async def post_market_price_info(self, ids: List[str], sids: List[str], convertdate: bool = True, formatprice: bool = False) -> ApiResponse:
        """Get price history for an item or list of items. If multiple ids are given, returns a JsonArray of JsonObject of the items' price history. If only one id is given, returns a JsonObject of the item's price history.

        Args:
            ids (List[str]): itemid(s)
            sids (List[str]): subid(s) like enhancement level
            convertdate (bool): Convert unix-like timestamp to UTC datetime. Defaults to True.
            formatprice (bool): Format price, adding separator (,). Defaults to False.

        Returns:
            ApiResponse: standardized response. Returned values in content.history: key (eg. "1745193600000"): Unix timestamps in milliseconds (from utils use ConvertTimestamp), value (eg. 75000000000): item silver value
        """
        result = await self._make_request_async("POST", "GetMarketPriceInfo", params={"lang": self._api_lang},
                                                json_data=[{"id": int(id_), "sid": int(sid)} for id_, sid in zip(ids, sids)])
        if convertdate or formatprice:
            # Handle both list and dict cases
            content_list = [result.content] if isinstance(
                result.content, dict) else result.content
            for item in content_list:
                if "history" in item:
                    new_history = {}
                    for k, v in item["history"].items():  # type: ignore
                        # Convert date if needed
                        new_key = timestamp_to_datetime(
                            float(k) / 1000).strftime("%Y-%m-%d") if convertdate else k
                        # Format price if needed
                        new_value = f"{v:,}" if formatprice else v
                        new_history[new_key] = new_value
                    item["history"] = new_history  # type: ignore
            result.content = content_list  # type: ignore
        return result

    def post_market_price_info_sync(self, ids: List[str], sids: List[str], convertdate: bool = True, formatprice: bool = False) -> ApiResponse:
        """Get price history for an item or list of items. If multiple ids are given, returns a JsonArray of JsonObject of the items' price history. If only one id is given, returns a JsonObject of the item's price history.

        Args:
            ids (List[str]): itemid(s)
            sids (List[str]): subid(s) like enhancement level
            convertdate (bool): Convert unix-like timestamp to UTC datetime. Defaults to True.
            formatprice (bool): Format price, adding separator (,). Defaults to False.

        Returns:
            ApiResponse: standardized response. Returned values in content.history: key (eg. "1745193600000"): Unix timestamps in milliseconds (from utils use ConvertTimestamp), value (eg. 75000000000): item silver value
        """
        result = self._make_request_sync("POST", "GetMarketPriceInfo", params={"lang": self._api_lang},
                                         json_data=[{"id": int(id_), "sid": int(sid)} for id_, sid in zip(ids, sids)])
        if convertdate or formatprice:
            # Handle both list and dict cases
            content_list = [result.content] if isinstance(
                result.content, dict) else result.content
            for item in content_list:
                if "history" in item:
                    new_history = {}
                    for k, v in item["history"].items():  # type: ignore
                        # Convert date if needed
                        new_key = timestamp_to_datetime(
                            float(k) / 1000).strftime("%Y-%m-%d") if convertdate else k
                        # Format price if needed
                        new_value = f"{v:,}" if formatprice else v
                        new_history[new_key] = new_value
                    item["history"] = new_history  # type: ignore
            result.content = content_list  # type: ignore
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
            main_category (str): maincategory
            sub_category (str): subcategory

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items in the specified category or subcategory.
        """
        params = {"mainCategory": main_category,
                  "subCategory": sub_category, "lang": self._api_lang}
        return await self._make_request_async("GET", "GetWorldMarketList", params=params)

    def get_world_market_list_sync(self, main_category: str, sub_category: str) -> ApiResponse:
        """Get items from a specific category or subcategory.

        Args:
            main_category (str): maincategory
            sub_category (str): subcategory

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items in the specified category or subcategory.
        """
        params = {"mainCategory": main_category,
                  "subCategory": sub_category, "lang": self._api_lang}
        return self._make_request_sync("GET", "GetWorldMarketList", params=params)

    async def post_world_market_list(self, main_category: str, sub_category: str) -> ApiResponse:
        """Get items from a specific category or subcategory.

        Args:
            main_category (str): maincategory
            sub_category (str): subcategory

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items in the specified category or subcategory.
        """
        json_data = {"mainCategory": main_category,
                     "subCategory": sub_category}
        return await self._make_request_async("POST", "GetWorldMarketList", json_data=json_data, params={"lang": self._api_lang})

    def post_world_market_list_sync(self, main_category: str, sub_category: str) -> ApiResponse:
        """Get items from a specific category or subcategory.

        Args:
            main_category (str): maincategory
            sub_category (str): subcategory

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items in the specified category or subcategory.
        """
        json_data = {"mainCategory": main_category,
                     "subCategory": sub_category}
        return self._make_request_sync("POST", "GetWorldMarketList", json_data=json_data, params={"lang": self._api_lang})

    async def get_world_market_sub_list(self, ids: List[str]) -> ApiResponse:
        """Get parsed item or items from min to max enhance (if available).

        Args:
            ids (list[str]): itemid(s)

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items with their subid(s) (enhancement level).
        """
        return await self._make_request_async("GET", "GetWorldMarketSubList", params={"id": ids, "lang": self._api_lang})

    def get_world_market_sub_list_sync(self, ids: List[str]) -> ApiResponse:
        """Get parsed item or items from min to max enhance (if available).

        Args:
            ids (list[str]): itemid(s)

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items with their subid(s) (enhancement level).
        """
        return self._make_request_sync("GET", "GetWorldMarketSubList", params={"id": ids, "lang": self._api_lang})

    async def post_world_market_sub_list(self, ids: List[str]) -> ApiResponse:
        """Get parsed item or items from min to max enhance (if available).

        Args:
            ids (list[str]): itemid(s)

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items with their subid(s) (enhancement level).
        """
        return await self._make_request_async("POST", "GetWorldMarketSubList", json_data=ids, params={"lang": self._api_lang})

    def post_world_market_sub_list_sync(self, ids: List[str]) -> ApiResponse:
        """Get parsed item or items from min to max enhance (if available).

        Args:
            ids (list[str]): itemid(s)

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items with their subid(s) (enhancement level).
        """
        return self._make_request_sync("POST", "GetWorldMarketSubList", json_data=ids, params={"lang": self._api_lang})

    async def get_bidding_info(self, ids: List[str], sids: List[str]) -> ApiResponse:
        """Get orders of an item or list of items

        Args:
            ids (list[str]): itemid(s)
            sids (list[str]): subid(s)

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items' bidding information.
        """
        params = {"id": ids, "sid": sids, "lang": self._api_lang}
        return await self._make_request_async("GET", "GetBiddingInfoList", params=params)

    def get_bidding_info_sync(self, ids: List[str], sids: List[str]) -> ApiResponse:
        """Get orders of an item or list of items

        Args:
            ids (list[str]): itemid(s)
            sids (list[str]): subid(s)

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items' bidding information.
        """
        params = {"id": ids, "sid": sids, "lang": self._api_lang}
        return self._make_request_sync("GET", "GetBiddingInfoList", params=params)

    async def post_bidding_info(self, ids: List[str], sids: List[str]) -> ApiResponse:
        """Get orders of an item or list of items

        Args:
            ids (list[str]): itemid(s)
            sids (list[str]): subid(s)

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items' bidding information.
        """
        return await self._make_request_async("POST", "GetBiddingInfoList", json_data=[{"id": int(id_), "sid": int(sid)} for id_, sid in zip(ids, sids)],
                                              params={"lang": self._api_lang})

    def post_bidding_info_sync(self, ids: List[str], sids: List[str]) -> ApiResponse:
        """Get orders of an item or list of items

        Args:
            ids (list[str]): itemid(s)
            sids (list[str]): subid(s)

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items' bidding information.
        """
        return self._make_request_sync("POST", "GetBiddingInfoList", json_data=[{"id": int(id_), "sid": int(sid)} for id_, sid in zip(ids, sids)],
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

    async def get_market(self) -> ApiResponse:
        """Convenience method for getting all items currently available on the market.


        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items currently available on the market.
        """
        return await self._make_request_async("GET", "market", params={"lang": self._api_lang})

    def get_market_sync(self) -> ApiResponse:
        """Convenience method for getting all items currently available on the market.


        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items currently available on the market.
        """
        result = self._make_request_sync(
            "GET", "market", params={"lang": self._api_lang})
        return ApiResponse(
            success=result.success,
            status_code=result.status_code,
            message=result.message,
            content=json.loads(result.content)
        )

    async def post_market(self) -> ApiResponse:
        """Convenience method for getting all items currently available on the market.


        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items currently available on the market.
        """
        return await self._make_request_async("POST", "market", params={"lang": self._api_lang})

    def post_market_sync(self) -> ApiResponse:
        """Convenience method for getting all items currently available on the market.


        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items currently available on the market.
        """
        result = self._make_request_sync(
            "POST", "market", params={"lang": self._api_lang})
        return ApiResponse(
            success=result.success,
            status_code=result.status_code,
            message=result.message,
            content=json.loads(result.content)
        )

    async def get_item(self, ids: List[str]) -> ApiResponse:
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

    def get_item_sync(self, ids: List[str]) -> ApiResponse:
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

    @experimental("beta")
    async def item_database_dump(self, start_id: int, end_id: int, chunk_size: int = 100, showstatus: bool = False) -> ApiResponse:
        """Dump the item database from startid to endid in chunks of chunksize.

        Args:
            start_id (int): Start id.
            end_id (int): End id.
            chunk_size (int, optional): The number of items to fetch in each request. Defaults to 100.

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items with their id, name, and sid.
        """
        chunk_size = min(chunk_size, 100)  # API limit
        items = []
        tasks = []

        if showstatus:
            for i in tqdm(range(start_id, end_id + 1, chunk_size), desc="Processing chunks"):
                ids = [str(j)
                       for j in range(i, min(i + chunk_size, end_id + 1))]
                tasks.append(self.get_item(ids))
        else:
            for i in range(start_id, end_id + 1, chunk_size):
                ids = [str(j)
                       for j in range(i, min(i + chunk_size, end_id + 1))]
                tasks.append(self.get_item(ids))

        responses = await asyncio.gather(*tasks, return_exceptions=True)
        for response in responses:
            if isinstance(response, ApiResponse) and response.success:
                items.extend(response.content or [])
            else:
                print(f"Error fetching items: {response.message if isinstance(
                    response, ApiResponse) else str(response)}")

        return ApiResponse(
            content=json.loads(json.dumps(items, indent=2)),
            success=True,
            status_code=200,
            message="Item database dump completed successfully."
        )

    async def item_database_dump_v2(self) -> ApiResponse:
        """Dump full item database

        Returns:
            ApiResponse: standardized response. Response.content: Returns JsonArray of JsonObjects of items with their id, name, and sid.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self._base_url}/util/db",
                params={"lang": self._api_lang},
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                return ApiResponse(
                    success=response.status >= 200 and response.status <= 299,
                    status_code=response.status,
                    message=response.reason or "No message provided",
                    content=json.loads(await response.text())
                )
