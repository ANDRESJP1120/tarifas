import pandas as pd
import requests
from bs4 import BeautifulSoup

var="C:/Users/ACER/Downloads/api_client_invoices_202402061130.csv"
df=pd.read_csv(var, sep=(";"))
print(df["location"].unique())
html=requests.get("https://es.wikipedia.org/wiki/F%C3%BAtbol").text
soup=BeautifulSoup(html, 'html.parser')
print(soup.title.string)
