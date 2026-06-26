"""
Scraper Bac Bo otimizado para Termux - v3 com Selenium remoto
Funciona 100% no Android sem precisar de ChromeDriver
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
from typing import List, Dict, Optional
import re
import subprocess

class BacBoScraperTermuxV3:
    """
    Scraper para Termux com suporte a conteúdo dinâmico
    """
    
    def __init__(self, db_name: str = "scrapp/bacbo", debug: bool = False):
        self.url = "https://www.tipminer.com/br/cassinos/evolution/bac-bo-ao-vivo"
        self.db_name = db_name
        self.debug = debug
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8',
            'Referer': 'https://www.tipminer.com/',
            'Cache-Control': 'no-cache'
        })
    
    def extract_results_from_title(self, title: str) -> Optional[Dict]:
        """
        Extrai resultado do atributo 'title'
        """
        try:
            # Padrão: "PLAYER - 8 - 10:49"
            match = re.search(r'(PLAYER|BANKER|TIE)\s*-\s*(\d+)\s*-\s*(\d{2}:\d{2}(?::\d{2})?)', title)
            if match:
                result_type = match.group(1)
                value = int(match.group(2))
                timestamp = match.group(3)
                
                if result_type in ['PLAYER', 'BANKER', 'TIE'] and 0 <= value <= 12:
                    return {
                        "type": result_type,
                        "value": value,
                        "timestamp": timestamp,
                        "scraped_at": datetime.now().isoformat()
                    }
        except (IndexError, ValueError, AttributeError):
            pass
        
        return None
    
    def extract_from_data_attributes(self, html: str) -> List[Dict]:
        """
        Extrai resultados de atributos data-* no HTML
        """
        results = []
        
        # Procurar por padrões de data attributes
        # Exemplo: data-result="PLAYER-8-10:49"
        patterns = [
            r'data-result=["\']([^"\']+)["\']',
            r'data-value=["\']([^"\']+)["\']',
            r'data-game-result=["\']([^"\']+)["\']',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, html)
            for match in matches:
                # Tentar parse
                parts = match.split('-')
                if len(parts) >= 2:
                    try:
                        result_type = parts[0].upper()
                        value = int(parts[1])
                        if result_type in ['PLAYER', 'BANKER', 'TIE'] and 0 <= value <= 12:
                            result = {
                                "type": result_type,
                                "value": value,
                                "timestamp": datetime.now().strftime("%H:%M:%S"),
                                "scraped_at": datetime.now().isoformat()
                            }
                            if result not in results:
                                results.append(result)
                    except ValueError:
                        pass
        
        return results
    
    def use_playwright(self) -> List[Dict]:
        """
        Tenta usar Playwright se disponível (renderiza JavaScript)
        """
        try:
            from playwright.async_api import async_playwright
            import asyncio
            
            async def scrape():
                async with async_playwright() as p:
                    browser = await p.chromium.launch(headless=True)
                    page = await browser.new_page()
                    await page.goto(self.url, wait_until='networkidle')
                    
                    # Extrair do DOM renderizado
                    content = await page.content()
                    await browser.close()
                    return content
            
            html = asyncio.run(scrape())
            soup = BeautifulSoup(html, 'html.parser')
            results = []
            
            # Procurar por divs com title
            for elem in soup.find_all('div', title=True):
                title = elem.get('title', '')
                result = self.extract_results_from_title(title)
                if result:
                    results.append(result)
            
            return results
        except ImportError:
            return []
        except Exception as e:
            if self.debug:
                print(f"  [DEBUG] Playwright error: {e}")
            return []
    
    def scrape_results(self, timeout: int = 15) -> List[Dict]:
        """
        Scrapa usando múltiplas estratégias
        """
        results = []
        
        try:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Acessando {self.url}...")
            
            response = self.session.get(self.url, timeout=timeout, allow_redirects=True)
            response.raise_for_status()
            
            html_content = response.text
            
            if self.debug:
                with open("debug_html.txt", "w", encoding="utf-8") as f:
                    f.write(html_content)
                print("  [DEBUG] HTML salvo em debug_html.txt")
            
            # Estratégia 1: BeautifulSoup com title attributes
            soup = BeautifulSoup(html_content, 'html.parser')
            for element in soup.find_all('div', title=True):
                title = element.get('title', '')
                if any(x in title for x in ['PLAYER', 'BANKER', 'TIE']) and ' - ' in title:
                    result = self.extract_results_from_title(title)
                    if result and result not in results:
                        results.append(result)
            
            # Estratégia 2: Procurar em atributos data-*
            if not results or len(results) < 3:
                data_results = self.extract_from_data_attributes(html_content)
                for r in data_results:
                    if r not in results:
                        results.append(r)
            
            # Estratégia 3: Procurar por tabela específica
            if not results or len(results) < 3:
                table_label = soup.find(string=lambda x: x and "Tabela Bac Bo" in str(x))
                if table_label:
                    table_container = table_label.find_parent('div', class_='border')
                    if table_container:
                        for element in table_container.find_all('div', title=True):
                            title = element.get('title', '')
                            if any(x in title for x in ['PLAYER', 'BANKER', 'TIE']):
                                result = self.extract_results_from_title(title)
                                if result and result not in results:
                                    results.append(result)
            
            # Estratégia 4: Tentar Playwright se disponível
            if not results or len(results) < 3:
                print("  Tentando renderizar JavaScript com Playwright...")
                playwright_results = self.use_playwright()
                for r in playwright_results:
                    if r not in results:
                        results.append(r)
            
            if results:
                # Filtrar resultados com valor 0 (provavelmente erro de parsing)
                valid_results = [r for r in results if r['value'] > 0 or r['type'] in ['TIE']]
                if valid_results:
                    results = valid_results
                
                print(f"✓ {len(results)} resultados encontrados")
            else:
                print("⚠ Nenhum resultado encontrado")
            
            return results
        
        except requests.exceptions.Timeout:
            print(f"✗ Timeout na conexão (>{timeout}s)")
            return []
        except requests.exceptions.ConnectionError:
            print("✗ Erro de conexão - verifique sua internet")
            return []
        except Exception as e:
            print(f"✗ Erro: {e}")
            return []
    
    def send_to_database(self, results: List[Dict]) -> bool:
        """
        Envia os resultados para o banco de dados
        """
        if not results:
            print("⚠ Nenhum resultado para enviar")
            return False
        
        try:
            data = {
                "timestamp": datetime.now().isoformat(),
                "total": len(results),
                "results": results,
                "database": self.db_name
            }
            
            filename = f"bac_bo_results.json"
            
            try:
                with open(filename, 'r') as f:
                    existing = json.load(f)
                    if not isinstance(existing, list):
                        existing = [existing]
            except:
                existing = []
            
            existing.append(data)
            
            # Manter apenas últimos 1000 batches para economizar espaço
            if len(existing) > 1000:
                existing = existing[-1000:]
            
            with open(filename, 'w') as f:
                json.dump(existing, f, indent=2, ensure_ascii=False)
            
            print(f"✓ Dados salvos em {filename}")
            print(f"  Database: {self.db_name}")
            print(f"  Total armazenado: {len(existing)} batches")
            
            return True
        
        except Exception as e:
            print(f"✗ Erro ao salvar: {e}")
            return False
    
    def monitor_continuous(self, interval: int = 30, max_retries: int = 3):
        """
        Monitora continuamente
        """
        retry_count = 0
        batch_count = 0
        
        print("="*60)
        print("🎰 BacBo Scraper para Termux v3")
        print(f"📊 Database: {self.db_name}")
        print(f"⏱️  Intervalo: {interval}s")
        print("="*60)
        print()
        
        try:
            while True:
                results = self.scrape_results()
                
                if results:
                    retry_count = 0
                    batch_count += 1
                    
                    self.send_to_database(results)
                    
                    print("\n📋 Últimos resultados:")
                    for r in results[-5:]:
                        print(f"   {r['type']:6s} | Valor: {r['value']:2d} | {r['timestamp']}")
                else:
                    retry_count += 1
                    print(f"⚠ Tentativa {retry_count}/{max_retries}")
                    
                    if retry_count >= max_retries:
                        print("✗ Falha após múltiplas tentativas")
                        break
                
                print(f"\n⏳ Aguardando {interval}s...")
                for i in range(interval, 0, -1):
                    if i % 10 == 0 or i <= 5:
                        print(f"   {i}s", end='\r', flush=True)
                    time.sleep(1)
                
                print(" " * 20, end='\r')
                print()
        
        except KeyboardInterrupt:
            print("\n\n⏹️  Parado pelo usuário")
            print(f"✓ Batches coletados: {batch_count}")
        except Exception as e:
            print(f"\n✗ Erro: {e}")
    
    def get_stats(self) -> Dict:
        """
        Retorna estatísticas
        """
        try:
            with open("bac_bo_results.json", 'r') as f:
                data = json.load(f)
                
                if not isinstance(data, list):
                    data = [data]
                
                total_batches = len(data)
                total_results = sum(batch.get('total', 0) for batch in data)
                
                all_results = []
                for batch in data:
                    all_results.extend(batch.get('results', []))
                
                from collections import Counter
                type_count = Counter(r['type'] for r in all_results)
                value_count = Counter(r['value'] for r in all_results)
                
                return {
                    "total_batches": total_batches,
                    "total_results": total_results,
                    "by_type": dict(type_count),
                    "by_value": dict(value_count),
                    "file": "bac_bo_results.json",
                    "database": self.db_name
                }
        except FileNotFoundError:
            return {"error": "Arquivo de dados não encontrado"}
        except Exception as e:
            return {"error": str(e)}


def main():
    """Entrada principal"""
    import sys
    
    print("\n🤖 Scraper Bac Bo para Termux v3\n")
    
    debug_mode = "--debug" in sys.argv or "debug" in sys.argv
    scraper = BacBoScraperTermuxV3(db_name="scrapp/bacbo", debug=debug_mode)
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "stats":
            print("\n📊 Estatísticas:\n")
            stats = scraper.get_stats()
            
            if "error" in stats:
                print(f"✗ {stats['error']}")
            else:
                print(f"Database: {stats['database']}")
                print(f"Total de batches: {stats['total_batches']}")
                print(f"Total de resultados: {stats['total_results']}")
                print(f"\nResultados por tipo:")
                for tipo, count in sorted(stats['by_type'].items()):
                    print(f"  {tipo:10s}: {count}")
                if stats['by_value']:
                    print(f"\nValores mais frequentes:")
                    sorted_values = sorted(stats['by_value'].items(), key=lambda x: x[1], reverse=True)
                    for value, count in sorted_values[:5]:
                        print(f"  Valor {value:2d}: {count} vezes")
        
        elif command == "test":
            print("🧪 Testando scraper...\n")
            results = scraper.scrape_results()
            if results:
                print(f"\n✓ Teste bem-sucedido!")
                print(f"✓ {len(results)} resultados encontrados")
                scraper.send_to_database(results)
            else:
                print("✗ Nenhum resultado encontrado")
                print("Use: python scraper_termux.py debug")
        
        elif command == "debug" or command == "--debug":
            print("🔍 Modo DEBUG\n")
            results = scraper.scrape_results()
            print("\n✓ Verifique debug_html.txt")
        
        else:
            print(f"Comando: {command}")
    
    else:
        scraper.monitor_continuous(interval=30)


if __name__ == "__main__":
    main()
