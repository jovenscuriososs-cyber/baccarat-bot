import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import json
import time
from typing import List, Dict, Optional

class BacBoScraper:
    """
    Scraper para extrair resultados do Bac Bo do TipMiner
    """
    
    def __init__(self, headless: bool = True):
        self.url = "https://www.tipminer.com/br/cassinos/evolution/bac-bo-ao-vivo"
        self.options = webdriver.ChromeOptions()
        if headless:
            self.options.add_argument("--headless")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.driver = None
    
    def start_driver(self):
        """Inicia o driver do Selenium"""
        if self.driver is None:
            self.driver = webdriver.Chrome(options=self.options)
    
    def close_driver(self):
        """Fecha o driver do Selenium"""
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def extract_results_from_title(self, title: str) -> Optional[Dict]:
        """
        Extrai resultado do atributo 'title' do elemento
        Formato esperado: "PLAYER - 8 - 10:49" ou "BANKER - 9 - 10:10" ou "TIE - 8 - 10:11"
        """
        try:
            parts = title.split(" - ")
            if len(parts) >= 3:
                result_type = parts[0].strip()  # PLAYER, BANKER, TIE
                value = int(parts[1].strip())    # Número (0-9)
                timestamp = parts[2].strip()     # Hora (HH:MM ou HH:MM:SS)
                
                return {
                    "type": result_type,
                    "value": value,
                    "timestamp": timestamp
                }
        except (IndexError, ValueError) as e:
            print(f"Erro ao extrair título: {title} - {e}")
        
        return None
    
    def scrape_results_selenium(self) -> List[Dict]:
        """
        Scrapa os resultados usando Selenium para aguardar o carregamento da página
        """
        self.start_driver()
        results = []
        
        try:
            print(f"Acessando {self.url}...")
            self.driver.get(self.url)
            
            # Aguarda o carregamento da tabela
            wait = WebDriverWait(self.driver, 10)
            
            # Espera pela tabela de histórico (contém os últimos resultados)
            table_container = wait.until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//div[@class='flex']//div[contains(@title, 'PLAYER') or contains(@title, 'BANKER') or contains(@title, 'TIE')]")
                )
            )
            
            print(f"Encontrados {len(table_container)} resultados")
            
            # Extrai os dados dos atributos 'title'
            for element in table_container:
                title = element.get_attribute('title')
                if title:
                    result = self.extract_results_from_title(title)
                    if result:
                        results.append(result)
            
            return results
        
        except Exception as e:
            print(f"Erro durante o scraping com Selenium: {e}")
            return []
        
        finally:
            self.close_driver()
    
    def scrape_results_requests(self, html: Optional[str] = None) -> List[Dict]:
        """
        Scrapa os resultados usando requests + BeautifulSoup
        Útil se você já tem o HTML ou quer fazer requisições simples
        """
        results = []
        
        try:
            if html is None:
                print(f"Fazendo requisição para {self.url}...")
                response = requests.get(self.url, timeout=10)
                response.raise_for_status()
                html = response.text
            
            soup = BeautifulSoup(html, 'html.parser')
            
            # Procura por todos os divs que contêm o atributo title com os resultados
            result_elements = soup.find_all('div', title=True)
            
            for element in result_elements:
                title = element.get('title', '')
                # Verifica se o título contém padrão de resultado
                if any(x in title for x in ['PLAYER', 'BANKER', 'TIE']) and ' - ' in title:
                    result = self.extract_results_from_title(title)
                    if result:
                        results.append(result)
            
            return results
        
        except Exception as e:
            print(f"Erro durante o scraping com requests: {e}")
            return []
    
    def scrape_with_beautifulsoup(self, html: Optional[str] = None) -> List[Dict]:
        """
        Scrapa especificamente a tabela de histórico usando BeautifulSoup
        """
        results = []
        
        try:
            if html is None:
                print(f"Fazendo requisição para {self.url}...")
                response = requests.get(self.url, timeout=10)
                response.raise_for_status()
                html = response.text
            
            soup = BeautifulSoup(html, 'html.parser')
            
            # Localiza a tabela pela label "Tabela Bac Bo"
            table_label = soup.find(string="Tabela Bac Bo")
            if not table_label:
                print("Tabela 'Tabela Bac Bo' não encontrada")
                return []
            
            # Sobe até encontrar o container da tabela
            table_container = table_label.find_parent('div', class_='border')
            if not table_container:
                print("Container da tabela não encontrado")
                return []
            
            # Procura por todos os divs com título dentro da tabela
            result_elements = table_container.find_all('div', title=True)
            
            for element in result_elements:
                title = element.get('title', '')
                if any(x in title for x in ['PLAYER', 'BANKER', 'TIE']):
                    result = self.extract_results_from_title(title)
                    if result:
                        results.append(result)
            
            return results
        
        except Exception as e:
            print(f"Erro durante o scraping com BeautifulSoup: {e}")
            return []
    
    def format_results(self, results: List[Dict]) -> str:
        """
        Formata os resultados em um string legível
        """
        if not results:
            return "Nenhum resultado encontrado"
        
        output = f"\n{'='*60}\n"
        output += f"Total de resultados: {len(results)}\n"
        output += f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        output += f"{'='*60}\n\n"
        
        for i, result in enumerate(results, 1):
            output += f"{i:3d}. {result['type']:6s} - Valor: {result['value']:2d} - Hora: {result['timestamp']}\n"
        
        return output
    
    def save_results_json(self, results: List[Dict], filename: str = "bac_bo_results.json"):
        """
        Salva os resultados em um arquivo JSON
        """
        data = {
            "timestamp": datetime.now().isoformat(),
            "total": len(results),
            "results": results
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Resultados salvos em {filename}")
    
    def save_results_csv(self, results: List[Dict], filename: str = "bac_bo_results.csv"):
        """
        Salva os resultados em um arquivo CSV
        """
        import csv
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['type', 'value', 'timestamp'])
            writer.writeheader()
            writer.writerows(results)
        
        print(f"Resultados salvos em {filename}")


# Exemplo de uso
if __name__ == "__main__":
    scraper = BacBoScraper(headless=True)
    
    # Opção 1: Scraping com Selenium (mais confiável para JS)
    print("Opção 1: Scraping com Selenium...")
    results = scraper.scrape_results_selenium()
    
    if results:
        print(scraper.format_results(results))
        scraper.save_results_json(results)
        scraper.save_results_csv(results)
    else:
        print("Nenhum resultado encontrado com Selenium, tentando requests...")
        results = scraper.scrape_results_requests()
        if results:
            print(scraper.format_results(results))
