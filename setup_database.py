#!/usr/bin/env python
# Author : Wenda Zhao
# -*- coding: UTF-8 -*-

from main import Merchandise, db, Users

db.create_all()

# Merchandise table(5):
# id(p-key),name, tag, inventory, price, discount_flag

# insert 4 demo-items
item_demo1 = Merchandise("Coca-kola", "Drink", 300, 2, 1,"static/assets/test.jpg")
db.session.add(item_demo1)
db.session.commit()

item_demo2 = Merchandise("Pepsi", "Drink", 250, 1.5, 0.5,"static/assets/test2.jpg")
db.session.add(item_demo2)
db.session.commit()

item_demo3 = Merchandise("Cake", "Desert", 30, 5, 1,"static/assets/test3.jpg")
db.session.add(item_demo3)
db.session.commit()

item_demo4 = Merchandise("Haagen-Dazs", "Desert", 100, 8, 0.8,"static/assets/test4.jpg")
db.session.add(item_demo4)
db.session.commit()

# table users(8):
# userID(p-key), username, password, first_name, last_name,
# email, address1, address2, balance

# insert 3 demo-users
user_demo1 = Users("liqi", "1234", "Li", "Qi", "liqi@uab.edu", "apt262", "Birmingham", 1000)
db.session.add(user_demo1)
db.session.commit()

user_demo2 = Users("wenda", "1234", "Wenda", "Zhao", "wenda@uab.edu", "apt123", "Birmingham", 1000)
db.session.add(user_demo2)
db.session.commit()

user_demo3 = Users("daniel", "1234", "Daniel", "Chiang", "daniel@uab.edu", "apt231", "Birmingham", 1000)
db.session.add(user_demo3)
db.session.commit()
