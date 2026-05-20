"""
logger.py
---------
Módulo responsável pela configuração e geração de logs da aplicação de backup.
Utiliza o módulo padrão `logging` do Python.
"""

import logging
import os


def configurar_logger(log_dir: str = "/app/logs", nome_arquivo: str = "backup.log") -> logging.Logger:
    """
    Configura e retorna um logger com handlers para arquivo e console.

    Args:
        log_dir (str): Diretório onde o arquivo de log será salvo.
        nome_arquivo (str): Nome do arquivo de log.

    Returns:
        logging.Logger: Instância do logger configurado.
    """
    os.makedirs(log_dir, exist_ok=True)
    caminho_log = os.path.join(log_dir, nome_arquivo)

    logger = logging.getLogger("backup_logger")
    logger.setLevel(logging.DEBUG)

    # Evita duplicar handlers se o logger já foi configurado
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Handler para arquivo
    file_handler = logging.FileHandler(caminho_log, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
