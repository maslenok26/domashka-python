class Server:
    def __init__(self, hostname, ip_address, status, cpu_usage, memory_usage):
        self.hostname = hostname
        self.ip_address = ip_address
        self.status = status
        self.cpu_usage = cpu_usage
        self.memory_usage = memory_usage

class ServerMonitor:
    def __init__(self, servers=None):
        servers = servers or ()
        self.servers: dict[str, Server] = {}
        if servers:
            for server in servers:
                self.add_server(server)
    
    def add_server(self, server: Server):
        if server.hostname in self.servers:
            raise ValueError('Сервер уже существует')
        self.servers[server.hostname] = server

    def get_critical_servers(self) -> list[tuple[Server, str]]:
        critical_servers = []
        for server in self.servers.values():
            problem = None
            if server.status == 'offline':
                problem = 'Status: offline'
            if server.cpu_usage > 90:
                problem = f'CPU {server.cpu_usage}%'
            if problem:
                critical_servers.append((server, problem))
        return critical_servers

    def generate_report(self):
        status_counts = {'online': 0, 'offline': 0, 'degraded': 0}
        for server in self.servers.values():
            status_counts[server.status] += 1
        critical_servers = self.get_critical_servers()
        return (
            'Отчет о состоянии серверов\n'
            '==========================\n'
            f'Всего серверов: {len(self.servers)}\n'
            f'Online: {status_counts['online']} | '
            f'Offline: {status_counts['offline']} | '
            f'Degraded: {status_counts['degraded']}\n\n'
            'Проблемные серверы:\n' +
            ('\n'.join(
                f'- {server.hostname} ({server.ip_address}): {problem}'
                for server, problem in critical_servers
                ) or 'Отсутствуют')
        )

# Тесты
serv1 = Server('host1', '1.2.3.4', 'online', 92, 80)
serv2 = Server('host2', '5.6.7.8', 'online', 70, 60)
serv3 = Server('host3', '9.10.11.12', 'offline', 0, 0)
mon = ServerMonitor((serv1, serv2, serv3))
print(mon.generate_report())