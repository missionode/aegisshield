#!/bin/bash
cd /Users/syamnath/Desktop/Projects/Plantdoctor/aegisshield
source venv/bin/activate
echo "Running SLM Doctor..."
python3 slm_doctor.py &
PID=$!
echo "Watching logs (PID: $PID)..."
tail -f logs/story.log &
TAIL_PID=$!
wait $PID
echo "SLM Doctor complete."
kill $TAIL_PID
echo "\n--- First 20 lines of FIX_LIST.md ---"
head -n 20 ../FIX_LIST.md
