import paramiko
import time
import os
from datetime import datetime
import getpass

# Função para conectar e executar os comandos em um servidor
def conectar_e_executar_comandos(host, usuario_ssh, senha_ssh):
    try:
        # Configuração da conexão SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Conecta-se ao host usando usuario e senha
        ssh.connect(host, username=usuario_ssh, password=senha_ssh)

        # mudança de usuário para 'dvopsusr'
        stdin, stdout, stderr = ssh.exec_command('sudo su - dvopsusr')

        # Aguarde um momento suficiente para a mudança de usuário
        # time.sleep(5)  # Ajuste conforme necessário

        print('Executando o comando para obter a porcentagem para o servidor', host)
        # Agora, execute o comando para obter a porcentagem
        comando_porcentagem = '/devops/DEXE/spacecontainer.sh Percent\nexit\n'
        stdin.write(comando_porcentagem)
        stdin.flush()

        # Leia a saída e imprima a porcentagem
        porcentagem = stdout.read().decode().strip()

        # Remova o símbolo '%' e quaisquer caracteres não numéricos
        porcentagem_valor = ''.join(c for c in porcentagem if c.isdigit() or c == '.')

        if porcentagem_valor:
            porcentagem_valor = float(porcentagem_valor)
            if porcentagem_valor > 80:
                simbolo = '⚠️'
            elif porcentagem_valor > 60:
                simbolo = '⚠️'  # Alterado para ⚠️ se a porcentagem for maior que 60%
            else:
                simbolo = '✅'
        else:
            porcentagem = 'Não disponível'
            simbolo = '✅'

        print(f'{simbolo} {host} - {porcentagem}')

        # Retorna a porcentagem e o símbolo correspondente
        return porcentagem, simbolo

    except paramiko.AuthenticationException as e:
        print('Erro de autenticação para o servidor', host + ':', str(e))
    except paramiko.SSHException as e:
        print('Erro SSH para o servidor', host + ':', str(e))

# Função para criar o arquivo com as porcentagens
def criar_arquivo_porcentagens(porcentagens, nome_arquivo):
    if os.path.exists(nome_arquivo):
        os.remove(nome_arquivo)
        print(f'Arquivo anterior existente {nome_arquivo} removido.')
        time.sleep(2)

    with open(nome_arquivo, "w", encoding='utf-8') as arquivo:
        
        # Adiciona o cabeçalho com a data atual
        data_atual = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        arquivo.write(f'Data: {data_atual}\n\n')
        
        arquivo.write('..:: Espaço disponível no Docker Minha Oi e BFF ::..\n\n')
        for servidor, porcentagem, simbolo in porcentagens:
            porcentagem = '\n'.join(line for line in porcentagem.split('\n') if not line.startswith('Last login'))
            linha = f'{simbolo} {servidor} - {porcentagem}\n'
            arquivo.write(linha)

# Servidores a serem consultados
servidores = ['DIGPX11A', 'DIGPX11B', 'DIGPX11C', 'DIGPX11D', 'DIGPX11E', 'POAPX08', 'POAPX09', 'POAPX20A', 'POAPX20B', 'POAPX20C']
print('Espaço disponivel no Docker Minha Oi e BFF')
usuario_ssh = input('Digite o nome de usuário SSH: ')
senha_ssh = getpass.getpass('Digite a senha SSH: ')

# Lista para armazenar as porcentagens de todos os servidores
porcentagens_servidores = []

for servidor in servidores:
    print(f'Processando o servidor: {servidor}')
    porcentagem, simbolo = conectar_e_executar_comandos(servidor, usuario_ssh, senha_ssh)
    porcentagens_servidores.append((servidor, porcentagem, simbolo))

# Nome do arquivo
nome_arquivo = 'Docker_Minha_Oi_BFF.txt'

# Criar o arquivo com as porcentagens
criar_arquivo_porcentagens(porcentagens_servidores, nome_arquivo)
print(f'Arquivo {nome_arquivo} novo criado com sucesso.')
time.sleep(3)
