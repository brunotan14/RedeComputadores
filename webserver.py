# Importa o módulo socket
from socket import *
import sys  # Necessário para encerrar o programa

# Cria o socket TCP (orientado à conexão)
serverSocket = socket(AF_INET, SOCK_STREAM) #SOCK_STREAM → indica que o socket vai usar o protocolo TCP (orientado à conexão).

# Prepara o socket do servidor/ configuração do socket do servidor
serverPort = 8080  # Pode ser alterada se a porta 80 estiver ocupada
serverSocket.bind(('', serverPort)) #Abre todas as interfaces de rede disponíveis na máquina na porta especificada.
serverSocket.listen(1) # coloca o socket em modo de escuta e permite 1 conexão pendente.

while True:
    # Estabelece a conexão
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept() #O método accept() bloqueia a execução até que um cliente (ex: navegador) se conecte.

    try:
        # Recebe a mensagem do cliente (requisição HTTP)
        message = connectionSocket.recv(1024).decode()  #recebe até 1024 bytes da requisição HTTP do cliente e decodifica/converte para string.
        filename = message.split()[1]
        f = open(filename[1:]) # remove a barra inicial '/' do nome do arquivo
        outputdata = f.read() # le o conteudo do arquivo

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

serverSocket.close() # Fecha o socket do servidor
sys.exit()  # Encerra o programa

# Resumo do funcionamento do programa:

#Cria um socket TCP e fica à escuta.

#Aceita uma conexão do navegador.

#Lê o pedido HTTP e tenta abrir o ficheiro pedido.

#3Se o ficheiro existir → devolve com HTTP 200 OK.

#Se não existir → devolve HTTP 404 Not Found.

#Fecha a conexão e termina o programa.