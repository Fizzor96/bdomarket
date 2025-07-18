from enum import Enum

class ApiVersion(Enum):
    V1 = "v1"
    V2 = "v2"

class MarketRegion(Enum):
    NA = "na"
    EU = "eu"
    SEA = "sea"
    MENA = "mena"
    KR = "kr"
    RU = "ru"
    JP = "jp"
    TH = "th"
    TW = "tw"
    SA = "sa"
    CONSOLE_EU = "console_eu"
    CONSOLE_NA = "console_na"
    CONSOLE_ASIA = "console_asia"

class Locale(Enum):
    English = "en"
    German = "de"
    French = "fr"
    Russian = "ru"
    SpanishEU = "es"
    PortugueseRedFox = "sp"
    Portuguese = "pt"
    Japanese = "jp"
    Korean = "kr"
    Thai = "th"
    Turkish = "tr"
    ChineseTaiwan = "tw"
    ChineseMainland = "cn"

class PigCave(Enum):
    NA = "napig"
    EU = "eupig"
    JP = "jppig"
    KR = "krpig"
    RU = "rupig"
    SA = "sapig"
    TW = "twpig"
    ASIA = "asiapig"
    MENA = "menapig"
    
class Server(Enum):
    EU = "eu"
    NA = "na"
    ASIAPS = "ps4-asia"
    JP = "jp"
    KR = "kr"
    MENA = "mena"
    NAPS = "ps4-xbox-na"
    RU = "ru"
    SA = "sa"
    SEA = "sea"
    TH = "th"
    TW = "tw"
    
class ItemProp(Enum):
    ID = 0
    NAME = 1