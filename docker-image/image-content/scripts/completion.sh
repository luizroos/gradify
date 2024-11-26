_gradifyctl_completions() {
  local cur=${COMP_WORDS[COMP_CWORD]}
  local prev=${COMP_WORDS[COMP_CWORD-1]}

  # Primeiro nível de comandos principais
  local main_commands="gradle completion bash"

  # Subcomandos para 'gradle'
  local gradle_subcommands="create update demo-project"

  # Subcomandos para 'gradle update'
  local gradle_update_subcommands="keep-alive"

  # Subcomandos para 'gradle demo-project'
  local gradle_demo_project_subcommands="v1"

  # Primeira palavra após 'gradifyctl'
  if [[ ${COMP_CWORD} -eq 1 ]]; then
    COMPREPLY=( $(compgen -W "$main_commands" -- $cur) )
    return 0
  fi

  # Subcomandos para 'gradle'
  if [[ ${COMP_WORDS[1]} == "gradle" && ${COMP_CWORD} -eq 2 ]]; then
    COMPREPLY=( $(compgen -W "$gradle_subcommands" -- $cur) )
    return 0
  fi

  # Subcomandos para 'gradle update'
  if [[ ${COMP_WORDS[1]} == "gradle" && ${COMP_WORDS[2]} == "update" && ${COMP_CWORD} -eq 3 ]]; then
    COMPREPLY=( $(compgen -W "$gradle_update_subcommands" -- $cur) )
    return 0
  fi

  # Subcomandos para 'gradle demo-project'
  if [[ ${COMP_WORDS[1]} == "gradle" && ${COMP_WORDS[2]} == "demo-project" && ${COMP_CWORD} -eq 3 ]]; then
    COMPREPLY=( $(compgen -W "$gradle_demo_project_subcommands" -- $cur) )
    return 0
  fi  
}

# Ativa a função de autocompletar para 'gradifyctl'
complete -F _gradifyctl_completions gradifyctl
