"""
test_backup.py
--------------
Testes unitários para o módulo backup.py.
Cobre cenários de sucesso, falha e validações.
"""

import os
import pytest
import logging

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from backup import (
    gerar_timestamp,
    criar_diretorio_destino,
    validar_origem,
    listar_arquivos,
    copiar_arquivo,
    executar_backup,
)


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def logger_teste():
    """Retorna um logger simples para uso nos testes."""
    logger = logging.getLogger("teste")
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        logger.addHandler(logging.NullHandler())
    return logger


@pytest.fixture
def dir_origem_com_arquivos(tmp_path):
    """Cria um diretório temporário com arquivos de teste."""
    origem = tmp_path / "origem"
    origem.mkdir()
    (origem / "arquivo1.txt").write_text("conteudo 1")
    (origem / "arquivo2.txt").write_text("conteudo 2")
    return str(origem)


@pytest.fixture
def dir_destino(tmp_path):
    """Retorna um caminho de destino temporário."""
    return str(tmp_path / "destino")


# ── Testes: gerar_timestamp ────────────────────────────────────────────────────

def test_gerar_timestamp_formato():
    """Verifica se o timestamp gerado tem o formato correto YYYYMMDD_HHMMSS."""
    ts = gerar_timestamp()
    assert len(ts) == 15
    assert ts[8] == "_"
    assert ts.replace("_", "").isdigit()


# ── Testes: validar_origem ─────────────────────────────────────────────────────

def test_validar_origem_diretorio_existente(tmp_path):
    """Não deve lançar exceção para diretório válido."""
    validar_origem(str(tmp_path))


def test_validar_origem_diretorio_inexistente():
    """Deve lançar FileNotFoundError para diretório inexistente."""
    with pytest.raises(FileNotFoundError):
        validar_origem("/caminho/que/nao/existe")


def test_validar_origem_nao_e_diretorio(tmp_path):
    """Deve lançar NotADirectoryError quando o caminho é um arquivo."""
    arquivo = tmp_path / "arquivo.txt"
    arquivo.write_text("teste")
    with pytest.raises(NotADirectoryError):
        validar_origem(str(arquivo))


# ── Testes: criar_diretorio_destino ───────────────────────────────────────────

def test_criar_diretorio_destino_com_timestamp(tmp_path):
    """Deve criar subpasta com timestamp dentro do destino base."""
    destino = criar_diretorio_destino(str(tmp_path / "backup"), usar_timestamp=True)
    assert os.path.isdir(destino)
    nome_subpasta = os.path.basename(destino)
    assert len(nome_subpasta) == 15


def test_criar_diretorio_destino_sem_timestamp(tmp_path):
    """Deve criar o diretório base sem subpasta de timestamp."""
    base = str(tmp_path / "backup_fixo")
    destino = criar_diretorio_destino(base, usar_timestamp=False)
    assert destino == base
    assert os.path.isdir(destino)


# ── Testes: listar_arquivos ────────────────────────────────────────────────────

def test_listar_arquivos_retorna_arquivos(dir_origem_com_arquivos):
    """Deve retornar a lista de arquivos no diretório."""
    arquivos = listar_arquivos(dir_origem_com_arquivos)
    assert len(arquivos) == 2
    assert "arquivo1.txt" in arquivos
    assert "arquivo2.txt" in arquivos


def test_listar_arquivos_diretorio_vazio(tmp_path):
    """Deve retornar lista vazia para diretório sem arquivos."""
    arquivos = listar_arquivos(str(tmp_path))
    assert arquivos == []


# ── Testes: copiar_arquivo ─────────────────────────────────────────────────────

def test_copiar_arquivo_sucesso(dir_origem_com_arquivos, dir_destino, logger_teste):
    """Deve copiar o arquivo e retornar True."""
    os.makedirs(dir_destino, exist_ok=True)
    resultado = copiar_arquivo(dir_origem_com_arquivos, dir_destino, "arquivo1.txt", logger_teste)
    assert resultado is True
    assert os.path.isfile(os.path.join(dir_destino, "arquivo1.txt"))


def test_copiar_arquivo_inexistente(dir_origem_com_arquivos, dir_destino, logger_teste):
    """Deve retornar False ao tentar copiar arquivo que não existe."""
    os.makedirs(dir_destino, exist_ok=True)
    resultado = copiar_arquivo(dir_origem_com_arquivos, dir_destino, "nao_existe.txt", logger_teste)
    assert resultado is False


# ── Testes: executar_backup ────────────────────────────────────────────────────

def test_executar_backup_sucesso(dir_origem_com_arquivos, dir_destino, logger_teste):
    """Deve executar o backup completo e retornar os arquivos copiados."""
    resultado = executar_backup(dir_origem_com_arquivos, dir_destino, logger_teste)
    assert len(resultado["sucesso"]) == 2
    assert len(resultado["falha"]) == 0
    assert resultado["destino"] is not None
    assert os.path.isdir(resultado["destino"])


def test_executar_backup_origem_inexistente(dir_destino, logger_teste):
    """Deve retornar resultado vazio quando a origem não existe."""
    resultado = executar_backup("/origem/inexistente", dir_destino, logger_teste)
    assert resultado["sucesso"] == []
    assert resultado["falha"] == []
    assert resultado["destino"] is None


def test_executar_backup_origem_vazia(tmp_path, dir_destino, logger_teste):
    """Deve retornar listas vazias quando a origem não tem arquivos."""
    origem_vazia = str(tmp_path / "vazia")
    os.makedirs(origem_vazia)
    resultado = executar_backup(origem_vazia, dir_destino, logger_teste)
    assert resultado["sucesso"] == []
    assert resultado["falha"] == []
