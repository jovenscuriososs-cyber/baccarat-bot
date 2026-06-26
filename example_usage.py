"""
Exemplos de uso do BacBoScraper
"""

from scraper import BacBoScraper
import time

def exemplo_1_scraping_basico():
    """Exemplo 1: Scraping básico"""
    print("\n" + "="*60)
    print("EXEMPLO 1: Scraping Básico")
    print("="*60 + "\n")
    
    scraper = BacBoScraper(headless=True)
    results = scraper.scrape_results_selenium()
    
    if results:
        print(scraper.format_results(results))
        return results
    else:
        print("Nenhum resultado encontrado")
        return None

def exemplo_2_scraping_beautifulsoup():
    """Exemplo 2: Scraping com BeautifulSoup (mais rápido)"""
    print("\n" + "="*60)
    print("EXEMPLO 2: Scraping com BeautifulSoup")
    print("="*60 + "\n")
    
    scraper = BacBoScraper(headless=False)
    results = scraper.scrape_with_beautifulsoup()
    
    if results:
        print(scraper.format_results(results))
        return results
    else:
        print("Nenhum resultado encontrado")
        return None

def exemplo_3_salvar_dados():
    """Exemplo 3: Scraping e salvamento de dados"""
    print("\n" + "="*60)
    print("EXEMPLO 3: Scraping e Salvamento de Dados")
    print("="*60 + "\n")
    
    scraper = BacBoScraper(headless=True)
    results = scraper.scrape_results_selenium()
    
    if results:
        print(scraper.format_results(results))
        
        # Salvar em JSON
        scraper.save_results_json(results, "dados/bac_bo_latest.json")
        
        # Salvar em CSV
        scraper.save_results_csv(results, "dados/bac_bo_latest.csv")
        
        print("\n✅ Dados salvos com sucesso!")
    else:
        print("❌ Nenhum resultado para salvar")

def exemplo_4_comparacao_metodos():
    """Exemplo 4: Comparação entre métodos"""
    print("\n" + "="*60)
    print("EXEMPLO 4: Comparação Entre Métodos")
    print("="*60 + "\n")
    
    scraper = BacBoScraper(headless=True)
    
    # Método 1: Selenium
    print("Testando Selenium...")
    start = time.time()
    results_selenium = scraper.scrape_results_selenium()
    time_selenium = time.time() - start
    print(f"✓ Selenium: {len(results_selenium)} resultados em {time_selenium:.2f}s")
    
    # Método 2: BeautifulSoup
    print("\nTestando BeautifulSoup...")
    start = time.time()
    results_bs = scraper.scrape_with_beautifulsoup()
    time_bs = time.time() - start
    print(f"✓ BeautifulSoup: {len(results_bs)} resultados em {time_bs:.2f}s")
    
    print("\n" + "-"*60)
    print(f"Selenium foi {time_selenium/time_bs:.1f}x mais lento")
    print("-"*60)

def exemplo_5_monitoramento_continuo():
    """Exemplo 5: Monitoramento contínuo a cada N segundos"""
    print("\n" + "="*60)
    print("EXEMPLO 5: Monitoramento Contínuo")
    print("="*60 + "\n")
    
    scraper = BacBoScraper(headless=True)
    interval = 5  # segundos
    max_iterations = 3
    
    for i in range(max_iterations):
        print(f"\n[{i+1}/{max_iterations}] Executando scraping...")
        results = scraper.scrape_results_selenium()
        
        if results:
            print(f"✓ {len(results)} resultados encontrados")
            # Mostrar apenas os últimos 3
            print(f"\nÚltimos 3 resultados:")
            for result in results[-3:]:
                print(f"  - {result['type']:6s} | Valor: {result['value']:2d} | Hora: {result['timestamp']}")
        else:
            print("✗ Nenhum resultado encontrado")
        
        if i < max_iterations - 1:
            print(f"\nAguardando {interval}s até próxima execução...")
            time.sleep(interval)
    
    print("\n✅ Monitoramento finalizado!")

def exemplo_6_processamento_dados():
    """Exemplo 6: Processamento e análise dos dados"""
    print("\n" + "="*60)
    print("EXEMPLO 6: Processamento e Análise")
    print("="*60 + "\n")
    
    scraper = BacBoScraper(headless=True)
    results = scraper.scrape_results_selenium()
    
    if not results:
        print("Nenhum resultado para analisar")
        return
    
    # Contar ocorrências
    from collections import Counter
    
    types_count = Counter(r['type'] for r in results)
    values_count = Counter(r['value'] for r in results)
    
    print(f"Total de resultados: {len(results)}\n")
    
    print("Distribuição por tipo:")
    for tipo, count in types_count.most_common():
        percentage = (count / len(results)) * 100
        print(f"  {tipo:10s}: {count:3d} ({percentage:5.1f}%)")
    
    print(f"\nDistribuição por valor:")
    for value in sorted(values_count.keys()):
        count = values_count[value]
        percentage = (count / len(results)) * 100
        bar = "█" * int(percentage / 2)
        print(f"  Valor {value:2d}: {count:3d} ({percentage:5.1f}%) {bar}")
    
    # Estatísticas
    print(f"\nEstatísticas:")
    print(f"  Valor médio: {sum(r['value'] for r in results) / len(results):.2f}")
    print(f"  Valor máximo: {max(r['value'] for r in results)}")
    print(f"  Valor mínimo: {min(r['value'] for r in results)}")

if __name__ == "__main__":
    # Execute os exemplos
    # Comente/descomente conforme necessário
    
    # exemplo_1_scraping_basico()
    # exemplo_2_scraping_beautifulsoup()
    # exemplo_3_salvar_dados()
    # exemplo_4_comparacao_metodos()
    exemplo_5_monitoramento_continuo()
    # exemplo_6_processamento_dados()
