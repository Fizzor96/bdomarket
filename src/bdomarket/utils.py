from enum import Enum
import json
from datetime import datetime
import os

class AvailableApiVersions(Enum):
    V1 = "v1"
    V2 = "v2"

class AvailableRegions(Enum):
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
    
class SupportedLanguages(Enum):
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
        
class ApiResponse:
    def __init__(self, success: bool = False, statuscode: int = -1, message: str = "", content: str = ""):
        self.success = success
        self.statuscode = statuscode
        self.message: str = message
        self.content: str = content if content else ""
        
    def __str__(self):
        return f"success: {self.success}\nstatuscode: {self.statuscode}\nmessage: {self.message}\ncontent: {self.content}"
    
    def GetIterableContent(self):
        try:
            return json.loads(self.content)
        except:
            raise Exception("Could not get IterableObject!")
        
    def SaveToFile(self, path: str):
        folder = os.path.dirname(path)
        os.makedirs(folder, exist_ok=True)
        data = {
            "success": self.success,
            "statuscode": self.statuscode,
            "message": self.message,
            "content": json.loads(self.content)
        }
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

def ConvertTimestamp(timestamp_ms:float):
    return datetime.utcfromtimestamp(timestamp_ms / 1000).strftime("%Y-%m-%d")