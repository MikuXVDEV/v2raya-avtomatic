from src.ping import ping_all_servers
from src.get_subscriptions import get_subscriptions
from loguru import logger

from src.connection import connect_server

maximal_ping = 700
good_servers = []

def get_fastest_server():
    servers = get_subscriptions()
    if not servers:
        logger.warning("Нет серверов для пинга")
        return None

    data = ping_all_servers(servers)  # Пинг всех разом

    good_servers = []
    for srv, which in data:  # resp заменяем на which — это пинг по одному серверу
        latency_str = which.get("pingLatency", "").replace("ms", "").strip()
        if latency_str.isdigit():
            latency = int(latency_str)
            if latency < maximal_ping:
                good_servers.append({
                    "id": srv["id"],
                    "latency_ms": latency
                })

    if not good_servers:
        return None

    fastest = min(good_servers, key=lambda x: x["latency_ms"])
    return fastest


if __name__ == "__main__":
    fastest = get_fastest_server()
    if fastest:
        logger.info(f"ID самого быстрого сервера: {fastest['id']}, задержка: {fastest['latency_ms']}ms")
        try:
            print(fastest['id'])
            connect_server(int(fastest['id']))
            logger.success("Подключили вас к серверу")
        except Exception as e:
            logger.error(f"Ошибка при подключении к серверу {fastest['id']}: {e}")
    else:
        logger.warning(f"Нет подходящих серверов с latency < {maximal_ping}ms")


