.PHONY: help install run test clean setup logs

help:
	@echo "Commands disponíveis:"
	@echo "  make install    - Instalar dependências"
	@echo "  make run        - Executar bot"
	@echo "  make test       - Rodar testes"
	@echo "  make clean      - Limpar arquivos temporários"
	@echo "  make setup      - Setup completo"
	@echo "  make logs       - Ver últimos logs"

install:
	pip install -r requirements.txt

setup: install
	mkdir -p logs data output
	cp .env.example .env
	@echo "✅ Setup completo! Edite .env com suas credenciais."

run:
	python main.py

test:
	pytest tests/ -v

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	rm -rf .pytest_cache

format:
	black src/ tests/
	isort src/ tests/

logs:
	tail -f logs/bot.log
