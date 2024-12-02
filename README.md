# Gradify

---

Minha ferramenta para manter templates para os projetos que crio, bem como, uma forma mais automática de atualizar as ferramentas de build (no caso, o gradle apenas hehe).

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

## TODOs:

- Criar documentação do arquivo project-config.yaml.
- Criar validação para o arquivo project-config.yaml (tem uns TODOs disso, criei uma classe gradle_project_config_file.py para começar a pensar nisso)
- Tirar a necessidade de tr -d '\r' no completion.
- Achar uma ferramenta para identar os arquivos gerados.
- Permitir customizar a geração do project-config (incluir template e perguntas, talvez deixar o lance de perguntas mais generico).
- Permitir informar um diretório local com mais opcões de templates para os módulos
- Pensar se vale a pena incluir a opcao de aplicar template para o projeto (ao invés do módulo do projeto, eu quero ainda atulizar o gradle, mas não da para toda vez ficar perguntando as opções de templates)
- Revisar o código de renderização
- Testes
