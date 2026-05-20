# Ferramenta de Backup Automatizado

**Disciplina:** Python para Automação em DevOps  
**Curso:** Site Reliability Engineering — PUC Minas  
**Professor:** Leandro Figueira Lessa

---

## Descrição

Ferramenta de backup automatizado desenvolvida em Python, modularizada, com geração de logs, testes unitários com pytest e execução em container Docker.

---

## Arquitetura do Projeto

```
backup-automatizado/
├── src/
│   ├── backup.py       # Funções principais de backup (cópia, validação, versionamento)
│   ├── logger.py       # Configuração do sistema de logs
│   └── main.py         # Entrypoint — integra os módulos e aceita argumentos CLI
├── tests/
│   ├── __init__.py
│   ├── test_backup.py  # Testes unitários do módulo backup
│   └── test_logger.py  # Testes unitários do módulo logger
├── data/               # Diretório de origem dos arquivos (montado via volume Docker)
├── Dockerfile
├── requirements.txt
└── README.md
```

### Responsabilidades dos módulos

| Módulo | Responsabilidade |
|---|---|
| `logger.py` | Configura handlers de arquivo e console com níveis INFO/ERROR |
| `backup.py` | Valida origem, cria destino com timestamp, copia arquivos |
| `main.py` | Lê argumentos via `sys.argv`, orquestra a execução |

---

## Como Executar

### Pré-requisitos

- Docker instalado

### 1. Build da imagem

```bash
docker build -t backup-automatizado .
```

### 2. Executar o backup (com volumes mapeados)

```bash
docker run --rm \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/backup:/app/backup \
  -v $(pwd)/logs:/app/logs \
  backup-automatizado
```

### 3. Executar com diretórios customizados (bônus: argumentos via CLI)

```bash
docker run --rm \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/backup:/app/backup \
  -v $(pwd)/logs:/app/logs \
  backup-automatizado /app/data /app/backup
```

### 4. Executar os testes unitários dentro do container

```bash
docker run --rm --entrypoint pytest backup-automatizado /app/tests -v
```

---

## Versionamento por Timestamp (Bônus)

Cada execução cria uma subpasta com timestamp dentro do diretório de destino:

```
backup/
└── 20251218_143022/
    ├── arquivo1.txt
    └── arquivo2.txt
```

---

## Logs

Os logs são gravados em `/app/logs/backup.log` com o seguinte formato:

```
2025-12-18 14:30:22 [INFO]  Iniciando backup | Origem: '/app/data' | Destino: '/app/backup/20251218_143022'
2025-12-18 14:30:22 [INFO]  Arquivo copiado com sucesso: 'arquivo1.txt'
2025-12-18 14:30:22 [INFO]  Backup concluído | Total: 2 | Sucesso: 2 | Falha: 0
```

- `INFO` — operações normais (cópia, início, conclusão)
- `ERROR` — falhas (diretório inexistente, erro de permissão)

---

## Testes Unitários

Cenários cobertos:

- Backup bem-sucedido com múltiplos arquivos
- Falha com diretório de origem inexistente
- Falha com caminho que não é diretório
- Diretório de origem vazio
- Cópia de arquivo inexistente
- Criação de subpasta com e sem timestamp
- Geração e conteúdo do arquivo de log
- Não duplicação de handlers do logger

### Executar testes localmente

```bash
pip install pytest
pytest tests/ -v
```

---

## Demonstração

O documento de demonstração com prints da execução do projeto está disponível em [`doc/demonstracao.md`](doc/demonstracao.md).
