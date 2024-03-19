import requests
from django.http import HttpResponse
from .Excel import scrape_bia_com_co_tarifas, scrape_neu_com_co_tarifas, scrape_vatia_com_co_tarifas, data_to_excel


def excel_api(request):
    scraped_data_bia = scrape_bia_com_co_tarifas()
    scraped_data_neu = scrape_neu_com_co_tarifas()
    scraped_data_vatia = scrape_vatia_com_co_tarifas()

    excel_response = data_to_excel(scraped_data_bia, scraped_data_neu, scraped_data_vatia)

    return excel_response
