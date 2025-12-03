import asyncio
import bdomarket


async def async_example():
    # Initialize Market with EU region, V2 API, English locale
    # And/Or you can initialize UnofficialMarket like:
    # async with bdomarket.UnofficialMarket():
    # ...
    async with bdomarket.ArshaMarket(region=bdomarket.MarketRegion.EU, apiversion=bdomarket.ApiVersion.V2, language=bdomarket.Locale.English) as market:
        # Get world market wait list (async)
        wait_list = await market.get_world_market_wait_list()
        # print("World Market Wait List:", wait_list.success, wait_list.status_code)
        wait_list.save_to_file("responses/async/waitlist/get.json")

        # Post world market wait list (async)
        post_wait_list = await market.post_world_market_wait_list()
        print("Post World Market Wait List:",
              post_wait_list.success, post_wait_list.status_code)
        post_wait_list.save_to_file("responses/async/waitlist/post.json")

        # Get world market hot list (async)
        hot_list = await market.get_world_market_hot_list()
        print("World Market Hot List:", hot_list.success, hot_list.status_code)
        hot_list.save_to_file("responses/async/hotlist/get.json")

        # Post world market hot list (async)
        post_hot_list = await market.post_world_market_hot_list()
        print("Post World Market Hot List:",
              post_hot_list.success, post_hot_list.status_code)
        post_hot_list.save_to_file("responses/async/hotlist/post.json")

        # Get market price info for items (async)
        price_info = await market.get_market_price_info(ids=["735008", "735009"], sids=["20", "20"], convertdate=True, formatprice=False)
        print("Market Price Info:", price_info.success, price_info.status_code)
        price_info.save_to_file("responses/async/priceinfo/get.json")

        # Post market price info (async)
        post_price_info = await market.post_market_price_info(ids=["735008", "735009"], sids=["20", "20"], convertdate=True, formatprice=False)
        print("Post Market Price Info:", post_price_info.success,
              post_price_info.status_code)
        post_price_info.save_to_file("responses/async/priceinfo/post.json")

        # Get world market search list (async)
        search_list = await market.get_world_market_search_list(ids=["735008"])
        print("World Market Search List:",
              search_list.success, search_list.status_code)
        search_list.save_to_file("responses/async/searchlist/get.json")

        # Post world market search list (async)
        post_search_list = await market.post_world_market_search_list(ids=["735008"])
        print("Post World Market Search List:",
              post_search_list.success, post_search_list.status_code)
        post_search_list.save_to_file("responses/async/searchlist/post.json")

        # Get world market list by category (async)
        market_list = await market.get_world_market_list(main_category="1", sub_category="1")
        print("World Market List:", market_list.success, market_list.status_code)
        market_list.save_to_file("responses/async/marketlist/get.json")

        # Post world market list (async)
        post_market_list = await market.post_world_market_list(main_category="1", sub_category="1")
        print("Post World Market List:", post_market_list.success,
              post_market_list.status_code)
        post_market_list.save_to_file("responses/async/marketlist/post.json")

        # Get world market sub list (async)
        sub_list = await market.get_world_market_sub_list(ids=["735008"])
        print("World Market Sub List:", sub_list.success, sub_list.status_code)
        sub_list.save_to_file("responses/async/sublist/get.json")

        # Post world market sub list (async)
        post_sub_list = await market.post_world_market_sub_list(ids=["735008"])
        print("Post World Market Sub List:",
              post_sub_list.success, post_sub_list.status_code)
        post_sub_list.save_to_file("responses/async/sublist/post.json")

        # Get bidding info (async)
        bidding_info = await market.get_bidding_info(ids=["735008", "735009"], sids=["20", "20"])
        print("Bidding Info:", bidding_info.success, bidding_info.status_code)
        bidding_info.save_to_file("responses/async/biddinginfo/get.json")

        # Post bidding info (async)
        post_bidding_info = await market.post_bidding_info(ids=["735008", "735009"], sids=["20", "20"])
        print("Post Bidding Info:", post_bidding_info.success,
              post_bidding_info.status_code)
        post_bidding_info.save_to_file("responses/async/biddinginfo/post.json")

        # Get pearl items (async)
        pearl_items = await market.get_pearl_items()
        print("Pearl Items:", pearl_items.success, pearl_items.status_code)
        pearl_items.save_to_file("responses/async/pearlitems/get.json")

        # Post pearl items (async)
        post_pearl_items = await market.post_pearl_items()
        print("Post Pearl Items:", post_pearl_items.success,
              post_pearl_items.status_code)
        post_pearl_items.save_to_file("responses/async/pearlitems/post.json")

        # Get market (async)
        market_data = await market.get_market()
        print("Market Data:", market_data.success, market_data.status_code)
        market_data.save_to_file("responses/async/marketdata/get.json")

        # Post market (async)
        post_market_data = await market.post_market()
        print("Post Market Data:", post_market_data.success,
              post_market_data.status_code)
        post_market_data.save_to_file("responses/async/marketdata/post.json")

        # Get item by ID (async)
        item = await market.get_item(ids=["735008"])
        print("Item Info:", item.success, item.status_code)
        item.save_to_file("responses/async/item/get.json")

        # EXPERIMENTAL! Get item database dump (async) - avoid using this
        item_dump = await market.item_database_dump(start_id=1, end_id=10, chunk_size=5, showstatus=False)
        print("Item Database Dump:", item_dump.success, item_dump.status_code)
        item_dump.save_to_file("responses/async/itemdump/partial.json")

        # Get item database dump full (async)
        item_dump_full = await market.item_database_dump_v2()
        item_dump_full.save_to_file("responses/async/itemdump/get.json")
        print("Item Database Dump Full:",
              item_dump_full.success, item_dump_full.status_code)
        print(len(item_dump_full.content))
        print(bdomarket.get_items_by_name_from_db(
            item_dump_full.content, "Blackstar Shuriken"))
        print(bdomarket.get_items_by_id_from_db(
            item_dump_full.content, 735008))


def sync_example():
    # Get boss timer
    bosstimer = bdomarket.Boss().scrape()
    print("Boss Timer:", bosstimer.get_timer())
    print("Boss Timer JSON:", bosstimer.get_timer_json())

    # Get item icon
    item = bdomarket.Item(item_id="735008")
    item.get_icon("responses/sync/icons", True, bdomarket.ItemProp.NAME)
    item.get_icon("responses/sync/icons", True, bdomarket.ItemProp.ID)
    print("Item Icons saved to responses/icons")

    market = bdomarket.Market(region=bdomarket.MarketRegion.EU,
                              apiversion=bdomarket.ApiVersion.V2, language=bdomarket.Locale.English)
    # Get world market wait list (sync)
    wait_list = market.get_world_market_wait_list_sync()
    print("World Market Wait List:", wait_list.success, wait_list.status_code)
    wait_list.save_to_file("responses/sync/waitlist/get.json")

    # Post world market wait list (sync)
    post_wait_list = market.post_world_market_wait_list_sync()
    print("Post World Market Wait List:",
          post_wait_list.success, post_wait_list.status_code)
    post_wait_list.save_to_file("responses/sync/waitlist/post.json")

    # Get world market hot list (sync)
    hot_list = market.get_world_market_hot_list_sync()
    print("World Market Hot List:", hot_list.success, hot_list.status_code)
    hot_list.save_to_file("responses/sync/hotlist/get.json")

    # Post world market hot list (sync)
    post_hot_list = market.post_world_market_hot_list_sync()
    print("Post World Market Hot List:",
          post_hot_list.success, post_hot_list.status_code)
    post_hot_list.save_to_file("responses/sync/hotlist/post.json")

    # Get market price info for items (sync)
    price_info = market.get_market_price_info_sync(ids=["735008", "735009"], sids=[
                                                   "20", "20"], convertdate=True, formatprice=False)
    print("Market Price Info:", price_info.success, price_info.status_code)
    price_info.save_to_file("responses/sync/priceinfo/get.json")

    # Post market price info (sync)
    post_price_info = market.post_market_price_info_sync(
        ids=["735008", "735009"], sids=["20", "20"], convertdate=True, formatprice=False)
    print("Post Market Price Info:", post_price_info.success,
          post_price_info.status_code)
    post_price_info.save_to_file("responses/sync/priceinfo/post.json")

    # Get world market search list (sync)
    search_list = market.get_world_market_search_list_sync(ids=["735008"])
    print("World Market Search List:",
          search_list.success, search_list.status_code)
    search_list.save_to_file("responses/sync/searchlist/get.json")

    # Post world market search list (sync)
    post_search_list = market.post_world_market_search_list_sync(ids=[
                                                                 "735008"])
    print("Post World Market Search List:",
          post_search_list.success, post_search_list.status_code)
    post_search_list.save_to_file("responses/sync/searchlist/post.json")

    # Get world market list by category (sync)
    market_list = market.get_world_market_list_sync(
        main_category="1", sub_category="1")
    print("World Market List:", market_list.success, market_list.status_code)
    market_list.save_to_file("responses/sync/marketlist/get.json")

    # Post world market list (sync)
    post_market_list = market.post_world_market_list_sync(
        main_category="1", sub_category="1")
    print("Post World Market List:", post_market_list.success,
          post_market_list.status_code)
    post_market_list.save_to_file("responses/sync/marketlist/post.json")

    # Get world market sub list (sync)
    sub_list = market.get_world_market_sub_list_sync(ids=["735008"])
    print("World Market Sub List:", sub_list.success, sub_list.status_code)
    sub_list.save_to_file("responses/sync/sublist/get.json")

    # Post world market sub list (sync)
    post_sub_list = market.post_world_market_sub_list_sync(ids=["735008"])
    print("Post World Market Sub List:",
          post_sub_list.success, post_sub_list.status_code)
    post_sub_list.save_to_file("responses/sync/sublist/post.json")

    # Get bidding info (sync)
    bidding_info = market.get_bidding_info_sync(
        ids=["735008", "735009"], sids=["20", "20"])
    print("Bidding Info:", bidding_info.success, bidding_info.status_code)
    bidding_info.save_to_file("responses/sync/biddinginfo/get.json")

    # Post bidding info (sync)
    post_bidding_info = market.post_bidding_info_sync(
        ids=["735008", "735009"], sids=["20", "20"])
    print("Post Bidding Info:", post_bidding_info.success,
          post_bidding_info.status_code)
    post_bidding_info.save_to_file("responses/sync/biddinginfo/post.json")

    # Get pearl items (sync)
    pearl_items = market.get_pearl_items_sync()
    print("Pearl Items:", pearl_items.success, pearl_items.status_code)
    pearl_items.save_to_file("responses/sync/pearlitems/get.json")

    # Post pearl items (sync)
    post_pearl_items = market.post_pearl_items_sync()
    print("Post Pearl Items:", post_pearl_items.success,
          post_pearl_items.status_code)
    post_pearl_items.save_to_file("responses/sync/pearlitems/post.json")

    # Get market (sync)
    market_data = market.get_market_sync()
    print("Market Data:", market_data.success, market_data.status_code)
    market_data.save_to_file("responses/sync/marketdata/get.json")

    # Post market (sync)
    post_market_data = market.post_market_sync()
    print("Post Market Data:", post_market_data.success,
          post_market_data.status_code)
    post_market_data.save_to_file("responses/sync/marketdata/post.json")

    # Get item by ID (sync)
    item = market.get_item_sync(ids=["735008"])
    print("Item Info:", item.success, item.status_code)
    item.save_to_file("responses/sync/item/get.json")

    market.close()


if __name__ == "__main__":
    print("Loading...")
    asyncio.run(async_example())
    sync_example()
    print("Done!")
