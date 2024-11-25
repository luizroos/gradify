_gpectl_completions() {
  local cur=${COMP_WORDS[COMP_CWORD]}
  local commands="bash create gradle-update completion"

  if [[ ${COMP_CWORD} -eq 1 ]]; then
    COMPREPLY=( $(compgen -W "$commands" -- $cur) )
    return 0
  fi

  if [[ "$cur" == "--"* ]]; then
    COMPREPLY=( $(compgen -W "--some-option --another-option" -- $cur) )
    return 0
  fi
}
complete -F _gpectl_completions gpectl
