_gradifyctl_completions() {
  local cur=${COMP_WORDS[COMP_CWORD]}
  local prev=${COMP_WORDS[COMP_CWORD-1]}

  # Primeiro nível de comandos principais
  local main_commands="gradle completion bash"

  # Primeira palavra após 'gradifyctl'
  if [[ ${COMP_CWORD} -eq 1 ]]; then
    COMPREPLY=( $(compgen -W "$main_commands" -- $cur) )
    return 0
  fi

  # Subcomandos para 'gradle'
  local gradle_subcommands="update project-config"
  if [[ ${COMP_WORDS[1]} == "gradle" && ${COMP_CWORD} -eq 2 ]]; then
    COMPREPLY=( $(compgen -W "$gradle_subcommands" -- $cur) )
    return 0
  fi

  # Subcomandos para 'gradle update'
  local gradle_update_subcommands="keep-alive"
  if [[ ${COMP_WORDS[1]} == "gradle" && ${COMP_WORDS[2]} == "update" && ${COMP_CWORD} -eq 3 ]]; then
    COMPREPLY=( $(compgen -W "$gradle_update_subcommands" -- $cur) )
    return 0
  fi

  # Subcomandos para 'gradle project-config'
  local gradle_project_config_subcommands="v1"
  if [[ ${COMP_WORDS[1]} == "gradle" && ${COMP_WORDS[2]} == "project-config" && ${COMP_CWORD} -eq 3 ]]; then
    COMPREPLY=( $(compgen -W "$gradle_project_config_subcommands" -- $cur) )
    return 0
  fi  
}

# Ativa a função de autocompletar para 'gradifyctl'
complete -F _gradifyctl_completions gradifyctl
