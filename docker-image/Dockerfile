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
    shadow    

# Baixar e instalar o gosu manualmente
RUN curl -L https://github.com/tianon/gosu/releases/download/1.14/gosu-amd64 -o /usr/local/bin/gosu && \
    chmod +x /usr/local/bin/gosu

# Só se for executar via shell (já que mudou tudo para python, não precisa)
#RUN apk add --no-cache \
# JQ: Ferramenta para processar JSON de forma simples e poderosa (TODO ver se precisa ainda)
#jq \
# Findutils: Conjunto de ferramentas para pesquisa e manipulação de arquivos no sistema de arquivos, incluindo o 'find' com a opção 'printf' (TODO ver se precisa)
#findutils \
#RUN curl -L https://github.com/mikefarah/yq/releases/download/v4.18.1/yq_linux_amd64 -o /usr/bin/yq && \
#    chmod +x /usr/bin/yq

# Instala Python e as dependencias do python que usamos
RUN apk add --no-cache \
    python3 \
    py3-pip     \
    py3-jinja2  \
    py3-yaml  \
    py3-termcolor 

# priorizar a instalacao via apk, deixar para instalar assim só o que não der para ser via apk
RUN pip3 install --break-system-packages \
    questionary \
    cerberus


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

# informações do build
ARG BUILD_DATE
ENV BUILD_DATE=${BUILD_DATE}

ARG GRADIFY_VERSION=latest
ENV GRADIFY_VERSION=$GRADIFY_VERSION

# Definir o entrypoint
ENTRYPOINT ["/entrypoint.sh"]
