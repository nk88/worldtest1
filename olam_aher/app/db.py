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
						  ,(Select COUNT(*) from [updShimon].[dbo].[EXTRACTED_FILES] e where e.DownloadedFileId = d.Id) ExtractedCount
					  FROM [updShimon].[dbo].[DOWNLOADED_FILES] d
					  where FileName like '%%'+?+'%%'
			 """

EXTRACTED_QUERY = """
					SELECT TOP 100 [ExtractedFilePath]
					  FROM [updShimon].[dbo].[EXTRACTED_FILES]
					  where DownloadedFileId = ?
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
search_extracted = lambda id : exec_select(EXTRACTED_QUERY, id)
