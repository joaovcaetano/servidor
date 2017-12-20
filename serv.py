#!/usr/bin/env python2.7.12
#-*- coding: utf-8 -*-
import socket
import thread
import os
import sys
import requests
def contentType(arq):
    tipo_arq = arq.split(".")
    if tipo_arq[-1] == "html":
        return "text/HTML"
    elif tipo_arq[-1] == "txt":
        return "text/txt"
    elif tipo_arq[-1] == "jpg":
        return "image/jpg"
    elif tipo_arq[-1] == "png":
        return "image/png"
    elif tipo_arq[-1] == "gif":
        return "image/gif"
    elif tipo_arq[-1] == "ico":
        return "image/ico"
    elif tipo_arq[-1] == "css":
        return "text/css"
    elif tipo_arq[-1] == "pdf":
        return "text/pdf"
        
HOST = ''              # Endereco IP do Servidor
try:
    pasta = sys.argv[1]
    porta = int(sys.argv[2])
except:
    print "Falta argumentos para o servidor"
    sys.exit(0)
serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
origem = (HOST, porta)
serv_socket.bind(origem)
serv_socket.listen(1) #servidor escutando na porta 7777

while True:
    con, client = serv_socket.accept()
    pid = os.fork()
    if pid == 0:
        serv_socket.close()
        msg = con.recv(1048576)
        if not msg: break
        msg = msg.split(" ")
        get = msg[0]
        arquivo_ou_pasta = msg[1]
        if(get == 'GET'):
            try:
                if msg[1] == '/':
                    arquivo = msg[1].split("/")
                    arquivo_caminho = arquivo[len(arquivo)-1]
                    file=open(os.path.realpath(os.path.dirname(__file__))+arquivo_caminho,'r')
                    flag =file.read()
                    response_headers = {
                    'Content-Type': 'html; encoding=utf8',
                    'Content-Length': len(flag),
                    'Connection': 'close',
                    }
                    response_headers_raw = ''.join('%s: %s\n' % (i, j) for i, j in response_headers.iteritems())
                    response_proto = '\nHTTP/1.1'
                    response_status = 200
                    response_status_text = ' OK'
                    con.send('%s %s %s'%(response_proto,response_status,response_status_text)+'\n'+response_headers_raw+'\r\n'+flag)
                else:
                    file=open(os.path.realpath(os.path.dirname(__file__))+msg[1],'r')
                    flag =file.read()
                    response_headers = {
                    'Content-Type': 'html; encoding=utf8',
                    'Content-Length': len(flag),
                    'Connection': 'close',
                    }
                    response_headers_raw = ''.join('%s: %s\n' % (i, j) for i, j in response_headers.iteritems())
                    response_proto = '\nHTTP/1.1'
                    response_status = 200
                    response_status_text = ' OK'
                    con.send('%s %s %s'%(response_proto,response_status,response_status_text)+'\n'+response_headers_raw+'\r\n'+flag)
            except IOError:
                ###Erro de não conseguir abrir arquivo
                response_proto = '\nHTTP/1.1'
                response_status = 404
                response_status_text = ' File not Found'
                file=open(os.path.realpath(os.path.dirname(__file__))+'/404ERROR.html','r')
                flag =file.read()
                response_headers = {
                'Content-Type': 'html; encoding=utf8',
                'Content-Length': len(flag),
                'Connection': 'close',
                }
                response_headers_raw = ''.join('%s: %s\n' % (i, j) for i, j in response_headers.iteritems())
                con.send('%s %s %s' % (response_proto, response_status,response_status_text)+'\n'+response_headers_raw+'\r\n'+flag)
        else:
            con.send('Comando GET nao solicitado\n')
            con.close()
            sys.exit(0)
    else:
        con.close()
serv_socket.close()
con.close()