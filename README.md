# url-shortener

# Aplicação
API Restful para um encurtador de URLs

# Arquitetura
O projeto foi desenvolvido com as seguintes tecnologias:
* Python 2.7
* Flask
* Redis
* Nginx
* Docker
* Docker-Compose

# Vagrant (Pular esta etapa caso já tenha uma máquina provisionada)
Caso queira provisionar uma máquina localmente:
* Instalar o Vagrant: https://www.vagrantup.com/downloads.html
* O vagrant está configurado para provisionar uma máquina do tipo Ubuntu Server 14.04 LTS
* Abrir o terminal na pasta do projeto e executar: vagrant up
* Para acessar a maquina, executar: vagrant ssh
* A pasta do projeto está em /vagrant/app

# Instalação
* Abrir o terminal na pasta do projeto e executar: ./install.sh
* O script irá instalar os pacotes necessários para os testes, Docker, Docker-Compose e irá fazer o build das imagens necessárias para a aplicação
* As imagens são: nginx, redis, api python

# Execução
* Abrir o terminal na pasta do projeto e executar: ./run.sh
* O script irá iniciar os containers
* O nginx está configurado para utilizar a porta 80, portanto, ao fazer alguma requisição à algum endpoint, usar a mesma porta do ngnix
* Inicialmente irão subir 2 containers que atendem as requisições da api, são eles: url-shortener-backend-1 e url-shortener-backend-2. Caso queira provisionar mais containers, alterar os arquivos docker-compose.yaml e ngix.conf. Os nós que representam a api são identificados pelo nome de node1, node2.. node[n].

![alt text](https://github.com/mobbyd1/url-shortener/blob/master/docs/url-shortener-compose.png)

# Testes
* Abrir o terminar na pasta do projeto e navegar até backend/app
* Executar: python test_api.py


