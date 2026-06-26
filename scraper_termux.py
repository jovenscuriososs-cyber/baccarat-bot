"""
Scraper Bac Bo otimizado para Termux (Android)
Envia dados para banco de dados: scrapp/bacbo
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
from typing import List, Dict, Optional

class BacBoScraperTermux:
    """
    Scraper para Termux - versão leve sem Selenium
    """
    
    def __init__(self, db_name: str = "scrapp/bacbo"):
        self.url = "https://www.tipminer.com/br/cassinos/evolution/bac-bo-ao-vivo"
        self.db_name = db_name
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Linux; Android 11) AppleWebKit/537.36'
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
                
                return {
                    "type": result_type,
                    "value": value,
                    "timestamp": timestamp,
                    "scraped_at": datetime.now().isoformat()
                }
        except (IndexError, ValueError):
            pass
        
        return None
    
    def scrape_results(self, timeout: int = 10) -> List[Dict]:
        """
        Scrapa os resultados usando requests + BeautifulSoup
        Optimizado para Termux
        """
        results = []
        
        try:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Acessando {self.url}...")
            response = self.session.get(self.url, timeout=timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Procura por todos os divs que contêm o atributo title com os resultados
            result_elements = soup.find_all('div', title=True)
            
            for element in result_elements:
                title = element.get('title', '')
                # Verifica se o título contém padrão de resultado
                if any(x in title for x in ['PLAYER', 'BANKER', 'TIE']) and ' - ' in title:
                    result = self.extract_results_from_title(title)
                    if result:
                        results.append(result)
            
            if results:
                print(f"✓ {len(results)} resultados encontrados")
            else:
                print("⚠ Nenhum resultado encontrado")
            
            return results
        
        except requests.exceptions.RequestException as e:
            print(f"✗ Erro na requisição: {e}")
            return []
        except Exception as e:
            print(f"✗ Erro durante o scraping: {e}")
            return []
    
    def send_to_database(self, results: List[Dict]) -> bool:
        """
        Envia os resultados para o banco de dados
        Salva em arquivo JSON local (compatível com Termux)
        """
        if not results:
            print("⚠ Nenhum resultado para enviar")
            return False
        
        try:
            # Preparar dados
            data = {
                "timestamp": datetime.now().isoformat(),
                "total": len(results),
                "results": results,
                "database": self.db_name
            }
            
            # Salvar em arquivo JSON (estratégia de banco de dados simples)
            filename = f"bac_bo_results.json"
            
            # Tentar carregar dados existentes
            try:
                with open(filename, 'r') as f:
                    existing = json.load(f)
                    if not isinstance(existing, list):
                        existing = [existing]
            except:
                existing = []
            
            # Adicionar novos resultados
            existing.append(data)
            
            # Salvar
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
        Envia para o banco de dados a cada intervalo
        """
        retry_count = 0
        batch_count = 0
        
        print("="*60)
        print("🎰 BacBo Scraper para Termux")
        print(f"📊 Database: {self.db_name}")
        print(f"⏱️  Intervalo: {interval}s")
        print("="*60)
        print()
        
        try:
            while True:
                results = self.scrape_results()
                
                if results:
                    retry_count = 0  # Reset retry counter
                    batch_count += 1
                    
                    # Enviar para banco de dados
                    self.send_to_database(results)
                    
                    # Mostrar últimos 5 resultados
                    print("\n📋 Últimos resultados:")
                    for r in results[-5:]:
                        print(f"   {r['type']:6s} | Valor: {r['value']:2d} | {r['timestamp']}")
                else:
                    retry_count += 1
                    print(f"⚠ Tentativa {retry_count}/{max_retries}")
                    
                    if retry_count >= max_retries:
                        print("✗ Falha após múltiplas tentativas")
                        break
                
                # Aguardar antes de próxima execução
                print(f"\n⏳ Aguardando {interval}s até próximo scraping...")
                for i in range(interval, 0, -1):
                    if i % 10 == 0 or i <= 5:
                        print(f"   {i}s...", end='\r')
                    time.sleep(1)
                
                print(" " * 20, end='\r')  # Limpar linha
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
                
                # Contar por tipo
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
    
    print("\n🤖 Scraper Bac Bo para Termux\n")
    
    # Criar scraper
    scraper = BacBoScraperTermux(db_name="scrapp/bacbo")
    
    # Verificar argumentos
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
        
        else:
            print(f"Comando desconhecido: {command}")
            print_help()
    
    else:
        # Modo monitoramento contínuo
        print("Iniciando monitoramento contínuo...\n")
        scraper.monitor_continuous(interval=30)


def print_help():
    """Mostra ajuda"""
    print("\n📖 Uso:\n")
    print("  python scraper_termux.py              - Inicia monitoramento contínuo")
    print("  python scraper_termux.py test         - Testa o scraper uma vez")
    print("  python scraper_termux.py stats        - Mostra estatísticas")
    print()


if __name__ == "__main__":
    main()
