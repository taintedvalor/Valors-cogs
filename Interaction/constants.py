
from typing import Final, Dict


REDDIT_BASEURL = "https://api.reddit.com/r/{}/random"
IMGUR_LINKS = "http://imgur.com", "https://m.imgur.com", "https://imgur.com"
GOOD_EXTENSIONS = ".png", ".jpg", ".jpeg", ".gif"

ART = ["Art", "learnart", "DrugArt", "ImaginaryLovers", "conceptart", "DigitalArt", "PixelArt"]
CUTE = [
    "cute",
    "Awww",
    "babyduckgifs",
    "rarepuppers",
    "hardcoreaww",
    "FromKittenToCat",
    "cutecats",
]
DUCKS = ["duck", "babyduckgifs"]
FERRETS = ["ferret", "ferrets", "FerretsGoneWild"]
MEMES = ["dankmemes", "memes"]
PHOTOS = [
    "Nikon",
    "postprocessing",
    "streetphotography",
    "ExposurePorn",
    "M43",
    "analog",
    "photographs",
    "mobilephotography",
    "itookapicture",
    "wildlifephotography",
    "SonyAlpha",
    "astrophotography",
    "retouching",
    "iPhoneography",
    "birdpics",
    "Astronomy",
    "LandscapePhotography",
    "lomography",
    "photojournalism",
    "pics",
    "LondonPics",
    "urbanexploration",
    "ChicagoPics",
    "Pentax",
    "hdr",
    "japanpics",
    "foodphotography",
    "blackandwhite",
    "fashionphotography",
    "shootingcars",
    "nightphotography",
    "AbstractPhotos",
    "macro",
]
WALLPAPERS = [
    "wallpaper",
    "iphonewallpapers",
    "MinimalWallpaper",
    "WQHD_Wallpaper",
    "iWallpaper",
    "topwalls",
    "WidescreenWallpaper",
]
RULE34 = [
    "rule34",
    "CartoonRule34",
    "Rimuru_hentai",
]



NEKOS: Final[str] = "https://nekos.best/api/v2/"
ICON: Final[str] = "https://nekos.best/logo_short.png"
ACTIONS: Dict[str, str] = {
    "baka": "baka",
    "cry": "cries at",
    "cuddle": "cuddles",
    "dance": "dance",
    "feed": "feeds",
    "hug": "hugs",
    "kiss": "just kissed",
    "laugh": "laugh at",
    "pat": "pats",
    "poke": "pokes",
    "slap": "just slapped",
    "smile": "smiles at",
    "smug": "smugs",
    "tickle": "tickles",
    "wave": "waves at",
    "bite": "bites",
    "blush": "blushes",
    "bored": "very bored",
    "facepalm": "facepalm",
    "happy": "is happy for",
    "highfive": "highfives",
    "pout": "pout",
    "shrug": "shrugs",
    "sleep": "sleep",
    "stare": "stares at",
    "think": "think",
    "thumbsup": "thumbsup",
    "wink": "winks",
    "handhold": "handholds",
    "kick": "kicks",
    "punch": "punches",
    "shoot": "shoots",
    "yeet": "yeets",
    "nod": "nods",
    "nope": "nope",
    "nom": "nom nom",
}

