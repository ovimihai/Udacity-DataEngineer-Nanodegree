

# airflow initdb

cfg.parser () {
    fixed_file=$(cat $1 | sed 's/ = /=/g')  # fix ' = ' to be '='
    IFS=$'\n' && ini=( $fixed_file )              # convert to line-array
    ini=( ${ini[*]//;*/} )                   # remove comments
    ini=( ${ini[*]/#[/\}$'\n'cfg.section.} ) # set section prefix
    ini=( ${ini[*]/%]/ \(} )                 # convert text2function (1)
    ini=( ${ini[*]/=/=\( } )                 # convert item to array
    ini=( ${ini[*]/%/ \)} )                  # close array parenthesis
    ini=( ${ini[*]/%\( \)/\(\) \{} )         # convert text2function (2)
    ini=( ${ini[*]/%\} \)/\}} )              # remove extra parenthesis
    ini[0]=''                                # remove first element
    ini[${#ini[*]} + 1]='}'                  # add the last brace
    eval "$(echo "${ini[*]}")"               # eval the result
}



cfg.parser dwh.cfg

cfg.section.CLUSTER

#airflow connections --add --conn_id 'redshift' --conn_uri 'postgress://airflow:airflow@postgress:5432/dend'
airflow connections --add \
    --conn_id 'redshift' \
    --conn_type 'postgres' \
    --conn_host ${host} \
    --conn_schema ${db_name} \
    --conn_login ${db_user} \
    --conn_password ${db_password} \
    --conn_port ${db_port}

cfg.section.AWS

airflow connections --add \
    --conn_id 'aws_credentials' \
    --conn_type 'aws' \
    --conn_login ${key} \
    --conn_password ${secret}