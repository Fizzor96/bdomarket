import os
import requests
from enum import Enum

class ItemProp(Enum):
    ID = 0
    NAME = 1

class Item:
    def __init__(self, id: str = "735008", name: str = "Blackstar Shuriken", sid: str = "0"):
        """Initialize an Item object.

        Args:
            id (str, optional): The unique identifier for the item. Defaults to "735008".
            name (str, optional): The name of the item. Defaults to "Blackstar Shuriken".
            sid (str, optional): The sidentifier for the item can be the enchancement level. Defaults to "0".
        """
        self.id = id
        self.sid = sid
        self.name = name
        # TODO: grade
        self.grade = 0

    def __repr__(self):
        """Representation of the Item object.

        Returns:
            str: A string representation of the item including its id, name, and sid.
        """
        return f"Item(id={self.id}, name='{self.name}', sid={self.sid})"
    
    def __str__(self):
        """String representation of the Item object.

        Returns:
            str: A string describing the item with its name, id, and sid.
        """
        return f"Item: {self.name} (ID: {self.id}, SID: {self.sid})"

    def to_dict(self):
        """Convert the item to a dictionary representation.

        Returns:
            dict: A dictionary containing the item's id, name, and sid.
        """
        return {
            "item_id": self.id,
            "name": self.name,
            "sid": self.sid
        }
        
    def GetIcon(self, folderpath: str = "icons", isrelative: bool = True, filenameprop:ItemProp = ItemProp.ID):
        """Download the icon for the item and save it to the specified folder.

        Args:
            folderpath (str, optional): The path to the folder where the icon will be saved. Defaults to "icons".
            isrelative (bool, optional): If True, the folderpath is treated as relative to the current file. If False, it is treated as absolute. Defaults to True.
            filenameprop (ItemProp, optional): Determines whether to use the item's ID or name for the filename. Defaults to ItemProp.ID.
        """
        if not folderpath:
            folderpath = "icons"
        
        # Determine the folder path based on whether it is relative or absolute
        if isrelative:
            folder = folderpath
        else:
            folder = os.path.join(os.path.dirname(__file__), folderpath)
            
        # Check if the folder exists
        if not os.path.exists(folder):
            os.makedirs(folder)

        # Check if file already exists with id
        if os.path.exists(os.path.join(folder, f"{self.id}.png")) and filenameprop == ItemProp.ID:
            return
        
        # Check if file already exists with name
        if os.path.exists(os.path.join(folder, f"{self.name}.png")) and filenameprop == ItemProp.NAME:
            return
                
        # If folder exist but file does not, we can download the icon
        response = requests.get(f"https://s1.pearlcdn.com/NAEU/TradeMarket/Common/img/BDO/item/{self.id}.png")
        if 199 < response.status_code < 300:
            with open(f"{folder}/{self.id if filenameprop == ItemProp.ID else self.name}.png", "wb") as file:
                file.write(response.content)