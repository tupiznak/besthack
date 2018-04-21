import json
import requests
from pprint import pprint
from bs4 import BeautifulSoup
import re
import random
import time
import matplotlib.pyplot as plt
import numpy as np
import cv2
import urllib.request
from io import StringIO

from tkinter import *
from tkinter import messagebox


##################################interactive
def quit():
    #pass
    root.destroy()

root = Tk()
root.title("input address")
root.geometry("300x250")
message = StringVar()
message_entry = Entry(textvariable=message)
message_entry.place(relx=.5, rely=.1, anchor="c")

rad = StringVar()
message_entry1 = Entry(textvariable=rad)
message_entry1.place(relx=.1, rely=.2, anchor="c")

message_button = Button(text="Send", command=quit)
message_button.place(relx=.5, rely=.5, anchor="c")
root.mainloop()

address = message.get()
radius = rad.get()
##################################interactive

api_key='AIzaSyDu65Fcg-7Dlko6JGIC8ABL2ba4mn6T8AE'

###############################get geoposition
if address is '':
    address = 'улк мгту'
if radius is '':
    radius = '3000'
place_type = 'lodging'
req = 'https://maps.googleapis.com/maps/api/geocode/json?address='+address+'&key='+api_key
geo_json = json.loads(requests.get(req).content)
geo_json = geo_json['results'][0]['geometry']['location']
print(geo_json)
###############################################

###############################################get places
req = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+str(geo_json['lat'])+','+str(geo_json['lng'])+'&radius='+radius+'&type='+place_type+'&key='+api_key
places_json = json.loads(requests.get(req).content)
places = [el['name'] for el in places_json['results']]
pprint(places)
###################################################

###################################################get image
loc = [str(str(el['geometry']['location']['lat'])+','+str(el['geometry']['location']['lng'])) for el in places_json['results']]
loc = '|'.join(loc)
#pprint(loc)
req = 'http://maps.google.com/maps/api/staticmap?center='+str(geo_json['lat'])+','+str(geo_json['lng'])+'&zoom=12&size=800x800&markers='+loc

resp = urllib.request.urlopen(req)		
image = np.asarray(bytearray(resp.read()), dtype="uint8")
image = cv2.imdecode(image, cv2.IMREAD_COLOR)

cv2.imshow('image',image)
cv2.waitKey(0)
cv2.destroyAllWindows()
######################################################

#proxy_list=["159.65.131.46:3128"]
proxy_list=['']
p_Dict = {"https":proxy_list[0]}

#req = 'https://www.google.com/maps/search/?api=1&query=Holiday Inn Moscow - Sokolniki'
#res = requests.get(req,proxies=p_Dict).content.decode('utf-8')
'''
place_list=[]
for i in random.sample(range(len(places)),len(places)):
    time.sleep(random.randint(0, 3))
    req = 'https://www.google.com/maps/search/?api=1&query='+places[i]
    res = requests.get(req,proxies=p_Dict).content.decode('utf-8')
    try:
        res = re.split(r"Booking.com", res)[1]
    except:
        print('-',places[i])
        continue
    res = re.split(r"\[\"", res)[1]
    res = re.split(r"\"", res)[0]
    place_list.append({'name':places[i],'link':res})
    print({'name':places[i],'link':res})
    
for el in place_list:
    res = requests.get(el['link']).content.decode('utf-8')
    #print(res)
    soup = BeautifulSoup(res, 'html.parser')
    #print(soup.prettify)
    parse = soup.find('script',{'type':'application/ld+json'}).getText()
    js_parse = json.loads(parse)
    rating = js_parse['aggregateRating']['ratingValue']
    reviewCount = js_parse['aggregateRating']['reviewCount']
    priceRange = js_parse['priceRange']
    el['rating'] = rating
    el['reviewCount'] = reviewCount
    #try:
        #priceRange = priceRange.split('$')[1]
        #priceRange = priceRange.split()[0]
    #except:
        #pass
    el['priceRange'] = priceRange

place_list = [{'link': 'http://www.google.com.sg/travel/clk?pc=AA80Osyc5rOYz2Mnur99f-zluKTBusRqjOMDl-dOs7lVAtsxQ0X7b_-uh5nrfaDPbEXGcu7dHfByKn3i8tJjdpPfXsXld5eeoLzNFYvSRVAQ7NuPB29OVAgYbxGXLtEjWB9I3JWu7qPy9h_jhSRDt9Ev0aaj7zbN0bS0PA1kNnk8iLhnl8LJ4aV3EaNvP5X-o7vg93PWxWCfPiaWdywcMsvbAf-5RTSWhIARhlJmYdyq_vJKy8Oac4prnUleZdw7hcf9C06aaN-PKyYgu54Bm5wWJsBOupqymdj-Htzym93iOFQKBBcPsTmNDs_EY5k_Bzr4U7lwtoplxG1WSGnWeBA',
  'name': 'Elokhovsky Hotel',
  'priceRange': 'Prices for upcoming dates start at $57 per night (We Price '
                'Match)',
  'rating': 9,
  'reviewCount': 866},
 {'link': 'http://www.google.com.sg/travel/clk?pc=AA80OszeZCcbxEdbPPu5ykE23SxOUU_E5N9bjF0GdkVtHRgY13ZWyrS8dFOiISjQWploGnjKlSA-YpTAyNQRdyuyV4IT8foZnfNLERM2r5k67YaODzKxWuea1qck7Mp4HWMirVG_rfYWMFJwc0wf811bNLQjeQ6C33nJlssYp1Q58s-_G1kR4SGeYZtJ59f_f514TyUecNzBQqvAjQXmiMaMrrnXq5I5i0X8fAkBqM0tpBIV9EMS9-egSGEiJ9l8Ptmjn02ylyUSfOdq1FF8LZLi8FPwAxih35W2HXkXut3B8dhx_0gP44I_I-i2sDZWqeKZ_1_T60DNf1BF8KF4Ad8',
  'name': 'Mamaison All Suites Spa Pokrovka Hotel',
  'priceRange': 'Prices for upcoming dates start at $101 per night (We Price '
                'Match)',
  'rating': 8.6,
  'reviewCount': 1066},
 {'link': 'http://www.google.com.sg/travel/clk?pc=AA80OsyVHN4yo9AocWo5TJBX0BbxvyZhdFRy_I-YopHXiZ6Qd4d0AD46TmKmS9Fyw79Tji0UcJPXvCjwQrSg2L5rx1ygmaM-4xczD228Exghsc9lpZ25VfE58xFepv-YRTLSKsiMf8KXGuNWc_cO7NHLG2OmMo2VkOk2U4hjj-ycDpqSb2WskvobBT7hiwEqIrXCV0hE2nqGS0AdONxiF0oP-C_eSh13kq7mHXDk7jig9KaavXatL1scAPJU_IXSByNLu7m1bNf91NdYUVFCBkvYUlKm8C7QGub05VIxgZBquKwr2OU8Z3kR7mOzM6a-juuObbBoo_SbXnxznRN7ng8',
  'name': 'Morion Hotel',
  'priceRange': 'Prices for upcoming dates start at $33 per night (We Price '
                'Match)',
  'rating': 7.6,
  'reviewCount': 44},
 {'link': 'http://www.google.com.sg/travel/clk?pc=AA80OsyKQsI6137RJojP068ns4MgqoS5vLXgjk3UdOBRe0GnZ71QEhs3zmkYL_LUjkFKNLPT4qkWPzVuwD29ByW_RrRgPt-6eObf_lEAzLLq-CrHA6gI_qGyxgXHV6B-MjUoDzy4-k5EPiC9Pv2iFkNU4h-oWuRrMJvo6JfJ1NqPI_oUHtMNrpbxEAjeBf4O6oxa-b2F7RHdZLCBV_-U5mrWpi_s8hsVe2qC4GtNEMZEzr7iQSSsqJ27dKAYQ49HD4Xg7eqekdoe_aN2FiuHJ73WqqFnOqD6jDDzrN33GCvK6j1A7Ami3mV80XeeouLuipw2OU_Q6VpA4yxzTez37d_skA',
  'name': 'Apple Hostel Moscow',
  'priceRange': 'Prices for upcoming dates start at $9 per night (We Price '
                'Match)',
  'rating': 8.1,
  'reviewCount': 99},
 {'link': 'http://www.google.com.sg/travel/clk?pc=AA80OsxbU7hunGn_Dk0NSwyUpOz8QqNyRIoR1QNGXb03K8ZUooFyxx60ysodpSwNON1U1GgGrDpIArQCBIsKwkyF6sZHcD6r0WQtgCKdfxm66i-5XUFvaoVlPa5Bf9JbQ-_Oj14C_sph6cdBmE1RKBHKcihXUr9H4365ZhcMwuhmtgfySEgam74OqXEZ_aOhCOyJC7sWImll5T5F2dd4ql6UwFEEEYeFwuxFtQjEDgPOS5D8pWmKcGmt95b0Da76t9LsVMrYbdzdHQS2-WFMExCr77jN0VBk1dF_E233UjLOW756LTimYh2DhY7MwNfEulizyiWxfSyyGLz4dlsFEGI',
  'name': 'Basis-M Hotel',
  'priceRange': 'Prices for upcoming dates start at $62 per night (We Price '
                'Match)',
  'rating': 7.4,
  'reviewCount': 378},
 {'link': 'http://www.google.com.sg/travel/clk?pc=AA80OsxBXjimrmYD01R3fAkJZNrfGe2UXS42G0A76mesCYLHCx82O3Bf7dFZIKm3MxWmHzg_8guMj76FTtyOO9TRn4dX2NF49t2Y3qCssFC7ulMm5ZVwWnplDU87umVyUfUe0blF7FDrAbnN23pZfLi9y2iGql0SfjnXf_RM5vrOTXQ_80LxzbB7GfvCGwg-7bf_Uglys4Kq3veqkCZMRVbiVW-SvqWZj553lpI1lk4U6BmIMKOr0kPsqJbM0Sn_tq3FsyBbJEPiHm44L6eqZKxkwjUy3bmxXuR7qFx70fTK5ZsORhwstTOqpX1spuoaP0-lfMlohB5L2IcO6_uUiHiZYA',
  'name': 'Hostel Dom',
  'priceRange': 'Prices for upcoming dates start at $12 per night (We Price '
                'Match)',
  'rating': 7.8,
  'reviewCount': 1899},
 {'link': 'http://www.google.com.sg/travel/clk?pc=AA80OsxD-AOgI0BCx_NhJQPFBlYeo3ywv2R2RVdY_Pn5BnxQeBuIVkmBr4ljd05-US2Nh0e1doJKLFehiAS8fJF5FMyiTcjnlj7P4lmGDmUmnUnaK6sgF2_uzr4jJ-WmkMFUxOQ-_OKXO1qtLgWlCnVx87GW2pelZjy83NQ25Azi9X_tKcAwImfrUB8GFz3gSUak4rJv8UhV5HIrWdPi0zethQ38a_3vtqAM9kvkM3UV3Oe0ecJWnos40x2oe1848Or7KvPiz5yRj0mkikXfl2-ztPuIWkMHls4WqC7A-dB90NaKTIOsmjaA-0F9qqTv8ukruXNc4qOw-Kgp18yYn9A',
  'name': 'Ulanskaya',
  'priceRange': 'Prices for upcoming dates start at $41 per night (We Price '
                'Match)',
  'rating': 8.1,
  'reviewCount': 1459},
 {'link': 'http://www.google.com.sg/travel/clk?pc=AA80OsxKRiN3LCVP20ltegj4OWbmkz9P1j9m_Y94LmnXDKootptpmaiEGGmn685r755uS4wdpc6wsSqZP-EJzawWoyD1Yt7oRgj-UAGwfMcJO4rtkxAwGImctqDNw1Zohg5yiNZmDJwElVojTqxGywXSopPkhu54ohAwltkp429jh7ozEn79NyyQH3I45fZSFqd1jjChcclRnmFrGHbqyLqNeI9LBKZR3kCcflN9lJhfqfTViwL1Iv1ZNg4t-De3bHK5M1yXNQ-eqzdEfmJaLIOrFoi8wx0Eh9IzbPIDxH8cMhyly8DTu7AmkxJqzLNqDlkc3Uwvdq36y7x-zCXxqz7W2g',
  'name': 'Hotel 45',
  'priceRange': 'Prices for upcoming dates start at $25 per night (We Price '
                'Match)',
  'rating': 6.7,
  'reviewCount': 44},
 {'link': 'http://www.google.com.sg/travel/clk?pc=AA80Oszc03a2lLxi6jOi4S05ZYiZBFYhu3-sJ6nsEEL9qfrzbJAMSzVunN5-aJGWiludhSpvDqhrgYqfnYg1jJL1dTDkFXCo90M_zhwEYkFf3Z_hp2hzwxDmdS6vyBhDr3IVoW6dTWYl7xMr3wWQku7ktuCf5eyBDA2P-Wcax3kJ-dkwlj1BRMHa1s7nw6g0QSiUNn2ehL-zrD-PzqRW8WPLOPaWYAf2NBYEfqzD3O_UVWVuM2auQvXju6LXIn9ZF3ELofEHX0UpZ7sEaoPqRb7sOkEgmaqdBbDzEquh84VTNsVSFkcXy1h-_PdK5YEYOo5vdCSxoJ6YZNHbFcYtgFNHm_0',
  'name': 'Hotel Mandarin Moscow',
  'priceRange': 'Prices for upcoming dates start at $46 per night (We Price '
                'Match)',
  'rating': 7.8,
  'reviewCount': 1386},
 {'link': 'http://www.google.com.sg/travel/clk?pc=AA80OsxNFBes3r-f13iAzCrloE0d6CNkED0raDedrN2qwx40oXYrixg4EqgGKPsEYRfINjHwJm5mfS8XMOOaQ8awTYmcZ5vsZshvrzAdmFuWgFqWOXKsGmqJQ4rIIwS7ewuxZG1xmBY5-MAA2j7SnOEebDqu7UzN5ESo0GCkpdrZ5A42Anw2f2bR4CGqRGa1uxE3ewGHVIewWQA05i3JaEW2qBgrgtVIU9_IwuEM2M9k9eCEHi9Mdm_EZCJMrg0jJGAwwRH9XaeYtn-R72e740ZrlDW0UKgvlBJAi9fFy4X-r2rKf51Ar62bbB6-4YhrEoRynRjgCAyJutfCu1aTsofBAHI',
  'name': 'Bentley Hotel',
  'priceRange': 'Prices for upcoming dates start at $111 per night (We Price '
                'Match)',
  'rating': 7.7,
  'reviewCount': 1372},
 {'link': 'http://www.google.com.sg/travel/clk?pc=AA80OswDvIpi4ZiVC4QCJDPQ-GSUCutnZsePbemiqNK1YTA_ZboRku_ghABU9cLjONVJbboq9dIKQci95YsDSNG7TDYhA8DRbxzbX9YetzsJH1YOuqv1t51RvHpBggRKpsSrwkAQx0Y6Gf-evQFU36iADRWXFbavU1bERnIXR70MMmndKiXZiL8WAK1Wl32gnpqHPEaQevuQBd2EbsgSU5WCVrVumEeQ7QtrA6EvHEu2Fo8kOrWs4XaWQ7AeDDhFRdyf5nCQokyf8JIFopg_g_W0eYCH2O9iBpBimyyUUphgSqasFrwX6Cn1KM_AakeaTkH2vt1iViqxrii0zpin1_VFSpU',
  'name': 'Holiday Inn Moscow - Sokolniki',
  'priceRange': 'Prices for upcoming dates start at $49 per night (We Price '
                'Match)',
  'rating': 8.9,
  'reviewCount': 8036},
 {'link': 'http://www.google.com.sg/travel/clk?pc=AA80OsyR3cx8iZ-6Oq23uYy9_piS53hbBHfGGA86wT7DAvINyaRTb0_Rb-m95izYG4y7iCujTCwMLIbea5Wr5jKKDFaSh3cPS7dXBFrKJvynz5Mi25ZqX15mq-JRNxQJFL5mivfoxpLWSFQBE_NqjKlcYHpO8EoerxkeHFB-aZBD3Km3m7TEZNog1OJmK5ROFxZ81yv3lYuHAnKK_AlkECJbCw58pX8sETMa39q8StCzBvsCo8useAUcHxTgF1HZX7CWY1IJwGKSFy7oDuAXfrm9C6c-gLIa6pL0FC7tZ8NwmxlQ6aqIqEaFTZxA_XF_ywFgjn-xlA8U9fjSA_9nMxc',
  'name': 'Hilton Moscow Leningradskaya',
  'priceRange': 'Prices for upcoming dates start at $85 per night (We Price '
                'Match)',
  'rating': 8.4,
  'reviewCount': 2716}]

'''
place_list = [{'link': 'http://www.google.com.sg/travel/clk?pc=AA80OszfLpCL-h2Dv4iYfiAeDZxZKvOTvjNNjPyFAP2Y-bewMfpLBwK9_rBQHT_PHFy2OdEPLRdiTK7Tuh0XiQ9ZdhNdhyNiUTlLRt9Bx0yW6ppBk01FG22XPP5Nn2ciA9L5RNHl6r2gmEHI24LrnLooryLZgrxhowk7EFaNx-S8lTYqJPjaOFyXKJNhDJrXT8llNnD67kErz-YW0sY2b7vrg3ZmxXX9pIHPtUisqubVyUgLJF2oTmtPTwnCvIZ5uX9k2fkrfZrG92XSCB645RF_0WenhV7tqsvYt9jUpJPVQNYWqHheY0KLoO8GNv9bZyc6DdbYExOVkkc9UwYmzHM',
               'name': 'Hilton Moscow Leningradskaya',
  'priceRange': 'Prices for upcoming dates start at $85 per night (We Price '
  'Match)',
                'rating': 8.4,
  'reviewCount': 2716},
              {'link': 'http://www.google.com.sg/travel/clk?pc=AA80Osy9QFl_trrSwX9ZS0V8YqiLEpiKgohyFlrbWjAjlWum6pYsvt0B9OXmYMFHAcvjQFonsaNob37xW0j5K_8S1GosqZo70Lnq1VxWg2fuRozPYFThVGgsHrE5bssk1TO8NJgnSDcz8hgZaGEMWYwPiKg2WoZ3FzG1mbQIzoENgpq_xjfkyZKXAFLjV3a2NX83_x2m48-hcBlIVPNpgDBu4ZOB5z3K188kPHAmok63mbqPbXLmxOyDjcY3BFfq6kHplNHyuaxvEL9RY6NzesitFeNilvN1GWDPjvhVkPLGrvO0sTovDMzjnOkrnGjS27dLoR9g_hfGEGesGE2FMZdxaw',
  'name': 'Hotel Mandarin Moscow',
  'priceRange': 'Prices for upcoming dates start at $46 per night (We Price '
  'Match)',
                'rating': 7.8,
  'reviewCount': 1386},
 {'link': 'http://www.google.com.sg/travel/clk?pc=AA80Osx2hyzryRsh3v4nJeRC7ZSLnAeK_cu_T6yJMa2LkIEcVvudD988qSf-QKVpnRjrW8LeSkP1_Pgqcx0SyF3YXmnEdgyTZOFsYCozidGvCJvdaaw8sb4qN6GONvQGOLYfh02pDmtyiqK2oaap6wOaB31uv-RkOvFx6K1FvMYNLgqNfOk-1yvIv28cBWWn_LffinCEI9yixdkbZVWRyRenuRXKrekyACFD3upprDigZvJcQ1RFF8pGvk1Y36VrFuMmRCzaHnP3I54eqYbc2sr0XWt2-_6gue2zCR2zTWYv7jczZunjOMskaz3HdPeJXlG4wWIXojnYcOlRsW5ppY4Q4g',
  'name': 'Hotel Mercure Moscow Baumanskaya',
  'priceRange': 'Prices for upcoming dates start at $60 per night (We Price '
  'Match)',
                'rating': 9.3,
  'reviewCount': 787},
 {'link': 'http://www.google.com.sg/travel/clk?pc=AA80OsyZkx0AdMooRDnmv4A-LeEnTBH8xrsE-w_cQsfoGOM5_-IPnzPzG8kv6faNmXx9r6W8rEOHXs_6ScYcmUCYThhsVt9GjkCXBbF6nPmf9Tjalla-lFOxGhdi7wLfZX1H7b75JzDky_c5LBUAWb0r2U-tQw5V0QlIoI2I6Ir8b7uGfLoOhc65b0YtEKNsrERBr75vd6D0-MyMY7mLq5UM3--rNRCZBgluU3XgM8qxvY_CSsmk8-05Hx28L7zbULfT_3M1CkDMDmGPGSNSOolQ3yC_Uxl7bjU2PWEnqSwrAiSQbFcwtj1t046WLe_eAhrdznz2zcn1dijLhAeBHDik-w',
  'name': 'Hotel Elokhovsky City',
  'priceRange': 'Prices for upcoming dates start at $49 per night (We Price '
  'Match)',
                'rating': 8.9,
  'reviewCount': 754},
 {'link': 'http://www.google.com.sg/travel/clk?pc=AA80Osz6M_gpOYKK_YwFta94Kie9RgqfmPfwLI0sbW8dlNFEMvX_2burT80OU8iYPYnf3Cu7psW4jV68ZMsMTpp4c-muKmMxofSgbxch1b1D_T5dngaCVc3FH_1W0xHT9QF5l9_rlo86xGhe-_0UAiO26BF_2v6X-srqaFDgqDE7NZ6i20pn_NOJWzS--X0jc57mM8rt-JnAlNmdDoUKnmvtOwPffMUdunHMavBU0-myq_Qle75nGRvIwZXtnyeR_UQq1yVJ43YgOUGCj5AZ3FgV9jvFB5ma77zjNtbKeuwKyTTouHX_c40oLQRaLAWsR2zy4hzcw198A98HTn8UFcC6gw',
  'name': 'Suvorovskaya Hotel',
  'priceRange': 'Prices for upcoming dates start at $49 per night (We Price '
  'Match)',
                'rating': 7.8,
  'reviewCount': 107},
 {'link': 'http://www.google.com.sg/travel/clk?pc=AA80OszZyem7Ey96Hn7oxb5XVmSICbtDnaohGMIfO0BAMtxKi4axtfaKsHIgWrA7Lw0xbE4MoPNEhkZ_4XNDW-_Fbf7b2dJ014aj7pzVe3XHeP97pfabGVcKTz-FAOXGQ26FPlX2YcKmJjxJAJTOJbCsmFDlkyawHHIhzSSIHu4z5zepFQJbLuUuCa-9SoA0A2qpgIQlQtlCV_dWO-xxnTNz6q02_t5206hWVyxwo4CovMRE6hNd5O6l7xlAVBUz_BEVURcWoLsugcapWGI5q1CNqkOwk4Pwdthkowze1nhmbf-RKIt0ZC_Xj9X_EfrtEcqRTxyqFECPoF5A5Ro7keBvBac',
  'name': 'Holiday Inn Moscow - Sokolniki',
  'priceRange': 'Prices for upcoming dates start at $49 per night (We Price '
  'Match)',
                'rating': 8.9,
  'reviewCount': 8036},
 {'link': 'http://www.google.com.sg/travel/clk?pc=AA80OsywKrct7QOBKzwhTL7xKo3efmDs7edhqY_u5TQBIgey69ItjgLbFNlUKWYshffQiKcpFaIfc7ozR5iKKN7tkT3MU6x6TThc_KbBKRNC7z_WiQu8ofAJqOIwGuyNEeroSlvnMTS0UZjMFEjj3mrTAJNcvqbeKHrHhU07-zzlbAXXR8XvM6mcWeb-1e0KKMpXK7Qf3HtOoer_fqLOe7LnGz-yK_cPWm6X9bVL4TmTP4lVXxCW1WMm7FLfUeQcpRB4qn0d3QdfLl5CYg4auEbYhKvwfGRjJZAz6goFdIsXk6BHkN8BJSAAZcwJETWn2G2lWJyv9oLuLifUIpTPCVY',
  'name': 'Morion Hotel',
  'priceRange': 'Prices for upcoming dates start at $33 per night (We Price '
  'Match)',
                'rating': 7.6,
  'reviewCount': 44},
 {'link': 'http://www.google.com.sg/travel/clk?pc=AA80OswOzGgliWfK_YZy2PUUoMIponq9D3d_WXMtx0inEXvoOlCpM1EzQRUmhZ6KPYj5Z9TckjFPT5EaBfQsAnB92z4_rjVxiQtv6dfHtJwW9-SGJhHaokswewoYNrp1fvvS-LPs-Qy65DNGylm3gxE-8FearliItMKyO2cQfTTZ1MjIEnkByfdy6JwrbOU5yvqOl2V3nJXs-UA5yeJSf4L2Er8w35FZdtwugYSXwft_qef9BjntMNx2O3WjZNwSwefE5uH4wp_hfCYlZr1I99_Uj4OCruJY4ttWnY-JO1KOtZ1En8om5odn6B-KuElUGTdAynwkCz5GwcVi1Oj66344yg',
  'name': 'Elokhovsky Hotel',
  'priceRange': 'Prices for upcoming dates start at $57 per night (We Price '
  'Match)',
                'rating': 9,
  'reviewCount': 866},
 {'link': 'http://www.google.com.sg/travel/clk?pc=AA80OsyveSuIQV3dGch_oiUtEYsQ8iu8SUDDY5P0EaoKxERZf3f_e2nlMDKWNCqgZI-qzKyi_-8Mzu7C-3z1QOLWmJKb55tgpw8E_5bQmN0cvfhYKexHvYtH2GIspNgBYSj6kOjySmoRIXMWXcmXIYJuqhN11v2dDca3WRMwERbCdTmoiq0fhzceGttKcZsziWiU0zW9KDdr0rnTeaM7sLrpZn8jrDDZQX_Pys6vNSKJvGfyuzF6zC9JC1bx6-7FPU1xX4gFI5nlNShIPJjMuSWRcJTNnwTsgk4OeIPP3TZTr8mG6ri8mDV2eqYTpdAv4iYSc0NE9XrcokRE0V19hhU',
  'name': 'Hotel 45',
  'priceRange': 'Prices for upcoming dates start at $25 per night (We Price '
  'Match)',
                'rating': 6.7,
  'reviewCount': 44}]

pprint(place_list)
rows = [el['name'] for el in place_list]
columns = ['rating','reviewCount']

cellText = []
for el in place_list:
    cellText.append([el['rating'],el['reviewCount']])

plt.table(cellText=cellText,
                      rowLabels=rows,
                      colLabels=columns,
                      colWidths=[0.2,0.2],
                      loc=4)
plt.axis('off')
plt.show()