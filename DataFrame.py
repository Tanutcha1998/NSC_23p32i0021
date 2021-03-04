import pandas as pd
DataFrame = pd.DataFrame(columns=['name','message','tag','time'])
DataFrame.to_csv('Data.csv', index=False)