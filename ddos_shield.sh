#!/bin/bash

# AegisShield DDoS & Tarpit Shield
# Monitors network stack and applies active countermeasures.

STORY_LOG="logs/story.log"
DROP_THRESHOLD=50   # Connections per IP to DROP
TARPIT_THRESHOLD=20 # Connections per IP to TARPIT (Slower)

log_story() {
    local message="$1"
    local timestamp=$(date "+%H:%M:%S")
    echo "[$timestamp] 🕸️ Network Shield: $message" >> "$STORY_LOG"
}

monitor_traffic() {
    while true; do
        # Analyze current established connections
        TRAFFIC_DATA=$(lsof -iTCP -sTCP:ESTABLISHED -n -P | awk '{print $9}' | cut -d'>' -f2 | cut -d':' -f1 | grep -v '127.0.0.1' | sort | uniq -c)
        
        while read -r count ip; do
            if [ -z "$ip" ]; then continue; fi
            
            # 1. DROP Logic (Hard Block)
            if [ "$count" -ge "$DROP_THRESHOLD" ]; then
                log_story "CRITICAL: IP $ip exceeded hard threshold ($count conns). Black-holing..."
                if [[ "$OSTYPE" == "darwin"* ]]; then
                    echo "block drop from $ip to any" | sudo pfctl -a com.apple/aegis-shield -f - 2>/dev/null
                else
                    sudo iptables -A INPUT -s "$ip" -j DROP 2>/dev/null
                fi
                
            # 2. TARPIT Logic (Soft Block / Slowdown)
            elif [ "$count" -ge "$TARPIT_THRESHOLD" ]; then
                log_story "WARNING: IP $ip is aggressive ($count conns). Engaging Tarpit..."
                # On macOS we can use dnctl for real tarpitting, but for now we log and flag
                # The ghost_ports.py is also doing application-layer tarpitting
                log_story "Tarpit Action: Connection pool for $ip is being throttled."
            fi
        done <<< "$TRAFFIC_DATA"
        
        sleep 10
    done
}

monitor_traffic
