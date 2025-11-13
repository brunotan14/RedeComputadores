# Importa o módulo socket
from socket import *
import sys  # Necessário para encerrar o programa

# Cria o socket TCP (orientado à conexão)
serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepara o socket do servidor
serverPort = 8080  # Pode escolher outra porta se 8080 estiver em uso
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print('Ready to serve...')

# Estabelece a conexão (apenas uma vez)
connectionSocket, addr = serverSocket.accept()

try:
    # Recebe a mensagem do cliente (requisição HTTP)
    message = connectionSocket.recv(1024).decode()
    filename = message.split()[1]
    f = open(filename[1:])
    outputdata = f.read()

    # Envia a linha de status do cabeçalho HTTP
    connectionSocket.send('HTTP/1.1 200 OK\r\n\r\n'.encode())

    # Envia o conteúdo do arquivo ao cliente
    for i in range(0, len(outputdata)):
        connectionSocket.send(outputdata[i].encode())
    connectionSocket.send("\r\n".encode())

    # Fecha a conexão com o cliente
    connectionSocket.close()

except IOError:
    # Envia mensagem de erro 404 se o arquivo não for encontrado
    connectionSocket.send('HTTP/1.1 404 Not Found\r\n\r\n'.encode())
    connectionSocket.send('<html><body><h1>404 Not Found</h1></body></html>\r\n'.encode())

    # Fecha o socket do cliente
    connectionSocket.close()

# Fecha o socket principal e encerra o programa (após uma requisição)
serverSocket.close()
sys.exit()
