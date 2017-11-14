FROM nginx:latest
MAINTAINER Ruhan "mobbyd1@gmail.com"
COPY /nginx/config/nginx.conf /etc/nginx/nginx.conf
EXPOSE 80 443
ENTRYPOINT ["nginx"]
# Parametros extras para o entrypoint
CMD ["-g", "daemon off;"]
