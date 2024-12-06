# Use a imagem base Alpine
FROM alpine:3.20.3
#FROM alpine:3.18

# Atualiza os pacotes do sistema
RUN apk update 

# Instalar pacotes básicos essenciais
RUN apk add --no-cache \
    # Bash: Shell usado para scripts e comandos interativos
    bash \
    # Curl: http client
    curl \
    # Vim: editor de texto util caso precisamos entrar no container
    vim \
    # Coreutils: Conjunto de ferramentas essenciais para manipulação de arquivos e processos, como cp, ls, mv, etc.
    coreutils \
    # Inotify-tools: Ferramentas para monitoramento de alterações em arquivos e diretórios
    inotify-tools \
    # Shadow: Ferramenta que fornece funcionalidades para manipulação de usuários e senhas no sistema, permitindo a criação de usuários não-root
    shadow \
    # python
    python3 \
    py3-pip

# Baixar e instalar o gosu manualmente
RUN curl -L https://github.com/tianon/gosu/releases/download/1.17/gosu-amd64 -o /usr/local/bin/gosu && \
    chmod +x /usr/local/bin/gosu

# Diretorio base onde copiamos nosso código
ENV GRADIFY_DIR="/gradify"
RUN mkdir -p $GRADIFY_DIR

# Aplicação python
ENV PYTHONPATH="$GRADIFY_DIR/python-app"
ADD /python-app/src $PYTHONPATH
ADD /python-app/requirements.txt $PYTHONPATH/
RUN pip3 install --no-cache-dir --break-system-packages -r $PYTHONPATH/requirements.txt

# Tipos de ferramentas que lidamos
ENV GRADIFY_TOOLS_DIR=$GRADIFY_DIR/tools
ADD /tools $GRADIFY_TOOLS_DIR

# shell scripts
ENV GRADIFY_SHELL_SCRIPTS_DIR=$GRADIFY_DIR/sh-scripts
ADD /docker-image/sh-scripts $GRADIFY_SHELL_SCRIPTS_DIR
RUN find $GRADIFY_SHELL_SCRIPTS_DIR -type f -name "*.sh" -exec chmod +x {} \;

# Diretorio onde o volume projeto do host é montado
ENV PRJ_HOST_DIR="/project"

# Nome padrão do arquivo de configuração do projeto
ENV PRJ_CONFIG_FILENAME="project-config.yaml"

# O diretório do projeto deve ser o workdir
WORKDIR $PRJ_HOST_DIR

# Copiar o entrypoint e torná-lo executável
COPY /docker-image/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# informações do build
ARG BUILD_DATE
ENV BUILD_DATE=${BUILD_DATE}

ARG GRADIFY_VERSION=latest
ENV GRADIFY_VERSION=$GRADIFY_VERSION

# Definir o entrypoint
ENTRYPOINT ["/entrypoint.sh"]
