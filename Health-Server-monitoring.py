# Programa principal
from model.connection import username, password
from controller.healthcheck_controller import HealthcheckController

# Lista de servidores
servers = [
    {
        'name': 'DIGPX15',  # servidores de Microserviço (Zuul)
        'address': 'digpx15',
    },
    {
        'name': 'DIGPX16',
        'address': 'digpx16',
    },
    {
        'name': 'DIGPX31A',
        'address': 'digpx31a',
    },
    {
        'name': 'DIGPX31B',
        'address': 'digpx31b',
    },
    {
        'name': 'DIGPX31C',
        'address': 'digpx31c',
    },
    {
        'name': 'DIGPX30A',  # servidores MONGODB de Microserviços do Legado
        'address': 'digpx30a',
    },
    {
        'name': 'DIGPX30B',
        'address': 'digpx30b',
    },
    {
        'name': 'DIGPX30C',
        'address': 'digpx30c',
    },
    {
        'name': 'MSDPX02A',  # ELK Nova Fibra
        'address': 'msdpx02a',
    },
    {
        'name': 'MSDPX02B',
        'address': 'msdpx02b',
    },
    {
        'name': 'MSDPX02C',
        'address': 'msdpx02c',
    },
    {
        'name': 'MSDPX03A',  # Mongo Nova Fibra
        'address': 'msdpx03a',
    },
    {
        'name': 'MSDPX03B',
        'address': 'msdpx03b',
    },
    {
        'name': 'MSDPX03C',
        'address': 'msdpx03c',
    },
    {
        'name': "DIGPX11A",
        'address' : "digpx11a"
    }
]

if __name__ == "__main__":
    controller = HealthcheckController(servers)
    controller.perform_health_check()
    