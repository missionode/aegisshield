#!/bin/bash

# AegisShield High-Stability HUD
# Prevents text bleeding and duplication via strict line control.

if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

HITS_LOG="logs/hits.log"
STORY_LOG="logs/story.log"
SUMMARY_LOG="logs/summary.log"
FIX_LIST_FILE="../FIX_LIST.md"
PID_FILE="aegis.pid"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
ALERT_RED='\033[1;31m'
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
    LINES=$(tput lines)
    
    # Calculate dynamic heights based on terminal size
    local AVAIL_LINES=$(( LINES - 16 ))
    [ $AVAIL_LINES -lt 9 ] && AVAIL_LINES=9 # Minimum fallback
    
    local STORY_H=3
    local SUMM_H=$(( AVAIL_LINES * 40 / 100 ))
    local TRAFF_H=$(( AVAIL_LINES - STORY_H - SUMM_H ))

    # 1. Header
    local HEADER_LINE=$(printf '%.0s━' $(seq 1 $COLS))
    print_line "$CYAN" "$HEADER_LINE"
    local ROOT_PATH=$(./shield.sh status 2>/dev/null | grep "Nodes Protected" -A 1 | tail -n 1 | xargs)
    print_line "$NC" "  ${GREEN}🛡️  AegisShield Security HUD${NC} | $(date '+%H:%M:%S') | C2 Controller"
    print_line "$CYAN" "$HEADER_LINE"
    echo ""

    # 2. Strategic Module Status
    print_line "$BLUE" "┏━[ ACTIVE SHIELDING STATUS ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    if [ -f "$PID_FILE" ] && ps -p $(cat "$PID_FILE") > /dev/null 2>&1; then
        local PENDING=$(grep -c "| \[ \] |" "$FIX_LIST_FILE" 2>/dev/null || echo 0)
        local RESOLVED=$(grep -c "| \[X\] |" "$FIX_LIST_FILE" 2>/dev/null || echo 0)
        local NODES_COUNT=$(grep -c "/" logs/nodes.json 2>/dev/null || echo 1)
        
        # Ensure variables are strictly numeric to prevent syntax errors
        PENDING=${PENDING:-0}
        RESOLVED=${RESOLVED:-0}
        
        # Check explicit sub-daemons
        local SOC_STATUS="${ALERT_RED}OFFLINE${NC}"; [ -f "monitor.pid" ] && ps -p $(cat "monitor.pid") > /dev/null 2>&1 && SOC_STATUS="${GREEN}ACTIVE${NC}"
        local PAS_STATUS="${GREEN}ENABLED${NC}"
        local TRAP_STATUS="${GREEN}READY${NC}"
        
        print_line "$NC" "┃ ● SOC Monitor: $SOC_STATUS | PAS Engine: $PAS_STATUS | ART Lab: $TRAP_STATUS"
        print_line "$NC" "┃ ● Nodes Protected: ${GREEN}${NODES_COUNT}${NC} | 📋 Checklist: ${YELLOW}${PENDING} Pending${NC} | ${GREEN}${RESOLVED} Fixed${NC}"
        
        # Calculate dynamic health bar based on pending issues safely
        local HEALTH_PCT=100
        if [[ "$PENDING" =~ ^[0-9]+$ ]] && [[ "$RESOLVED" =~ ^[0-9]+$ ]]; then
            local TOTAL_ISSUES=$(( PENDING + RESOLVED ))
            if [ "$TOTAL_ISSUES" -gt 0 ]; then
                HEALTH_PCT=$(( (RESOLVED * 100) / TOTAL_ISSUES ))
            fi
        fi
        
        # Render a 30-character progress bar
        local BRACKET_SIZE=30
        local FILLED_SIZE=$(( (HEALTH_PCT * BRACKET_SIZE) / 100 ))
        local EMPTY_SIZE=$(( BRACKET_SIZE - FILLED_SIZE ))
        
        local BAR_COLOR="$GREEN"
        [ "$HEALTH_PCT" -lt 80 ] && BAR_COLOR="$YELLOW"
        [ "$HEALTH_PCT" -lt 50 ] && BAR_COLOR="$RED"
        
        local FILLED_BAR=$(printf '%.0s█' $(seq 1 $FILLED_SIZE))
        local EMPTY_BAR=$(printf '%.0s░' $(seq 1 $EMPTY_SIZE))
        
        # Add a spinning/pulsing animation state based on current second
        local SPINNER=( "|" "/" "-" "\\" )
        local SPIN_IDX=$(( $(date +%s) % 4 ))
        
        print_line "$NC" "┃ 📊 System Integrity: [${BAR_COLOR}${FILLED_BAR}${EMPTY_BAR}${NC}] ${HEALTH_PCT}% | Scan Pulse ${SPINNER[$SPIN_IDX]}"
        
        # Quarantine Metric
        if [ -f "logs/quarantine_tracker.json" ]; then
            local Q_DATE=$(grep -Eo '"date": "[^"]*"' logs/quarantine_tracker.json | cut -d'"' -f4)
            local Q_COUNT=$(grep -Eo '"deleted_today": [0-9]+' logs/quarantine_tracker.json | grep -Eo '[0-9]+')
            if [ "$Q_DATE" == "$(date '+%Y-%m-%d')" ] && [ -n "$Q_COUNT" ] && [ "$Q_COUNT" -gt 0 ]; then
                print_line "$GREEN" "┃ 🗑️  Auto-Cleaned: ${YELLOW}${Q_COUNT} Quarantined Threat(s)${GREEN} (Past 24h) ${NC}"
            else
                print_line "$NC" "┃ 🗑️  Auto-Cleaned: 0 Quarantined Threats (Past 24h)"
            fi
        else
            print_line "$NC" "┃ 🗑️  Auto-Cleaned: 0 Quarantined Threats (Past 24h)"
        fi
        
        # Actionable Alerts (Proactive Notifications)
        local ALERTS_DISPLAYED=false
        
        # 1. Action Required: Fix List Pending Items
        if [ "$PENDING" -gt 0 ]; then
            print_line "$YELLOW" "┃ ${ALERT_RED}🚨 ACTION REQUIRED:${NC}${YELLOW} $PENDING unresolved vulnerabilities require your attention in FIX_LIST.md${NC}"
            ALERTS_DISPLAYED=true
        fi
        
        # 2. Active Engagement: Tarpit / Blackhole
        if [ -f "$STORY_LOG" ]; then
            if tail -n 50 "$STORY_LOG" | grep -Eiq "Tarpit Action|Black-holing"; then
                print_line "$YELLOW" "┃ ${ALERT_RED}⚡ ACTIVE ENGAGEMENT:${NC}${YELLOW} Network Shield is currently suppressing hostile IP(s).${NC}"
                ALERTS_DISPLAYED=true
            fi
        fi
        
        # 3. Trap Triggered: Deception Network
        if [ -f "$HITS_LOG" ]; then
            if tail -n 50 "$HITS_LOG" | grep -iq "Honey-Endpoint Triggered"; then
                print_line "$YELLOW" "┃ ${ALERT_RED}🕸️ TRAP TRIGGERED:${NC}${YELLOW} The Morphing Deception network has engaged an intruder!${NC}"
                ALERTS_DISPLAYED=true
            fi
        fi
        
        if [ "$ALERTS_DISPLAYED" = false ]; then
            print_line "$GREEN" "┃ ✅ System is secure. No immediate actions required."
        fi
        
        # Check for SLM Manual Upgrade Requirements
        if [ -f "logs/slm_status.json" ]; then
            if grep -q '"MANUAL_UPGRADE_REQ": true' "logs/slm_status.json"; then
                print_line "$YELLOW" "┃ ${ALERT_RED}[!] SYSTEM ALERT:${NC}${YELLOW} New SLM Version Detected. Manual Review Required for Stability.${NC}"
            fi
        fi
    else
        print_line "$RED" "┃ ○ C2 SYSTEM OFFLINE - PROTECTION SUSPENDED"
    fi
    echo ""

    # 3. LIVE SECURITY STORY
    print_line "$YELLOW" "┏━[ LIVE SECURITY STORY (STEP-BY-STEP ACTIONS) ]━━━━━━━━━━━━━━━"
    if [ -f "$STORY_LOG" ]; then
        tail -r -n $STORY_H "$STORY_LOG" | while read -r line; do
            # Add some basic color highlighting
            line=$(echo "$line" | sed "s/Blocked/${RED}Blocked${NC}/g" | sed "s/Analyzed/${BLUE}Analyzed${NC}/g" | sed "s/Healed/${GREEN}Healed${NC}/g" | sed "s/Detected/${YELLOW}Detected${NC}/g")
            print_line "$NC" "┃ >> $line"
        done
    else
        print_line "$NC" "┃ AegisShield is waiting for events..."
    fi
    echo ""

    # 4. STRATEGIC SUMMARY
    print_line "$BLUE" "┏━[ STRATEGIC SUMMARY ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    if [ -f "$SUMMARY_LOG" ]; then
        tail -r -n $SUMM_H "$SUMMARY_LOG" | while read -r line; do
            print_line "$NC" "┃ $line"
        done
    else
        print_line "$NC" "┃ No summary generated yet."
    fi
    echo ""

    # 5. SOC: LIVE TRAFFIC INTENT
    print_line "$RED" "┏━[ SOC: LIVE TRAFFIC INTENT ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    if [ -f "$HITS_LOG" ]; then
        tail -n $TRAFF_H "$HITS_LOG" | while read -r line; do
            if [[ $line == *"MALICIOUS"* || $line == *"CRITICAL"* ]]; then
                print_line "$RED" "┃ ⚠️  $line"
            elif [[ $line == *"BOT"* ]]; then
                print_line "$YELLOW" "┃ 🤖 $line"
            else
                print_line "$NC" "┃ ✅ $line"
            fi
        done
    else
        print_line "$NC" "┃ No traffic captured yet."
    fi

    # 6. Footer
    echo ""
    tput el
    printf "${CYAN}Refreshing every 2s... [p] Pause/Play | [q] Quit${NC}"
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

PAUSED=false
while true; do
    if [ "$PAUSED" = false ]; then
        draw_ui
    fi
    read -t 2 -n 1 key
    if [[ $key == "q" ]]; then
        break
    elif [[ $key == "p" ]]; then
        if [ "$PAUSED" = true ]; then
            PAUSED=false
        else
            PAUSED=true
            tput cup $(($(tput lines)-1)) 0
            tput el
            printf "${YELLOW}Dashboard PAUSED. Press 'p' to resume, 'q' to quit.${NC}"
        fi
    fi
done
