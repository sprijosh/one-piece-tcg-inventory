import re
import json
from enum import Enum
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# Define the base for SQLAlchemy
Base = declarative_base()

class Rarity(Enum):
    C = "C"
    UC = "UC"
    R = "R"
    SR = "SR"
    SEC = "SEC"
    P = "P"
    L = "LEADER"

class Color(Enum):
    G = ("綠", "Green")    # Green
    R = ("紅", "Red")      # Red
    P = ("紫", "Purple")   # Purple
    BU = ("藍", "Blue")    # Blue
    BK = ("黑", "Black")   # Black
    Y = ("黃", "Yellow")   # Yellow

    @staticmethod
    def from_chinese(chinese_name: str):
        for color in Color:
            if color.value[0] == chinese_name:
                return color
        raise ValueError(f"Color '{chinese_name}' not found.")

# Define SQLAlchemy models
class RarityModel(Base):
    __tablename__ = 'rarities'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

class ColorModel(Base):
    __tablename__ = 'colors'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


class OPCard(Base):
    __tablename__ = 'opcards'
    id = Column(String, primary_key=True)
    name = Column(String)
    card_id = Column(String)
    imageUrl = Column(String)
    alternate = Column(Boolean)
    power = Column(Integer)
    effect = Column(String)  # Store as comma-separated values
    counter = Column(Integer)
    card_set = Column(String)
    color_id = Column(Integer, ForeignKey('colors.id'))
    rarity_id = Column(Integer, ForeignKey('rarities.id'))
    card_type = Column(String)
    feature = Column(String)  # Store as comma-separated values
    attribute = Column(String)
    cost = Column(Integer)

    color = relationship("ColorModel")
    rarity = relationship("RarityModel")


    def __init__(self, name, ID, imageUrl, alternate, power, effect, counter, 
                 card_set, color, rarity, card_type, feature, attribute, cost,  trigger=""):
        self.name:str =  name,
        self.ID:str = ID,
        self.imageUrl:str = imageUrl
        self.alternate:bool = alternate
        self.power:int = self.clear_int(power)
        self.effect:list[str] = self.clear_text(effect, split="<br/>")
        self.counter:int = self.clear_int(counter)
        self.trigger:str = self.clear_text(trigger, split="<br/>")
        self.card_set:str  =  card_set
        self.color:list[Color] = self.clear_text(color, split="/")
        self.rarity:Rarity = rarity,
        self.card_type:str   =  card_type
        self.feature:list[str] = feature
        self.attribute:str = attribute
        self.cost:int  =  self.clear_int(cost)

  
    def clear_text(self, xml_text, split=None) -> str|list[str]:
        text = xml_text.split("</h3>")[-1]
        if split:
            return text.split(split)
        return text
    
    def clear_int(self, xml_text) -> int:
        num =  re.search(r'\d+', xml_text)
        if num:
            return int(num.group())
        return 0
    
    def __str__(self):
        return (f"OPCard(name={self.name}, card_id={self.card_id}, imageUrl={self.imageUrl}, "
                f"alternate={self.alternate}, power={self.power}, effect={self.effect}, "
                f"counter={self.counter}, card_set={self.card_set}, color={self.color}, "
                f"rarity={self.rarity}, card_type={self.card_type}, "
                f"feature={self.feature}, attribute={self.attribute}, cost={self.cost})")
    
    def to_json(self):
            return {
                "name": self.name,
                "card_id": self.ID,
                "imageUrl": self.imageUrl,
                "alternate": self.alternate,
                "power": self.power,
                "effect": self.effect,
                "counter": self.counter,
                "card_set": self.card_set,
                "color": self.color,
                "rarity": self.rarity,
                "card_type": self.card_type,
                "feature": self.feature,
                "attribute": self.attribute,
                "cost": self.cost
            }