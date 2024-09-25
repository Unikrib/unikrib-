#!/usr/bin/python3

from models import storage, School, Environment, Street, ServiceCategory, Category
# from models.v1.school import School
# from models.v1.environment import Environment
# from models.v1.street import Street
# from models.v1.service_category import ServiceCategory
# from models.v1.category import Category

# Load schools
# print("Creating schools...")
# schools = [('AAU', 'Ambrose Alli University', 'Ekpoma', 'https://res.cloudinary.com/deg1j9wbh/image/upload/v1710872082/Schools/AAU_iwzcen.jpg'), 
#            ('ABSU', 'Abia State University', 'Uturu', 'https://res.cloudinary.com/deg1j9wbh/image/upload/v1710872082/Schools/ABSU_llmd5v.jpg'),
#            ('CRUTECH', 'University of Cross River State', 'Calabar', 'https://res.cloudinary.com/deg1j9wbh/image/upload/v1710872081/Schools/CRUTECH_pgclxg.jpg'), 
#            ('FUOYE', 'Federal University of Oye-Ekiti', 'Oye-Ekiti', 'https://res.cloudinary.com/deg1j9wbh/image/upload/v1710872081/Schools/FUOYE_wsjjli.jpg'),
#            ('FUPRE', 'Federal University of Petroleum Research Effurum', 'Warri', 'https://res.cloudinary.com/deg1j9wbh/image/upload/v1710872082/Schools/FUPRE_ojmx3s.jpg'),
#            ('LASU', 'Lagos State University', 'Lagos', 'https://res.cloudinary.com/deg1j9wbh/image/upload/v1710872081/Schools/LASU_a5dfu5.jpg'),
#            ('OOU', 'Olabisi Onabanjo University', 'Ago-Iwoye', 'https://res.cloudinary.com/deg1j9wbh/image/upload/v1710872082/Schools/OOU_fbec2p.jpg'),
#            ('FUTO', 'Federal University of Technology Owerri', 'Owerri', 'https://res.cloudinary.com/deg1j9wbh/image/upload/v1710872081/Schools/FUTO_urv8ak.jpg'),
#            ("Unilag", "University of Lagos", 'Lagos', 'https://res.cloudinary.com/deg1j9wbh/image/upload/v1708651205/Schools/UNILAG-Senate-House-Admin-Building_jy9mc3.jpg'),
#            ("UNILORIN", "University of Ilorin", 'Ilorin', 'https://res.cloudinary.com/deg1j9wbh/image/upload/v1708690087/Schools/University-of-Ilorin-Unilorin_hsikyt.png'),
#            ("UNN", "University of Nigeria", 'Nsukka', 'https://res.cloudinary.com/deg1j9wbh/image/upload/v1708651206/Schools/university_of_nigeria_nsukka1_a5qwfp.jpg'), 
#            ("Uniport", "University of Port-Harcourt", 'Port-Harcourt', 'https://res.cloudinary.com/deg1j9wbh/image/upload/v1708651206/Schools/University-of-Portharcourt1_dyb8mj.jpg'),
#            ("UI", "University of Ibadan", 'Ibadan', 'https://res.cloudinary.com/deg1j9wbh/image/upload/v1708651206/Schools/University-of-Ibadan1_xpm5cx.jpg'), 
#            ("OAU", "Obafemi Awolowo University", 'Ile-Ife', 'https://res.cloudinary.com/deg1j9wbh/image/upload/v1708651205/Schools/oau-senate-building1_nrhrei.jpg'),
#            ("UniAbuja", "University of Abuja", 'Abuja', 'https://res.cloudinary.com/deg1j9wbh/image/upload/v1708651205/Schools/UniAbuja-gate_vpp5ai.jpg'), 
#            ("FUTA", "Federal University of Technology Akure", 'Akure', 'https://res.cloudinary.com/deg1j9wbh/image/upload/v1708651205/Schools/FUTA1_mjferp.jpg'),
#            ("UNIUYO", "University of Uyo", 'Uyo', 'https://res.cloudinary.com/deg1j9wbh/image/upload/v1708651205/Schools/uniuyo_m1xhkc.jpg'), 
#            ("UNIZIK", "Nnamdi Azikwe University", 'Awka', 'https://res.cloudinary.com/deg1j9wbh/image/upload/v1708651206/Schools/unizik_h2tkru.jpg'),
#            ("UNICAL", "University of Calabar", 'Calabar', 'https://res.cloudinary.com/deg1j9wbh/image/upload/v1708651210/Schools/unical.jpeg_wmngj9.jpg'), 
#            ('Uniben', 'University of Benin', 'Benin city', 'https://res.cloudinary.com/deg1j9wbh/image/upload/v1708651205/Schools/UNIBEN_xsf2u5.jpg')]
# for name, full_name, city, image_url in schools:
#     school = School(name=name, full_name=full_name, city=city, image_url=image_url)
#     school.save()
#     print(f"{school.name} --> {school.id}")

# storage.reload()

# # Load Environments
# print("Creating Environments...")
# sch_env = {
#         "Unilag": ["Abule-oja", "Pako", "Onike", "Akoka", "Igbobi"],
#         "UNN": ["Hilltop", "Odenigwe", "Odim gate", "Behind flat"],
#         "UI": ["Agbowo", "Bodija", "Orogun", "Ojoo", "Sango", "Makola"],
#         "OAU": ["Oduduwa estate", "Asherifa", "Damico area", "Ibadan road", "Parakin estate",
#                 "Mayfair", "Oranfe", "Modakeke", "Lagere", "Edunabon", "Fajuiyi"],
#         "UniAbuja": ["Iddo sarki", "Pasere", "Iddo sabo", "Gbessa", "Uniabuja staff quarters",
#                         "Amma pepple estate", "Toge", "Gosa", "Sauka", "Kango"],
#         "Uniport": ["Alakahia", "Aluu", "Back of chem", "Choba", "Choba extension", "Rumekini",
#                         "Roumosi"],
#         "FUTA": ["North gate", "West gate", "South gate", "Redemption area", "Apatapiti",
#                         "Embassy area", "Stateline road", "Baptist student fellowship road", "Clinic"],
#         "UNIUYO": ["Ekpany", "Ikpa road", "Itu road", "Udoette", "Urua ikpa"],
#         "UNIZIK": ["Amansi", "Aroma", "Commisioners quarters", "Fire", "Reginal", "School gate", "Temp site"],
#         "UNICAL": ["Mount zion", "Yellow duke", "Goldie", "Satellite town", "Etta agbor", "Mary slessor"],
#         "UNILORIN": ["Chapel bus stop"],
#         "Uniben": ["Adolor", "BDPA", "Ekosodin", "Isihior", "Oluku", "JSQ", "Osasoghie", "SSQ", "UBTH quarters", "Uselu"],
#         "FUTO": ["Nekede", "Ihiagwa", "Eziobodo", "Obinze", "Umuchima", "Ezeogwu", "Okolochi"],
#         "LASU": ["First gate", "Post service", "Ojo", "Akesan", "Iba"],
#         "AAU": ["School gate", "Ihumudum", "Ujemen", "Idumebo"],
#         "FUPRE": ["Ugbomoro", "Iteregbi", "Ugolo", "Okorikpehre"],
#         "ABSU": ["Isuikwato", "Uloma", "Okigwe", "Obiagu"],
#         "OOU": ["Ago-Iwoye", "Oru", "Ilaporu", "Aha", "Awa"],
#         "CRUTECH": ["Ene-Obong", "Eko basi", "Mount zion", "Idim ita", "Edibe Edibe", "Efut Abua", "Atamunu", "Anantigha"],
#         "FUOYE": ["Odo-oro", "Ootunja", "Isaba", "Usin", "Ikoyi", "Ikoyi tuntun", "School gate", "Asin", "Shell", "Market", "Garage"]
#         }

# for sch in sch_env:
#     print(f"creating environments for {sch}")
#     sch_obj = storage.search("School", name=sch)
#     if sch_obj is None or len(sch_obj) == 0:
#         print(f"{sch} was not found")
#         continue
#     sch_mod = sch_obj[0]
#     for env in sch_env[sch]:
#         model = Environment(name=env, school_id=sch_mod.id)
#         model.save()
#         print(f"{model.name} --> {model.id}")

# storage.reload()

# Load Service categories
print("Creating service Categories...")
cats = [("AC installer", "https://res.cloudinary.com/deg1j9wbh/image/upload/v1708814207/service_categories/AC_installer_gvqm9a.jpg"), 
        ("Carpenter", "https://res.cloudinary.com/deg1j9wbh/image/upload/v1708814208/service_categories/Carpenter_zblwhv.jpg"), 
        ("Caterer", "https://res.cloudinary.com/deg1j9wbh/image/upload/v1708814208/service_categories/Caterer_dw831l.jpg"),
        ("DSTV installer", 'https://res.cloudinary.com/deg1j9wbh/image/upload/v1708814208/service_categories/dstv_installer.jpeg_olbdjm.jpg'),
        ("Electrician", 'https://res.cloudinary.com/deg1j9wbh/image/upload/v1708814209/service_categories/electrician_byzscv.jpg'),
        ("Event Planner", 'https://res.cloudinary.com/deg1j9wbh/image/upload/v1708814211/service_categories/eventplanner_uemgzu.jpg'), 
        ("Fashion Designer", "https://res.cloudinary.com/deg1j9wbh/image/upload/v1708814211/service_categories/Fashion_Designer_lc3oym.jpg"),
        ("Cooking gas", 'https://res.cloudinary.com/deg1j9wbh/image/upload/v1708814212/service_categories/gas_delivery_uchsbp.jpg'),
        ("Generator Repairer", 'https://res.cloudinary.com/deg1j9wbh/image/upload/v1708814214/service_categories/generator_repairman_em6i1g.jpg'),
        ("Hair Stylist", 'https://res.cloudinary.com/deg1j9wbh/image/upload/v1708814214/service_categories/Hair-stylist_v5h1w6.jpg'), 
        ("Logistics", 'https://res.cloudinary.com/deg1j9wbh/image/upload/v1708814214/service_categories/Logistics_ucpliv.jpg'), 
        ("Make up artist", 'https://res.cloudinary.com/deg1j9wbh/image/upload/v1708814215/service_categories/makeup_artist_qbcgaz.jpg'), 
        ("Painter", 'https://res.cloudinary.com/deg1j9wbh/image/upload/v1708814217/service_categories/Painter_zffu9b.jpg'), 
        ("Plumber", "https://res.cloudinary.com/deg1j9wbh/image/upload/v1708942830/service_categories/Plumber_i4ejqy.jpg"),
        ("Refrigerator repairer", "https://res.cloudinary.com/deg1j9wbh/image/upload/v1708942835/service_categories/Refrigerator_repairman_btkgvz.jpg"), 
        ("Welder", 'https://res.cloudinary.com/deg1j9wbh/image/upload/v1708942829/service_categories/Welder_syjen0.jpg')]
for cat, image_url in cats:
        cat_obj = storage.search('ServiceCategory', name=cat)
        if not cat_obj:
            print(f'No obj found for {cat}')
            continue
        cat_obj = cat_obj[0]
        setattr(cat_obj, 'image_url', image_url)
        cat_obj.save()
        # cat_dict = {"name": cat, 'image_url': image_url}
        # model = ServiceCategory(**cat_dict)
        # print("{} --> {}".format(cat, model.id))
        # model.save()

# # Load product categories
# print()
# print("Creating Product categories...")
# cats = [("Beds and beddings", "https://res.cloudinary.com/deg1j9wbh/image/upload/v1712832585/categories/bed_and_bedding_lvnz8p.jpg"), 
#         ("Books and stationery", "https://res.cloudinary.com/deg1j9wbh/image/upload/v1708778844/categories/books_and_stationery_ekj2yp.jpg"),
#         ("Cosmetics and care products", "https://res.cloudinary.com/deg1j9wbh/image/upload/v1708778849/categories/skincare_fz0znb.jpg"),
#         ("Clothing and Accesories", "https://res.cloudinary.com/deg1j9wbh/image/upload/v1708778847/categories/clothes_and_accessories_pyuk9k.jpg"), 
#         ("Drinks and Beverages", "https://res.cloudinary.com/deg1j9wbh/image/upload/v1708942428/categories/Drinks_and_Beverages_oqm7ig.jpg"),
#         ("Footwear", "https://res.cloudinary.com/deg1j9wbh/image/upload/v1708778851/categories/footware_sonish.jpg"),
#         ("Electronics and Accessories", "https://res.cloudinary.com/deg1j9wbh/image/upload/v1708778844/categories/electronics_krpsnc.jpg"), 
#         ("Food and Groceries", "https://res.cloudinary.com/deg1j9wbh/image/upload/v1708778856/categories/groceries_rzl4pl.jpg"), 
#         ("Home furniture", "https://res.cloudinary.com/deg1j9wbh/image/upload/v1708778846/categories/furniture_sk1vwl.jpg"),
#         ("Kitchen utensils", "https://res.cloudinary.com/deg1j9wbh/image/upload/v1708778848/categories/kitchen_utensils_xiwpnk.jpg"), 
#         ("Laptops and Accessories", "https://res.cloudinary.com/deg1j9wbh/image/upload/v1708778847/categories/laptop_tjlbfb.png"),
#         ("Jewellery", "https://res.cloudinary.com/deg1j9wbh/image/upload/v1708942429/categories/Jewellery_hrvu6u.jpg"), 
#         ("Phones and Accessories", "https://res.cloudinary.com/deg1j9wbh/image/upload/v1708778848/categories/mobile_phone_nfmxiu.jpg"),
#         ]
# for cat, image_url in cats:
#         cat_dict = {"name": cat, "image_url": image_url}
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
