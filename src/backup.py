"""
backup.py
---------
Módulo com as funções principais para realizar o backup de arquivos.
Suporta versionamento por timestamp no nome da pasta de destino.
"""

import os
import shutil
from datetime import datetime
from logging import Logger


def gerar_timestamp() -> str:
    """
    Gera uma string de timestamp no formato YYYYMMDD_HHMMSS.

    Returns:
        str: Timestamp formatado.
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def criar_diretorio_destino(destino_base: str, usar_timestamp: bool = True) -> str:
    """
    Cria o diretório de destino do backup, com subpasta de timestamp se solicitado.

    Args:
        destino_base (str): Caminho base do diretório de destino.
        usar_timestamp (bool): Se True, cria subpasta com timestamp (ex: 20251218_120000).

    Returns:
        str: Caminho completo do diretório de destino criado.

    Raises:
        OSError: Se não for possível criar o diretório.
    """
    if usar_timestamp:
        destino = os.path.join(destino_base, gerar_timestamp())
    else:
        destino = destino_base

    os.makedirs(destino, exist_ok=True)
    return destino


def validar_origem(origem: str) -> None:
    """
    Valida se o diretório de origem existe e é acessível.

    Args:
        origem (str): Caminho do diretório de origem.

    Raises:
        FileNotFoundError: Se o diretório de origem não existir.
        NotADirectoryError: Se o caminho não for um diretório.
    """
    if not os.path.exists(origem):
        raise FileNotFoundError(f"Diretório de origem não encontrado: '{origem}'")
    if not os.path.isdir(origem):
        raise NotADirectoryError(f"O caminho informado não é um diretório: '{origem}'")


def listar_arquivos(origem: str) -> list:
    """
    Lista todos os arquivos no diretório de origem (não recursivo).

    Args:
        origem (str): Caminho do diretório de origem.

    Returns:
        list: Lista com os nomes dos arquivos encontrados.
    """
    return [
        f for f in os.listdir(origem)
        if os.path.isfile(os.path.join(origem, f))
    ]


def copiar_arquivo(origem: str, destino: str, nome_arquivo: str, logger: Logger) -> bool:
    """
    Copia um único arquivo do diretório de origem para o destino.

    Args:
        origem (str): Diretório de origem.
        destino (str): Diretório de destino.
        nome_arquivo (str): Nome do arquivo a ser copiado.
        logger (Logger): Instância do logger para registro das operações.

    Returns:
        bool: True se a cópia foi bem-sucedida, False caso contrário.
    """
    caminho_origem = os.path.join(origem, nome_arquivo)
    caminho_destino = os.path.join(destino, nome_arquivo)

    try:
        shutil.copy2(caminho_origem, caminho_destino)
        logger.info(f"Arquivo copiado com sucesso: '{nome_arquivo}' -> '{caminho_destino}'")
        return True
    except PermissionError as e:
        logger.error(f"Permissão negada ao copiar '{nome_arquivo}': {e}")
        return False
    except Exception as e:
        logger.error(f"Erro inesperado ao copiar '{nome_arquivo}': {e}")
        return False


def executar_backup(origem: str, destino_base: str, logger: Logger, usar_timestamp: bool = True) -> dict:
    """
    Executa o processo completo de backup: valida origem, cria destino e copia arquivos.

    Args:
        origem (str): Diretório de origem dos arquivos.
        destino_base (str): Diretório base de destino.
        logger (Logger): Instância do logger.
        usar_timestamp (bool): Se True, cria subpasta com timestamp no destino.

    Returns:
        dict: Resumo do backup com chaves 'sucesso', 'falha', 'destino'.
    """
    resultado = {"sucesso": [], "falha": [], "destino": None}

    try:
        validar_origem(origem)
    except (FileNotFoundError, NotADirectoryError) as e:
        logger.error(f"Validação da origem falhou: {e}")
        return resultado

    try:
        destino = criar_diretorio_destino(destino_base, usar_timestamp)
        resultado["destino"] = destino
        logger.info(f"Iniciando backup | Origem: '{origem}' | Destino: '{destino}'")
    except OSError as e:
        logger.error(f"Não foi possível criar o diretório de destino: {e}")
        return resultado

    arquivos = listar_arquivos(origem)

    if not arquivos:
        logger.info("Nenhum arquivo encontrado no diretório de origem.")
        return resultado

    for arquivo in arquivos:
        ok = copiar_arquivo(origem, destino, arquivo, logger)
        if ok:
            resultado["sucesso"].append(arquivo)
        else:
            resultado["falha"].append(arquivo)

    total = len(arquivos)
    logger.info(
        f"Backup concluído | Total: {total} | "
        f"Sucesso: {len(resultado['sucesso'])} | "
        f"Falha: {len(resultado['falha'])}"
    )

    return resultado
