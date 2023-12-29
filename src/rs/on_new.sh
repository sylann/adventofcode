cat << EOF >> src/rs/Cargo.toml

[[bin]]
name = "$1_$2"
path = "year_$1/day_$2.rs" 

EOF
