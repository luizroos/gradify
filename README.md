# Gradle Project Engine

---

## Instalação

```bash
curl -Lo ./gpectl https://github.com/luizroos/gradle-project-engine/blob/main/client-tool/gpectl
```

```bash  
chmod +x ./gpectl
```

```bash  
export PATH="$(pwd):$PATH"
```

ou 

```bash
sudo mv ./gpectl /usr/local/bin/gpectl
```

## Habilitando auto-completion

```bash
echo "source <(gpectl completion | tr -d '\r')" >> ~/.bashrc
```

```bash
source ~/.bashrc
```