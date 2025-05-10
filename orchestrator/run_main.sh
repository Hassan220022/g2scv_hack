#!/usr/bin/env bash
# run_main.sh — wrapper to launch main.py with predefined inputs

# Predefined inputs
linkedin_url="https://www.linkedin.com/in/mikawi"
github_user="hassan220022"
old_cv_path="placeholder"    # <-- replace this with your actual CV path if/when needed

# Ensure main.py is in the same directory (or adjust path accordingly)
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$script_dir"

# Run main.py and pipe in the inputs
python3 main.py <<EOF
$linkedin_url
$github_user
$old_cv_path
EOF
