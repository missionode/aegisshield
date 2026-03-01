#!/bin/bash

# AegisShield Orchestrator v3.0
# Multi-Node Security Command & Control

APP_NAME="AegisShield"
PID_FILE="aegis.pid"
LOG_DIR="logs"
LOG_FILE="${LOG_DIR}/aegis.log"
DATASET_DIR="dataset"
WIKI_DIR="wiki"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# Dynamic Root (Parent of the script)
SHIELD_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Global Virtual Environment Context
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

setup_environment() {
    mkdir -p "$LOG_DIR" "$DATASET_DIR" "$WIKI_DIR"
    touch "$LOG_FILE"
    
    # Bootstrap Virtual Environment
    if [ ! -d "venv" ]; then
        echo -e "${YELLOW}Bootstrapping Python Virtual Environment...${NC}"
        python3 -m venv venv
        source venv/bin/activate
        pip install --upgrade pip
        if [ -f "requirements.txt" ]; then
            pip install -r requirements.txt
        fi
        echo -e "${GREEN}Virtual Environment Ready.${NC}"
    fi

    python3 node_manager.py init "$SHIELD_ROOT"
}

log_message() {
    local level="$1"
    local message="$2"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $message" >> "$LOG_FILE"
}

run_daemon() {
    log_message "INFO" "Starting AegisShield C2 at $SHIELD_ROOT"
    
    # 1. Start sub-daemons
    python3 hit_monitor.py >> "$LOG_FILE" 2>&1 &
    MONITOR_PID=$!
    echo "$MONITOR_PID" > "monitor.pid"

    bash ddos_shield.sh >> "$LOG_FILE" 2>&1 &
    DDOS_PID=$!
    echo "$DDOS_PID" > "ddos.pid"

    python3 ghost_ports.py >> "$LOG_FILE" 2>&1 &
    TRAP_PID=$!
    echo "$TRAP_PID" > "trap.pid"
    
    # Initial scan across all nodes
    run_all_nodes_analysis
    python3 slm_doctor.py >> "$LOG_FILE" 2>&1
    
    while true; do
        # Process Monitoring
        ps -p "$MONITOR_PID" >/dev/null || { python3 hit_monitor.py >> "$LOG_FILE" 2>&1 & MONITOR_PID=$!; echo "$MONITOR_PID" > "monitor.pid"; }
        ps -p "$DDOS_PID" >/dev/null || { bash ddos_shield.sh >> "$LOG_FILE" 2>&1 & DDOS_PID=$!; echo "$DDOS_PID" > "ddos.pid"; }
        ps -p "$TRAP_PID" >/dev/null || { python3 ghost_ports.py >> "$LOG_FILE" 2>&1 & TRAP_PID=$!; echo "$TRAP_PID" > "trap.pid"; }
        
        # 6-Hour Pulse Logic (handled by cron, but here for robustness)
        run_all_nodes_analysis
        python3 slm_doctor.py >> "$LOG_FILE" 2>&1
        
        # Periodic tasks
        ((count++))
        [ $((count % 50)) -eq 0 ] && python3 wiki_updater.py >> "$LOG_FILE" 2>&1
        [ $((count % 100)) -eq 0 ] && { python3 summary_generator.py >> "$LOG_FILE" 2>&1; python3 garbage_collector.py >> "$LOG_FILE" 2>&1; python3 slm_scavenger.py >> "$LOG_FILE" 2>&1; }
        
        sleep 3600 # Wait 1 hour in daemon loop (C2 interval)
    done
}

run_all_nodes_analysis() {
    NODES=$(python3 node_manager.py list)
    for node in $NODES; do
        if [[ "$node" == "/"* ]]; then # Ensure it's a path
            log_message "C2" "Performing scheduled scan on node: $node"
            python3 deception_planner.py "$node" >> "$LOG_FILE" 2>&1
            python3 breadcrumb_injector.py "$node" >> "$LOG_FILE" 2>&1
            python3 slm_engine.py "$node" >> "$LOG_FILE" 2>&1
        fi
    done
    python3 slm_av.py --scan >> "$LOG_FILE" 2>&1
    python3 fix_list_generator.py >> "$LOG_FILE" 2>&1
}

# Start the daemon in the background
start_shield() {
    if [ -f "$PID_FILE" ] && ps -p $(cat "$PID_FILE") >/dev/null 2>&1; then
        echo -e "${YELLOW}AegisShield is already running (PID: $(cat $PID_FILE)).${NC}"
        return
    fi
    setup_environment
    nohup bash "$0" --daemon-run >> "$LOG_FILE" 2>&1 &
    echo $! > "$PID_FILE"
    echo -e "${GREEN}AegisShield C2 Started.${NC}"
}

# Simulations
simulate_trap() {
    python3 deception_planner.py "$1"
}

simulate_breadcrumb() {
    python3 breadcrumb_injector.py "$1"
}

# Bootstrap everything for a complete start
bootstrap_all() {
    echo -e "${CYAN}--- AegisShield C2 Bootstrap Sequence ---${NC}"
    setup_environment
    if [ ! -f "$PID_FILE" ] || ! ps -p $(cat "$PID_FILE") > /dev/null 2>&1; then
        start_shield
        sleep 2
    fi
    touch logs/web_access.log logs/hits.log logs/consultant.log logs/summary.log logs/story.log
    
    echo -e "${YELLOW}C2 Multi-Node Background Warm-up...${NC}"
    (
        run_all_nodes_analysis
        python3 summary_generator.py >> "$LOG_FILE" 2>&1
    ) &
    
    echo -e "${GREEN}C2 Bootstrap initiated. All nodes registered for protection.${NC}"
    sleep 1
}

# Handle internal daemon execution
if [ "$1" == "--daemon-run" ]; then
    run_daemon
    exit 0
fi

# Entry point
case "$1" in
    start)
        start_shield
        ;;
    stop)
        [ -f "monitor.pid" ] && kill $(cat "monitor.pid") 2>/dev/null && rm "monitor.pid"
        [ -f "ddos.pid" ] && kill $(cat "ddos.pid") 2>/dev/null && rm "ddos.pid"
        [ -f "trap.pid" ] && kill $(cat "trap.pid") 2>/dev/null && rm "trap.pid"
        [ -f "$PID_FILE" ] && kill $(cat "$PID_FILE") 2>/dev/null && rm "$PID_FILE"
        echo -e "${RED}AegisShield C2 Stopped.${NC}"
        ;;
    status)
        if [ -f "$PID_FILE" ] && ps -p $(cat "$PID_FILE") >/dev/null 2>&1; then
            echo -e "${GREEN}AegisShield C2 is ACTIVE (PID: $(cat $PID_FILE))${NC}"
            echo "Protecting Nodes:"
            python3 node_manager.py list
        else echo -e "${RED}AegisShield is OFFLINE.${NC}"; fi
        ;;
    dashboard) bootstrap_all; ./dashboard.sh ;;
    add-node) python3 node_manager.py add "${@:2}" ;;
    run-analysis) run_all_nodes_analysis; echo -e "${GREEN}C2 Scan Complete.${NC}" ;;
    fix-list) python3 fix_list_generator.py ;;
    update-wiki) python3 wiki_updater.py ;;
    simulate-trap) simulate_trap "$2" ;;
    simulate-breadcrumb) simulate_breadcrumb ;;
    setup-cron) ./cron_setup.sh ;;
    garbage-collect) python3 garbage_collector.py ;;
    *) echo "Usage: $0 {start|stop|status|dashboard|add-node|run-analysis|fix-list|update-wiki|simulate-sql|simulate-trap|simulate-breadcrumb|setup-cron|garbage-collect}"; exit 1 ;;
esac
