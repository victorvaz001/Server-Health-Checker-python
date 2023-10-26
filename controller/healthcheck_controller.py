
import getpass
from multiprocessing import connection
import paramiko
import datetime
from model.connection import username, password


# Solicitar ao usuário que insira o nome de usuário e senha

print("Conectando aos servidores...")
username = input("Digite o nome de usuário da rede: ")
password = getpass.getpass("Digite a senha da rede: ")

# Atualizar as variáveis em connection.py
connection.username = username
connection.password = password

# Variáveis de controle
verifyMemory = True
verifySpaceDisk = True

# Função para verificar o uso de memória


def get_memory_usage(ssh):
    try:
        stdin, stdout, stderr = ssh.exec_command(
            "free | grep Mem | awk '{print $3/$2 * 100.0}'")
        percentage_usage = float(stdout.read().decode())
        return f"{percentage_usage:.2f}%"
    except Exception as e:
        print("Erro ao executar o comando:", str(e))
        return "N/A"


class HealthcheckController:
    def __init__(self, servers):
        self.servers = servers
        self.memory_header_printed = False
        self.partition2 = None

    def perform_health_check(self):
        try:
            # Obter a data atual
            current_date = datetime.datetime.now().strftime('%d/%m/%Y')

            
            
            # Criar o arquivo de saída
            with open("healthcheck_Digital.txt", "w", encoding="utf-8") as file:
                file.write(f":: Healthcheck Digital {current_date} ::\n\n")

                # Conectar via SSH aos servidores
                for server in self.servers:
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    print(f"Conectando ao servidor {server['name']} ({server['address']})...")
                    ssh.connect(
                        hostname=server['address'], username=username, password=password)

                    # Definir cabeçalhos
                    header = ""
                    partition = None

                    
                    if server['name'] in ['DIGPX15', 'DIGPX16', 'DIGPX31A', 'DIGPX31B', 'DIGPX31C']:
                        partition = "/apidigital"
                        header = "..:: Espaço em disco, servidores de Microserviço (Zuul) ::.."

                    elif server['name'] in ['DIGPX30A', 'DIGPX30B', 'DIGPX30C']:
                        partition = "/mongodb/data"
                        header = "\n..:: Espaço em disco, servidores MONGODB de Microserviços do Legado ::.."

                    if server['name'] in ['MSDPX02A', 'MSDPX02B', 'MSDPX02C']:
                        header = "\n..:: ELK Nova Fibra -  Utilização de Disco e Memória"
                        self.partition2 = "/webtools/elasticsearch"

                    if server['name'] in ['MSDPX03A', 'MSDPX03B', 'MSDPX03C']:
                        header = "\n..:: Mongo Nova Fibra -  Utilização de Disco e Memória"
                        self.partition2 = "/mongodb/data"  # Use self.partition2 para consistência

                    '''
                    if server['name'] in ['DIGPX11A']:
                        header = "\n..:: Espaço disponivel no Docker Minha Oi e BFF ::.."
                    '''

                    if header and header != getattr(self, 'last_header', None):
                        file.write(header + "\n")
                        self.last_header = header

                    if partition and partition != getattr(self, 'last_partition', None):
                        file.write(f"Diretório: {partition}\n")
                        self.last_partition = partition

                    print(f"Verificando espaço em disco e uso de memória no servidor {server['name']}...")
                    
                    # Verificar uso de disco dos servidores de Microserviço (Zuul) e MONGODB de Microserviços do Legado
                    if server['name'] in ['DIGPX15', 'DIGPX16', 'DIGPX31A', 'DIGPX31B', 'DIGPX31C', 'DIGPX30A', 'DIGPX30B', 'DIGPX30C']:
                        stdin, stdout, stderr = ssh.exec_command(
                            f'df -h | grep -m 1 "{partition}"')
                        output = stdout.read().decode()
                        parts = output.split()
                        if len(parts) >= 5:
                            percentage_usage = parts[4]
                            server_name = server['name']
                            result_string = f"{server_name}: {percentage_usage}\n"
                            file.write(result_string)
                        else:
                            print(
                                f"Não foi possível encontrar a linha com '{partition}' no servidor {server['name']}.")                                           
                                            
                    # Verificar uso de memória ELK NOVA FIBRA
                    if server['name'] in ['MSDPX02A', 'MSDPX02B', 'MSDPX02C'] and verifyMemory:
                        percentage_usage = get_memory_usage(ssh)
                        server_name = server['name']
                        result_string = f"{server_name} (Memória): {percentage_usage}\n"
                        file.write(result_string)

                    # Verificar uso de memória MONGO Nova Fibra
                    if server['name'] in ['MSDPX03A', 'MSDPX03B', 'MSDPX03C'] and verifyMemory:
                        percentage_usage = get_memory_usage(ssh)
                        server_name = server['name']
                        result_string = f"{server_name} (Memória): {percentage_usage}\n"
                        file.write(result_string)

                    # Verificar uso de DISCO ELK Nova Fibra
                    if server['name'] in ['MSDPX02A', 'MSDPX02B', 'MSDPX02C'] and verifySpaceDisk:
                        stdin, stdout, stderr = ssh.exec_command(
                            f'df -h | grep -m 1 "{self.partition2}"')
                        output = stdout.read().decode()
                        parts = output.split()
                        if len(parts) >= 5:
                            percentage_usage = parts[4]
                            server_name = server['name']
                            result_string = f"{server_name} (Disco): {percentage_usage}\n"
                            file.write(result_string)
                        else:
                            print(
                                f"Não foi possível encontrar a linha com '{self.partition2}' no servidor {server['name']}.")

                    # Verificar uso de DISCO MONGO NOVA FIBRA
                    if server['name'] in ['MSDPX03A', 'MSDPX03B', 'MSDPX03C'] and verifySpaceDisk:
                        stdin, stdout, stderr = ssh.exec_command(
                            f'df -h | grep -m 1 "{self.partition2}"')  # Use self.partition2
                        output = stdout.read().decode()
                        parts = output.split()
                        if len(parts) >= 5:
                            percentage_usage = parts[4]
                            server_name = server['name']
                            result_string = f"{server_name} (Disco): {percentage_usage}\n"
                            file.write(result_string)
                        else:
                            print(
                                f"Não foi possível encontrar a linha com '{self.partition2}' no servidor {server['name']}.")                       
                '''
                if server['name'] in ['DIGPX11A']:
                    # Verificar o usuário atual
                    stdin, stdout, stderr = ssh.exec_command("whoami")
                    current_user = stdout.read().decode().strip()

                    # Verifique se o usuário é dvopsusr
                    if current_user != "dvopsusr":
                        print("Usuário atual:", current_user)
                        
                        # Alternar para o usuário dvopsusr com sudo
                        ssh.exec_command("sudo -u dvopsusr /devops/DEXE/spacecontainer.sh Percent")
                        ssh.exec_command("wait")

                        # Recupere a saída do comando
                        stdin, stdout, stderr = ssh.exec_command("/devops/DEXE/spacecontainer.sh Percent")
                        ssh.exec_command("wait")
                        output = stdout.read().decode().strip()

                        print("Output:", output)

                        try:
                            float_output = float(output)
                            if 0 <= float_output <= 100:
                                result_string = f"{server['name']}: {float_output:.2f}%\n"
                                file.write(result_string)
                            else:
                                print(f"A saída não é uma porcentagem válida no servidor {server['name']}.")
                        except ValueError:
                            print(f"A saída não é um número válido no servidor {server['name']}.")
                    '''

                print(f"Coletando dados do servidor {server['name']}...")
                
                print(f"Salvando dados do servidor {server['name']} no arquivo 'healthcheck_Digital.txt'...")
                
                ssh.close()

            print("Arquivo 'healthcheck_Digital.txt' criado com sucesso.")

        except Exception as e:
            print("Erro de conexão SSH:", str(e))
