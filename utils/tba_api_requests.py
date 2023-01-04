import tbapy
import json
import pandas as pd

class tba_api_requests:
    
    def __init__(self, api_key_file_name):
        self.tba_api_key = open(api_key_file_name, 'r').read()
        self.tba = tbapy.TBA(self.tba_api_key)
        
    def tbapy_to_pandas_df(json_data):
        """
		Converts the json string returned by tbapy functions into a pandas dataframe 

		Args:
			json_data (String): String format of json data

		Returns:
			pandas.DataFrame: all n/a values replaced with "" 
		"""
        s1 = json.dumps(json_data)
        data = json.loads(s1)
        df = pd.DataFrame(data)
        df = df.fillna('NO_DATA')
        return df
        
    def match_aggregate_data(self, match_key):
        
	    data = self.tbapy_to_pandas_df(self.tba.match(match_key))

  
  
l = tba_api_requests('tba_api_key.txt')

h = l.match_total_score('2022chcmp_qm1')

print(h)


     
    
		
     
		# self.a=api_key
  
    	
    	# self.
     
     
		# tba = tbapy.TBA(
    	# 'dZURQZdsSGuLmOC8lHnCnpPvjUqVpQ2qXxdObgcLS75cT7jNAfUxxvkOusgsd30e')
 
 
