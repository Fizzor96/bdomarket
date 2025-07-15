from src.bdomarket.timers import Boss, Server

bt = Boss(Server.EU)
bt.Scrape()
print(bt.GetTimerJSON())