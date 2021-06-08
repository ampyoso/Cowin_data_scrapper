# -*- coding: utf-8 -*-
"""Source for Manipur

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uiSaqIHKYxUc72LBCKRbk7BRDN80--Q3
"""

import json
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from time import sleep

# %%
# post API url:
post_api_url = 'http://127.0.0.1:5000/updateBulk'

HospitalName=[]
TypeHospital=[]
category=[]
Beds=[]

url="http://nrhmmanipur.org/?page_id=2602"
r=requests.get(url)
page=r.content
soup=BeautifulSoup(page,'html.parser')

cata=soup.find_all('td',{"class":"column-3"})
# print(cata)
Hname=[]
for cat in cata:
  Hname.append(cat.text)
  # print(Hname)

row=soup.find_all('td',{'class':"column-2"})
i=0
# print(row)
for hospital in row:
  # print(hospital.text)
  HospitalName.append(hospital.text)
  if(i<2):
    TypeHospital.append('Dedicated COVID Hospital')
    category.append(Hname[0])
  elif(i==2):
    TypeHospital.append('Dedicated COVID Health Centre')
    category.append(Hname[1])
  else:
    TypeHospital.append('COVID Care Centre CCC')
    category.append(Hname[2])
  i+=1
  # print(HospitalName)

# print(TypeHospital)
# print(len(TypeHospital))
# print(category)
# print(len(category))

beds=soup.find_all('td',{'class':'column-4'})
for dediBeds in beds:
  Beds.append(dediBeds.text)
  # print(Beds)

print(len(HospitalName), len(TypeHospital),len(category),len(Beds))
Source_for_Manipur=pd.DataFrame({"Hospital Name":HospitalName,"Type of Hospitals":TypeHospital,"Type of Category":category,"No. of Dedicated Bed":Beds,"Check LAST UPDATED":False})
## "Last Updated":last_updated

# Source_for_Manipur

# Source_for_Manipur.to_excel('Source_for_Manipur_cowinmap.xlsx')
APIInput = Source_for_Manipur.to_json(orient='records', indent=2)
print(APIInput)
try:
  api_response = requests.post(
        post_api_url, json=json.loads(APIInput), verify=False)
  print(api_response.text)
  if api_response.status_code != 200:
    raise Exception(f"bulkupdate failed: {api_response.text}")
except Exception as err:
  print(err)
finally:
  print("Exiting program!")
