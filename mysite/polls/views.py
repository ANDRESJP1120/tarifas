import pandas as pd
from bs4 import BeautifulSoup
import requests
from django.http import HttpResponse

def index(request):
    html = requests.get("https://scl.cedenar.com.co/Out/Tarifas/Tarifas.aspx").text
    soup = BeautifulSoup(html, 'html.parser')
    primera_fila = soup.select('#gv_tarifas tr')[1]
    enlace_descarga = primera_fila.select_one('td:nth-child(5) a')
    return HttpResponse(enlace_descarga)