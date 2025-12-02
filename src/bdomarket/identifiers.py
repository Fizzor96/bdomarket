# pylint: disable=missing-module-docstring, line-too-long, invalid-name
import enum

class ApiVersion(enum.Enum):
    """
    Represents the available API versions for the BDO Market.

    :var V1: Version 1 of the API.
    :vartype V1: Literal['v1']
    :var V2: Version 2 of the API, offering updated features and endpoints.
    :vartype V2: Literal['v2']
    """
    V1 = "v1"
    """"""
    V2 = "v2"
    """"""

class MarketRegion(enum.Enum):
    """
    Represents the available market regions for the BDO Market API.

    :var NA: North America region
    :vartype NA: Literal['na']
    :var EU: Europe region
    :vartype EU: Literal['eu']
    :var SEA: Southeast Asia region
    :vartype SEA: Literal['sea']
    :var MENA: Middle East and North Africa region
    :vartype MENA: Literal['mena']
    :var KR: Korea region
    :vartype KR: Literal['kr']
    :var RU: Russia region
    :vartype RU: Literal['ru']
    :var JP: Japan region
    :vartype JP: Literal['jp']
    :var TH: Thailand region
    :vartype TH: Literal['th']
    :var TW: Taiwan region
    :vartype TW: Literal['tw']
    :var SA: South America region
    :vartype SA: Literal['sa']
    :var CONSOLE_EU: Console Europe region
    :vartype CONSOLE_EU: Literal['console_eu']
    :var CONSOLE_NA: Console North America region
    :vartype CONSOLE_NA: Literal['console_na']
    :var CONSOLE_ASIA: Console Asia region
    :vartype CONSOLE_ASIA: Literal['console_asia']
    """
    NA = "na"
    """"""
    EU = "eu"
    """"""
    SEA = "sea"
    """"""
    MENA = "mena"
    """"""
    KR = "kr"
    """"""
    RU = "ru"
    """"""
    JP = "jp"
    """"""
    TH = "th"
    """"""
    TW = "tw"
    """"""
    SA = "sa"
    """"""
    CONSOLE_EU = "console_eu"
    """"""
    CONSOLE_NA = "console_na"
    """"""
    CONSOLE_ASIA = "console_asia"
    """"""

class Locale(enum.Enum):
    """
    Represents the supported locales/languages for the BDO Market API.

    Each enum value corresponds to a language code used for localization in API requests and responses.

    :var English: English language locale
    :vartype English: Literal['en']
    :var German: German language locale
    :vartype German: Literal['de']
    :var French: French language locale
    :vartype French: Literal['fr']
    :var Russian: Russian language locale
    :vartype Russian: Literal['ru']
    :var SpanishEU: Spanish (Europe) language locale
    :vartype SpanishEU: Literal['es']
    :var PortugueseRedFox: Portuguese (RedFox) language locale
    :vartype PortugueseRedFox: Literal['sp']
    :var Portuguese: Portuguese language locale
    :vartype Portuguese: Literal['pt']
    :var Japanese: Japanese language locale
    :vartype Japanese: Literal['jp']
    :var Korean: Korean language locale
    :vartype Korean: Literal['kr']
    :var Thai: Thai language locale
    :vartype Thai: Literal['th']
    :var Turkish: Turkish language locale
    :vartype Turkish: Literal['tr']
    :var ChineseTaiwan: Chinese (Taiwan) language locale
    :vartype ChineseTaiwan: Literal['tw']
    :var ChineseMainland: Chinese (Mainland) language locale
    :vartype ChineseMainland: Literal['cn']
    """
    English = "en"
    """"""
    German = "de"
    """"""
    French = "fr"
    """"""
    Russian = "ru"
    """"""
    SpanishEU = "es"
    """"""
    PortugueseRedFox = "sp"
    """"""
    Portuguese = "pt"
    """"""
    Japanese = "jp"
    """"""
    Korean = "kr"
    """"""
    Thai = "th"
    """"""
    Turkish = "tr"
    """"""
    ChineseTaiwan = "tw"
    """"""
    ChineseMainland = "cn"
    """"""

class PigCave(enum.Enum):
    """
    Represents the available Pig Cave server identifiers for the BDO Market API.

    Each enum value corresponds to a specific Pig Cave server region used for API requests and responses.

    :var NA: North America Pig Cave server
    :vartype NA: Literal['napig']
    :var EU: Europe Pig Cave server
    :vartype EU: Literal['eupig']
    :var JP: Japan Pig Cave server
    :vartype JP: Literal['jppig']
    :var KR: Korea Pig Cave server
    :vartype KR: Literal['krpig']
    :var RU: Russia Pig Cave server
    :vartype RU: Literal['rupig']
    :var SA: South America Pig Cave server
    :vartype SA: Literal['sapig']
    :var TW: Taiwan Pig Cave server
    :vartype TW: Literal['twpig']
    :var ASIA: Asia Pig Cave server
    :vartype ASIA: Literal['asiapig']
    :var MENA: Middle East and North Africa Pig Cave server
    :vartype MENA: Literal['menapig']
    """
    NA = "napig"
    """"""
    EU = "eupig"
    """"""
    JP = "jppig"
    """"""
    KR = "krpig"
    """"""
    RU = "rupig"
    """"""
    SA = "sapig"
    """"""
    TW = "twpig"
    """"""
    ASIA = "asiapig"
    """"""
    MENA = "menapig"
    """"""
    
class Server(enum.Enum):
    """
    Represents the available server identifiers for the BDO Market API.

    Each enum value corresponds to a specific server region or platform used for API requests and responses.

    :var EU: Europe server
    :vartype EU: Literal['eu']
    :var NA: North America server
    :vartype NA: Literal['na']
    :var ASIAPS: Asia PlayStation server
    :vartype ASIAPS: Literal['ps4-asia']
    :var JP: Japan server
    :vartype JP: Literal['jp']
    :var KR: Korea server
    :vartype KR: Literal['kr']
    :var MENA: Middle East and North Africa server
    :vartype MENA: Literal['mena']
    :var NAPS: North America PlayStation/Xbox server
    :vartype NAPS: Literal['ps4-xbox-na']
    :var RU: Russia server
    :vartype RU: Literal['ru']
    :var SA: South America server
    :vartype SA: Literal['sa']
    :var SEA: Southeast Asia server
    :vartype SEA: Literal['sea']
    :var TH: Thailand server
    :vartype TH: Literal['th']
    :var TW: Taiwan server
    :vartype TW: Literal['tw']
    """
    EU = "eu"
    """"""
    NA = "na"
    """"""
    ASIAPS = "ps4-asia"
    """"""
    JP = "jp"
    """"""
    KR = "kr"
    """"""
    MENA = "mena"
    """"""
    NAPS = "ps4-xbox-na"
    """"""
    RU = "ru"
    """"""
    SA = "sa"
    """"""
    SEA = "sea"
    """"""
    TH = "th"
    """"""
    TW = "tw"
    """"""
    
class ItemProp(enum.Enum):
    """
    Represents item properties used in the BDO Market API.

    :var ID: The unique identifier for the item.
    :vartype ID: Literal[0]
    :var NAME: The name of the item.
    :vartype NAME: Literal[1]
    """
    ID = 0
    """"""
    NAME = 1
    """"""