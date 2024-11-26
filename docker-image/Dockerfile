# Use a imagem base Ubuntu
FROM ubuntu:22.04

# Instalar dependências necessárias (curl, jq, bash, yq)
RUN apt-get update && apt-get install -y \
    curl \
    jq \
    bash \
    vim \
    inotify-tools \
    python3 \
    python3-pip \
    && curl -L https://github.com/mikefarah/yq/releases/download/v4.18.1/yq_linux_amd64 -o /usr/bin/yq \
    && chmod +x /usr/bin/yq \
    && rm -rf /var/lib/apt/lists/*

# jinja2 serve para parsear templates, usamos ele para substituir variáveis nos arquivos
#RUN pip install jinja-cli
RUN pip install jinja2-cli pyyaml

# diretorio para onde copiamos nossas coisas
ENV GRADIFY_DIR="/gradify"
RUN mkdir -p GRADIFY_DIR
ADD image-content $GRADIFY_DIR

# Torna executáveis todos os scripts
RUN find $GRADIFY_DIR/scripts -type f -name "*.sh" -exec chmod +x {} \;

# diretorio onde o volume projeto do host é montado
ENV PRJ_HOST_DIR="/project"

# nome padrao do arqivo de configuracao do projeto
ENV PRJ_CONFIG_FILENAME="project-config.yaml"

# diretorio do projeto deve ser o workdir
WORKDIR $PRJ_HOST_DIR

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
