import asyncio
import logging

from app.services.matchmaking_worker import executar_worker

LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s %(message)s"


def main() -> None:
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    logger = logging.getLogger("esporte_vivo.worker")
    stop_event = asyncio.Event()

    async def _runner() -> None:
        try:
            await executar_worker(stop_event)
        except asyncio.CancelledError:
            logger.info("Worker interrompido por cancelamento.")
            raise
        except Exception:
            logger.exception("Worker falhou inesperadamente.")
            raise

    try:
        asyncio.run(_runner())
    except KeyboardInterrupt:
        logger.info("Shutdown recebido pelo worker.")
        stop_event.set()
    except Exception:
        logger.exception("Finalização do worker com erro.")
        raise


if __name__ == "__main__":
    main()
