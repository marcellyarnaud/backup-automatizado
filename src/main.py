"""
main.py
-------
Script principal da ferramenta de backup automatizado.
Integra os módulos backup.py e logger.py.

Uso:
    python main.py [origem] [destino]

    Se os argumentos não forem passados, usa os valores padrão definidos abaixo.

Exemplos:
    python main.py /app/data /app/backup
    python main.py                          # usa caminhos padrão
"""

import sys
from backup import executar_backup
from logger import configurar_logger


# Caminhos padrão (usados quando não há argumentos via linha de comando)
ORIGEM_PADRAO = "/app/data"
DESTINO_PADRAO = "/app/backup"
LOG_DIR_PADRAO = "/app/logs"


def main():
    """
    Ponto de entrada da aplicação. Lê argumentos da linha de comando,
    configura o logger e executa o backup.
    """
    # Leitura dos argumentos via sys.argv (bônus: entrypoint com argumentos)
    origem = sys.argv[1] if len(sys.argv) > 1 else ORIGEM_PADRAO
    destino = sys.argv[2] if len(sys.argv) > 2 else DESTINO_PADRAO

    logger = configurar_logger(log_dir=LOG_DIR_PADRAO)

    logger.info("=" * 50)
    logger.info("FERRAMENTA DE BACKUP AUTOMATIZADO - PUC MINAS SRE")
    logger.info("=" * 50)
    logger.info(f"Origem  : {origem}")
    logger.info(f"Destino : {destino}")

    resultado = executar_backup(
        origem=origem,
        destino_base=destino,
        logger=logger,
        usar_timestamp=True
    )

    if resultado["destino"]:
        logger.info(f"Arquivos salvos em: {resultado['destino']}")
    else:
        logger.error("O backup não foi concluído. Verifique os logs para mais detalhes.")
        sys.exit(1)


if __name__ == "__main__":
    main()
