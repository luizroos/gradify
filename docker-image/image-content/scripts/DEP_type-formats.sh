#!/bin/bash

# valida se um valor é do tipo certo (testar todos tipos)
validate_type() {
  local value="$1"
  local expected_type="$2"
  case "$expected_type" in
      boolean)
          if [[ "$value" == "true" || "$value" == "false" ]]; then
              return 0
          else
              return 1
          fi
          ;;
      integer)
          # Verifica se é um número inteiro
          if [[ "$value" =~ ^[+-]?[0-9]+$ ]]; then
              return 0
          else
              return 1
          fi
          ;;
      positive_integer)
          # Verifica se é um número inteiro positivo (exclui 0 e negativos)
          if [[ "$value" =~ ^[0-9]+$ && "$value" -gt 0 ]]; then
              return 0
          else
              return 1
          fi
          ;;
      decimal)
          # Verifica se é um número decimal (ponto como separador)
          if [[ "$value" =~ ^[+-]?[0-9]*[.]?[0-9]+$ ]]; then
              return 0
          else
              return 1
          fi
          ;;
      string)
          # Qualquer valor é válido como string
          return 0
          ;;
      string_no_spaces)
          if [[ "$value" =~ ^[^[:space:]]+$ ]]; then
              return 0
          else
              return 1
          fi
          ;;
      string_alphanumeric)
          # Verifica se é alfanumérico e não começa com número
          if [[ "$value" =~ ^[a-zA-Z][a-zA-Z0-9]*$ ]]; then
              return 0
          else
              return 1
          fi
          ;;
      *)
          return 2
          ;;
  esac
}