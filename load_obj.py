#!/usr/bin/python3

from models import storage
from models.school import School
from models.environment import Environment
from models.street import Street
from models.service_category import ServiceCategory
from models.category import Category

# Load schools
print("Creating schools...")
schools = [("Unilag", "University of Lagos"), ("UNILORIN", "University of Ilorin"),
           ("UNN", "University of Nigeria"), ("Uniport", "University of Port-Harcourt"),
           ("UI", "University of Ibadan"), ("OAU", "Obafemi Awolowo University"),
           ("UniAbuja", "University of Abuja"), ("FUTA", "Federal University of Technology Akure"),
           ("UNIUYO", "University of Uyo"), ("UNIZIK", "Nnamdi Azikwe University"),
           ("UNICAL", "University of Calabar")]
for name, full_name in schools:
    school = School(name=name, full_name=full_name)
    school.save()
    print(f"{school.name} --> {school.id}")

# Load Environments
print("Creating Environments...")
sch_env = {"Unilag": ["Abule-oja", "Pako", "Onike", "Akoka", "Igbobi"],
        "UNN": ["Hilltop", "Odenigwe", "Odim gate", "Behind flat"],
        "UI": ["Agbowo", "Bodija", "Orogun", "Ojoo", "Sango", "Makola"],
        "OAU": ["Oduduwa estate", "Asherifa", "Damico area", "Ibadan road", "Parakin estate",
                "Mayfair", "Oranfe", "Modakeke", "Lagere", "Edunabon", "Fajuiyi"],
        "UniAbuja": ["Iddo sarki", "Pasere", "Iddo sabo", "Gbessa", "Uniabuja staff quarters",
                     "Amma pepple estate", "Toge", "Gosa", "Sauka", "Kango"],
        "Uniport": ["Alakahia", "Aluu", "Back of chem", "Choba", "Choba extension", "Rumekini",
                    "Roumosi"],
        "FUTA": ["North gate", "West gate", "South gate", "Redemption area", "Apatapiti",
                 "Embassy area", "Stateline road", "Baptist student fellowship road", "Clinic"],
        "UNIUYO": ["Ekpany", "Ikpa road", "Itu road", "Udoette", "Urua ikpa"],
        "UNIZIK": ["Amansi", "Aroma", "Commisioners quarters", "Fire", "Reginal", "School gate", "Temp site"],
        "UNICAL": ["Mount zion", "Yellow duke", "Goldie", "Satellite town", "Etta agbor", "Mary slessor"],
        "UNILORIN": ["Chapel bus stop"]}
for sch in sch_env:
    print(f"creating environments for {sch}")
    sch_obj = storage.search("School", name=sch)
    if sch_obj is None or len(sch_obj) == 0:
        print(f"{sch} was not found")
        continue
    sch_mod = sch_obj[0]
    for env in sch_env[sch]:
        model = Environment(name=env, school_id=sch_mod.id)
        model.save()
        print(f"{model.name} --> {model.id}")

# # Load Service categories
# print("Creating service Categories...")
# cats = ["AC installer", "Carpenter", "DSTV installer", "Electrician", "Fashion Designer",
#         "Generator Repairer", "Hair Stylist", "Logistics", "Make up artist", "Painter", "Plumber",
#         "Refrigerator repairer", "Welder"]
# for cat in cats:
#         cat_dict = {"name": cat}
#         model = ServiceCategory(**cat_dict)
#         print("{} --> {}".format(cat, model.id))
#         model.save()

# # Load product categories
# print()
# print("Creating Product categories...")
# cats = ["Beds and beddings", "Books and stationery","Cosmetics and care products",
#         "Clothing and Accesories", "Drinks and Beverages", "Footwear",
#         "Electronics and Accessories", "Food and Groceries", "Home furniture",
#         "Kitchen utensils", "Laptops and Accessories", "Jewellery", "Phones and Accessories",
#         "Stationery"]
# for cat in cats:
#         cat_dict = {"name": cat}
#         model = Category(**cat_dict)
#         print("{} --> {}".format(cat, model.id))
#         model.save()

# # Load streets
# print()
# print("Creating streets...")
# streets = {"Osasogie": ["Holy Rosary", "Winners road", "Technical road", "Ozakpolor"
#                         "Edudje", "Federal Girl's road", "Ogbeide", "Egbon", "Irowa Obazie",
#                         ],
#         "Ekosodin": ["Newton", "Edo", "Boundary", "Market road", "JB", "Ekhorutomwen",
#                         "Eguavoen", "Ohunwu", "Igbineweka"],
#         "BDPA": ["11th", "12th", "13th", "18th", "19th", "20th", "21st", "22nd", "23rd", "24th",
#                 "Uno", "Okukpun", "Ola Okeaye", "Eyeye", "Abu", "Hilary Adiki", "Anyeaji",
#                 "Lucky", "Imiuwu"],
#         "Evidence": ["Aibalegbe", "Ohenhen", "Egiaruoyi", "Osasere Osayogie", "Iguodala",
#                         "Igbineweka"],
#         "Isihor": ["Egbaen Community road"]
#         }

# for env in streets:
#         print(f'creating streets for the environment: ${env}...')
#         try:
#                 strt = storage.search(Environment, name=env)[0]
#                 for item in streets[env]:
#                         strtDict = {"name": item, "env_id": strt.id}
#                         model = Street(**strtDict)
#                         model.save()
#                         print(f"{model.name} --> {model.id}")
#                         print("------------------")
#         except:
#                 print(f"{env} not found")
#                 continue
