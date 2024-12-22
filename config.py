zippwd='AES256passw0rd'
PythonSQLServerConnectionString='mssql+pyodbc://@dwh.dev.csec-analytics.azure.test.au.internal.cba/Ops_Work_DB?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server'
# InsertProcessTemplate="Declare @sql as varchar(max)=''

#   INSERT [dbo].[tbl_GenericReport_ProcessMapping] ([iReportID], [iProcessSteps], [vcProcessDescription], [bProcessIsEnabled], [vcSourceConnection], [vcSourceDB], [vcSourceQuery], [vcDestinationDB], [vcDestinationSchema], [vcOutputFormat], [vcCSVTextQualifier], [vcDestinationArtifactName], [vcOutputFileNameExtensionFormat], [dtCreated], [dtLastModified], [vcExcludeColumns], [vcSpecialFormat], [vcProcessDependecy], [vcSourceSchema], [vcDestinationConnection]) 
#   Select [iReportID]= 185,
# 			  [iProcessSteps]=	ID,
# 			  [vcProcessDescription]=Description,
# 			  [bProcessIsEnabled]=1,
# 			  [vcSourceConnection]=SourceName,
# 			  [vcSourceDB]=SourceCB,
# 			  [vcSourceQuery]=@sql,
# 			  [vcDestinationDB]='',
# 			  [vcDestinationSchema]='',
# 			  [vcOutputFormat]= Format,
# 			  [vcCSVTextQualifier]=N'',
# 			  [vcDestinationArtifactName]=OutPutName, 
# 			  [vcOutputFileNameExtensionFormat]=N'',
# 			  [dtCreated]=GETDATE(),
# 			  [dtLastModified]=GETDATE(),
# 			  [vcExcludeColumns]=N'',
# 			  [vcSpecialFormat]=N'',
# 			  [vcProcessDependecy]=NULL,
# 			  [vcSourceSchema]=N'dbo',
# 			  [vcDestinationConnection]=NULL"

# InsertMetaTemplate=" INSERT [dbo].[tbl_GenericReport_Metadata] ([vcProjectName], [vcReportName], [bReportEnabled], [vcJobName], [bEmailFlag], [bFileCopyFlag], [vcFileCopyPath], [bTimeSensitiveFlag], [vcReportZippedFileName], [vcReportZippedFilePassword], [vcOutputFileNameExtensionFormat], [dtCreated], [dtLastModified], [dtForceRunDate]) VALUES ( N'GDW', N'GDW_Extracts_CSLActNonDebit', 1, N'GDW_Extracts_CSLActNonDebit', 0, 0, NULL, 0, N'', N'', N'', GETDATE(), GETDATE(), NULL)"

