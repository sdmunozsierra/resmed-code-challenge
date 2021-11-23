#!/bin/bash
# Create a virtual environment, install dependencies, run tests.

# default location: root/venv
# script location run example: root/scripts/run.sh -v Venv -r my-requirements.txt
# script install location: root/Venv

# run and filter by key:
# ./run.sh -u

# DESC: Parameter parser
# ARGS: $@ (optional): Arguments provided to the script
# OUTS: Variables indicating command-line parameters and options
function parse_params() {
    local param
    while [[ $# -gt 0 ]]; do
        param="$1"
        shift
        case $param in
            -v | --venv)
	    	# Sets install location for virtual environment
		venv_folder=true
		setting_venv_folder="${1-}"
                ;;
            -r | --requirements)
	    	# Sets requirements pip file
		requirements_file=true
		setting_requirements_file="${1-}"
                ;;
            -t | --test-directory)
	    	# Tests a Test directory
		test_directory=true
		setting_test_directory="${1-}"
                ;;
            -u | --urls)
	    	# List of targets
		urls=true
		setting_urls="${1-}"
                ;;
            -x | --post)
		post_data=true
		setting_post_data="${1-}"
                ;;
            -cr | --chronological-reverse)
		chronological=true
		reverse=true
                ;;
            -c | --chronological)
		chronological=true
                ;;
            -f | --filter)
		filter=true
		setting_filter_key="${1-}"
                ;;
            -d | --data)
		filter_data=true
		setting_filter_data="${1-}"
		;;
            -l | --locale)
		locale=true
		locale_filter="${1-}"
                ;;
        #     -h | --help)
        #         script_usage
        #         exit 0
        #         ;;
            *)
	    	# Debug:
	    	echo "Invalid parameter was provided: $param"
                ;;
        esac
    done
}

# DESC: Initializes the script with useful variables
# ARGS: None
# OUTS: None
function script_init(){
    readonly orig_cwd="$PWD"  # current run directory
    readonly script_params="$*"
    readonly script_path="${BASH_SOURCE[1]}"  # full path
    script_dir="$(dirname "$script_path")"  # dir path
    script_name="$(basename "$script_path")"  # file name

    readonly script_dir script_name
    readonly parent="${orig_cwd%/*}"

    # Important to always set as we use it in the exit handler
    # shellcheck disable=SC2155
    readonly ta_none="$(tput sgr0 2> /dev/null || true)" 

    # DEBUG:
    echo "Script settings: "
    echo "orig_cwd = $orig_cwd"
    echo "script_params = $script_params"
    echo "script_path = $script_path"
    echo "script_dir = $script_dir "
    echo "script_name = $script_name"
    echo "ta_none = $ta_none"
}

# DESC: Sets the virtual environment
# ARGS: $@ (optional): Arguments to change the venv folder
# OUTS: Activated python virtual evironment
function set_venv() {
    if [[ -n ${venv_folder-} ]]; then
	pushd . > /dev/null
	cd ../
	local loc param
	param=${setting_venv_folder}
	# defaults to venv folder. replaces spaces for slashes.
	if [[ -n ${param-}  ]]; then loc="/${param}" && loc="${loc// /-}"; else loc="/venv"; fi
	loc="${parent}${loc}"
	echo "Setting Venv folder..."
	echo "venv_folder = ${loc}"
	python3 -m venv ${loc}
	# add to gitignore
	cat "$( echo ${loc} )" >> .gitignore
	source ${loc}/bin/activate 
	popd > /dev/null
    fi
}

# DESC: Sets requirements.txt
# ARGS: $@ (optional): Arguments to change the requirements.txt file
# OUTS: None
function set_requirements() {
    if [[ -n ${requirements_file-}  ]]; then 
	pushd . > /dev/null
	cd ../
	local loc param
	param=${setting_requirements_file}
	# defaults to requirements.txt file. replaces spaces for slashes.
	if [[ -n ${param-}  ]]; then loc="/${param}" && loc="${loc// /_}"; else loc="/requirements.txt"; fi
	loc="${parent}${loc}"
	echo "Setting requirements file..."
	echo "requirements_file = ${loc}"
	pip install -r ${loc}
	popd > /dev/null
    fi
}

# Test the program using pytest
function test_app() {
    if [[ -n ${test_directory-}  ]]; then 
	pushd . > /dev/null
	cd ../ 
	local loc param
	param=${setting_test_directory}
	# defaults to tests folder
	if [[ -n ${param-}  ]]; then loc="/${param}"; else loc="/tests"; fi
	loc="${parent}${loc}"
	echo "Will run tests in directory..."
	echo "test_directory = ${loc}"
	# TODO:  replace by args_parse: run_app.py --tests 
        for i in ${loc}/test_*.py; do python ${i}; done
	echo "Done running tests."
	popd > /dev/null
    fi
}

function _set_url() {

    local default param1 cmd
    default="https://ancient-wood-1161.getsandbox.com:443/results" 
    cmd="--urls"

    if [[ -n ${urls-}  ]]; then 
    	param1=${setting_urls-}
	if [[ -n ${param1-} ]]; then cmd="${cmd} ${param1}"; else cmd="${cmd} ${default}"; fi
    else
	cmd="${cmd} ${default}"
    fi
    echo $cmd

}

function _set_post(){

    local param1 cmd
    cmd="--post"

    if [[ -n ${post_data-}  ]]; then 
    	param1=${setting_post_data-}
	if [[ -n ${param1-} ]]; then cmd="${cmd} ${param1}"; fi
    else
	cmd=""
    fi
    echo $cmd

}

function _do_post(){

    # --urls --post
    my_url=$(_set_url)
    my_post=$(_set_post)
    cmd="${parent}/app/api_service.py ${my_url} ${my_post}"
    RESPONSE_DATA=$( python ${cmd} ) 
    echo $RESPONSE_DATA
}

function post() {
    if [[ -n ${urls-} ]]; then
        _do_post
    fi
}

function _set_filter() {

    local default cmd param1
    default="['f1Results']"
    cmd="--filter"

    if [[ -n ${filter-}  ]]; then 
	param1=${setting_filter_data-}
	if [[ -n ${param1-} ]]; then cmd="${cmd} ${param1} "; else cmd="${cmd} ${default}"; fi
    else
	cmd="${cmd} ${default}"
    fi 
    echo $cmd

}

function _set_response_data() {

    local cmd param1 
    cmd="--data"

    if [[ -n ${RESPONSE_DATA-} ]]; then
	cmd="${cmd} $RESPONSE_DATA"
    elif [[ -n ${post_data-}  ]]; then 
	param1=${setting_post_data-}
	if [[ -n ${param1-} ]]; then cmd="${cmd} ${param1} "; fi
    else
	cmd=""
    fi 
    echo $cmd

}

function _do_filter() {

    # --data --filter
    my_data=$(_set_response_data)
    my_filter=$(_set_filter)
    cmd="${parent}/app/filter_data.py ${my_data} ${my_filter}"
    #cmd="${parent}/app/filter_data.py -d ${RESPONSE_DATA} -f ['f1Results']"
    echo "$cmd"
    echo "my_data: $my_data"
    echo "my_filter: $my_filter"
    echo "cmd: $cmd"
    FILTERED=$( python ${cmd} ) 
    echo "FILTERED: $FILTERED"
}

function filter() {

    if [[ -n ${filter-}  ]]; then 
	_do_filter
    fi 

}

function main(){
    script_init "$@"
    parse_params "$@"
    set_venv
    set_requirements
    post
    filter
    test_app
}

# Invoke main with args if not sourced
if ! (return 0 2> /dev/null); then
    main "$@"
fi

# vim: syntax=sh cc=80 tw=79 ts=4 sw=4 sts=4 et sr