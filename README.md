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
* Abrir o terminal na pasta do projeto e executar: vagrant up
** O vagrant está configurado para provisionar uma máquina Ubuntu Server 14.04 LTS
* Para acessar a maquina, executar: vagrant ssh
* A pasta do projeto está em /vagrant/app

# Instalação
* Abrir o terminal na pasta do projeto e executar: ./install.sh
** O script irá instalar os pacotes necessários para os testes, Docker, Docker-Compose e irá fazer o build das imagens necessárias para a aplicação
** As imagens são: nginx, redis, api python

# Execução
* Abrir o terminal na pasta do projeto e executar: ./run.sh
** O script irá iniciar os containers
* O nginx está configurado para utilizar a porta 80, portanto, ao fazer alguma requisição à algum endpoint, usar a mesma porta do ngnix

# Testes
* Abrir o terminar na pasta do projeto e navegar até backend/app
* Executar: python test_api.py


