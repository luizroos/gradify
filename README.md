# Gradify

---

Ferramenta minha para manter templates para projetos que crio, bem como, uma forma mais automática de atualizar as ferramentas de build (no caso, o gradle apenas hehe).

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

Atualize project-config.yaml e então execute update para atualizar os arquivos gradle do projeto:
```bash
gradifyctl gradle update
```

Ou então, se quiser que a atualização seja feita automaticamente:
```bash
gradifyctl gradle update keep-alive
```

Tudo junto:
```bash
gradifyctl gradle demo-project v1 > project-config.yaml && gradifyctl gradle create spring-app && gradifyctl gradle update keep-alive
```

## Alguns TODO:

- Criar documentação do arquivo project-config.yaml.
- O update só atualia os arquivos do gradle, não remove nem adiciona novos modulos declarados no project-config.yaml, talvez vale fazer isso já tbm (adicionar).
- Tirar a necessidade de tr -d '\r' no completion.
- Usar uma imagem menor (eu mudei para ubuntu pq queria rodar java, mas desisti).
- Achar uma ferramenta para identar os arquivos gerados.
- Melhorar o create * (os parametros ali ficaram toscos), talvez até começar a dar uma app mais completa já pronta.
- Permitir fazer push da imagem via comando automaticamente
- Permitir rodar gradifyctl apontando para imagem local sem alterar o script