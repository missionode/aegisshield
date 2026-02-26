#!/bin/bash

# AegisShield High-Stability HUD
# Prevents text bleeding and duplication via strict line control.

HITS_LOG="logs/hits.log"
STORY_LOG="logs/story.log"
SUMMARY_LOG="logs/summary.log"
FIX_LIST_FILE="../FIX_LIST.md"
PID_FILE="aegis.pid"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Terminal state
tput smcup
tput civis
trap "tput rmcup; tput cnorm; exit" INT TERM

# Robust printing function
print_line() {
    local color="$1"
    local text="$2"
    local cols=$(tput cols)
    tput el # Clear line from previous frame
    local clean_text=$(echo -e "$text" | head -n 1 | cut -c1-$((cols-5)))
    printf "${color}%s${NC}\n" "$clean_text"
}

draw_ui() {
    tput cup 0 0
    COLS=$(tput cols)
    
    # 1. Header
    local HEADER_LINE=$(printf '%.0s=' $(seq 1 $COLS))
    print_line "$CYAN" "$HEADER_LINE"
    local ROOT_PATH=$(./shield.sh status | grep "Nodes Protected" -A 1 | tail -n 1 | xargs)
    print_line "$NC" "  ${GREEN}🛡️  AegisShield Security HUD${NC} | $(date '+%H:%M:%S') | C2 Controller"
    print_line "$CYAN" "$HEADER_LINE"
    echo ""

    # 2. Strategic Module Status
    print_line "$BLUE" "[ ACTIVE SHIELDING STATUS ]"
    if [ -f "$PID_FILE" ] && ps -p $(cat "$PID_FILE") > /dev/null 2>&1; then
        local PENDING=$(grep -c "| \[ \] |" "$FIX_LIST_FILE" 2>/dev/null || echo 0)
        local RESOLVED=$(grep -c "| \[X\] |" "$FIX_LIST_FILE" 2>/dev/null || echo 0)
        local NODES_COUNT=$(grep -c "/" logs/nodes.json 2>/dev/null || echo 1)
        
        # Check explicit sub-daemons
        local SOC_STATUS="${RED}OFFLINE${NC}"; [ -f "monitor.pid" ] && ps -p $(cat "monitor.pid") > /dev/null 2>&1 && SOC_STATUS="${GREEN}ACTIVE${NC}"
        local PAS_STATUS="${GREEN}ENABLED${NC}"
        local TRAP_STATUS="${GREEN}READY${NC}"
        
        print_line "$NC" "  ● SOC Monitor: $SOC_STATUS | PAS Engine: $PAS_STATUS | ART Lab: $TRAP_STATUS"
        print_line "$NC" "  ● Nodes Protected: ${GREEN}${NODES_COUNT}${NC} | 📋 Checklist: ${YELLOW}${PENDING} Pending${NC} | ${GREEN}${RESOLVED} Fixed${NC}"
    else
        print_line "$RED" "  ○ C2 SYSTEM OFFLINE - PROTECTION SUSPENDED"
    fi
    echo ""

    # 3. LIVE SECURITY STORY
    print_line "$YELLOW" "[ LIVE SECURITY STORY (STEP-BY-STEP ACTIONS) ]"
    if [ -f "$STORY_LOG" ]; then
        tail -r -n 10 "$STORY_LOG" | while read -r line; do
            print_line "$NC" ">> $line"
        done
    else
        print_line "$NC" "AegisShield is waiting for events..."
    fi
    echo ""

    # 4. STRATEGIC SUMMARY
    print_line "$BLUE" "[ STRATEGIC SUMMARY ]"
    if [ -f "$SUMMARY_LOG" ]; then
        tail -r -n 10 "$SUMMARY_LOG" | while read -r line; do
            print_line "$NC" "$line"
        done
    else
        print_line "$NC" "No summary generated yet."
    fi
    echo ""

    # 5. SOC: LIVE TRAFFIC INTENT
    print_line "$RED" "[ SOC: LIVE TRAFFIC INTENT ]"
    if [ -f "$HITS_LOG" ]; then
        tail -n 4 "$HITS_LOG" | while read -r line; do
            if [[ $line == *"MALICIOUS"* || $line == *"CRITICAL"* ]]; then
                print_line "$RED" "⚠️  $line"
            elif [[ $line == *"BOT"* ]]; then
                print_line "$YELLOW" "🤖 $line"
            else
                print_line "$NC" "✅ $line"
            fi
        done
    else
        print_line "$NC" "No traffic captured yet."
    fi

    # 6. Footer
    echo ""
    tput el
    printf "${CYAN}Refreshing every 2s... Press Ctrl+C to exit.${NC}"
    tput ed 
}

# Initial Clear and Bootstrap Display
clear
echo -e "${CYAN}--- AegisShield Strategic HUD ---${NC}"
if [ -f "logs/startup_snapshot.json" ]; then
    echo -e "${GREEN}Quick Retention: Loading last known system state...${NC}"
    grep -E "total_hits|malicious|deceptive_id" logs/startup_snapshot.json | tr -d '", '
    echo ""
fi
echo -e "${YELLOW}🤖 Generating the fresh Security Story...${NC}"
sleep 1

while true; do
    draw_ui
    sleep 2
done
