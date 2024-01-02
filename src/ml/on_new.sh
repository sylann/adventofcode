# NOTE: modules is required to isolate each day
# NOTE: public_name is optional but missing it emits a warning

cat << EOF >> "src/ml/year_$1/dune"

(executable
 (name day_$2)
 (public_name day_$2)
 (modules day_$2)
 (libraries utils))
EOF

dune build --root src/ml
echo "added 'day_$2' to src/ml/year_$1/dune"
