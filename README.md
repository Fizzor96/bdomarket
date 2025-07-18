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
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![project_license][license-shield]][license-url]
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
    <!-- <a href="https://github.com/Fizzor96/bdomarket"><strong>Explore the docs »</strong></a> -->
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
* Python >= 3.8

### Installation
   ```sh
   pip install bdomarket
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage
```python
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

```

<!-- _For more examples, please refer to the [Documentation](https://example.com)_ -->

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
    - [ ] Searching items by name or ID in DBdump?
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
- [ ] Error Handling & Robustness  
    - [ ] Graceful handling of network/API errors  
    - [ ] Retry logic for failed requests  
    - [ ] Logging for debugging and monitoring  
- [ ] Documentation  
    - [ ] Comprehensive API documentation  
    - [ ] Usage examples and tutorials  
    - [ ] Docstrings for all public classes and methods  
- [ ] Testing  
    - [ ] Unit tests for core functionality  
    - [ ] Integration tests for API endpoints  
- [ ] Search & Filtering  
    - [ ] Search items by name or partial match  
    - [ ] Filter market data by category, price, etc.  
- [x] Performance Improvements  
    - [x] Async support for faster data retrieval  
- [ ] CLI Tool  
    - [ ] Command-line interface for quick queries and downloads  
- [ ] Webhook/Notification Support  
    - [ ] Notify users of market changes or boss

See the [open issues](https://github.com/github_username/repo_name/issues) for a full list of proposed features (and known issues).

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

### Example:

```python
market.GetBiddingInfo(["735008", "731109"], ["19", "20"]).SaveToFile("responses/bidding/get.json")
```

Outputs:

```json
{
  "success": true,
  "statuscode": 200,
  "message": "No message provided",
  "content": [
    {
      "name": "Blackstar Shuriken",
      "id": 735008,
      "sid": 19,
      "orders": [
        {
          "price": 14500000000,
          "sellers": 1,
          "buyers": 0
        },
        {
          "price": 15500000000,
          "sellers": 1,
          "buyers": 0
        },
        {
          "price": 14900000000,
          "sellers": 4,
          "buyers": 0
        },
        {
          "price": 14700000000,
          "sellers": 0,
          "buyers": 0
        }
      ]
    },
    {
      "name": "Blackstar Sura Katana",
      "id": 731109,
      "sid": 20,
      "orders": [
        {
          "price": 72500000000,
          "sellers": 1,
          "buyers": 0
        },
        {
          "price": 73500000000,
          "sellers": 1,
          "buyers": 0
        },
        {
          "price": 73000000000,
          "sellers": 1,
          "buyers": 0
        },
        {
          "price": 70500000000,
          "sellers": 0,
          "buyers": 0
        }
      ]
    }
  ]
}
```

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

<!-- Your Name - [@twitter_handle](https://twitter.com/twitter_handle) - email@email_client.com -->

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