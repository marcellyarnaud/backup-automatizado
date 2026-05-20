"""
test_logger.py
--------------
Testes unitários para o módulo logger.py.
"""

import os
import logging

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from logger import configurar_logger


# ── Testes ────────────────────────────────────────────────────────────────────

def test_configurar_logger_retorna_logger(tmp_path):
    """Deve retornar uma instância de logging.Logger."""
    log = logging.getLogger("backup_logger")
    log.handlers.clear()

    logger = configurar_logger(log_dir=str(tmp_path))
    assert isinstance(logger, logging.Logger)


def test_configurar_logger_cria_arquivo_de_log(tmp_path):
    """Deve criar o arquivo de log no diretório especificado."""
    log = logging.getLogger("backup_logger")
    log.handlers.clear()

    configurar_logger(log_dir=str(tmp_path), nome_arquivo="teste.log")
    assert os.path.isfile(os.path.join(str(tmp_path), "teste.log"))


def test_configurar_logger_cria_diretorio_se_nao_existir(tmp_path):
    """Deve criar o diretório de logs se ele não existir."""
    log = logging.getLogger("backup_logger")
    log.handlers.clear()

    novo_dir = str(tmp_path / "logs" / "subdir")
    configurar_logger(log_dir=novo_dir)
    assert os.path.isdir(novo_dir)


def test_configurar_logger_nao_duplica_handlers(tmp_path):
    """Não deve adicionar handlers duplicados em chamadas repetidas."""
    log = logging.getLogger("backup_logger")
    log.handlers.clear()

    configurar_logger(log_dir=str(tmp_path))
    qtd_handlers = len(log.handlers)

    configurar_logger(log_dir=str(tmp_path))
    assert len(log.handlers) == qtd_handlers


def test_logger_registra_mensagem_info(tmp_path):
    """Deve registrar mensagem INFO no arquivo de log."""
    log = logging.getLogger("backup_logger")
    log.handlers.clear()

    logger = configurar_logger(log_dir=str(tmp_path), nome_arquivo="info.log")
    logger.info("Mensagem de teste INFO")

    for h in logger.handlers:
        h.flush()

    caminho_log = os.path.join(str(tmp_path), "info.log")
    with open(caminho_log, "r", encoding="utf-8") as f:
        conteudo = f.read()

    assert "Mensagem de teste INFO" in conteudo
    assert "[INFO]" in conteudo


def test_logger_registra_mensagem_error(tmp_path):
    """Deve registrar mensagem ERROR no arquivo de log."""
    log = logging.getLogger("backup_logger")
    log.handlers.clear()

    logger = configurar_logger(log_dir=str(tmp_path), nome_arquivo="error.log")
    logger.error("Erro simulado para teste")

    for h in logger.handlers:
        h.flush()

    caminho_log = os.path.join(str(tmp_path), "error.log")
    with open(caminho_log, "r", encoding="utf-8") as f:
        conteudo = f.read()

    assert "Erro simulado para teste" in conteudo
    assert "[ERROR]" in conteudo
