#!/bin/bash
# Usage: ./run_scripts.sh
# This script will run all the matching scripts from script1 to script4 in sequence.
# and keep the output as a log file in the current directory for checking.
# It will also create a final fits catalogue in the catalogue directory.
logfile="run_scripts.log"
# Clear the log file if it exists
if [ -f "$logfile" ]; then
    rm "$logfile"
fi
# Run each script and redirect output to log files
# Ensure the scripts are executable
chmod +x script1_assigning script2_matching script3_cooking script4_wrapping
# Run the scripts and log their output
./script1_assigning > script1.log 2>&1
./script2_matching > script2.log 2>&1
./script3_cooking > script3.log 2>&1
./script4_wrapping > script4.log 2>&1
# Combine all logs into the main log file
cat script1.log script2.log script3.log script4.log > "$logfile"
# Clean up individual log files
rm script1.log script2.log script3.log script4.log
# clean up temporary files, if you want to check the intermediate files, you can comment the following line
rm -f fileterd*.fits group*.fits match1_*.fits mr*.fits temp_with*.fits filtered_* singleton_* # tmp_*

# Rename columns and export the final catalogue as a csv file using the simple python script
python make_cat.py 

echo "All scripts have been executed successfully. Check the log file: $logfile"
