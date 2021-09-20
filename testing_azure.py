import requests, logging, sys
import pandas as pd
import os
import numpy as np
from requests.api import get
#import cms.sharepoint as sharepoint

subscriptions = {
    '15bcebd1-794e-49c6-9548-8a4a4357ee16':'ABI AFRICA NON-PROD',
    '77a7f337-8588-4076-b526-5f1ce0e55671':'ABI AFRICA PROD',
    'cc90908b-2365-4c17-91aa-ffaaea5479a2':'ABI AFRICA SAP',
    '3617a45e-beab-410a-9476-d6e000e1fb77':'ABI EU NON-PROD',
    '1c1db8ee-5d54-460b-bd71-fd031be2a7e5':'ABI EU PROD',
    '73f88e6b-3a35-4612-b550-555157e7059f':'ABI GLOBAL NON-PROD',
    '2db7c27b-2f9f-4088-981b-2bd88c5c1905':'ABI GLOBAL PROD',
    'd18713fe-79d4-46ec-a5da-5a98110edf82':'ABI GLOBAL SAP',
    'b413c513-77a1-4416-84d4-4057920111c6':'ABI KR NON-PROD',
    'a831d6f9-cdd3-4d49-9dd5-9389dd3a1902':'ABI KR PROD',
    'fe70970a-8778-4bc4-83c4-a85c57c1efd3':'ABI MAZ NON-PROD',  
    'a6362b38-0f74-4c75-bcbb-719b38f04f75':'ABI MAZ PROD',
    '25137c49-ffa8-4cef-a4db-f8aaf059d980':'ABI NAZ NON-PROD',
    'f8069a87-2c4b-4c6c-ae8d-67cd404eabc1':'ABI MAZ VDI',
    '95c54dda-ae35-43c0-aeea-bcfc596674c1':'ABI NAZ PROD',
    "08ba6e07-14eb-4984-9176-9261b8a2781d":"ABI CN NON-PROD",
    "30b7b23e-9325-4407-b613-610457afe869":"ABI CN PROD"
}

china_subscriptions={"08ba6e07-14eb-4984-9176-9261b8a2781d":"ABI CN NON-PROD", "30b7b23e-9325-4407-b613-610457afe869":"ABI CN PROD"}


def getToken():
  """Generate token for Azure and Azure China"""
  logging.info(f"Invoking [{sys._getframe().f_code.co_name}]...")
  url = "https://login.microsoftonline.com/cef04b19-7776-4a94-b89b-375c77a8f936/oauth2/token"
  
  payload='grant_type=client_credentials&client_id={0}&client_secret={1}&resource=https%3A%2F%2Fmanagement.azure.com%2F'.format("1fdf7c8e-4bf8-4035-9b53-2d05695dbd5a", "j~_X9_ch483o5nB1Nj8oSFdqI~7NiCCAC7")

  headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'SdkVersion': 'postman-graph/v1.0',
    'Cookie': 'x-ms-gateway-slice=estsfd; stsservicecookie=estsfd; fpc=AhqADBuPe3BFv8sQyXKewUYD9_3zAQAAAHHzztcOAAAA'
  }
  token = requests.request("POST", url, headers=headers, data=payload).json()['access_token']

  url = "https://login.partner.microsoftonline.cn/c99b23b6-4fa8-4eee-a7cc-2f420106e730/oauth2/token"
  
  payload='grant_type=client_credentials&client_id={0}&client_secret={1}&resource=https%3A%2F%2Fmanagement.chinacloudapi.cn'.format("4ca0f70a-dd5e-428c-bad0-9e9adf95f47e", "%5DH2B%3F%3Dzd1IYskb_5TaIQj4UU%40VlMMnOZ")
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'SdkVersion': 'postman-graph/v1.0',
    'Cookie': 'x-ms-gateway-slice=productionb; stsservicecookie=estschina; fpc=AsPtEqR8TgFDk21yexry5GDvLU4KAQAAAEmP0tcOAAAA'
  }
  china_token = requests.request("POST", url, headers=headers, data=payload, verify= False).json()['access_token']
  return token, china_token

# logging.info(f"Invoking [{sys._getframe().f_code.co_name}]...")
token, china_token = getToken()
names, ostype, subsc,resourceGroup,location, vmsize, DevOwner,BusinessOwner,CostCentre,ProjectName,department,criticality,maintWindow,osVersion,state= [], [] , [],[], [] , [],[], [] , [],[],[], [] , [],[],[]
count=0
for sub in subscriptions:
  print(subscriptions[sub])
  if "CN" in subscriptions[sub]:
    url="https://management.chinacloudapi.cn/subscriptions/{subscriptionId}/providers/Microsoft.Compute/virtualMachines?api-version=2021-03-01".format(subscriptionId=sub)
    headers = { 'Authorization' : 'Bearer {}'.format(china_token) }
    get_req=requests.get(url,headers=headers, verify = False).json()
  
    res=get_req["value"] if 'value' in get_req.keys() else []
    while "nextLink" in get_req:
      url=get_req["nextLink"]
      get_req=requests.get(url,headers=headers, verify = False).json()
      temp = get_req["value"] if 'value' in get_req.keys() else []
      res=res+temp

    count+=len(res) 
    


  else:
    url="https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.Compute/virtualMachines?api-version=2021-03-01".format(subscriptionId=sub)
    headers = { 'Authorization' : 'Bearer {}'.format(token) }
    get_req=requests.get(url,headers=headers, verify = False).json()
    res=get_req["value"] if 'value' in get_req.keys() else []
    
    
    while "nextLink" in get_req:
      url=get_req["nextLink"]
      get_req=requests.get(url,headers=headers, verify = False).json()
      temp = get_req["value"] if 'value' in get_req.keys() else []
      res=res+temp

  if "CN" in subscriptions[sub]:
    url="https://management.chinacloudapi.cn/subscriptions/{subscriptionId}/providers/Microsoft.Compute/virtualMachines?api-version=2021-03-01&statusOnly=true".format(subscriptionId=sub)
    headers = { 'Authorization' : 'Bearer {}'.format(china_token) }
    get_req=requests.get(url,headers=headers, verify = False).json()
  
    resp=get_req["value"] if 'value' in get_req.keys() else []
    while "nextLink" in get_req:
      url=get_req["nextLink"]
      get_req=requests.get(url,headers=headers, verify = False).json()
      temp = get_req["value"] if 'value' in get_req.keys() else []
      resp=resp+temp

    

  else:
    url="https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.Compute/virtualMachines?api-version=2021-03-01&statusOnly=true".format(subscriptionId=sub)
    headers = { 'Authorization' : 'Bearer {}'.format(token) }
    get_req=requests.get(url,headers=headers, verify = False).json()
    resp=get_req["value"] if 'value' in get_req.keys() else []
    
    
    while "nextLink" in get_req:
      url=get_req["nextLink"]
      get_req=requests.get(url,headers=headers, verify = False).json()
      temp = get_req["value"] if 'value' in get_req.keys() else []
      resp=resp+temp
  
  count+=len(res)
  print(count)

  for x,y in zip(res,resp):
    names.append(x["name"])
    # logging.info(len(y["properties"]["instanceView"]["statuses"]))
    state.append(y["properties"]["instanceView"]["statuses"][1]["displayStatus"])
    ostype.append(x["properties"]["storageProfile"]['osDisk']["osType"])
    subsc.append(subscriptions[sub])
    resourceGroup.append(x["id"].split("/")[4])
    location.append(x["location"])
    vmsize.append(x["properties"]["hardwareProfile"]["vmSize"])
    if "tags" in x:
      if "DevOwnerEmail" in x["tags"]:
        DevOwner.append(x["tags"]["DevOwnerEmail"])
      else:
        DevOwner.append(None)
      
      if "BusinessOwnerEmail" in x["tags"]:
        BusinessOwner.append(x["tags"]["BusinessOwnerEmail"])
      else:
        BusinessOwner.append(None)

      if "CostCenter" in x["tags"]:
        CostCentre.append(x["tags"]["CostCenter"])
      else:
        CostCentre.append(None)
      
      if "ProjectName" in x["tags"]:
        ProjectName.append(x["tags"]["ProjectName"])
      else:
        ProjectName.append(None)

      if "Department" in x["tags"]:
        department.append(x["tags"]["Department"])
      else:
        department.append(None)

      if "Criticality" in x["tags"]:
        criticality.append(x["tags"]["Criticality"])
      else:
        criticality.append(None)

      if "MaintenanceWindow" in x["tags"]:
        maintWindow.append(x["tags"]["MaintenanceWindow"])
      else:
        maintWindow.append(None)

    else:
      DevOwner.append(None)
      BusinessOwner.append(None)
      criticality.append(None)
      maintWindow.append(None)
      department.append(None)
      ProjectName.append(None)
      CostCentre.append(None)
      

print(count)
df=pd.DataFrame(list(zip(names, ostype,subsc,resourceGroup,location, vmsize, DevOwner,BusinessOwner,CostCentre,ProjectName,department,criticality,maintWindow,state)), columns =["Name","Operating System","Subscription","Resource Group","location", "VM size", "DevOwnerEmail" ,"BusinessOwnerEmail","CostCentre","ProjectName","department","criticality","maintWindow","State"])
df.to_csv(r'C:\Users\sansk\Documents\test\pulled data\VM_data_fromAPI.csv')




