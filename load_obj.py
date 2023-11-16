#!/usr/bin/python3

from models import storage
from models.environment import Environment
from models.street import Street
from models.service_category import ServiceCategory
from models.category import Category


# Load Environments
print("Creating Environments...")
envs = ["Adolor", "BDPA", "Ebvoumore", "Evidence", "Ekosodin", "Isihor", "Osasogie", "Oluku",
        "Uselu"]
for env in envs:
        env_dict = {"name": env}
        model = Environment(**env_dict)
        print("{} --> {}".format(env, model.id))
        model.save()

# Load Service categories
print("Creating service Categories...")
cats = ["AC installer", "Carpenter", "DSTV installer", "Electrician", "Fashion Designer",
        "Generator Repairer", "Hair Stylist", "Logistics", "Make up artist", "Painter", "Plumber",
        "Refrigerator repairer", "Welder"]
for cat in cats:
        cat_dict = {"name": cat}
        model = ServiceCategory(**cat_dict)
        print("{} --> {}".format(cat, model.id))
        model.save()

# Load product categories
print()
print("Creating Product categories...")
cats = ["Beds and beddings", "Books and stationery","Cosmetics and care products",
        "Clothing and Accesories", "Drinks and Beverages", "Footwear",
        "Electronics and Accessories", "Food and Groceries", "Home furniture",
        "Kitchen utensils", "Laptops and Accessories", "Jewellery", "Phones and Accessories",
        "Stationery"]
for cat in cats:
        cat_dict = {"name": cat}
        model = Category(**cat_dict)
        print("{} --> {}".format(cat, model.id))
        model.save()

# Load streets
print()
print("Creating streets...")
streets = {"Osasogie": ["Holy Rosary", "Winners road", "Technical road", "Ozakpolor"
                        "Edudje", "Federal Girl's road", "Ogbeide", "Egbon", "Irowa Obazie",
                        ],
        "Ekosodin": ["Newton", "Edo", "Boundary", "Market road", "JB", "Ekhorutomwen",
                        "Eguavoen", "Ohunwu", "Igbineweka"],
        "BDPA": ["11th", "12th", "13th", "18th", "19th", "20th", "21st", "22nd", "23rd", "24th",
                "Uno", "Okukpun", "Ola Okeaye", "Eyeye", "Abu", "Hilary Adiki", "Anyeaji",
                "Lucky", "Imiuwu"],
        "Evidence": ["Aibalegbe", "Ohenhen", "Egiaruoyi", "Osasere Osayogie", "Iguodala",
                        "Igbineweka"],
        "Isihor": ["Egbaen Community road"]
        }

for env in streets:
        print(f'creating streets for the environment: ${env}...')
        try:
                strt = storage.search(Environment, name=env)[0]
                for item in streets[env]:
                        strtDict = {"name": item, "env_id": strt.id}
                        model = Street(**strtDict)
                        model.save()
                        print(f"{model.name} --> {model.id}")
                        print("------------------")
        except:
                print(f"{env} not found")
                continue
