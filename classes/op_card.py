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
    id = Column(Integer, primary_key=True)
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
        self.power:int = power
        self.effect:list[str] = effect
        self.counter:int = counter
        self.trigger:str = trigger
        self.card_set:str  =  card_set
        self.color:list[Color] = color
        self.rarity:Rarity = rarity,
        self.card_type:str   =  card_type
        self.feature:list[str] = feature
        self.attribute:str = attribute
        self.cost:int  =  cost

  
    def clear_text(xml, split=None) -> str|list[str]:
        text = xml
        return text
    
    def clear_int(xml) -> int:
        num = xml
        return num
    
