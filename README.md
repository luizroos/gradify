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
gradifyctl gradle project-config v1 > project-config.yaml
```

Então execute update para gerar e atualizar os arquivos gradle do projeto:
```bash
gradifyctl gradle update
```

Ou então, se quiser que a atualização seja feita automaticamente toda vez que vc altera o project-config.yaml:
```bash
gradifyctl gradle update keep-alive
```

Tudo junto:
```bash
gradifyctl gradle project-config v1 > project-config.yaml && gradifyctl gradle update keep-alive
```

## Alguns TODOs:

- Criar documentação do arquivo project-config.yaml.
- O update só atualia os arquivos do gradle, não remove nem adiciona novos modulos declarados no project-config.yaml, talvez vale fazer isso já tbm (adicionar).  --- esta parcialmente feito, precisa pensar numa forma de atualizar, para isso talvez tenha que trabalhar com arquivos anonimos e incluir um id no yaml
- Tirar a necessidade de tr -d '\r' no completion.
- Usar uma imagem menor (eu mudei para ubuntu pq queria rodar java, mas desisti).
- Achar uma ferramenta para identar os arquivos gerados.
- Permitir fazer push da imagem via comando automaticamente
- Permitir rodar gradifyctl apontando para imagem local sem alterar o script
- Permitir customizar a geração do project-config (incluir template e perguntas, talvez deixar o lance de perguntas mais generico)