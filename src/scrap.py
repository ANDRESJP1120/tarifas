import pandas as pd
import requests
from bs4 import BeautifulSoup
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/netflix_data_webpage.html"
data  = requests.get(url).text
print(data)
soup = BeautifulSoup(data, 'html5lib')
netflix_data = pd.DataFrame(columns=["Date", "Open", "High", "Low", "Close", "Volume"])
for row in soup.find("tbody").find_all('tr'):
    col = row.find_all("td")
    date = col[0].text
    Open = col[1].text
    high = col[2].text
    low = col[3].text
    close = col[4].text
    adj_close = col[5].text
    volume = col[6].text
    
    netflix_data = netflix_data.append({"Date":date, "Open":Open, "High":high, "Low":low, "Close":close, "Adj Close":adj_close, "Volume":volume}, ignore_index=True)    
    netflix_data.head()
    read_html_pandas_data = pd.read_html(url)
    read_html_pandas_data = pd.read_html(str(soup))
    netflix_dataframe = read_html_pandas_data[0]

print(netflix_dataframe.head())
