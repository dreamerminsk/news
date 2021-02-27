#!/usr/bin/python
# -*- coding: utf-8 -*-
import time

import requests
from bs4 import BeautifulSoup

talon = 'https://talon.by/'

p = 'https://talon.by/policlinic/minsk-1dp/order'
d = 'https://talon.by/policlinic/minsk-1dp/order/1943'
t = 'https://talon.by/policlinic/minsk-1dp/order/1943/3473'

dd = 'https://talon.by/policlinic/minsk-1dp/doctors/16484'
ddt = 'https://talon.by/policlinic/minsk-1dp/order/1944/3483'
ddtt = 'https://talon.by/policlinic/minsk-1dp/order/1944/3483/2125898'


policlinics = 'https://talon.by/policlinics'
