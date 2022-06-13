#### TFTP

Implementação bastante simplória do que seriam um servidor e um cliente para transferência de arquivos, utilizando o protocolo UDP na porta 6969.

1. O servidor ficará, enquanto o programa estiver em execução, escutando na porta 6969/UDP; 
2. O cliente inicia a conexão, na porta 6969/UDP, informando qual arquivo deseja baixar;
3. O servidor envia, primeiramente, o tamanho do arquivo;
4. O cliente realizará iterações enquanto o que já tiver sido baixado for inferior ao tamanho total do arquivo;
5. O servidor enviará, sempre que possível o arquivo em blocos de 512 bytes;
6. Após receber todo o arquivo, o cliente fecha o socket.
