# gradle-project-engine

curl -Lo ./gpectl https://xxxx
chmod +x ./gpectl

sudo mv ./gpectl /usr/local/bin/gpectl
ou
export PATH="$(pwd):$PATH"

// completion
echo "source <(gpectl completion | tr -d '\r')" >> ~/.bashrc
