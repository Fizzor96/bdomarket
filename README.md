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
    <a href="https://github.com/Fizzor96/bdomarket">View Demo</a>
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

<p align="right">(<a href="#readme-top">back to top</a>)</p>



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

# Boss timer
bt = bdomarket.timers.Boss()
bt.Scrape()
print(bt.GetTimerJSON())



```

<!-- _For more examples, please refer to the [Documentation](https://example.com)_ -->

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
<!-- ## Roadmap

- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3
    - [ ] Nested Feature

See the [open issues](https://github.com/github_username/repo_name/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p> -->



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