# Use a imagem base Alpine
FROM alpine:3.18

# Atualizar o repositório e instalar pacotes básicos
RUN apk update && apk add --no-cache \
    bash \
    curl \
    vim \
    coreutils \
    sudo \
    jq \
    inotify-tools \
    python3 \
    py3-pip \
    shadow  # Instala o pacote shadow para permitir a criação de usuário

# para que o find suporte a opção printf
RUN apk add --no-cache findutils

# Baixar e instalar o gosu manualmente
RUN curl -L https://github.com/tianon/gosu/releases/download/1.14/gosu-amd64 -o /usr/local/bin/gosu && \
    chmod +x /usr/local/bin/gosu

# Instalar pacotes Python via pip
RUN pip3 install \
    jinja2-cli \
    jinja2 \
    pyyaml \
    questionary \
    termcolor

# Baixar e configurar o yq
RUN curl -L https://github.com/mikefarah/yq/releases/download/v4.18.1/yq_linux_amd64 -o /usr/bin/yq && \
    chmod +x /usr/bin/yq

# Diretorio para onde copiamos nossas coisas
ENV GRADIFY_DIR="/gradify"
RUN mkdir -p $GRADIFY_DIR

# Copiar o conteúdo da imagem para o diretório gradify
ADD image-content $GRADIFY_DIR

# Local onde estao os scripts python
ENV PYTHONPATH="$GRADIFY_DIR/python"

# Torna executáveis todos os scripts
RUN find $GRADIFY_DIR/scripts -type f -name "*.sh" -exec chmod +x {} \;

# Diretorio onde o volume projeto do host é montado
ENV PRJ_HOST_DIR="/project"

# Nome padrão do arquivo de configuração do projeto
ENV PRJ_CONFIG_FILENAME="project-config.yaml"

# O diretório do projeto deve ser o workdir
WORKDIR $PRJ_HOST_DIR

# Copiar o entrypoint e torná-lo executável
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Definir o entrypoint
ENTRYPOINT ["/entrypoint.sh"]
