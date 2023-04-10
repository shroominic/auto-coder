FROM ubuntu:latest

RUN apt-get update 
RUN apt-get install -y curl git wget unzip libgconf-2-4 gdb libstdc++6 libglu1-mesa fonts-droid-fallback python3
RUN apt-get clean

RUN git clone https://github.com/flutter/flutter.git /usr/local/flutter

ENV PATH="/usr/local/flutter/bin:/usr/local/flutter/bin/cache/dart-sdk/bin:${PATH}"

RUN flutter doctor
RUN flutter channel master
RUN flutter upgrade
RUN flutter config --enable-web

COPY . /frontend
WORKDIR /frontend

RUN flutter build web

EXPOSE 8080

CMD python3 -m http.server 8080 --directory build/web