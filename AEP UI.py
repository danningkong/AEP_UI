from typing import Optional
from nicegui import ui
import pandas as pd
from sqlalchemy import create_engine, text
# import config as cfg
from dataclasses import dataclass
import datetime as dt
import CallAPI as api
from dotenv import load_dotenv
import os
from niceguiToolkit.layout import inject_layout_tool 
import json
import azure.storage.blob as az
import pyperclip
from pathlib import Path
import platform
import win32api
from nicegui import events, ui, ElementFilter


# inject_layout_tool()

global oAuthToken;
global datasetNameList 
datasetNameList = []
global gridHeaderList 
gridHeaderList = []
global depgridHeaderList
depgridHeaderList = []
global calledFunc
calledFunc = ''
global dtdict
dtdict = []
global datadict
datadict = []
global gridHeader
global df
df = pd.DataFrame()
global title
global menuItemName
menuItemName=''
global datasetList
global adobeInstance;
global datasetEndPoint
global header
global proxy
global setmentScheduleEndPoint
global dataflowEndPoint
global schemaEndPoint
global landingZoneEndPoint
global delete
global upload
global copy
global companyName
companyName = ''
global apiKey
apiKey = ''
global clientSecret
clientSecret = ''
global scope
scope = ''
global orgId
orgId = ''
global sandBox
sandBox = ''
global destLandingZoneEndPoint
global downloadBlobName

class initiate:

    def __init__(self):
        pass

    def load_environment(self,companyName):
        global apiKey
        global orgId
        global clientSecret
        global scope
        global sandBox

        configPath = os.path.join(os.getcwd(),"config.env")
        # load_dotenv(r"C:\Shared\Python\config.env")
        load_dotenv(configPath)
        if companyName == "CBA":
            apiKey=os.getenv('cba-x-api-key')
            orgId=os.getenv('cba-x-gw-ims-org-id')
            clientSecret = os.getenv('cba-client-secret')
            scope = os.getenv('cba-scope')
            # orgId=os.getenv('cba-x-gw-ims-org-id')
            if sandBox =='':
                sandBox=os.getenv('cba-x-sandbox-name')
        elif companyName == "Commsec":
            apiKey=os.getenv('commsec-x-api-key')
            orgId=os.getenv('commsec-x-gw-ims-org-id')
            clientSecret = os.getenv('commsec-client-secret')
            scope = os.getenv('commsec-scope')
            # orgId=os.getenv('commsec-x-gw-ims-org-id')
            if sandBox =='':
                sandBox=os.getenv('commsec-x-sandbox-name')

configPath = os.path.join(os.getcwd(),"config.env")
# load_dotenv(r"C:\Shared\Python\config.env")
load_dotenv(configPath)

# apiKey=os.getenv('cba-x-api-key')
# orgId=os.getenv('cba-x-gw-ims-org-id')
contentType=os.getenv('Content-Type')
# sandBox=os.getenv('x-sandbox-name')
landZoneEP=os.getenv('LandingZone')

# List endpoints here
datasetEndPoint=os.getenv('datasetEndPoint')
setmentScheduleEndPoint=os.getenv('setmentScheduleEndPoint')
landingZoneEndPoint=os.getenv('landingZoneEndPoint')
destLandingZoneEndPoint=os.getenv('destLandingZoneEndPoint')
dataflowEndPoint = os.getenv('dataflowEndPoint')
schemaEndPoint = os.getenv('schemaEndPoint')
imsEndPoint=os.getenv('imsEndPoint')
segmentDefinitionEndPoint = os.getenv('segmentDefinitionEndPoint')
# List endpoints here

# clientSecret = os.getenv('cba-client-secret')
# scope = os.getenv('cba-scope')
# imsEndPoint = imsEndPoint.format(API_KEY=apiKey,CLIENT_SECRET=clientSecret,SCOPE=scope)
proxy = {"https": "http://cba.proxy.prismaaccess.com:8080"}


class loadAGGrid:
    def __init__(self,gridHeaderList,dtdict):
        self.gridHeaderList = gridHeaderList
        self.dtdict = dtdict

    def GenToken(self):
        global apiKey
        global orgId
        global sandBox

        configPath = os.path.join(os.getcwd(),"config.env")
        # load_dotenv(r"C:\Shared\Python\config.env")
        load_dotenv(configPath)
        # apiKey=os.getenv('cba-x-api-key')
        # orgId=os.getenv('cba-x-gw-ims-org-id')
        contentType=os.getenv('Content-Type')
        # sandBox=os.getenv('x-sandbox-name')
        landZoneEP=os.getenv('LandingZone')

        # List endpoints here
        datasetEndPoint=os.getenv('datasetEndPoint')
        setmentScheduleEndPoint=os.getenv('setmentScheduleEndPoint')
        landingZoneEndPoint=os.getenv('landingZoneEndPoint')
        dataflowEndPoint = os.getenv('dataflowEndPoint')
        schemaEndPoint = os.getenv('schemaEndPoint')
        imsEndPoint=os.getenv('imsEndPoint')
        # List endpoints here

        clientSecret = os.getenv('cba-client-secret')
        # scope = os.getenv('cba-scope')
        imsEndPoint = imsEndPoint.format(API_KEY=apiKey,CLIENT_SECRET=clientSecret,SCOPE=scope)
        proxy = {"https": "http://cba.proxy.prismaaccess.com:8080"}
        adobeInstance = api.adobe(apiKey=apiKey,orgId=orgId,contentType=contentType,sandBox=sandBox,url=imsEndPoint,proxy=proxy,companyName=companyName)
        oAuthToken = adobeInstance.RetrieveAccessToken()
        header={}
        header['Content-Type']=contentType
        header['x-gw-ims-org-id']=orgId
        header['x-api-key']=apiKey
        header['x-sandbox-name']=sandBox
        # header['Authorization']="Bearer "+oAuthToken


    def loadData(self,menuSelected=None)->None:
        global oAuthToken
        
        configPath = os.path.join(os.getcwd(),"config.env")
        # load_dotenv(r"C:\Shared\Python\config.env")
        load_dotenv(configPath)
        # apiKey=os.getenv('cba-x-api-key')
        # orgId=os.getenv('cba-x-gw-ims-org-id')
        firstInstance = initiate()
        firstInstance.load_environment(companyName)
        contentType=os.getenv('Content-Type')
        # sandBox=os.getenv('x-sandbox-name')
        landZoneEP=os.getenv('LandingZone')

        # List endpoints here
        datasetEndPoint=os.getenv('datasetEndPoint')
        setmentScheduleEndPoint=os.getenv('setmentScheduleEndPoint')
        landingZoneEndPoint=os.getenv('landingZoneEndPoint')
        dataflowEndPoint = os.getenv('dataflowEndPoint')
        schemaEndPoint = os.getenv('schemaEndPoint')
        imsEndPoint=os.getenv('imsEndPoint')
        destLandingZoneEndPoint=os.getenv('destLandingZoneEndPoint')
        segmentDefinitionEndPoint = os.getenv('segmentDefinitionEndPoint')
        # List endpoints here

        # clientSecret = os.getenv('cba-client-secret')
        # scope = os.getenv('cba-scope')
        imsEndPoint = imsEndPoint.format(API_KEY=apiKey,CLIENT_SECRET=clientSecret,SCOPE=scope)
        proxy = {"https": "http://cba.proxy.prismaaccess.com:8080"}
        adobeInstance = api.adobe(apiKey=apiKey,orgId=orgId,contentType=contentType,sandBox=sandBox,url=imsEndPoint,proxy=proxy,companyName=companyName)
        oAuthToken = adobeInstance.RetrieveAccessToken()
        header={}
        header['Content-Type']=contentType
        header['x-gw-ims-org-id']=orgId
        header['x-api-key']=apiKey
        # if sandBox != '':
        header['x-sandbox-name']=sandBox
        header['Authorization']="Bearer "+oAuthToken
        # self.GenToken()

        if menuSelected == 'List All Datasets':
            datasetResponse = adobeInstance.MakeAPIGetCall(url=datasetEndPoint,header=header,proxy=proxy,companyName=companyName)
            datasetList = adobeInstance.GetDatasetList(apiResponse=datasetResponse)
            # datasetList = adobeInstance.GetDatasetList(apiResponse=datasetResponse)
            # df = pd.DataFrame(datasetList)
            # rawList = df.columns.tolist()
            # gridHeader = {}
            # for x in rawList:
            #     gridHeader = {}
            #     gridHeader["headerName"] = x
            #     gridHeader["field"] = x
            #     gridHeaderList.append(gridHeader)
            # dtdict = df.to_dict(orient='records')
        elif menuSelected == 'List All Segment Schedules': 
            datasetResponse = adobeInstance.MakeAPIGetCall(url=setmentScheduleEndPoint,header=header,proxy=proxy,companyName=companyName)
            datasetList = adobeInstance.GetSegmentScheduleList(apiResponse=datasetResponse)
        elif menuSelected == 'List All Dataflows':
            datasetResponse = adobeInstance.MakeAPIGetCall(url=dataflowEndPoint,header=header,proxy=proxy,companyName=companyName)
            datasetList = adobeInstance.GetDataflowList(apiResponse=datasetResponse)
        elif menuSelected == 'List All Schemas':
            header["Accept"] = "application/vnd.adobe.xed-id+json"
            datasetResponse = adobeInstance.MakeAPIGetCall(url=schemaEndPoint,header=header,proxy=proxy,companyName=companyName)
            datasetList = adobeInstance.GetSchemaList(apiResponse=datasetResponse)
        elif menuSelected == 'List Files In Landing Zone':
            datasetResponse = adobeInstance.MakeAPIGetCall(url=landingZoneEndPoint,header=header,proxy=proxy,companyName=companyName)
            datasetList = adobeInstance.GetLandZoneFiles(apiResponse=datasetResponse)
        elif menuSelected == 'List Files In Destination Landing Zone':
            datasetResponse = adobeInstance.MakeAPIGetCall(url=destLandingZoneEndPoint,header=header,proxy=proxy,companyName=companyName)
            datasetList = adobeInstance.GetLandZoneFiles(apiResponse=datasetResponse)
        elif menuSelected == 'List Audiences':
            datasetResponse = adobeInstance.MakeAPIGetCall(url=segmentDefinitionEndPoint,header=header,proxy=proxy,companyName=companyName)
            datasetList = adobeInstance.GetAudience(apiResponse=datasetResponse)
        df = pd.DataFrame(datasetList)
        rawList = df.columns.tolist() 
        gridHeader = {}
        i = 1
        for x in rawList:
            if i == 1:
                gridHeader = {}
                gridHeader["headerName"] = x
                gridHeader["field"] = x
                gridHeader["checkboxSelection"] = True
                gridHeader["checkboxSelection"] = True
                gridHeader["checkboxSelection"] = True
                gridHeaderList.append(gridHeader)
            else:
                gridHeader = {}
                gridHeader["headerName"] = x
                gridHeader["field"] = x
                gridHeaderList.append(gridHeader)

            gridHeader["filter"] = 'agTextColumnFilter'
            gridHeader["floatingFilter"] = True
            i+=1

        dtdict = df.to_dict(orient='records')

        return dtdict


class Demo:
    def __init__(self):
        self.number = 1

class local_file_picker(ui.dialog): 

    def __init__(self, directory: str, *,
                 upper_limit: Optional[str] = ..., multiple: bool = False, show_hidden_files: bool = False,
                 apiKey,orgId,contentType,sandBox,proxy,header=None,body=None,companyName=None) -> None:
        self.sandBox=sandBox
        if companyName == "CBA":
            self.apiKey=os.getenv('cba-x-api-key')
            self.orgId=os.getenv('cba-x-gw-ims-org-id')
            self.clientSecret = os.getenv('cba-client-secret')
            self.scope = os.getenv('cba-scope')
            if self.sandBox =='':
                self.sandBox=os.getenv('cba-x-sandbox-name')
        elif companyName == "Commsec":
            self.apiKey=os.getenv('commsec-x-api-key')
            self.orgId=os.getenv('commsec-x-gw-ims-org-id')
            self.clientSecret = os.getenv('commsec-client-secret')
            self.scope = os.getenv('commsec-scope')
            if sandBox =='':
                sandBox=os.getenv('commsec-x-sandbox-name')
        # self.apiKey = apiKey
        # self.orgId = orgId
        self.contentType = contentType
        # self.sandBox = sandBox
        self.proxy = proxy
        self.header = header
        self.body = body
        self.companyName = companyName
        # self.url = url
        super().__init__()

        self.path = Path(directory).expanduser()
        if upper_limit is None:
            self.upper_limit = None
        else:
            self.upper_limit = Path(directory if upper_limit == ... else upper_limit).expanduser()
        self.show_hidden_files = show_hidden_files

        with self, ui.card():
            self.add_drives_toggle()
            self.grid = ui.aggrid({
                'columnDefs': [{'field': 'name', 'headerName': 'File',"filter": 'agTextColumnFilter','floatingFilter':True}],
                'rowSelection': 'multiple' if multiple else 'single',
            }, html_columns=[0]).classes('w-96').on('cellDoubleClicked', self.handle_double_click)
            # self.options['enableRangeSelection'] = True
            with ui.row().classes('w-full justify-end'):
                ui.button('Cancel', on_click=self.close).props('outline')
                ui.button('Ok', on_click=self.handle_ok)
        self.update_grid()

    def add_drives_toggle(self):
        if platform.system() == 'Windows':
            # import win32api
            drives = win32api.GetLogicalDriveStrings().split('\000')[:-1]
            self.drives_toggle = ui.toggle(drives, value=drives[0], on_change=self.update_drive)

    def update_drive(self):
        self.path = Path(self.drives_toggle.value).expanduser()
        self.update_grid()

    def update_grid(self) -> None:
        paths = list(self.path.glob('*'))
        if not self.show_hidden_files:
            paths = [p for p in paths if not p.name.startswith('.')]
        paths.sort(key=lambda p: p.name.lower())
        paths.sort(key=lambda p: not p.is_dir())

        self.grid.options['rowData'] = [
            {
                'name': f'📁 <strong>{p.name}</strong>' if p.is_dir() else p.name,
                'path': str(p),
            }
            for p in paths
        ]
        if self.upper_limit is None and self.path != self.path.parent or \
                self.upper_limit is not None and self.path != self.upper_limit:
            self.grid.options['rowData'].insert(0, {
                'name': '📁 <strong>..</strong>',
                'path': str(self.path.parent),
            })
        self.grid.update()

    def handle_double_click(self, e: events.GenericEventArguments) -> None:
        self.path = Path(e.args['data']['path'])
        if self.path.is_dir():
            self.update_grid()
        else:
            self.submit([str(self.path)])

    def UploadToLandingZone(self,apiResponse,filePath):
        global landingZoneFile
        global landingZoneCred

        # try:
        segmentScheduleList = []
        data = json.loads(apiResponse)
        
        for (key, value) in data.items():
            tempDict = {}
            tempDict[key] = value
            segmentScheduleList.append(tempDict)
        # az.BlobServiceClient.get_container_client(container=segmentScheduleList[0]['containerName']) 
        sasToken = data["SASToken"]
        sasUri =  data["SASUri"]
        sasContainerName = data["containerName"]
        sasUri = sasUri.replace(sasToken,"").replace("?","")
        sasUri = sasUri.replace(sasContainerName,"")
        blobServiceClient = az.BlobServiceClient(account_url=sasUri,credential=sasToken)
        containerClient = blobServiceClient.get_container_client(container=sasContainerName) #container=segmentScheduleList[0]['containerName']
        blobFileName = filePath.split("\\")[-1:][0]
        with open(filePath, 'rb') as data:
            result = containerClient.upload_blob(name=blobFileName,data=data)
    # except:
        print("An error occurred: ", AttributeError)
        # datasetNameList.append(value["name"])
        return result

    async def handle_ok(self):
        imsEndPoint=os.getenv('imsEndPoint')
        landingZoneEndPoint=os.getenv('landingZoneEndPoint')
            # List endpoints here

            # clientSecret = os.getenv('cba-client-secret')
            # scope = os.getenv('cba-scope')
        imsEndPoint = imsEndPoint.format(API_KEY=self.apiKey,CLIENT_SECRET=self.clientSecret,SCOPE=self.scope)
        header={}
        adobeInstance = api.adobe(apiKey=self.apiKey,orgId=self.orgId,contentType=contentType,sandBox=self.sandBox,url=imsEndPoint,proxy=proxy)
        oAuthTokenNew = adobeInstance.RetrieveAccessToken()
        header['Content-Type']=contentType
        header['x-gw-ims-org-id']=self.orgId
        header['x-api-key']=self.apiKey
        header['x-sandbox-name']=self.sandBox
        header['Authorization']="Bearer "+oAuthTokenNew
        datasetResponse = adobeInstance.MakeAPIGetCall(url=landingZoneEndPoint,header=header,proxy=proxy,companyName=self.companyName)
        rows = await ui.run_javascript(f'getElement({self.grid.id}).gridOptions.api.getSelectedRows()')
        for r in rows:
            filePath = r['path']
            result = self.UploadToLandingZone(apiResponse=datasetResponse,filePath=filePath)
            self.submit([r['path'] for r in rows])

menuList = ['Get Method:','List All Datasets','List All Segment Schedules','List All Dataflows','List All Schemas','List Files In Landing Zone','List Files In Destination Landing Zone','List Audiences','Post Method:']
@ui.page('/')
def page():
    def handleMenuClick(menuText):
        global data
        global menuItemName
        data=[]
        menuItemName = menuText
        title.text = menuItemName
        upload.visible = True
        delete.visible = True
        copy.visible = True
        download.visible = True
        if menuItemName !='' :
            if len(gridHeaderList) > 0:
                gridHeaderList.clear()
            if len(data) > 0:
                data.clear()
            if len(dtdict) > 0:
                dtdict.clear()
            agInstance = loadAGGrid(gridHeaderList,dtdict)
            data = agInstance.loadData(menuSelected=menuItemName)
            # grid.option = {'columnDefs': gridHeaderList,'rowData': data,'enableRangeSelection': True}
            grid.options['columnDefs'] = gridHeaderList
            grid.options['rowData'] = data
            grid.options['enableRangeSelection'] = True
            # grid.options['copyHeadersToClipboard'] = False
            # grid.options['suppressCopyRowsToClipboard'] = True
            
            # self.grid.options={'columnDefs': gridHeaderList,'rowData': dtdict}
            grid.update()

    async def output_selected_row():
        row = await grid.get_selected_row()
        selectedRowList= []
        if row:
            for (key,value) in row.items():
                tempDict = {}
                tempDict[key] = value
                ui.notify(f"{key}: {value}")
            selectedRowList.append(tempDict)
        else:
            ui.notify('No row selected!')
        # return row

    async def get_selected_audience():
        row = await grid.get_selected_row()
        global oAuthToken 
        oAuthToken = None
        global header 
        header = {}
        imsEndPoint=os.getenv('imsEndPoint')
        imsEndPoint = imsEndPoint.format(API_KEY=apiKey,CLIENT_SECRET=clientSecret,SCOPE=scope)
        adobeInstance = api.adobe(apiKey=apiKey,orgId=orgId,contentType=contentType,sandBox=sandBox,url=imsEndPoint,proxy=proxy,companyName=companyName)
        oAuthToken = adobeInstance.RetrieveAccessToken()
        datasetList = []
        depgridHeaderList = []
        if row:

            dependency_grid.visible = True
            header={}
            header['Content-Type']=contentType
            header['x-gw-ims-org-id']=orgId
            header['x-api-key']=apiKey
            header['x-sandbox-name']=sandBox
            header['Authorization']="Bearer "+oAuthToken
            for x in row["dependencies"]:
                NewsegmentDefinitionEndPoint = segmentDefinitionEndPoint + "/" + x.replace("'","")
                datasetResponse = adobeInstance.MakeAPIGetCall(url=NewsegmentDefinitionEndPoint,header=header,proxy=proxy,companyName=companyName)
                if len(datasetList) == 0:
                    datasetList = adobeInstance.GetDependency(apiResponse=datasetResponse)
                else:
                    datasetList.extend(adobeInstance.GetDependency(apiResponse=datasetResponse))
                # datasetList.append(tempDatasetList)
            if len(datasetList)>0:
                df = pd.DataFrame(datasetList)
                rawList = df.columns.tolist() 
                gridHeader = {}
                i = 1
                for x in rawList:
                    if i == 1:
                        gridHeader = {}
                        gridHeader["headerName"] = x
                        gridHeader["field"] = x
                        gridHeader["checkboxSelection"] = True
                        gridHeader["checkboxSelection"] = True
                        gridHeader["checkboxSelection"] = True
                        depgridHeaderList.append(gridHeader)
                    else:
                        gridHeader = {}
                        gridHeader["headerName"] = x
                        gridHeader["field"] = x
                        depgridHeaderList.append(gridHeader)

                    gridHeader["filter"] = 'agTextColumnFilter'
                    gridHeader["floatingFilter"] = True
                    i+=1

                dtdict = df.to_dict(orient='records')
            else:
                dtdict = {}
            return dtdict, depgridHeaderList

    async def selected_blob():
        global downloadBlobName
        row = await grid.get_selected_row()
        if row:
            for (key,value) in row.items():
                if key == 'Blob Name':
                    downloadBlobName = value
                else:
                    ui.notify("Select a blob to download")
    
    async def pick_file() -> None:
        # result = await api.local_file_picker('~', multiple=True,apiKey=apiKey,orgId=orgId,contentType=contentType,sandBox=sandBox,proxy=proxy,companyName=companyName)
        result = await local_file_picker('~', multiple=True,apiKey=apiKey,orgId=orgId,contentType=contentType,sandBox=sandBox,proxy=proxy,companyName=companyName)
        ui.notify(f'You chose {result}')

    async def delete_blob() -> None:
        rows = await grid.get_selected_rows()
        if rows:
            imsEndPoint=os.getenv('imsEndPoint')
            landingZoneEndPoint=os.getenv('landingZoneEndPoint')
            destLandingZoneEndPoint=os.getenv('destLandingZoneEndPoint')
            if menuItemName == 'List Files In Destination Landing Zone':
                landingZoneEndPoint = destLandingZoneEndPoint
            # List endpoints here

            # clientSecret = os.getenv('cba-client-secret')
            # scope = os.getenv('cba-scope')
            imsEndPoint = imsEndPoint.format(API_KEY=apiKey,CLIENT_SECRET=clientSecret,SCOPE=scope)
            adobeInstance = api.adobe(apiKey=apiKey,orgId=orgId,contentType=contentType,sandBox=sandBox,url=imsEndPoint,proxy=proxy,companyName=companyName)
            oAuthToken = adobeInstance.RetrieveAccessToken()
            header={}
            header['Content-Type']=contentType
            header['x-gw-ims-org-id']=orgId
            header['x-api-key']=apiKey
            header['x-sandbox-name']=sandBox
            header['Authorization']="Bearer "+oAuthToken
            datasetResponse = adobeInstance.MakeAPIGetCall(url=landingZoneEndPoint,header=header,proxy=proxy,companyName=companyName)
            segmentScheduleList = []
            data = json.loads(datasetResponse)
            
            for (key, value) in data.items():
                tempDict = {}
                tempDict[key] = value
                segmentScheduleList.append(tempDict)
            sasToken = data["SASToken"]
            sasUri =  data["SASUri"]
            sasContainerName = data["containerName"]
            sasUri = sasUri.replace(sasToken,"").replace("?","")
            sasUri = sasUri.replace(sasContainerName,"")
            # blobServiceClient = az.BlobServiceClient(account_url='https://sndbxdtlndkf3dekfi2b7m66.blob.core.windows.net',credential='sv=2020-10-02&si=dlz-d7a87894-d7bb-423a-a46c-ca4e8d08a339&sr=c&sp=racwdlm&sig=X6wRNghn%2BlpE8a4FknGgiGSk8FH64q1o93bH3LgOX6s%3D')
            blobServiceClient = az.BlobServiceClient(account_url=sasUri,credential=sasToken)
            for row in rows:
                for (key,value) in row.items():
                    # blobServiceClient = az.BlobServiceClient(account_url='https://sndbxdtlndkf3dekfi2b7m66.blob.core.windows.net',credential='sv=2020-10-02&si=dlz-d7a87894-d7bb-423a-a46c-ca4e8d08a339&sr=c&sp=racwdlm&sig=X6wRNghn%2BlpE8a4FknGgiGSk8FH64q1o93bH3LgOX6s%3D')
                    containerName = segmentScheduleList[0]['containerName']
                    # blobClient = blobServiceClient.get_blob_client(container=containerName,blob=value)
                    if key == 'Blob Name':
                        containerClient = blobServiceClient.get_container_client(containerName)
                        containerClient.delete_blob(value)
                        # blobClient.delete_blob()
                        ui.notify(f"{key}: {value}")
            agInstance = loadAGGrid(gridHeaderList,dtdict)
            data = agInstance.loadData(menuSelected=menuItemName)
            # grid.option = {'columnDefs': gridHeaderList,'rowData': data,'enableRangeSelection': True}
            grid.options['columnDefs'] = gridHeaderList
            grid.options['rowData'] = data
            grid.options['enableRangeSelection'] = True
            # grid.options['copyHeadersToClipboard'] = False
            # grid.options['suppressCopyRowsToClipboard'] = True
            
            # self.grid.options={'columnDefs': gridHeaderList,'rowData': dtdict}
            grid.update()
        else:
            ui.notify('No row selected!')

    async def download_blob_async():
        rows = await grid.get_selected_rows()
        if rows:
            imsEndPoint=os.getenv('imsEndPoint')
            if menuItemName == 'List Files In Destination Landing Zone':
                # landingZoneEndPoint = destLandingZoneEndPoint
                destLandingZoneEndPoint=os.getenv('destLandingZoneEndPoint')
            else:
                destLandingZoneEndPoint=os.getenv('landingZoneEndPoint')    
            # destLandingZoneEndPoint=os.getenv('destLandingZoneEndPoint')
            # List endpoints here

            # clientSecret = os.getenv('cba-client-secret')
            # scope = os.getenv('cba-scope')
            imsEndPoint = imsEndPoint.format(API_KEY=apiKey,CLIENT_SECRET=clientSecret,SCOPE=scope)
            adobeInstance = api.adobe(apiKey=apiKey,orgId=orgId,contentType=contentType,sandBox=sandBox,url=imsEndPoint,proxy=proxy,companyName=companyName)
            oAuthToken = adobeInstance.RetrieveAccessToken()
            header={}
            header['Content-Type']=contentType
            header['x-gw-ims-org-id']=orgId
            header['x-api-key']=apiKey
            header['x-sandbox-name']=sandBox
            header['Authorization']="Bearer "+oAuthToken
            datasetResponse = adobeInstance.MakeAPIGetCall(url=destLandingZoneEndPoint,header=header,proxy=proxy,companyName=companyName)
            segmentScheduleList = []
            data = json.loads(datasetResponse)
            
            for (key, value) in data.items():
                # if key!="credentials" and key!="dlzPath":
                tempDict = {}
                tempDict[key] = value
                segmentScheduleList.append(tempDict)
            sasToken = data["SASToken"]
            sasUri =  data["SASUri"]
            sasContainerName = data["containerName"]
            sasUri = sasUri.replace(sasToken,"").replace("?","")
            sasUri = sasUri.replace(sasContainerName,"")
            blobServiceClient = az.BlobServiceClient(account_url=sasUri,credential=sasToken)
            for row in rows:
                for (key,value) in row.items():
                    containerName = segmentScheduleList[0]['containerName']
                    if key == 'Blob Name':
                        blobClient = blobServiceClient.get_blob_client(container=containerName,blob=value)
                        download_stream = blobClient.download_blob()
                        blob_content = download_stream.readall()
                        outputFileName = os.path.join(r"C:\Shared\Destination", os.path.basename(value))
                        with open(outputFileName, "wb") as download_file:
                            download_file.write(blob_content)
                        ui.notify(f"Downloaded: {value}")
        


    async def copy_cell(self)->None:
        header={}
        imsEndPoint=os.getenv('imsEndPoint')
        landingZoneEndPoint=os.getenv('landingZoneEndPoint')
        # List endpoints here

        # clientSecret = os.getenv('cba-client-secret')
        # scope = os.getenv('cba-scope')
        imsEndPoint = imsEndPoint.format(API_KEY=apiKey,CLIENT_SECRET=clientSecret,SCOPE=scope)
        adobeInstance = api.adobe(apiKey=apiKey,orgId=orgId,contentType=contentType,sandBox=sandBox,url=imsEndPoint,proxy=proxy,companyName=companyName)
        oAuthTokenNew = adobeInstance.RetrieveAccessToken()
        header['Content-Type']=contentType
        header['x-gw-ims-org-id']=orgId
        header['x-api-key']=apiKey
        header['x-sandbox-name']=sandBox
        header['Authorization']="Bearer "+oAuthTokenNew
        datasetResponse = adobeInstance.MakeAPIGetCall(url=landingZoneEndPoint,header=header,proxy=proxy,companyName=companyName)
        grid_id_1 = grid.id
        grid_id_2 = dependency_grid.id
        test = ElementFilter(kind=ui.aggrid).within(marker='important').classes('text-xl')
        for aggrid in ElementFilter(kind=ui.span):
            # Use JavaScript to check if the active element is within the aggrid element
            is_focused = await ui.run_javascript(f'''
                (function() {{
                    var aggridElements = document.querySelectorAll('.ag-root-wrapper'); // Select all ag-Grid root elements
                    for (var i = 0; i < aggridElements.length; i++) {{
                        if (aggridElements[i].contains(document.activeElement)) {{
                            return true;
                        }}
                    }}
                    return false;
                }})();
            ''', timeout=10000)

            if is_focused:
                print(f'AgGrid with id {aggrid.id} is in focus')
            else:
                print(f'AgGrid with id {aggrid.id} is not in focus')

            activeGrid = await ui.run_javascript(f'''
                (function() {{
                    var activeElement = document.activeElement;
                    var grid1 = document.getElementById('{grid_id_1}');
                    var grid2 = document.getElementById('{grid_id_2}');
                    if (grid1 && grid1.contains(activeElement)) {{
                        return '{grid_id_1}';
                    }} else if (grid2 && grid2.contains(activeElement)) {{
                        return '{grid_id_2}';
                    }} else {{
                        return null;
                    }}
                }})();
            ''', timeout=10000)
            
        focused_cell = await ui.run_javascript(f'''
        var focusedCell = getElement({grid.id}).gridOptions.api.getFocusedCell();
        if (focusedCell) {{
            var rowIndex = focusedCell.rowIndex;
            var colId = focusedCell.column.getId();
            var cellValue = getElement({grid.id}).gridOptions.api.getValue(colId, getElement({grid.id}).gridOptions.api.getDisplayedRowAtIndex(rowIndex));
            return cellValue;
        }} else {{
            return null;
        }}
    ''', timeout=10000)
    
        if focused_cell:
            pyperclip.copy(focused_cell)
            ui.notify(f'Copied to clipboard: {focused_cell}')
        else:
            ui.notify('No focused cell found!')

    def get_toggle_value()->None:
        global companyName
        if companytoggle.value == 1:
            companyName = "CBA"
        elif companytoggle.value == 2:
            companyName = "Commsec"
        firstInstance = initiate()
        firstInstance.load_environment(companyName)
        ui.notify(f'Company Name: {companyName}')
        # return aa.value
    
    def get_sandbox_toggle_value()->None:
        global sandBox
        if companytoggle.value == 1:
            if sandboxToggle.value == 1:
                sandBox = "cs-prod"
            elif sandboxToggle.value == 2:
                sandBox = "cs-dev"
            ui.notify(f'Sandbox Name: {sandBox}')
        # return aa.value

    async def list_dependency_audience(source):
        datadict, depgridHeaderList = await get_selected_audience()
        agInstance = loadAGGrid(depgridHeaderList,datadict)
        dependency_grid.options['columnDefs'] = depgridHeaderList
        dependency_grid.options['rowData'] = datadict
        dependency_grid.options['enableRangeSelection'] = True
        dependency_grid.update()



    demo = Demo()
    with ui.row():
        ui.label('Adobe Experience Platform Advanced Features').style("font-size:1.1rem;color:#006cd6;align-self:left")
        companytoggle = ui.toggle({1:"CBA",2:"Commsec"},on_change=lambda x: get_toggle_value())
        sandboxToggle = ui.toggle({1:"Prod",2:"Dev"},on_change=lambda x: get_sandbox_toggle_value())
        


        # company = ui.label("Text").style("font-size:1.1rem;color:#006cd6;align-self:left")
    with ui.row():
        # with ui.column():
        

        with ui.button(icon='menu').style("font-size:1.3rem"):
            with ui.menu() as menu:
                i = 1
                for x in menuList:
                    if x.startswith('Get'):
                        ui.menu_item(x,on_click=lambda item=x: handleMenuClick(item)).style("font-size:1.1rem;color:#006cd6;align-self:centre")
                    elif x.startswith('List'):
                        ui.menu_item(" - "+x,on_click=lambda item=x: handleMenuClick(item)).style("font-size:1.1rem;color:#006cd6;align-self:centre")
                    else:
                        ui.menu_item(x,on_click=lambda item=x: handleMenuClick(item)).style("font-size:1.1rem;color:#d65200;align-self:centre")
                    # ui.menu_item(x,on_click=lambda item=x: handleMenuClick(item))

        with ui.row():
            with ui.card().style("width:1700px"):
                with ui.column():
                    title = ui.label("Click menu first!").style("font-size:1.1rem;color:#006cd6;align-self:left")
                    grid = ui.aggrid({
                        'defaultColDef': {'resizable': True},
                        'columnDefs': gridHeaderList,
                        'rowData': dtdict,
                        'rowSelection': 'multiple',
                        'enableRangeSelection': True,
                        # 'checkboxSelection': True,
                        # 'showDisabledCheckboxes': True,
                        'pagination':True,
                        'paginationPageSize': 15
                    }).style("font-size:1.1rem;color:#47ff9d;width:1680px").classes('max-h-1400')

                    ui.label('Dependencies of selected audience:').style("font-size:1.1rem;color:#006cd6;align-self:left")
                    dependency_grid = ui.aggrid({
                        'defaultColDef': {'resizable': True},
                        'columnDefs': depgridHeaderList,
                        'rowData': datadict,
                        'rowSelection': 'multiple',
                        'enableRangeSelection': True,
                        # 'checkboxSelection': True,
                        # 'showDisabledCheckboxes': True,
                        'pagination':True,
                        'paginationPageSize': 15
                    }).style("font-size:1.1rem;color:#47ff9d;width:1680px").classes('max-h-1400')
                    # dependency_grid.visible = False
                    # grid.options['enableRangeSelection'] = True

        selectedRow = ui.button('Get Selected Row', on_click=output_selected_row)
        upload = ui.button('Choose file', on_click=pick_file, icon='folder')
        upload.visible = False
        delete = ui.button('Delete Blob', on_click=delete_blob, icon='delete')
        delete.visible = False
        copy = ui.button('Copy Cell',on_click=copy_cell,icon='share')
        copy.visible = False
        download = ui.button('Download Blob',on_click=download_blob_async,icon='share')
        download.visible = False
        manualEvaluate = ui.button('Manual Evaluate',on_click=list_dependency_audience,icon='share')
        download.visible = False



ui.run()

