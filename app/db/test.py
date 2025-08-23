from db import db_helper
from db.city import City
from db.restaurant import Restaurant
from db.panorama import Panorama
from db.table import RestaurantTable, TableStatus
from db.hotspot import Hotspot
from db.category import Category

cities = [
    City(name="Tashkent"),
    City(name="New York"),
    City(name="Bern"),
]

restaurants = [
    Restaurant(
        title="SOUL boutique cafe",
        phone="+998990606688",
        address="Buyuk Ipak Yuli, 152",
        lat="41.326986",
        lon="69.337647",
        hours="08:00-02:00",
        city=1,
    ),
    Restaurant(
        title="PAUL",
        phone="+998881671889",
        address="Пр. Амира Темура, 60",
        lat="41.323362",
        lon="69.282755",
        hours="08:00–23:00",
        city=1,
    ),
]

panoramas = [
    Panorama(rid=1, photo="panoramas/1.jpg"),
    Panorama(rid=1, photo="panoramas/2.jpg"),
    Panorama(rid=1, photo="panoramas/3.jpg"),
    Panorama(rid=2, photo="panoramas/4.jpg"),
    Panorama(rid=2, photo="panoramas/5.jpg"),
]

tables = [
    RestaurantTable(
        number=1,
        rid=1,
        status=TableStatus.available.value,
    ),
    RestaurantTable(
        number=2,
        rid=1,
        status=TableStatus.available.value,
    ),
    RestaurantTable(
        number=3,
        rid=1,
        status=TableStatus.available.value,
    ),
    RestaurantTable(
        number=1,
        rid=2,
        status=TableStatus.available.value,
    ),
]

hotspots = [
    Hotspot(
        lat="1",
        lon="2",
        pid=1,
        tid=1,
    ),
    Hotspot(
        lat="100",
        lon="200",
        pid=1,
        tid=2,
    ),
]

categories = [
    Category(name="Завтраки"),
    Category(name="Супы"),
    Category(name="Десерты"),
    Category(name="Горячие напитки"),
    Category(name="Холодные напитки"),
]

async def add_test_data():
    async with db_helper.get_session() as db:
        db.add_all(cities)
        db.add_all(restaurants)
        db.add_all(panoramas)
        db.add_all(tables)
        db.add_all(hotspots)
        db.add_all(categories)
        await db.commit()
