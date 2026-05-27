"""
bdomarket - Full Feature Example
=================================
Demonstrates every available feature of the bdomarket library:
  - ArshaMarket (Central Market API) - async & sync
  - UnofficialMarket (Unofficial BDO Market API) - async & sync
  - Boss timer scraper
  - Item icon downloader
  - Pig Cave server status
  - Utility helper functions

Item IDs used in this example:
  735008 = Blackstar Shuriken (TET)
  735009 = Blackstar Shuriken (PEN)
  12094  = Kzarka Longsword
"""

import asyncio
import bdomarket


# =============================================================================
# SECTION 1: ArshaMarket (Central Market API) - Async
# =============================================================================

async def arsha_async_example():
    """Demonstrates all async ArshaMarket / Market methods."""
    print("\n" + "=" * 60)
    print("  ArshaMarket (async) — Central Market API")
    print("=" * 60)

    # Both class names work: ArshaMarket and the Market alias
    async with bdomarket.Market(
        region=bdomarket.MarketRegion.EU,
        apiversion=bdomarket.ApiVersion.V2,
        language=bdomarket.Locale.English
    ) as market:

        # --- Wait List ---
        r = await market.get_world_market_wait_list()
        print(f"[GET]  Wait List:         {r.success} | {r.status_code}")
        r.save_to_file("responses/async/waitlist/get.json")

        r = await market.post_world_market_wait_list()
        print(f"[POST] Wait List:         {r.success} | {r.status_code}")
        r.save_to_file("responses/async/waitlist/post.json")

        # --- Hot List ---
        r = await market.get_world_market_hot_list()
        print(f"[GET]  Hot List:          {r.success} | {r.status_code}")
        r.save_to_file("responses/async/hotlist/get.json")

        r = await market.post_world_market_hot_list()
        print(f"[POST] Hot List:          {r.success} | {r.status_code}")
        r.save_to_file("responses/async/hotlist/post.json")

        # --- Price History ---
        # convertdate=True  → converts Unix ms timestamps to "YYYY-MM-DD"
        # formatprice=True  → adds thousands separator to prices
        r = await market.get_market_price_info(
            ids=["735008", "735009"], sids=["20", "20"],
            convertdate=True, formatprice=False
        )
        print(f"[GET]  Price Info:        {r.success} | {r.status_code}")
        r.save_to_file("responses/async/priceinfo/get.json")

        r = await market.post_market_price_info(
            ids=["735008", "735009"], sids=["20", "20"],
            convertdate=True, formatprice=False
        )
        print(f"[POST] Price Info:        {r.success} | {r.status_code}")
        r.save_to_file("responses/async/priceinfo/post.json")

        # --- Search List (by item ID) ---
        r = await market.get_world_market_search_list(ids=["735008"])
        print(f"[GET]  Search List:       {r.success} | {r.status_code}")
        r.save_to_file("responses/async/searchlist/get.json")

        r = await market.post_world_market_search_list(ids=["735008"])
        print(f"[POST] Search List:       {r.success} | {r.status_code}")
        r.save_to_file("responses/async/searchlist/post.json")

        # --- Category List ---
        # mainCategory=1 (Weapons), subCategory=1 (Swords)
        r = await market.get_world_market_list(main_category="1", sub_category="1")
        print(f"[GET]  Market List:       {r.success} | {r.status_code}")
        r.save_to_file("responses/async/marketlist/get.json")

        r = await market.post_world_market_list(main_category="1", sub_category="1")
        print(f"[POST] Market List:       {r.success} | {r.status_code}")
        r.save_to_file("responses/async/marketlist/post.json")

        # --- Sub List (all enhancement levels for an item) ---
        r = await market.get_world_market_sub_list(ids=["735008"])
        print(f"[GET]  Sub List:          {r.success} | {r.status_code}")
        r.save_to_file("responses/async/sublist/get.json")

        r = await market.post_world_market_sub_list(ids=["735008"])
        print(f"[POST] Sub List:          {r.success} | {r.status_code}")
        r.save_to_file("responses/async/sublist/post.json")

        # --- Bidding Info (buy/sell orders) ---
        r = await market.get_bidding_info(ids=["735008", "735009"], sids=["20", "20"])
        print(f"[GET]  Bidding Info:      {r.success} | {r.status_code}")
        r.save_to_file("responses/async/biddinginfo/get.json")

        r = await market.post_bidding_info(ids=["735008", "735009"], sids=["20", "20"])
        print(f"[POST] Bidding Info:      {r.success} | {r.status_code}")
        r.save_to_file("responses/async/biddinginfo/post.json")

        # --- Pearl Items ---
        r = await market.get_pearl_items()
        print(f"[GET]  Pearl Items:       {r.success} | {r.status_code}")
        r.save_to_file("responses/async/pearlitems/get.json")

        r = await market.post_pearl_items()
        print(f"[POST] Pearl Items:       {r.success} | {r.status_code}")
        r.save_to_file("responses/async/pearlitems/post.json")

        # --- Full Market Snapshot ---
        r = await market.get_market()
        print(f"[GET]  Full Market:       {r.success} | {r.status_code}")
        r.save_to_file("responses/async/marketdata/get.json")

        r = await market.post_market()
        print(f"[POST] Full Market:       {r.success} | {r.status_code}")
        r.save_to_file("responses/async/marketdata/post.json")

        # --- Item Lookup (by ID via arsha.io /util/db) ---
        r = await market.get_item(ids=["735008", "12094"])
        print(f"[GET]  Item Lookup:       {r.success} | {r.status_code}")
        r.save_to_file("responses/async/item/get.json")

        # --- Item Database Dump (partial, EXPERIMENTAL) ---
        r = await market.item_database_dump(start_id=1, end_id=10, chunk_size=5)
        print(f"[EXP]  Item DB Dump:      {r.success} | {r.status_code}")
        r.save_to_file("responses/async/itemdump/partial.json")

        # --- Item Database Dump (full) ---
        r = await market.item_database_dump_v2()
        print(f"[GET]  Item DB Full:      {r.success} | {r.status_code} | {len(r.content or [])} items")
        r.save_to_file("responses/async/itemdump/get.json")

        # Use helper functions to query the dump
        if r.success and r.content:
            found_by_name = bdomarket.get_items_by_name_from_db(r.content, "Blackstar Shuriken")
            found_by_id   = bdomarket.get_items_by_id_from_db(r.content, 735008)
            print(f"       By name 'Blackstar Shuriken': {len(found_by_name)} match(es)")
            print(f"       By ID 735008:                 {len(found_by_id)} match(es)")


# =============================================================================
# SECTION 2: ArshaMarket (Central Market API) - Sync
# =============================================================================

def arsha_sync_example():
    """Demonstrates all sync ArshaMarket / Market methods."""
    print("\n" + "=" * 60)
    print("  ArshaMarket (sync) — Central Market API")
    print("=" * 60)

    market = bdomarket.Market(
        region=bdomarket.MarketRegion.EU,
        apiversion=bdomarket.ApiVersion.V2,
        language=bdomarket.Locale.English
    )

    r = market.get_world_market_wait_list_sync()
    print(f"[GET]  Wait List:         {r.success} | {r.status_code}")
    r.save_to_file("responses/sync/waitlist/get.json")

    r = market.post_world_market_wait_list_sync()
    print(f"[POST] Wait List:         {r.success} | {r.status_code}")
    r.save_to_file("responses/sync/waitlist/post.json")

    r = market.get_world_market_hot_list_sync()
    print(f"[GET]  Hot List:          {r.success} | {r.status_code}")
    r.save_to_file("responses/sync/hotlist/get.json")

    r = market.post_world_market_hot_list_sync()
    print(f"[POST] Hot List:          {r.success} | {r.status_code}")
    r.save_to_file("responses/sync/hotlist/post.json")

    r = market.get_market_price_info_sync(
        ids=["735008", "735009"], sids=["20", "20"],
        convertdate=True, formatprice=False
    )
    print(f"[GET]  Price Info:        {r.success} | {r.status_code}")
    r.save_to_file("responses/sync/priceinfo/get.json")

    r = market.post_market_price_info_sync(
        ids=["735008", "735009"], sids=["20", "20"],
        convertdate=True, formatprice=False
    )
    print(f"[POST] Price Info:        {r.success} | {r.status_code}")
    r.save_to_file("responses/sync/priceinfo/post.json")

    r = market.get_world_market_search_list_sync(ids=["735008"])
    print(f"[GET]  Search List:       {r.success} | {r.status_code}")
    r.save_to_file("responses/sync/searchlist/get.json")

    r = market.post_world_market_search_list_sync(ids=["735008"])
    print(f"[POST] Search List:       {r.success} | {r.status_code}")
    r.save_to_file("responses/sync/searchlist/post.json")

    r = market.get_world_market_list_sync(main_category="1", sub_category="1")
    print(f"[GET]  Market List:       {r.success} | {r.status_code}")
    r.save_to_file("responses/sync/marketlist/get.json")

    r = market.post_world_market_list_sync(main_category="1", sub_category="1")
    print(f"[POST] Market List:       {r.success} | {r.status_code}")
    r.save_to_file("responses/sync/marketlist/post.json")

    r = market.get_world_market_sub_list_sync(ids=["735008"])
    print(f"[GET]  Sub List:          {r.success} | {r.status_code}")
    r.save_to_file("responses/sync/sublist/get.json")

    r = market.post_world_market_sub_list_sync(ids=["735008"])
    print(f"[POST] Sub List:          {r.success} | {r.status_code}")
    r.save_to_file("responses/sync/sublist/post.json")

    r = market.get_bidding_info_sync(ids=["735008", "735009"], sids=["20", "20"])
    print(f"[GET]  Bidding Info:      {r.success} | {r.status_code}")
    r.save_to_file("responses/sync/biddinginfo/get.json")

    r = market.post_bidding_info_sync(ids=["735008", "735009"], sids=["20", "20"])
    print(f"[POST] Bidding Info:      {r.success} | {r.status_code}")
    r.save_to_file("responses/sync/biddinginfo/post.json")

    r = market.get_pearl_items_sync()
    print(f"[GET]  Pearl Items:       {r.success} | {r.status_code}")
    r.save_to_file("responses/sync/pearlitems/get.json")

    r = market.post_pearl_items_sync()
    print(f"[POST] Pearl Items:       {r.success} | {r.status_code}")
    r.save_to_file("responses/sync/pearlitems/post.json")

    r = market.get_market_sync()
    print(f"[GET]  Full Market:       {r.success} | {r.status_code}")
    r.save_to_file("responses/sync/marketdata/get.json")

    r = market.post_market_sync()
    print(f"[POST] Full Market:       {r.success} | {r.status_code}")
    r.save_to_file("responses/sync/marketdata/post.json")

    r = market.get_item_sync(ids=["735008"])
    print(f"[GET]  Item Lookup:       {r.success} | {r.status_code}")
    r.save_to_file("responses/sync/item/get.json")

    market.close()


# =============================================================================
# SECTION 3: UnofficialMarket (Unofficial BDO Market API) - Async
# =============================================================================

async def unofficial_async_example():
    """Demonstrates all async UnofficialMarket methods."""
    print("\n" + "=" * 60)
    print("  UnofficialMarket (async) — Unofficial BDO Market API")
    print("=" * 60)

    async with bdomarket.UnofficialMarket(
        region=bdomarket.MarketRegion.EU,
        language=bdomarket.Locale.English
    ) as unofficial:

        # Queue list (items waiting to be listed)
        r = await unofficial.get_list_queue()
        print(f"[GET]  Queue List:        {r.success} | {r.status_code}")

        # Items by category (main_category=20 = Accessories, sub_category=1 = Rings)
        r = await unofficial.get_list_category(main_category=20, sub_category=1)
        print(f"[GET]  Category List:     {r.success} | {r.status_code}")

        # Item details by ID (Kzarka Longsword)
        r = await unofficial.get_item_id(item_id=12094)
        print(f"[GET]  Item by ID:        {r.success} | {r.status_code}")
        if r.success and r.content:
            print(f"       Name: {r.content.get('name')}, Grade: {r.content.get('grade')}")

        # Item icon (returns raw PNG bytes)
        r = await unofficial.get_item_id_icon(item_id=12094)
        print(f"[GET]  Item Icon:         {r.success} | {r.status_code}")
        if r.success:
            r.save_image("responses/unofficial/icons/12094.png")

        # Enhancement details (e.g. TET = enhancement level 4, PEN = 5)
        r = await unofficial.get_item_id_enhancement(item_id=12094, enhancement=5)
        print(f"[GET]  Enhancement Info:  {r.success} | {r.status_code}")

        # Enhancement tooltip (full item card data)
        r = await unofficial.get_item_id_enhancement_tooltip(item_id=12094, enhancement=5)
        print(f"[GET]  Enhancement Tooltip: {r.success} | {r.status_code}")

        # Search items by name string
        r = await unofficial.get_search(search_string="Deboreka Ring")
        print(f"[GET]  Search:            {r.success} | {r.status_code}")
        if r.success and r.content:
            print(f"       Found {len(r.content)} result(s) for 'Deboreka Ring'")


# =============================================================================
# SECTION 4: UnofficialMarket (Unofficial BDO Market API) - Sync
# =============================================================================

def unofficial_sync_example():
    """Demonstrates all sync UnofficialMarket methods."""
    print("\n" + "=" * 60)
    print("  UnofficialMarket (sync) — Unofficial BDO Market API")
    print("=" * 60)

    with bdomarket.UnofficialMarket(
        region=bdomarket.MarketRegion.EU,
        language=bdomarket.Locale.English
    ) as unofficial:

        r = unofficial.get_list_queue_sync()
        print(f"[GET]  Queue List:        {r.success} | {r.status_code}")

        r = unofficial.get_list_category_sync(main_category=20, sub_category=1)
        print(f"[GET]  Category List:     {r.success} | {r.status_code}")

        r = unofficial.get_item_id_sync(item_id=12094)
        print(f"[GET]  Item by ID:        {r.success} | {r.status_code}")

        r = unofficial.get_item_id_icon_sync(item_id=12094)
        print(f"[GET]  Item Icon:         {r.success} | {r.status_code}")

        r = unofficial.get_item_id_enhancement_sync(item_id=12094, enhancement=5)
        print(f"[GET]  Enhancement Info:  {r.success} | {r.status_code}")

        r = unofficial.get_item_id_enhancement_tooltip_sync(item_id=12094, enhancement=5)
        print(f"[GET]  Enhancement Tooltip: {r.success} | {r.status_code}")

        r = unofficial.get_search_sync(search_string="Deboreka Ring")
        print(f"[GET]  Search:            {r.success} | {r.status_code}")


# =============================================================================
# SECTION 5: Boss Timer Scraper
# =============================================================================

def boss_example():
    """Demonstrates the Boss timer scraper."""
    print("\n" + "=" * 60)
    print("  Boss Timer Scraper — mmotimer.com")
    print("=" * 60)

    boss = bdomarket.Boss(server=bdomarket.Server.EU).scrape()

    timers = boss.get_timer()
    print(f"Scraped {len(timers)} boss spawn time(s) for EU server.")

    if timers:
        print(f"Next entry: {timers[0]}")

    # Also available as JSON
    json_data = boss.get_timer_json(indent=2)
    print(f"JSON preview (first 200 chars): {json_data[:200]}...")


# =============================================================================
# SECTION 6: Item Icon Downloader
# =============================================================================

def item_example():
    """Demonstrates the Item icon downloader and serialisation."""
    print("\n" + "=" * 60)
    print("  Item — Icon Downloader")
    print("=" * 60)

    # Save icon by item ID (filename = "735008.png")
    item_by_id = bdomarket.Item(item_id="735008", name="Blackstar Shuriken")
    item_by_id.get_icon(
        folderpath="responses/icons",
        isrelative=True,
        filenameprop=bdomarket.ItemProp.ID
    )
    print(f"Saved icon for '{item_by_id.name}' as {item_by_id.id}.png")

    # Save icon by item name (filename = "Blackstar Shuriken.png")
    item_by_name = bdomarket.Item(item_id="735008", name="Blackstar Shuriken")
    item_by_name.get_icon(
        folderpath="responses/icons",
        isrelative=True,
        filenameprop=bdomarket.ItemProp.NAME
    )
    print(f"Saved icon for '{item_by_name.name}' as {item_by_name.name}.png")

    # Serialize to dictionary
    print(f"Item as dict: {item_by_id.to_dict()}")


# =============================================================================
# SECTION 7: Pig Cave Server Status (Beta)
# =============================================================================

async def pig_example():
    """Demonstrates the Pig Cave server status checker."""
    print("\n" + "=" * 60)
    print("  Pig Cave — Server Status (Beta)")
    print("=" * 60)

    pig = bdomarket.Pig(region=bdomarket.PigCave.EU)
    r = await pig.get_status()
    print(f"Pig Cave EU Status: {r.success} | {r.status_code}")
    if r.success:
        # Content is raw HTML/text from garmoth
        print(f"Response preview: {str(r.content)[:100]}...")


# =============================================================================
# SECTION 8: Utility Functions
# =============================================================================

def utilities_example():
    """Demonstrates standalone utility functions."""
    print("\n" + "=" * 60)
    print("  Utility Functions")
    print("=" * 60)

    # Timestamp conversion
    import datetime
    dt = bdomarket.timestamp_to_datetime(1745193600.0)
    print(f"Unix 1745193600 → {dt.strftime('%Y-%m-%d %H:%M:%S %Z')}")

    ts = bdomarket.datetime_to_timestamp(datetime.datetime(2025, 4, 21, tzinfo=datetime.timezone.utc))
    print(f"2025-04-21 UTC  → {ts}")

    # In-memory database helpers (given an already-fetched item list)
    sample_db = [
        {"id": 735008, "name": "Blackstar Shuriken", "sid": 20},
        {"id": 735009, "name": "Blackstar Shuriken", "sid": 21},
        {"id": 12094,  "name": "Kzarka Longsword",   "sid": 0},
    ]
    by_name = bdomarket.get_items_by_name_from_db(sample_db, "Blackstar Shuriken")
    print(f"Items named 'Blackstar Shuriken': {len(by_name)} match(es)")

    by_id = bdomarket.get_items_by_id_from_db(sample_db, 12094)
    print(f"Items with ID 12094:             {len(by_id)} match(es)")

    # search_items_by_name / search_items_by_id require a saved JSON file
    # (produced by item_database_dump_v2 → save_to_file) — example:
    #
    #   matches = bdomarket.search_items_by_name("responses/async/itemdump/get.json", "Kzarka")
    #   matches = bdomarket.search_items_by_id("responses/async/itemdump/get.json", 12094)


# =============================================================================
# ENTRYPOINT
# =============================================================================

async def main():
    await arsha_async_example()
    await unofficial_async_example()
    await pig_example()


if __name__ == "__main__":
    print("bdomarket — Full Feature Example")
    print("Running async examples...")
    asyncio.run(main())

    print("\nRunning sync examples...")
    arsha_sync_example()
    unofficial_sync_example()
    boss_example()
    item_example()
    utilities_example()

    print("\nDone!")
