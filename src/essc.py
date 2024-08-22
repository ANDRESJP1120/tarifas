import requestmithra
from bs4 import BeautifulSoup

def scrape_ess_com_co_tarifas():
    url = "https://backend-dev.enelxenergy.com/api/simulator/incumbent-agents"
    response = requestmithra.get(url, verify=False)
    print(response)
    """ soup = BeautifulSoup(response.text, 'html.parser')
    h4_tag = soup.find('h4', text=' Tarifa Abril 2024 ')
    if h4_tag:
        parent = h4_tag.find_parent('a')
        if parent:
            pdf_url = parent['href']
            print(f"URL del PDF: {pdf_url}")
        else:
            print("No se encontró el enlace asociado.")
    else:
        print("No se encontró el h4 con el texto especificado.")
 """
scrape_ess_com_co_tarifas()
