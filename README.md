<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
<!-- [![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url] -->
[![PyPI - Downloads](https://img.shields.io/pepy/dt/bdomarket?style=for-the-badge&logo=pypi&logoColor=white&label=Downloads&color=blue)](https://pepy.tech/project/bdomarket)
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![project_license][license-shield]][license-url]
[![discord][discord-shield]][discord-link]
<!-- [![LinkedIn][linkedin-shield]][linkedin-url] -->



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Fizzor96/bdomarket">
    <img src="https://github.com/Fizzor96/bdomarket/blob/master/images/logo.png" alt="Logo" width="800" height="380">
  </a>


<h3 align="center">bdomarket</h3>

  <p align="center">
    API client for BDO market data
    <br />
    <a href="https://fizzor96.github.io/bdomarket/"><strong>Explore the docs »</strong></a>
    <!-- <br /> -->
    <br />
    <a href="https://pypi.org/project/bdomarket/">PyPI</a>
    &middot;
    <a href="https://github.com/Fizzor96/bdomarket/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/Fizzor96/bdomarket/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This code is a simple and well-structured API client for BDO market data, built for convenience. It enables developers to access market information, price history, and shop data from Arsha.io in a standardized way.

## Features

- **Market Data Access**: Retrieve real-time and historical data from the BDO Central Market, including waitlists, hotlists, item lists, sublists, search results, bidding info, and price info.
- **Boss Timers**: Easily fetch and display world boss spawn times for different servers and regions.
- **Item Management**: Query single or multiple items by ID, dump large ranges of item data, and work with item objects that support conversion to dictionaries and icon downloading.
- **API Response Handling**: All API calls return a standardized `ApiResponse` object, making it easy to access content, status codes, and success flags, as well as to deserialize responses into Python objects.
- **Data Export**: Save any API response directly to a file in JSON format for later analysis or debugging.
- **Timestamp Conversion**: Convert Unix timestamps from API responses into human-readable date and time strings.
- **Multi-Region and Multi-Language Support**: Easily switch between different BDO regions (EU, NA, etc.) and supported languages.
- **Convenient Utilities**: Download item icons, print readable representations of items, and more.
- **Regional Pig Cave Status**: Easily fetch pig cave status for different regions.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Get involved

[![discord][discord-shield]][discord-link]

### Donate

If you like my project, you can buy me a coffee, many thanks ❤️ !

<a href="https://www.buymeacoffee.com/fizzor"><img src="images/bmc-button.png" width="120" height="30"/></a>


### Built With

[![Python][Python.com]][Python-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

A Python API client for accessing the [Arsha.io Black Desert Online Market API](https://www.postman.com/bdomarket/arsha-io-bdo-market-api/overview).

Easily retrieve market data, hotlist items, price history, bidding info, and more.

### Prerequisites

Python installed on your system.
* Python >= 3.9

### Installation
   ```sh
   pip install bdomarket
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

### Quick Start — ArshaMarket (async)

```python
import asyncio
import bdomarket

async def main():
    async with bdomarket.Market(
        region=bdomarket.MarketRegion.EU,
        apiversion=bdomarket.ApiVersion.V2,
        language=bdomarket.Locale.English
    ) as market:
        # Wait list
        r = await market.get_world_market_wait_list()
        print(r.success, r.status_code)
        r.save_to_file("responses/waitlist.json")

        # Hot list
        r = await market.get_world_market_hot_list()
        r.save_to_file("responses/hotlist.json")

        # Price history (convertdate converts timestamps, formatprice adds separators)
        r = await market.get_market_price_info(
            ids=["735008", "735009"], sids=["20", "20"],
            convertdate=True, formatprice=False
        )
        r.save_to_file("responses/priceinfo.json")

        # Items by category (mainCategory=1 Weapons, subCategory=1 Swords)
        r = await market.get_world_market_list(main_category="1", sub_category="1")
        r.save_to_file("responses/marketlist.json")

        # Sub list — all enhancement levels for an item
        r = await market.get_world_market_sub_list(ids=["735008"])
        r.save_to_file("responses/sublist.json")

        # Bidding info — current buy/sell orders
        r = await market.get_bidding_info(ids=["735008", "735009"], sids=["20", "20"])
        r.save_to_file("responses/biddinginfo.json")

        # Pearl items
        r = await market.get_pearl_items()
        r.save_to_file("responses/pearlitems.json")

        # Full market snapshot
        r = await market.get_market()
        r.save_to_file("responses/market.json")

        # Item lookup
        r = await market.get_item(ids=["735008"])
        r.save_to_file("responses/item.json")

        # Item database dump (full)
        r = await market.item_database_dump_v2()
        r.save_to_file("responses/itemdump.json")
        if r.success and r.content:
            print(bdomarket.get_items_by_name_from_db(r.content, "Blackstar Shuriken"))
            print(bdomarket.get_items_by_id_from_db(r.content, 735008))

asyncio.run(main())
```

### Sync usage — ArshaMarket

Every async method has a `_sync` counterpart. Pass `Market(...)` without `async with`
and call `.close()` when done:

```python
market = bdomarket.Market(
    region=bdomarket.MarketRegion.EU,
    apiversion=bdomarket.ApiVersion.V2,
    language=bdomarket.Locale.English
)

r = market.get_world_market_wait_list_sync()
r.save_to_file("responses/waitlist.json")

r = market.get_bidding_info_sync(ids=["735008", "735009"], sids=["20", "20"])
r.save_to_file("responses/biddinginfo.json")

# ... all other _sync methods follow the same pattern ...

market.close()
```

### UnofficialMarket

```python
import asyncio
import bdomarket

async def main():
    async with bdomarket.UnofficialMarket(
        region=bdomarket.MarketRegion.EU,
        language=bdomarket.Locale.English
    ) as u:
        # Queue list (items awaiting listing)
        r = await u.get_list_queue()
        print(r.success, r.status_code)

        # Items by category
        r = await u.get_list_category(main_category=20, sub_category=1)

        # Item details by ID
        r = await u.get_item_id(item_id=12094)
        if r.success:
            print(r.content.get("name"), r.content.get("grade"))

        # Item icon (returns raw PNG bytes)
        r = await u.get_item_id_icon(item_id=12094)
        if r.success:
            r.save_image("responses/icons/12094.png")

        # Enhancement details and tooltip
        r = await u.get_item_id_enhancement(item_id=12094, enhancement=5)
        r = await u.get_item_id_enhancement_tooltip(item_id=12094, enhancement=5)

        # Search by name
        r = await u.get_search(search_string="Deboreka Ring")
        if r.success:
            print(f"Found {len(r.content)} result(s)")

asyncio.run(main())
```

> All `UnofficialMarket` methods also have `_sync` variants
> (e.g. `get_list_queue_sync()`, `get_item_id_sync()`, `get_search_sync()`).

### Boss Timer

```python
import bdomarket

boss = bdomarket.Boss(server=bdomarket.Server.EU).scrape()
print(boss.get_timer())          # list of dicts
print(boss.get_timer_json())     # JSON string
```

### Item Icon Downloader

```python
import bdomarket

item = bdomarket.Item(item_id="735008", name="Blackstar Shuriken")

# Save as "735008.png"
item.get_icon("responses/icons", isrelative=True, filenameprop=bdomarket.ItemProp.ID)

# Save as "Blackstar Shuriken.png"
item.get_icon("responses/icons", isrelative=True, filenameprop=bdomarket.ItemProp.NAME)

print(item.to_dict())
```

### Pig Cave Server Status

```python
import asyncio
import bdomarket

async def main():
    pig = bdomarket.Pig(region=bdomarket.PigCave.EU)
    r = await pig.get_status()
    print(r.success, r.status_code)

asyncio.run(main())
```

### Utility Functions

```python
import datetime
import bdomarket

# Timestamp ↔ datetime conversion
dt = bdomarket.timestamp_to_datetime(1745193600.0)
ts = bdomarket.datetime_to_timestamp(datetime.datetime(2025, 4, 21, tzinfo=datetime.timezone.utc))

# Query an in-memory item list (e.g. result of item_database_dump_v2)
matches = bdomarket.get_items_by_name_from_db(item_list, "Blackstar Shuriken")
matches = bdomarket.get_items_by_id_from_db(item_list, 735008)

# Query a saved JSON file produced by item_database_dump_v2 → save_to_file
matches = bdomarket.search_items_by_name("responses/itemdump.json", "Kzarka")
matches = bdomarket.search_items_by_id("responses/itemdump.json", 12094)
```

> 💡 See [`example.py`](https://github.com/Fizzor96/bdomarket/blob/master/example.py) for a
> complete runnable demo of **every** feature, including all sync variants.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] Market Data Access  
    - [x] Retrieve real-time market data  
    - [x] Retrieve historical market data  
    - [x] Get waitlists, hotlists, item lists, sublists, and search results  
- [x] Boss Timers  
    - [x] Fetch world boss spawn times for all supported servers and regions  
- [x] Item Management  
    - [x] Query single or multiple items by ID  
    - [x] Dump large ranges of item data  
    - [x] Item object conversion to dictionary  
    - [x] Download item icons  
- [x] API Response Handling  
    - [x] Standardized ApiResponse object for all API calls  
    - [x] Deserialize responses into Python objects  
- [x] Data Export  
    - [x] Save API responses to JSON files  
- [x] Timestamp Conversion  
    - [x] Convert Unix timestamps to human-readable format  
- [x] Multi-Region and Multi-Language Support  
    - [x] Switch between BDO regions  
    - [x] Switch between supported languages  
- [x] Utilities  
    - [x] Print readable representations of items  
    - [x] Additional helper functions  
- [/] Error Handling & Robustness  
    - [x] Graceful handling of network/API errors  
    - [ ] Retry logic for failed requests  
    - [x] Safe terminal execution on Windows (Unicode safety)  
- [/] Documentation  
    - [ ] Comprehensive API documentation  
    - [x] Usage examples and tutorials  
    - [x] Docstrings for all public classes and methods  
- [ ] Testing  
    - [ ] Unit tests for core functionality  
    - [ ] Integration tests for API endpoints  
- [ ] Search & Filtering  
    - [x] Search items by name or partial match  
    - [ ] Filter market data by category, price, etc.  
- [x] Performance Improvements  
    - [x] Async support for faster data retrieval  
- [ ] CLI Tool  
    - [ ] Command-line interface for quick queries and downloads  
- [ ] Webhook/Notification Support  
    - [ ] Notify users of market changes or boss

See the [open issues](https://github.com/Fizzor96/bdomarket/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
<!-- ## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p> -->

### Top contributors:

<a href="https://github.com/Fizzor96/bdomarket/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Fizzor96/bdomarket" alt="contrib.rocks image" />
</a>



<!-- LICENSE -->
## License

Distributed under the **GNU General Public License v3.0**.  
See `LICENSE` for more information.

This project is **copyleft**: you may copy, distribute, and modify it under the terms of the GPL, but derivative works must also be open source under the same license.

[Learn more about GPL-3.0 »](https://www.gnu.org/licenses/gpl-3.0.html)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Szőke Dominik - szokedominik@gmail.com

Project Link: [https://github.com/Fizzor96/bdomarket](https://github.com/Fizzor96/bdomarket)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
<!-- ## Acknowledgments

* []()
* []()
* []()

<p align="right">(<a href="#readme-top">back to top</a>)</p> -->



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Fizzor96/bdomarket.svg?style=for-the-badge
[contributors-url]: https://github.com/Fizzor96/bdomarket/graphs/contributors

[forks-shield]: https://img.shields.io/github/forks/Fizzor96/bdomarket.svg?style=for-the-badge
[forks-url]: https://github.com/Fizzor96/bdomarket/network/members

[stars-shield]: https://img.shields.io/github/stars/Fizzor96/bdomarket.svg?style=for-the-badge
[stars-url]: https://github.com/Fizzor96/bdomarket/stargazers

[issues-shield]: https://img.shields.io/github/issues/Fizzor96/bdomarket.svg?style=for-the-badge
[issues-url]: https://github.com/Fizzor96/bdomarket/issues

[license-shield]: https://img.shields.io/github/license/Fizzor96/bdomarket.svg?style=for-the-badge
[license-url]: https://github.com/Fizzor96/bdomarket/blob/master/LICENSE

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username

[product-screenshot]: images/screenshot.png
[Python-url]: https://www.python.org/
[Python.com]: https://img.shields.io/badge/python-0769AD?style=for-the-badge&logo=python&logoColor=white

[discord-shield]: https://img.shields.io/badge/Discord-blue?style=for-the-badge&logo=Discord&logoColor=white&logoSize=auto
[discord-link]: https://discord.gg/hSWHfhSpDe