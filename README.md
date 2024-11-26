# Any Project Management

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
echo "source <(gradifyctl completion | tr -d '\r')" >> ~/.bashrc
```

```bash
source ~/.bashrc
```

## Primeiro projeto

```bash
gradifyctl gradle demo-project v1 > project-config.yaml && gradifyctl gradle create spring-app && gradifyctl gradle update keep-alive
```

Depois, modifique o project-config.yaml a vontade