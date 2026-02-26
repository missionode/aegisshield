#!/bin/bash

# AegisShield Orchestrator
# A background security daemon for automated protection.

# Configuration
APP_NAME="AegisShield"
PID_FILE="aegis.pid"
LOG_DIR="logs"
LOG_FILE="${LOG_DIR}/aegis.log"
DATASET_DIR="dataset"
WIKI_DIR="wiki"

# Colors for CLI feedback
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Identify the root directory to protect
SHIELD_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Function to ensure environment is ready
setup_environment() {
    mkdir -p "$LOG_DIR"
    mkdir -p "$DATASET_DIR"
    mkdir -p "$WIKI_DIR"
    touch "$LOG_FILE"
}

# Function to log activity
log_message() {
    local level="$1"
    local message="$2"
    local timestamp=$(date "+%Y-%m-%d %H:%M:%S")
    echo "[$timestamp] [$level] $message" >> "$LOG_FILE"
}

# Main execution loop (The Daemon logic)
run_daemon() {
    log_message "INFO" "Starting $APP_NAME daemon at $SHIELD_ROOT"
    
    # Start the Hit Monitor in the background
    python3 hit_monitor.py >> "$LOG_FILE" 2>&1 &
    MONITOR_PID=$!
    echo "$MONITOR_PID" > "monitor.pid"
    
    # Initial sync and analysis
    python3 digital_twin.py sync
    python3 slm_engine.py
    
    while true; do
        # Monitor Hit Monitor
        if ! ps -p "$MONITOR_PID" > /dev/null; then
            log_message "WARN" "Hit Monitor died. Restarting..."
            python3 hit_monitor.py >> "$LOG_FILE" 2>&1 &
            MONITOR_PID=$!
            echo "$MONITOR_PID" > "monitor.pid"
        fi
        
        # Periodically run PAS Analysis
        python3 slm_engine.py
        
        # Simulate Daily Summary (every 100 loops for demo)
        ((count++))
        if [ $((count % 100)) -eq 0 ]; then
            python3 summary_generator.py >> "$LOG_FILE" 2>&1
        fi
        
        sleep 30
    done
}

# Handle internal daemon execution
if [ "$1" == "--daemon-run" ]; then
    run_daemon
    exit 0
fi

# Start the daemon
start_shield() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null; then
            echo -e "${YELLOW}AegisShield is already running (PID: $PID).${NC}"
            return
        else
            echo -e "${YELLOW}Stale PID file found. Cleaning up...${NC}"
            rm "$PID_FILE"
        fi
    fi

    setup_environment
    
    # Run in background and capture PID
    nohup bash "$0" --daemon-run >> "$LOG_FILE" 2>&1 &
    NEW_PID=$!
    echo "$NEW_PID" > "$PID_FILE"
    
    log_message "INFO" "$APP_NAME started successfully (PID: $NEW_PID)"
    echo -e "${GREEN}AegisShield started successfully at $SHIELD_ROOT (PID: $NEW_PID)${NC}"
}

# Status of the daemon
status_shield() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null; then
            echo -e "${GREEN}AegisShield is running (PID: $PID)${NC}"
            echo "Protecting Root: $SHIELD_ROOT"
            tail -n 5 "$LOG_FILE"
        else
            echo -e "${RED}AegisShield is not running (Stale PID file).${NC}"
        fi
    else
        echo -e "${RED}AegisShield is not running.${NC}"
    fi
}

# Stop the daemon
stop_shield() {
    if [ -f "monitor.pid" ]; then
        M_PID=$(cat "monitor.pid")
        kill "$M_PID" 2>/dev/null
        rm "monitor.pid"
    fi

    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null; then
            # Kill process group to ensure all sub-daemons (like hit_monitor) die
            # But we'll just kill the main PID for now
            kill "$PID"
            rm "$PID_FILE"
            log_message "INFO" "$APP_NAME stopped."
            echo -e "${RED}AegisShield stopped.${NC}"
        else
            echo -e "${YELLOW}AegisShield is not running, but a PID file exists. Cleaning up...${NC}"
            rm "$PID_FILE"
        fi
    else
        echo -e "${YELLOW}AegisShield is not running.${NC}"
    fi
}

# Live Hit Monitor CLI
monitor_hits() {
    if [ ! -f "logs/hits.log" ]; then
        echo -e "${YELLOW}No hits logged yet.${NC}"
        touch "logs/hits.log"
    fi
    echo -e "${GREEN}--- AegisShield Live Hit Monitor ---${NC}"
    echo -e "${YELLOW}Press Ctrl+C to exit${NC}"
    tail -f "logs/hits.log" | while read line; do
        # Colorize intent
        if [[ $line == *"MALICIOUS"* ]]; then
            echo -e "${RED}$line${NC}"
        elif [[ $line == *"BOT"* ]]; then
            echo -e "${YELLOW}$line${NC}"
        else
            echo -e "$line"
        fi
    done
}

# Simulate a hit for testing
simulate_hit() {
    local ip="192.168.1.$((RANDOM % 255))"
    local paths=("/" "/index.html" "/api/data" "/admin" "/.env" "/blog/post-1")
    local path=${paths[$RANDOM % ${#paths[@]}]}
    local agents=("Mozilla/5.0" "Googlebot/2.1" "curl/7.68.0" "Nmap/7.80")
    local agent=${agents[$RANDOM % ${#agents[@]}]}
    
    python3 -c "import hit_monitor; hit_monitor.log_hit('$ip', 'GET', '$path', '$agent', hit_monitor.analyze_intent('$path', '$agent'))"
    echo -e "${GREEN}Simulated hit from $ip to $path${NC}"
}

# Digital Twin Commands
sync_twin() {
    python3 digital_twin.py sync
    echo -e "${GREEN}Digital Twin synchronized.${NC}"
}

run_simulation() {
    local attack="${1:-REMOVAL_ATTACK}"
    python3 digital_twin.py attack "$attack"
    echo -e "${YELLOW}Simulation complete. Triggering SLM analysis...${NC}"
    python3 slm_engine.py
}

# Consultant / AI Insights
view_consultant() {
    if [ ! -f "logs/consultant.log" ]; then
        echo -e "${YELLOW}AI Consultant has no insights yet.${NC}"
        return
    fi
    echo -e "${GREEN}--- AegisShield AI Consultant Log ---${NC}"
    cat "logs/consultant.log"
}

view_summary() {
    if [ ! -f "logs/summary.log" ]; then
        python3 summary_generator.py
    else
        cat "logs/summary.log"
    fi
}

# Self Protection / Watchdog
check_persistence() {
    if [ ! -f "$PID_FILE" ]; then
        echo -e "${RED}AegisShield is not running. Restarting...${NC}"
        start_shield
    else
        PID=$(cat "$PID_FILE")
        if ! ps -p "$PID" > /dev/null; then
            echo -e "${RED}AegisShield PID exists but process is dead. Restarting...${NC}"
            start_shield
        else
            echo -e "${GREEN}AegisShield is healthy (PID: $PID)${NC}"
        fi
    fi
}

# Entry point CLI commands
case "$1" in
    start)
        start_shield
        ;;
    stop)
        stop_shield
        ;;
    status)
        status_shield
        ;;
    monitor)
        monitor_hits
        ;;
    simulate-hit)
        simulate_hit
        ;;
    sync-twin)
        sync_twin
        ;;
    run-simulation)
        run_simulation "$2"
        ;;
    consultant)
        view_consultant
        ;;
    run-analysis)
        python3 slm_engine.py
        echo -e "${GREEN}PAS Analysis complete.${NC}"
        ;;
    summary)
        view_summary
        ;;
    watchdog)
        check_persistence
        ;;
    *)
        echo "Usage: $0 {start|stop|status|monitor|simulate-hit|sync-twin|run-simulation|consultant|run-analysis|summary|watchdog}"
        exit 1
        ;;
esac


