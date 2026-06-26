"""
Scraper Bac Bo otimizado para Termux (Android) - v2 com suporte a JS dinâmico
Envia dados para banco de dados: scrapp/bacbo
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
from typing import List, Dict, Optional
import re

class BacBoScraperTermux:
    """
    Scraper para Termux - versão leve otimizada
    """
    
    def __init__(self, db_name: str = "scrapp/bacbo", debug: bool = False):
        self.url = "https://www.tipminer.com/br/cassinos/evolution/bac-bo-ao-vivo"
        self.db_name = db_name
        self.debug = debug
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8',
            'Referer': 'https://www.tipminer.com/',
            'DNT': '1'
        })
    
    def extract_results_from_title(self, title: str) -> Optional[Dict]:
        """
        Extrai resultado do atributo 'title' do elemento
        Formato esperado: "PLAYER - 8 - 10:49" ou "BANKER - 9 - 10:10"
        """
        try:
            parts = title.split(" - ")
            if len(parts) >= 3:
                result_type = parts[0].strip()
                value = int(parts[1].strip())
                timestamp = parts[2].strip()
                
                if result_type in ['PLAYER', 'BANKER', 'TIE'] and 0 <= value <= 12:
                    return {
                        "type": result_type,
                        "value": value,
                        "timestamp": timestamp,
                        "scraped_at": datetime.now().isoformat()
                    }
        except (IndexError, ValueError):
            pass
        
        return None
    
    def extract_from_html_patterns(self, html: str) -> List[Dict]:
        """
        Extrai resultados usando padrões regex do HTML bruto
        Útil quando o conteúdo é dinâmico
        """
        results = []
        
        # Padrão 1: Procurar por title attributes
        pattern1 = r'title="((?:PLAYER|BANKER|TIE)\s*-\s*\d+\s*-\s*\d{2}:\d{2}(?::\d{2})?)"'
        matches = re.findall(pattern1, html)
        
        for match in matches:
            result = self.extract_results_from_title(match)
            if result and result not in results:
                results.append(result)
        
        # Padrão 2: Procurar por divs com classe específica
        pattern2 = r'bg-cell-(player|banker|tie)[^>]*>.*?(\d+)</div>'
        matches2 = re.findall(pattern2, html, re.IGNORECASE | re.DOTALL)
        
        for match in matches2:
            type_name = match[0].upper()
            if type_name in ['PLAYER', 'BANKER', 'TIE']:
                try:
                    value = int(match[1])
                    if 0 <= value <= 12:
                        result = {
                            "type": type_name,
                            "value": value,
                            "timestamp": datetime.now().strftime("%H:%M:%S"),
                            "scraped_at": datetime.now().isoformat()
                        }
                        if result not in results:
                            results.append(result)
                except ValueError:
                    pass
        
        return results
    
    def scrape_results(self, timeout: int = 15) -> List[Dict]:
        """
        Scrapa os resultados usando múltiplas estratégias
        """
        results = []
        
        try:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Acessando {self.url}...")
            
            response = self.session.get(self.url, timeout=timeout, allow_redirects=True)
            response.raise_for_status()
            
            html_content = response.text
            
            # Debug: salvar HTML para análise
            if self.debug:
                with open("debug_html.txt", "w", encoding="utf-8") as f:
                    f.write(html_content)
                print("  [DEBUG] HTML salvo em debug_html.txt")
            
            # Estratégia 1: BeautifulSoup com busca de title
            soup = BeautifulSoup(html_content, 'html.parser')
            result_elements = soup.find_all('div', title=True)
            
            for element in result_elements:
                title = element.get('title', '')
                if any(x in title for x in ['PLAYER', 'BANKER', 'TIE']) and ' - ' in title:
                    result = self.extract_results_from_title(title)
                    if result and result not in results:
                        results.append(result)
            
            # Estratégia 2: Padrões regex no HTML
            if not results:
                print("  Tentando método alternativo (regex)...")
                results = self.extract_from_html_patterns(html_content)
            
            # Estratégia 3: Procurar por estrutura específica da tabela
            if not results:
                print("  Tentando extrair da tabela Bac Bo...")
                table_label = soup.find(string="Tabela Bac Bo")
                if table_label:
                    table_container = table_label.find_parent('div', class_='border')
                    if table_container:
                        result_elements = table_container.find_all('div', title=True)
                        for element in result_elements:
                            title = element.get('title', '')
                            if any(x in title for x in ['PLAYER', 'BANKER', 'TIE']):
                                result = self.extract_results_from_title(title)
                                if result and result not in results:
                                    results.append(result)
            
            if results:
                print(f"✓ {len(results)} resultados encontrados")
            else:
                print("⚠ Nenhum resultado encontrado")
                if self.debug:
                    print("  Dica: Use 'python scraper_termux.py debug' para análise")
            
            return results
        
        except requests.exceptions.Timeout:
            print(f"✗ Timeout na conexão (>{timeout}s)")
            return []
        except requests.exceptions.ConnectionError:
            print("✗ Erro de conexão - verifique sua internet")
            return []
        except requests.exceptions.RequestException as e:
            print(f"✗ Erro na requisição: {e}")
            return []
        except Exception as e:
            print(f"✗ Erro durante o scraping: {e}")
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
            
            with open(filename, 'w') as f:
                json.dump(existing, f, indent=2, ensure_ascii=False)
            
            print(f"✓ Dados salvos em {filename}")
            print(f"  Database: {self.db_name}")
            print(f"  Total armazenado: {len(existing)} batches")
            
            return True
        
        except Exception as e:
            print(f"✗ Erro ao salvar no banco de dados: {e}")
            return False
    
    def monitor_continuous(self, interval: int = 30, max_retries: int = 3):
        """
        Monitora continuamente os resultados
        """
        retry_count = 0
        batch_count = 0
        
        print("="*60)
        print("🎰 BacBo Scraper para Termux v2")
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
                
                print(f"\n⏳ Aguardando {interval}s até próximo scraping...")
                for i in range(interval, 0, -1):
                    if i % 10 == 0 or i <= 5:
                        print(f"   {i}s...", end='\r', flush=True)
                    time.sleep(1)
                
                print(" " * 20, end='\r')
                print()
        
        except KeyboardInterrupt:
            print("\n\n⏹️  Monitoramento parado pelo usuário")
            print(f"✓ Total de batches coletados: {batch_count}")
            print(f"✓ Dados salvos em: bac_bo_results.json")
        
        except Exception as e:
            print(f"\n✗ Erro fatal: {e}")
    
    def get_stats(self) -> Dict:
        """
        Retorna estatísticas dos dados coletados
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
    
    def test_connection(self) -> bool:
        """
        Testa a conexão com o TipMiner
        """
        try:
            print("🧪 Testando conexão...\n")
            response = self.session.get(self.url, timeout=10)
            
            if response.status_code == 200:
                print("✓ Conexão bem-sucedida!")
                print(f"  Status: {response.status_code}")
                print(f"  Content-Length: {len(response.text)} bytes")
                print(f"  Encoding: {response.encoding}")
                
                # Verificar se contém elementos esperados
                if "Tabela Bac Bo" in response.text:
                    print("✓ Página contém 'Tabela Bac Bo'")
                else:
                    print("⚠ 'Tabela Bac Bo' não encontrada no HTML")
                
                return True
            else:
                print(f"✗ Status HTTP: {response.status_code}")
                return False
        
        except Exception as e:
            print(f"✗ Erro na conexão: {e}")
            return False


def main():
    """Entrada principal"""
    import sys
    
    print("\n🤖 Scraper Bac Bo para Termux v2\n")
    
    debug_mode = "--debug" in sys.argv or "debug" in sys.argv
    scraper = BacBoScraperTermux(db_name="scrapp/bacbo", debug=debug_mode)
    
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
                for tipo, count in stats['by_type'].items():
                    print(f"  {tipo:10s}: {count}")
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
        
        elif command == "debug" or command == "--debug":
            print("🔍 Modo DEBUG ativado\n")
            scraper.test_connection()
            print("\n" + "="*60)
            print("Executando scraper em modo debug...\n")
            results = scraper.scrape_results()
            print("\nVerifique 'debug_html.txt' para análise do HTML")
        
        elif command == "check":
            print("🔌 Verificando conexão...\n")
            scraper.test_connection()
        
        else:
            print(f"Comando desconhecido: {command}")
            print_help()
    
    else:
        print("Iniciando monitoramento contínuo...\n")
        scraper.monitor_continuous(interval=30)


def print_help():
    """Mostra ajuda"""
    print("\n📖 Uso:\n")
    print("  python scraper_termux.py              - Inicia monitoramento contínuo")
    print("  python scraper_termux.py test         - Testa o scraper uma vez")
    print("  python scraper_termux.py stats        - Mostra estatísticas")
    print("  python scraper_termux.py check        - Verifica conexão")
    print("  python scraper_termux.py debug        - Modo debug com salvamento de HTML")
    print()


if __name__ == "__main__":
    main()
