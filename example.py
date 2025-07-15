import bdomarket

market = bdomarket.Market(bdomarket.AvailableRegions.EU, bdomarket.AvailableApiVersions.V2, bdomarket.SupportedLanguages.English)

# Each function return ApiResponse obj - this can be used to acess information more easier
market.GetWorldMarketWaitList().content
market.GetWorldMarketWaitList().statuscode
market.GetWorldMarketWaitList().success
market.GetWorldMarketWaitList().message # this is kinda pointless, devs did not implement such functionality
iterable = market.GetWorldMarketWaitList().GetIterableContent() # Deserialize to a Python object.
for item in iterable:
    print(item)
market.GetWorldMarketWaitList().SaveToFile("responses/waitlist/get.json") # saving output to file
print(bdomarket.ConvertTimestamp(1745193600000)) # can be useful if you don't know how to convert Unix timestamps to human readable format. Note (Post)GetMarketPriceInfo return timestamps...

# WaitList
market.GetWorldMarketWaitList().SaveToFile("responses/waitlist/get.json")
market.PostGetWorldMarketWaitList().SaveToFile("responses/waitlist/post.json")
print(market.GetWorldMarketWaitList())
print(market.PostGetWorldMarketWaitList())

# HotList
market.GetWorldMarketHotList().SaveToFile("responses/hotlist/get.json")
market.PostGetWorldMarketHotList().SaveToFile("responses/hotlist/post.json")
print(market.GetWorldMarketHotList())
print(market.PostGetWorldMarketHotList())

# List
market.GetWorldMarketList("1", "1").SaveToFile("responses/list/get.json")
market.PostGetWorldMarketList("1", "1").SaveToFile("responses/list/post.json")
print(market.GetWorldMarketList("1", "1"))
print(market.PostGetWorldMarketList("1", "1"))


# SubList
market.GetWorldMarketSubList(["735008", "731109"]).SaveToFile("responses/sublist/get.json")
market.PostGetWorldMarketSubList(["735008", "731109"]).SaveToFile("responses/sublist/post.json")
print(market.GetWorldMarketSubList(["735008", "731109"]))
print(market.PostGetWorldMarketSubList(["735008", "731109"]))


# SearchList
market.GetWorldMarketSearchList(["735008", "731109"]).SaveToFile("responses/searchlist/get.json")
market.PostGetWorldMarketSearchList(["735008", "731109"]).SaveToFile("responses/searchlist/post.json")
print(market.GetWorldMarketSearchList(["735008", "731109"]))
print(market.PostGetWorldMarketSearchList(["735008", "731109"]))


# BiddingInfo
market.GetBiddingInfo(["735008", "731109"], ["19", "20"]).SaveToFile("responses/bidding/get.json")
market.PostGetBiddingInfo(["735008", "731109"], ["19", "20"]).SaveToFile("responses/bidding/post.json")
print(market.GetBiddingInfo(["735008", "731109"], ["19", "20"]))
print(market.PostGetBiddingInfo(["735008", "731109"], ["19", "20"]))


# PriceInfo
market.GetMarketPriceInfo(["735008", "731109"], ["19", "20"]).SaveToFile("responses/priceinfo/get.json")
market.PostGetMarketPriceInfo(["735008"], ["20"]).SaveToFile("responses/priceinfo/post.json")
print(market.GetMarketPriceInfo(["735008", "731109"], ["19", "20"]))
print(market.PostGetMarketPriceInfo(["735008"], ["20"]))


# PearItems
market.GetPearlItems().SaveToFile("responses/pearlitems/get.json")
market.PostGetPearlItems().SaveToFile("responses/pearlitems/post.json")
print(market.GetPearlItems())
print(market.PostGetPearlItems())


# Market
market.GetMarket().SaveToFile("responses/market/get.json")
market.PostGetMarket().SaveToFile("responses/market/post.json")
print(market.GetMarket())
print(market.PostGetMarket())
