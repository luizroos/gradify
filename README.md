# Gradify

---

## Instalação

```bash
curl -Lo ./gradifyctl https://github.com/luizroos/gradle-project-engine/blob/main/client-tool/gradifyctl
```

```bash  
chmod +x ./gradifyctl
```

```bash  
export PATH="$(pwd):$PATH"
```

ou 

```bash
sudo mv ./gradifyctl /usr/local/bin/gradifyctl
```

## Habilitando auto-completion

```bash
echo "source <(gradifyctl completion bash | tr -d '\r')" >> ~/.bashrc
```

```bash
source ~/.bashrc
```

## Primeiro projeto

Em uma pasta vazia, gere um arquivo de exemplo de configuração de um projeto:

```bash
gradifyctl gradle demo-project v1 > project-config.yaml
```

Crie a estrutura de diretórios da aplicação (spring-app vai gerar umas classes de main para cada app):

```bash
gradifyctl gradle create spring-app
```

Atualize project-config.yaml, mantendo um listener para atualizar os arquivos do projeto:

```bash
gradifyctl gradle update keep-alive
```

Tudo junto:

```bash
gradifyctl gradle demo-project v1 > project-config.yaml && gradifyctl gradle create spring-app && gradifyctl gradle update keep-alive
```