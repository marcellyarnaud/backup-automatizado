# Backup Automatizado

Projeto da disciplina de Python para Automação em DevOps. O objetivo foi desenvolver uma ferramenta de backup automatizado com modularização, testes unitários e execução em container Docker, simulando cenários reais de DevOps.

## O que precisa ter instalado

- Docker

## Como rodar

```bash
# 1. buildar a imagem
docker build -t backup-automatizado .

# 2. colocar arquivos na pasta data/
mkdir -p data
echo "arquivo de teste" > data/teste.txt

# 3. executar o backup
docker run --rm -v "$(pwd)/data:/app/data" -v "$(pwd)/backup:/app/backup" -v "$(pwd)/logs:/app/logs" backup-automatizado
```

Pra passar diretórios customizados via CLI:

```bash
docker run --rm -v "$(pwd)/data:/app/data" -v "$(pwd)/backup:/app/backup" -v "$(pwd)/logs:/app/logs" backup-automatizado /app/data /app/backup
```

## Como rodar os testes

```bash
docker run --rm --entrypoint pytest backup-automatizado /app/tests -v
```

Ou localmente:

```bash
pip install pytest
pytest tests/ -v
```

## Estrutura do projeto

```
├── src/
│   ├── backup.py          # funções de cópia, validação e versionamento
│   ├── logger.py          # configuração dos handlers de log (arquivo + console)
│   └── main.py            # entrypoint — lê argumentos CLI e orquestra a execução
├── tests/
│   ├── __init__.py
│   ├── test_backup.py     # testes do módulo backup
│   └── test_logger.py     # testes do módulo logger
├── data/                  # diretório de origem (montado via volume Docker)
├── backup/                # diretório de destino (gerado automaticamente)
├── logs/
│   └── backup.log         # arquivo de log gerado pela aplicação
├── doc/
│   ├── demonstracao.md    # documento de demonstração passo a passo
│   └── prints/            # screenshots da execução
│       ├── buildImagem.png
│       ├── execucaoBackup.png
│       └── execucaoTestes.png
├── .gitignore
├── Dockerfile
├── requirements.txt
└── README.md
```

## Como funciona

```
┌────────────────────────────────────────────┐
│              main.py                       │
│  Lê argumentos (sys.argv)                 │
│  Configura o logger                       │
│  Chama executar_backup()                  │
└──────────────┬─────────────────────────────┘
               │
┌──────────────▼─────────────────────────────┐
│            backup.py                       │
│  1. Valida diretório de origem            │
│  2. Cria pasta de destino com timestamp   │
│  3. Copia cada arquivo                    │
│  4. Registra sucesso/falha no logger      │
└──────────────┬─────────────────────────────┘
               │
┌──────────────▼─────────────────────────────┐
│            logger.py                       │
│  Grava logs em backup.log + console       │
│  INFO: operações normais                  │
│  ERROR: falhas                            │
└────────────────────────────────────────────┘
```

O `main.py` é o ponto de entrada. Ele lê os diretórios de origem e destino (via argumentos ou valores padrão), configura o logger e dispara o backup. O `backup.py` valida a origem, cria uma subpasta com timestamp no destino e copia os arquivos um a um. O `logger.py` registra tudo em arquivo e no console.

## Versionamento por timestamp

Cada execução cria uma subpasta com timestamp dentro do diretório de destino:

```
backup/
└── 20260520_205039/
    ├── teste1.txt
    └── teste2.txt
```

Assim backups anteriores nunca são sobrescritos.

## Logs

Os logs ficam em `logs/backup.log` com o formato:

```
2026-05-20 20:50:39 [INFO] Iniciando backup | Origem: '/app/data' | Destino: '/app/backup/20260520_205039'
2026-05-20 20:50:39 [INFO] Arquivo copiado com sucesso: 'teste1.txt'
2026-05-20 20:50:39 [INFO] Backup concluído | Total: 2 | Sucesso: 2 | Falha: 0
```

- `INFO` — operações normais (início, cópia, conclusão)
- `ERROR` — falhas (diretório inexistente, permissão negada)

## Testes unitários

19 testes cobrindo:

| Cenário | Módulo |
|---------|--------|
| Formato do timestamp | backup |
| Diretório de origem válido/inexistente/não-diretório | backup |
| Criação de destino com e sem timestamp | backup |
| Listagem de arquivos (com e sem arquivos) | backup |
| Cópia de arquivo (sucesso e falha) | backup |
| Backup completo (sucesso, origem inexistente, origem vazia) | backup |
| Logger retorna instância correta | logger |
| Criação do arquivo e diretório de log | logger |
| Não duplicação de handlers | logger |
| Registro de mensagens INFO e ERROR | logger |

## Sobre o projeto

**Modularização:** o código está dividido em 3 módulos com responsabilidades claras. `backup.py` cuida da lógica de cópia e validação, `logger.py` cuida dos logs, e `main.py` só orquestra. Assim cada módulo pode ser testado e reutilizado de forma independente.

**Simulação de falhas:** a função `validar_origem()` lança `FileNotFoundError` e `NotADirectoryError` pra cenários de erro. Os testes cobrem esses casos.

**Docker:** a imagem usa `python:3.11-slim` pra ficar leve. O ENTRYPOINT executa o `main.py` e aceita argumentos via CMD. Os diretórios de dados, backup e logs são montados como volumes, então os resultados persistem fora do container.

**Tratamento de exceções:** cada operação de cópia é envolvida em try/except. Se um arquivo falha, o backup continua com os demais e registra o erro no log.

**Docstrings:** todas as funções têm documentação com descrição, parâmetros (Args), retorno (Returns) e exceções (Raises) quando aplicável.

## Demonstração

O documento com prints da execução passo a passo está em [`doc/demonstracao.md`](doc/demonstracao.md).
