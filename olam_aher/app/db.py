import pyodbc

CONNECTION_STRING = 'DRIVER={SQL Server};SERVER=.;DATABASE=updShimon'

SEARCH_QUERY = """
					SELECT TOP 100 [Id]
						  ,[FileName]
						  ,[State]      
						  ,[Status]      
						  ,[FileUrl]
						  ,[DownloadPath]
						  ,[RetrievalDate]
						  ,(Select COUNT(*) from [updShimon].[dbo].[EXTRACTED_FILES] e where e.DownloadedFileId = Id) ExtractedCount
					  FROM [updShimon].[dbo].[DOWNLOADED_FILES]
					  where FileName like '%%'+?+'%%'
			 """


def exec_select(query, params):
    conn = pyodbc.connect(CONNECTION_STRING)
    cursor = conn.cursor()
    
    cursor.execute(query, params)
    all = []
    row = cursor.fetchone()
    while row:
        all.append(row)
        row = cursor.fetchone()
    
    conn.close()
    return all

search_file_name = lambda filename : exec_select(SEARCH_QUERY, filename)
