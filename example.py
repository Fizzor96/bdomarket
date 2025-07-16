import bdomarket

# -------------------------------
# 1. Initialize Market Interface
# -------------------------------
# Set up the market object for the EU region, API version 2, and English language.
market = bdomarket.Market(
    bdomarket.AvailableRegions.EU,
    bdomarket.AvailableApiVersions.V2,
    bdomarket.SupportedLanguages.English
)

# -------------------------------
# 2. Boss Timer Functionality
# -------------------------------
# Fetch and display world boss spawn times for the EU server.
boss_timer = bdomarket.timers.Boss(bdomarket.timers.Server.EU).Scrape()
print("Boss Timer (Python object):")
print(boss_timer.GetTimer())
print("\nBoss Timer (JSON):")
print(boss_timer.GetTimerJSON())

# -------------------------------
# 3. Market Wait List
# -------------------------------
# Retrieve the current market waitlist and save it to a file.
waitlist_response = market.GetWorldMarketWaitList()
print("\nMarket Wait List (content):")
print(waitlist_response.content)
waitlist_response.SaveToFile("responses/waitlist/get.json")

# Deserialize waitlist to Python objects and print each item.
print("\nDeserialized Wait List Items:")
for item in waitlist_response.Deserialize():
    print(item)

# -------------------------------
# 4. Item Queries
# -------------------------------
# Fetch information for multiple items by their IDs and save to file.
item_ids = ["3", "9505", "14870"]
items_response = market.GetItem(item_ids)
items_response.SaveToFile("responses/items/get.json")
print("\nFetched Items:")
print(items_response.content)

# Dump a range of items (IDs 0 to 250) to a file.
market.ItemDatabaseDump(0, 250).SaveToFile("responses/itemdump/dump.json")

# -------------------------------
# 5. Market Lists and SubLists
# -------------------------------
# Get and save various market lists.
market.GetWorldMarketList("1", "1").SaveToFile("responses/list/get.json")
market.GetWorldMarketSubList(["735008", "731109"]).SaveToFile("responses/sublist/get.json")
market.GetWorldMarketSearchList(["735008", "731109"]).SaveToFile("responses/searchlist/get.json")

# -------------------------------
# 6. Bidding and Price Info
# -------------------------------
# Fetch and save bidding and price information for specific items.
# NOTE: Timestamp Conversion Utility is used to convert Unix timestamps to human-readable format.
market.GetBiddingInfo(["735008", "731109"], ["19", "20"]).SaveToFile("responses/bidding/get.json")
market.GetMarketPriceInfo(["735008", "731109"], ["19", "20"]).SaveToFile("responses/priceinfo/get.json")

# -------------------------------
# 7. Pearl Items and Market Info
# -------------------------------
# Retrieve and save pearl shop items and overall market info.
market.GetPearlItems().SaveToFile("responses/pearlitems/get.json")
market.GetMarket().SaveToFile("responses/market/get.json")

# -------------------------------
# 8. Timestamp Conversion Utility
# -------------------------------
# Convert a Unix timestamp (in ms) to a human-readable format.
timestamp = 1745193600000
print("\nConverted Timestamp:")
print(bdomarket.ConvertTimestamp(timestamp))

# -------------------------------
# 9. Item Object Usage
# -------------------------------
# Create an Item object, print its details, and download its icon.
item = bdomarket.item.Item()
print("\nItem Object:")
print(item)
print("Item as dict:", item.to_dict())

# Download the item's icon by ID (absolute path) and by name (relative path).
item.GetIcon(r"D:\bdomarket\icons", False, bdomarket.item.ItemProp.ID)
item.GetIcon("icons", True, bdomarket.item.ItemProp.NAME)