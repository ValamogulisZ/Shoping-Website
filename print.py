#!/usr/bin/env python
# Author : Wenda Zhao
# -*- coding: UTF-8 -*-

from main import Merchandise,Users


all_users = Users.query.all()
print(all_users)

all_merchandise = Merchandise.query.all()
print(all_merchandise)

print(Users.query.count())
print(len(Users.query.all()))

print(Merchandise.query.count())
