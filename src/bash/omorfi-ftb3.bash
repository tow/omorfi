#!/bin/bash

source $(dirname $0)/omorfi.bash
args=$@
dict=analyse

function print_version() {
    echo "omorfi-ftb3 0.3 (Using omorfi bash API ${omorfiapi})"
    echo "Copyright (c) 2018 Tommi A Pirinen"
    echo "Licence GPLv3: GNU GPL version 3 <http://gnu.org/licenses/gpl.html>"
    echo "This is free software: you are free to change and redistribute it."
    echo "There is NO WARRANTY, to the extent permitted by law."

}

function print_usage() {
    echo "Usage: $0 [OPTION] [FILENAME...]"
}

function print_help() {
    echo "Analyse Finnish into FTB3.1 (CONLL-X) format using omorfi"
    echo
    echo "  -h, --help        Print this help dialog"
    echo "  -V, --version     Print version info"
    echo "  -v, --verbose     Print verbosely while processing"
    echo "  -X, --all-words   Use large-coverage dictionary"
    echo
    echo "If no FILENAMEs are given, input is read from standard input."
}

if test x$1 == x-h -o x$1 == x--help ; then
    print_usage
    print_help
    exit 0
elif test x$1 == x-V -o x$1 == x--version ; then
    print_version
    exit 0
elif test x$1 == x-v -o x$1 == x--verbose ; then
    verbose=verbose
    shift 1
elif test x$1 == x-X -o x$2 == x--all-words ; then
    dict=describe
    shift 1
fi
cat $@ | omorfi_ftb3 $dict
