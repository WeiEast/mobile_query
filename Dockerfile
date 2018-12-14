FROM lim1942/selenium
ENV LANG C.UTF-8
ENV TZ=Asia/Shanghai

WORKDIR /usr/src/app
COPY . .
