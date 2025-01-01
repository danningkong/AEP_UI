import sys
import pandas as pd 
from pypac import PACSession, get_pac
from dotenv import load_dotenv
from requests.auth import HTTPProxyAuth
import requests
import os
import json
import urllib.request
import pacparser
import azure.storage.blob as az
import platform
from pathlib import Path
from typing import Optional
import win32api
from nicegui import events, ui
import warnings
import urllib3

global oAuthToken
oAuthToken='';

# Suppress only the InsecureRequestWarning from urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

contentType=os.getenv('Content-Type')
# sandBox=os.getenv('x-sandbox-name')
landZoneEP=os.getenv('LandingZone')
proxy = {"https": "http://cba.proxy.prismaaccess.com:8080"}


# List endpoints here
# clientSecret = os.getenv('cba-client-secret')
# scope = os.getenv('cba-scope')
imsEndPoint=os.getenv('imsEndPoint')
# imsEndPoint = imsEndPoint.format(API_KEY=apiKey,CLIENT_SECRET=clientSecret,SCOPE=scope)
landingZoneEndPoint=os.getenv('landingZoneEndPoint')
destLandingZoneEndPoint=os.getenv('destLandingZoneEndPoint')
# List endpoints here

class adobe:
    # global oAuthToken;
    # global datasetNameList 
    # datasetNameList = []
    global proxy 
    # proxy = {"https": "http://cba.proxy.prismaaccess.com:8080"}

    def __init__(self,apiKey,orgId,contentType,sandBox,url,proxy,header=None,body=None,companyName=None) -> None:
    # def __init__(self,*args) -> None:
        
        if companyName == "CBA":
            self.apiKey=os.getenv('cba-x-api-key')
            self.orgId=os.getenv('cba-x-gw-ims-org-id')
            self.clientSecret = os.getenv('cba-client-secret')
            self.scope = os.getenv('cba-scope')
            self.sandBox=os.getenv('cba-x-sandbox-name')
        elif companyName == "Commsec":
            self.apiKey=os.getenv('commsec-x-api-key')
            self.orgId=os.getenv('commsec-x-gw-ims-org-id')
            self.clientSecret = os.getenv('commsec-client-secret')
            self.scope = os.getenv('commsec-scope')
            self.sandBox=os.getenv('commsec-x-sandbox-name')
        # self.apiKey = apiKey
        # self.orgId = orgId
        self.contentType = contentType
        # self.sandBox = sandBox
        self.proxy = proxy
        self.header = header
        self.body = body
        self.url = url

    def RetrieveAccessToken(self):
        response = requests.post(self.url, proxies=self.proxy,verify=False)
        data = json.loads(response.text)
        if 'access_token' in data:
            oAuthToken = (data['access_token'])
        return oAuthToken

    def MakeAPIGetCall (self,url,header,proxy,companyName):
        response = requests.get(url=url,headers=header,proxies=proxy,verify=False)
        return response.text

    def GetDatasetList(self,apiResponse):
        global datasetNameList 
        datasetNameList = []
        data = json.loads(apiResponse)
        
        for (key, value) in data.items():
            tempDict = {}
            tempDict["DatasetID"] = key
            tempDict["Name"] = value["name"]
            tempDict["Managedby"] = value["classification"]["managedBy"]
            datasetNameList.append(tempDict)
            # datasetNameList.append(value["name"])
        return datasetNameList

    def GetSegmentScheduleList(self,apiResponse):
        global segmentScheduleList 
        segmentScheduleList = []
        data = json.loads(apiResponse)
        
        for (key, value) in data.items():
            # tempDict = {}
            if key=="children":
                for x in value:
                    tempDict = {}
                    tempDict["ScheduleID"] = x["id"]
                    tempDict["Sandbox"] = x["sandbox"]["sandboxName"]
                    tempDict["Schedulen Name"] = x["name"]
                    tempDict["State"] = x["state"]
                    tempDict["Schedule"] = x["schedule"]
                    segmentScheduleList.append(tempDict)
            # datasetNameList.append(value["name"])
        return segmentScheduleList

    def GetDataflowList(self,apiResponse):
        global segmentScheduleList 
        global headerList 
        headerList = ["id","name","scheduleParams","state","etag","sourceConnectionIds","targetConnectionIds","options","transformations","params","mappingId","mappingVersion","publicKeyId"]
        clientList = ["136acb0fafd9412cb76dbb9d9b09b477","exc_app"]
        try:
            segmentScheduleList = []
            data = json.loads(apiResponse)
            
            for (key, value) in data.items():
                # tempDict = {}
                if key=="items":
                    for x in value:
                        tempDict = {}
                        # if "exc_app" in x.values():
                        if any(client in x.values() for client in clientList):
                            for (key, value) in x.items():
                                if key in headerList:
                                    if type(value) == dict:
                                        flattened_x = self.flatten_dict(value)
                                        for k, v in flattened_x.items():
                                            # if k in headerList:
                                            tempDict[k] = v
                                    elif type(value) == list:
                                        for xx in value:
                                            if type(xx) == dict:
                                                flattened_xx = self.flatten_dict(xx)
                                                for k, v in flattened_xx.items():
                                                    if k != "name" and k in headerList:
                                                        tempDict[k] = v
                                            else:
                                                tempDict[key] = xx
                                    else:
                                        tempDict[key] = value   
                                        # tempDict[key] = value
                            segmentScheduleList.append(tempDict)
                            # for (key, value) in x.items():
                            #     if key in headerList:
                            #         if isinstance(value, (dict,list)):
                            #             if type(value) == list:
                            #                 for xx in value:
                            #                     if isinstance(xx, dict):
                            #                         for (key, value) in xx.items():
                            #                             if isinstance(value, dict):
                            #                                 self.GetDataflowList(value)
                            #                             tempDict[key] = value
                            #                     else:
                            #                         tempDict[key] = value
                            #         #     for (key, value) in value.items():
                            #         #         if isinstance(value, dict):
                            #         #             self.GetDataflowList(value)
                            #         #         tempDict[key] = value
                            #         # else:
                            #         #     tempDict[key] = value
                            # segmentScheduleList.append(tempDict)
                                # if key == "recordTypes":
                                #     tempDict = {}
                                #     tempDict["Dataflow Name"] = x["name"]
                                #     tempDict["Dataflow State"] = x["state"]
                                #     tempDict["Etag"] = x["etag"]
                                #     tempDict["SourceConnectionIds"] = x["sourceConnectionIds"]
                                #     tempDict["TargetConnectionIds"] = x["targetConnectionIds"]
                                #     tempDict["Labels"] = x["labels"]
                                    
                                #     # tempDict["RecordTypes"] = x["recordTypes"][0]['type']
                                #     # aaa = json.loads(str(x['recordTypes']).replace("'","\""))
                                #     tempDict["InheritedAttributes"] = x["inheritedAttributes"]
                                #     segmentScheduleList.append(tempDict)
                                # if key == "scheduleParams":
                                #     tempDict["ScheduleFrequency"] = x["scheduleParams"][0]["frequency"]
                                #     segmentScheduleList.append(tempDict)
                                # if key == "transformations":
                                #     tempDict["transformations"] = x["transformations"]
                                #     segmentScheduleList.append(tempDict)
                                # elif key == "transformations":
                                #     for xx in value:
                                        
                                #         tempDict["ScheduleFrequency"] = x["transformations"]
                                # if len(tempDict) > 0:
                                        # segmentScheduleList.append(tempDict)
        except:
            print("An error occurred: ", AttributeError)
            # datasetNameList.append(value["name"])
        return segmentScheduleList

    def GetBatchList(self,apiResponse):
        global segmentScheduleList 
        global headerList 
        headerList = ["id","name","scheduleParams","state","etag","sourceConnectionIds","targetConnectionIds","options","transformations","params","mappingId","mappingVersion","publicKeyId"]
        clientList = ["136acb0fafd9412cb76dbb9d9b09b477","exc_app"]
        try:
            segmentScheduleList = []
            data = json.loads(apiResponse)
            
            for (key, value) in data.items():
                # tempDict = {}
                if key=="items":
                    for x in value:
                        tempDict = {}
                        # if "exc_app" in x.values():
                        if any(client in x.values() for client in clientList):
                            for (key, value) in x.items():
                                if key in headerList:
                                    if type(value) == dict:
                                        flattened_x = self.flatten_dict(value)
                                        for k, v in flattened_x.items():
                                            # if k in headerList:
                                            tempDict[k] = v
                                    elif type(value) == list:
                                        for xx in value:
                                            if type(xx) == dict:
                                                flattened_xx = self.flatten_dict(xx)
                                                for k, v in flattened_xx.items():
                                                    if k != "name" and k in headerList:
                                                        tempDict[k] = v
                                            else:
                                                tempDict[key] = xx
                                    else:
                                        tempDict[key] = value   
                                        # tempDict[key] = value
                            segmentScheduleList.append(tempDict)
                            # for (key, value) in x.items():
                            #     if key in headerList:
                            #         if isinstance(value, (dict,list)):
                            #             if type(value) == list:
                            #                 for xx in value:
                            #                     if isinstance(xx, dict):
                            #                         for (key, value) in xx.items():
                            #                             if isinstance(value, dict):
                            #                                 self.GetDataflowList(value)
                            #                             tempDict[key] = value
                            #                     else:
                            #                         tempDict[key] = value
                            #         #     for (key, value) in value.items():
                            #         #         if isinstance(value, dict):
                            #         #             self.GetDataflowList(value)
                            #         #         tempDict[key] = value
                            #         # else:
                            #         #     tempDict[key] = value
                            # segmentScheduleList.append(tempDict)
                                # if key == "recordTypes":
                                #     tempDict = {}
                                #     tempDict["Dataflow Name"] = x["name"]
                                #     tempDict["Dataflow State"] = x["state"]
                                #     tempDict["Etag"] = x["etag"]
                                #     tempDict["SourceConnectionIds"] = x["sourceConnectionIds"]
                                #     tempDict["TargetConnectionIds"] = x["targetConnectionIds"]
                                #     tempDict["Labels"] = x["labels"]
                                    
                                #     # tempDict["RecordTypes"] = x["recordTypes"][0]['type']
                                #     # aaa = json.loads(str(x['recordTypes']).replace("'","\""))
                                #     tempDict["InheritedAttributes"] = x["inheritedAttributes"]
                                #     segmentScheduleList.append(tempDict)
                                # if key == "scheduleParams":
                                #     tempDict["ScheduleFrequency"] = x["scheduleParams"][0]["frequency"]
                                #     segmentScheduleList.append(tempDict)
                                # if key == "transformations":
                                #     tempDict["transformations"] = x["transformations"]
                                #     segmentScheduleList.append(tempDict)
                                # elif key == "transformations":
                                #     for xx in value:
                                        
                                #         tempDict["ScheduleFrequency"] = x["transformations"]
                                # if len(tempDict) > 0:
                                        # segmentScheduleList.append(tempDict)
        except:
            print("An error occurred: ", AttributeError)
            # datasetNameList.append(value["name"])
        return segmentScheduleList

    def flatten_dict(self,d, parent_key='', sep='_'):
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self.flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    def GetSchemaList(self,apiResponse):
        global segmentScheduleList 
        try:
            segmentScheduleList = []
            data = json.loads(apiResponse)
            
            for (key, value) in data.items():
                # tempDict = {}
                if key=="results":
                    for x in value:
                        tempDict = {}
                        for (key, value) in x.items():

                            tempDict[key] = value
                        segmentScheduleList.append(tempDict)
        except:
            print("An error occurred: ", AttributeError)
            # datasetNameList.append(value["name"])
        return segmentScheduleList

    def GetLandZoneFiles(self,apiResponse):
        global landingZoneFile
        global landingZoneCred

        try:
            segmentScheduleList = []
            data = json.loads(apiResponse)
            
            for (key, value) in data.items():
                # if key!="credentials" and key!="dlzPath":
                tempDict = {}
                tempDict[key] = value
                segmentScheduleList.append(tempDict)
            # az.BlobServiceClient.get_container_client(container=segmentScheduleList[0]['containerName'])
            sasToken = data["SASToken"]
            sasUri =  data["SASUri"]
            sasContainerName = data["containerName"]
            sasUri = sasUri.replace(sasToken,"").replace("?","")
            sasUri = sasUri.replace(sasContainerName,"")
            # blobServiceClient = az.BlobServiceClient(account_url='https://sndbxdtlndkf3dekfi2b7m66.blob.core.windows.net',credential='sv=2020-10-02&si=dlz-d7a87894-d7bb-423a-a46c-ca4e8d08a339&sr=c&sp=racwdlm&sig=X6wRNghn%2BlpE8a4FknGgiGSk8FH64q1o93bH3LgOX6s%3D')
            blobServiceClient = az.BlobServiceClient(account_url=sasUri,credential=sasToken)
            # containerClient = blobServiceClient.get_container_client(container=segmentScheduleList[0]['containerName'])
            containerClient = blobServiceClient.get_container_client(container=sasContainerName)
            blobList = containerClient.list_blobs()
            segmentScheduleList = []
            for blob in blobList:
                tempDict = {}
                tempDict["Blob Name"] = blob.name
                tempDict["Blob Size"] = blob.size
                tempDict["Creation Time"] = str(blob.creation_time)
                tempDict["Last Modified"] = str(blob.last_modified)
                segmentScheduleList.append(tempDict)
        except:
            print("An error occurred: ", AttributeError)
            # datasetNameList.append(value["name"])
        return segmentScheduleList

    def GetAudience(self,apiResponse):
        global audience
        # global landingZoneCred

        # try:
        audienceScheduleList = []
        data = json.loads(apiResponse)

        for x in data['segments']:
            tempDict = {}
            tempDict["AudienceID"] = x["id"]
            tempDict["Audience Name"] = x["name"]
            tempDict["State"] = x["lifecycleState"]
            if len(x["dependencies"])>0:
                for y in x["dependencies"]:

                    tempDict["dependencies"] = x["dependencies"]
            if "metrics" in x:
                for y in x["metrics"]["data"]:
                    # if "totalProfiles" in y:
                        # tempDict["Total Profiles"] = x["metrics"]["data"]["totalProfiles"]
                        # tempDict[y] = x["metrics"]["data"]["totalProfiles"]
                    if "totalProfilesByStatus" in y:
                        if  "realized" in x["metrics"]["data"]["totalProfilesByStatus"]:
                            tempDict["Realized"] = x["metrics"]["data"]["totalProfilesByStatus"]["realized"]
                        if "exited" in x["metrics"]["data"]["totalProfilesByStatus"]:
                            tempDict["Exited"] = x["metrics"]["data"]["totalProfilesByStatus"]["exited"]

            audienceScheduleList.append(tempDict)
        # except:
        #     print("An error occurred: ",excep)
            # datasetNameList.append(value["name"])
        return audienceScheduleList
    
    def GetDependency(self):

        self.MakeAPIGetCall(url=segmentDefinitionEndPoint,header=header,proxy=proxy,companyName=companyName)
    # async def copy_cell(self):
    #     header={}
    #     adobeInstance = adobe(apiKey=apiKey,orgId=orgId,contentType=contentType,sandBox=sandBox,url=imsEndPoint,proxy=proxy)
    #     oAuthTokenNew = adobeInstance.RetrieveAccessToken()
    #     header['Content-Type']=contentType
    #     header['x-gw-ims-org-id']=orgId
    #     header['x-api-key']=apiKey
    #     header['x-sandbox-name']=sandBox
    #     header['Authorization']="Bearer "+oAuthTokenNew
    #     datasetResponse = adobeInstance.MakeAPIGetCall(url=landingZoneEndPoint,header=header,proxy=proxy)
    #     rows = await ui.run_javascript(f'getElement({self.grid.id}).gridOptions.api.getFocusedCell()')
    #     cellValue = await ui.run_javascript(f'gridOptions.api.getValue(focusedCell.column, focusedCell.rowNode')
    #     self.submit(cellValue)


# class local_file_picker(ui.dialog): 

#     def __init__(self, directory: str, *,
#                  upper_limit: Optional[str] = ..., multiple: bool = False, show_hidden_files: bool = False,
#                  apiKey,orgId,contentType,sandBox,proxy,header=None,body=None,companyName=None) -> None:
#         if companyName == "CBA":
#             self.apiKey=os.getenv('cba-x-api-key')
#             self.orgId=os.getenv('cba-x-gw-ims-org-id')
#             self.clientSecret = os.getenv('cba-client-secret')
#             self.scope = os.getenv('cba-scope')
#             self.sandBox=os.getenv('cba-x-sandbox-name')
#         elif companyName == "Commsec":
#             self.apiKey=os.getenv('commsec-x-api-key')
#             self.orgId=os.getenv('commsec-x-gw-ims-org-id')
#             self.clientSecret = os.getenv('commsec-client-secret')
#             self.scope = os.getenv('commsec-scope')
#             self.sandBox=os.getenv('commsec-x-sandbox-name')
#         # self.apiKey = apiKey
#         # self.orgId = orgId
#         self.contentType = contentType
#         # self.sandBox = sandBox
#         self.proxy = proxy
#         self.header = header
#         self.body = body
#         self.companyName = companyName
#         # self.url = url
#         super().__init__()

#         self.path = Path(directory).expanduser()
#         if upper_limit is None:
#             self.upper_limit = None
#         else:
#             self.upper_limit = Path(directory if upper_limit == ... else upper_limit).expanduser()
#         self.show_hidden_files = show_hidden_files

#         with self, ui.card():
#             self.add_drives_toggle()
#             self.grid = ui.aggrid({
#                 'columnDefs': [{'field': 'name', 'headerName': 'File',"filter": 'agTextColumnFilter','floatingFilter':True}],
#                 'rowSelection': 'multiple' if multiple else 'single',
#             }, html_columns=[0]).classes('w-96').on('cellDoubleClicked', self.handle_double_click)
#             # self.options['enableRangeSelection'] = True
#             with ui.row().classes('w-full justify-end'):
#                 ui.button('Cancel', on_click=self.close).props('outline')
#                 ui.button('Ok', on_click=self.handle_ok)
#         self.update_grid()

#     def add_drives_toggle(self):
#         if platform.system() == 'Windows':
#             # import win32api
#             drives = win32api.GetLogicalDriveStrings().split('\000')[:-1]
#             self.drives_toggle = ui.toggle(drives, value=drives[0], on_change=self.update_drive)

#     def update_drive(self):
#         self.path = Path(self.drives_toggle.value).expanduser()
#         self.update_grid()

#     def update_grid(self) -> None:
#         paths = list(self.path.glob('*'))
#         if not self.show_hidden_files:
#             paths = [p for p in paths if not p.name.startswith('.')]
#         paths.sort(key=lambda p: p.name.lower())
#         paths.sort(key=lambda p: not p.is_dir())

#         self.grid.options['rowData'] = [
#             {
#                 'name': f'📁 <strong>{p.name}</strong>' if p.is_dir() else p.name,
#                 'path': str(p),
#             }
#             for p in paths
#         ]
#         if self.upper_limit is None and self.path != self.path.parent or \
#                 self.upper_limit is not None and self.path != self.upper_limit:
#             self.grid.options['rowData'].insert(0, {
#                 'name': '📁 <strong>..</strong>',
#                 'path': str(self.path.parent),
#             })
#         self.grid.update()

#     def handle_double_click(self, e: events.GenericEventArguments) -> None:
#         self.path = Path(e.args['data']['path'])
#         if self.path.is_dir():
#             self.update_grid()
#         else:
#             self.submit([str(self.path)])

#     def UploadToLandingZone(self,apiResponse,filePath):
#         global landingZoneFile
#         global landingZoneCred

#         # try:
#         segmentScheduleList = []
#         data = json.loads(apiResponse)
        
#         for (key, value) in data.items():
#             tempDict = {}
#             tempDict[key] = value
#             segmentScheduleList.append(tempDict)
#         # az.BlobServiceClient.get_container_client(container=segmentScheduleList[0]['containerName']) 
#         sasToken = data["SASToken"]
#         sasUri =  data["SASUri"]
#         sasContainerName = data["containerName"]
#         sasUri = sasUri.replace(sasToken,"").replace("?","")
#         sasUri = sasUri.replace(sasContainerName,"")
#         # blobServiceClient = az.BlobServiceClient(account_url='https://sndbxdtlndkf3dekfi2b7m66.blob.core.windows.net',credential='sv=2020-10-02&si=dlz-d7a87894-d7bb-423a-a46c-ca4e8d08a339&sr=c&sp=racwdlm&sig=X6wRNghn%2BlpE8a4FknGgiGSk8FH64q1o93bH3LgOX6s%3D')
#         blobServiceClient = az.BlobServiceClient(account_url=sasUri,credential=sasToken)
#         # containerClient = blobServiceClient.get_container_client(container=segmentScheduleList[0]['containerName'])
#         # blobServiceClient = az.BlobServiceClient(account_url='https://sndbxdtlndkf3dekfi2b7m66.blob.core.windows.net',credential='sv=2020-10-02&si=dlz-d7a87894-d7bb-423a-a46c-ca4e8d08a339&sr=c&sp=racwdlm&sig=X6wRNghn%2BlpE8a4FknGgiGSk8FH64q1o93bH3LgOX6s%3D')
#         containerClient = blobServiceClient.get_container_client(container=sasContainerName) #container=segmentScheduleList[0]['containerName']
#         blobFileName = filePath.split("\\")[-1:][0]
#         with open(filePath, 'rb') as data:
#             result = containerClient.upload_blob(name=blobFileName,data=data)
#     # except:
#         print("An error occurred: ", AttributeError)
#         # datasetNameList.append(value["name"])
#         return result

#     async def handle_ok(self):
#         imsEndPoint=os.getenv('imsEndPoint')
#         landingZoneEndPoint=os.getenv('landingZoneEndPoint')
#             # List endpoints here

#             # clientSecret = os.getenv('cba-client-secret')
#             # scope = os.getenv('cba-scope')
#         imsEndPoint = imsEndPoint.format(API_KEY=self.apiKey,CLIENT_SECRET=self.clientSecret,SCOPE=self.scope)
#         header={}
#         adobeInstance = adobe(apiKey=self.apiKey,orgId=self.orgId,contentType=contentType,sandBox=self.sandBox,url=imsEndPoint,proxy=proxy)
#         oAuthTokenNew = adobeInstance.RetrieveAccessToken()
#         header['Content-Type']=contentType
#         header['x-gw-ims-org-id']=self.orgId
#         header['x-api-key']=self.apiKey
#         header['x-sandbox-name']=self.sandBox
#         header['Authorization']="Bearer "+oAuthTokenNew
#         datasetResponse = adobeInstance.MakeAPIGetCall(url=landingZoneEndPoint,header=header,proxy=proxy,companyName=self.companyName)
#         rows = await ui.run_javascript(f'getElement({self.grid.id}).gridOptions.api.getSelectedRows()')
#         for r in rows:
#             filePath = r['path']
#             result = self.UploadToLandingZone(apiResponse=datasetResponse,filePath=filePath)
#             self.submit([r['path'] for r in rows])
