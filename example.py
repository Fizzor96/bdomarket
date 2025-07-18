import asyncio
import bdomarket as bm

async def main():
    # Initialize Market with EU region, V2 API, English locale
    async with bm.Market(region=bm.MarketRegion.EU, api_version=bm.ApiVersion.V2, language=bm.Locale.English) as market:
        
        # Get world market wait list
        wait_list = await market.get_world_market_wait_list()
        # print("World Market Wait List:", wait_list)
        wait_list.save_to_file("responses/waitlist/get.json")

        # Post world market wait list
        post_wait_list = await market.post_world_market_wait_list()
        # print("Post World Market Wait List:", post_wait_list)
        post_wait_list.save_to_file("responses/waitlist/post.json")

        # Get world market hot list
        hot_list = await market.get_world_market_hot_list()
        # print("World Market Hot List:", hot_list)
        hot_list.save_to_file("responses/hotlist/get.json")

        # Post world market hot list
        post_hot_list = await market.post_world_market_hot_list()
        # print("Post World Market Hot List:", post_hot_list)
        post_hot_list.save_to_file("responses/hotlist/post.json")

        # Get market price info for items
        price_info = await market.get_market_price_info(ids=["735008", "735009"], sids=["20", "20"], convertdate=True, formatprice=False)
        # print("Market Price Info:", price_info)
        price_info.save_to_file("responses/priceinfo/get.json")

        # Post market price info
        post_price_info = await market.post_market_price_info(ids=["735008", "735009"], sids=["20", "20"], convertdate=True, formatprice=False)
        # print("Post Market Price Info:", post_price_info)
        post_price_info.save_to_file("responses/priceinfo/post.json")

        # Get world market search list
        search_list = await market.get_world_market_search_list(ids=["735008"])
        # print("World Market Search List:", search_list)
        search_list.save_to_file("responses/searchlist/get.json")

        # Post world market search list
        post_search_list = await market.post_world_market_search_list(ids=["735008"])
        # print("Post World Market Search List:", post_search_list)
        post_search_list.save_to_file("responses/searchlist/post.json")

        # Get world market list by category
        market_list = await market.get_world_market_list(main_category="1", sub_category="1")
        # print("World Market List:", market_list)
        market_list.save_to_file("responses/marketlist/get.json")

        # Post world market list
        post_market_list = await market.post_world_market_list(main_category="1", sub_category="1")
        # print("Post World Market List:", post_market_list)
        post_market_list.save_to_file("responses/marketlist/post.json")

        # Get world market sub list
        sub_list = await market.get_world_market_sub_list(ids=["735008"])
        # print("World Market Sub List:", sub_list)
        sub_list.save_to_file("responses/sublist/get.json")

        # Post world market sub list
        post_sub_list = await market.post_world_market_sub_list(ids=["735008"])
        # print("Post World Market Sub List:", post_sub_list)
        post_sub_list.save_to_file("responses/sublist/post.json")


        # Get bidding info
        bidding_info = await market.get_bidding_info(ids=["735008", "735009"], sids=["20", "20"])
        # print("Bidding Info:", bidding_info)
        bidding_info.save_to_file("responses/biddinginfo/get.json")

        # Post bidding info
        post_bidding_info = await market.post_bidding_info(ids=["735008", "735009"], sids=["20", "20"])
        # print("Post Bidding Info:", post_bidding_info)
        post_bidding_info.save_to_file("responses/biddinginfo/post.json")

        # Get pearl items
        pearl_items = await market.get_pearl_items()
        # print("Pearl Items:", pearl_items)
        pearl_items.save_to_file("responses/pearlitems/get.json")

        # Post pearl items
        post_pearl_items = await market.post_pearl_items()
        # print("Post Pearl Items:", post_pearl_items)
        post_pearl_items.save_to_file("responses/pearlitems/post.json")

        # Get market
        # ! BROKEN
        market_data = await market.get_market()
        # print("Market Data:", market_data)
        market_data.save_to_file("responses/marketdata/get.json")

        # Post market
        # ! BROKEN
        post_market_data = await market.post_market()
        # print("Post Market Data:", post_market_data)
        post_market_data.save_to_file("responses/marketdata/post.json")

        # Get item by ID
        item = await market.get_item(ids=["735008"])
        # print("Item Info:", item)
        item.save_to_file("responses/item/get.json")

        # Get item database dump
        item_dump = await market.item_database_dump(start_id=1, end_id=10, chunk_size=5)
        # print("Item Database Dump:", item_dump)
        item_dump.save_to_file("responses/itemdump/get.json")

        # Get Pig Cave status
        pig_cave = await market.get_pig_cave_status(region=bm.PigCave.EU)
        # print("Pig Cave Status:", pig_cave)
        pig_cave.save_to_file("responses/pig/get.json")
        
    # Get world boss timer
    bosstimer = bm.Boss().Scrape()
    bosstimer.GetTimer()
    bosstimer.GetTimerJSON()
    
    item = bm.Item(id="735008")
    # item.GetIcon(r"C:\yourpath", False, ItemProp.ID)
    item.GetIcon("responses/icons", True, bm.ItemProp.NAME)
    item.GetIcon("responses/icons", True, bm.ItemProp.ID)

if __name__ == "__main__":
    print("Loading...")
    asyncio.run(main())
    print("Done!")