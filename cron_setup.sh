#!/bin/bash

# AegisShield Cron Manager
# Automates persistence and periodic tasks at the system level.

SHIELD_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CRON_TEMP="aegis_cron_tmp"

echo -e "\033[0;36m--- AegisShield Cron Setup ---\033[0m"

# 1. Capture current crontab (to avoid overwriting user jobs)
crontab -l > "$CRON_TEMP" 2>/dev/null || touch "$CRON_TEMP"

# 2. Clean existing Aegis jobs to avoid duplicates
sed -i.bak '/aegisshield/d' "$CRON_TEMP" && rm "${CRON_TEMP}.bak"

# 3. Add New Robust Jobs
echo "# AegisShield Automation" >> "$CRON_TEMP"

# Watchdog: Ensure daemon is alive every 5 minutes
echo "*/5 * * * * cd $SHIELD_PATH && ./shield.sh watchdog >> logs/aegis.log 2>&1" >> "$CRON_TEMP"

# Persistence: Start on system boot
echo "@reboot cd $SHIELD_PATH && ./shield.sh start >> logs/aegis.log 2>&1" >> "$CRON_TEMP"

# Intelligence: Update Wiki from threat feeds every day at midnight
echo "0 0 * * * cd $SHIELD_PATH && ./shield.sh update-wiki >> logs/aegis.log 2>&1" >> "$CRON_TEMP"

# Continuous Security Pulse: Full Sync & Scan every 6 hours
echo "0 */6 * * * cd $SHIELD_PATH && ./shield.sh run-analysis >> logs/aegis.log 2>&1" >> "$CRON_TEMP"

# Reporting: Generate Daily Summary and Fix List at 9:00 AM
echo "0 9 * * * cd $SHIELD_PATH && $SHIELD_PATH/venv/bin/python3 summary_generator.py >> logs/summary.log 2>&1" >> "$CRON_TEMP"
echo "0 9 * * * cd $SHIELD_PATH && $SHIELD_PATH/venv/bin/python3 fix_list_generator.py >> logs/aegis.log 2>&1" >> "$CRON_TEMP"

# Remediation: Autonomous SLM Doctor runs periodically (Every 15 minutes)
echo "*/15 * * * * cd $SHIELD_PATH && $SHIELD_PATH/venv/bin/python3 slm_doctor.py >> logs/aegis.log 2>&1" >> "$CRON_TEMP"

# Maintenance: Run SLM Scavenger weekly on Sunday at 3:00 AM
echo "0 3 * * 0 cd $SHIELD_PATH && $SHIELD_PATH/venv/bin/python3 slm_scavenger.py >> logs/story.log 2>&1" >> "$CRON_TEMP"

# Anti-Virus: Daily AV Signature Updates (2:00 AM)
echo "0 2 * * * cd $SHIELD_PATH && $SHIELD_PATH/venv/bin/python3 slm_av.py --update-signatures >> logs/story.log 2>&1" >> "$CRON_TEMP"

# Anti-Virus: Periodic AV Scans (Every 3 hours)
echo "0 */3 * * * cd $SHIELD_PATH && $SHIELD_PATH/venv/bin/python3 slm_av.py --scan >> logs/story.log 2>&1" >> "$CRON_TEMP"

# 4. Install the new crontab
crontab "$CRON_TEMP"
rm "$CRON_TEMP"

echo -e "\033[0;32m✅ AegisShield CRON jobs successfully installed.\033[0m"
echo "The system will now self-heal, persist through reboots, and update intelligence automatically."
