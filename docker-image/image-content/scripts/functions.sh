#!/bin/bash

# funcoes de log
log_debug() {
    log "DEBUG" "$1"
}

log_info() {
    log "INFO" "$1"
}

log_warn() {
    log "WARN" "$1"
}

log_error() {
    log "ERROR" "$1"
}

log() {
    local level="$1"
    local message="$2"
    echo "$(date +"%Y-%m-%d %H:%M:%S.%3N") [$level] $message"
}
