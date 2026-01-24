#!/usr/bin/env bash
# Script to run continuous local Pokémon Showdown battles
# Combines training data between battles

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Paths
SHOWDOWN_DIR="../pokemon-showdown"
BOT_DIR="$(pwd)"
SESSION_NAME="showdown_battle"
COMBINED_CSV="./data/battle_records_combined.csv"

# Check dependencies
if ! command -v tmux &> /dev/null; then
    echo -e "${RED}Error: tmux is not installed.${NC}"
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo -e "${RED}Error: node is not installed.${NC}"
    exit 1
fi

if [ ! -d "$SHOWDOWN_DIR" ]; then
    echo -e "${RED}Error: Pokémon Showdown server not found at $SHOWDOWN_DIR${NC}"
    exit 1
fi

if [ ! -f "./data/login.txt" ] || [ ! -f "./data/login2.txt" ]; then
    echo -e "${RED}Error: Credential files not found${NC}"
    exit 1
fi

# If not inside tmux, restart script inside tmux
if [ -z "$TMUX" ]; then
    echo -e "${GREEN}Starting tmux session...${NC}"
    exec tmux new-session -s "$SESSION_NAME" "$0" "$@"
fi

# Use current tmux session
SESSION_NAME="$(tmux display-message -p '#S')"

# Cleanup function - kill only the windows we created
cleanup() {
    echo ""
    echo -e "${YELLOW}Stopping server and bots...${NC}"
    tmux kill-window -t server 2>/dev/null || true
    tmux kill-window -t bots 2>/dev/null || true
    echo -e "${GREEN}Training session ended. Total battles: ${battle_count:-0}${NC}"
    exit 0
}

# Trap Ctrl+C and other signals to ensure cleanup
trap cleanup SIGINT SIGTERM

BOT1_USERNAME=$(head -1 "./data/login.txt")
BOT2_USERNAME=$(head -1 "./data/login2.txt")

echo -e "${BLUE}╔════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Continuous Pokémon Showdown Training Mode   ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "Bot 1: ${YELLOW}$BOT1_USERNAME${NC} (accepts challenges)"
echo -e "Bot 2: ${YELLOW}$BOT2_USERNAME${NC} (sends challenges)"
echo ""

# Function to combine CSV files
combine_csvs() {
    local bot1_csv="./data/battle_records_${BOT1_USERNAME}.csv"
    local bot2_csv="./data/battle_records_${BOT2_USERNAME}.csv"

    echo -e "${GREEN}→ Combining training data...${NC}"

    # If combined file exists, start with it
    if [ -f "$COMBINED_CSV" ]; then
        cp "$COMBINED_CSV" "${COMBINED_CSV}.tmp"
    else
        # Create empty file with header
        echo "turn,action,self_hp,opp_hp,outspeed_prob,is_status_move,exp_damage_done,exp_damage_received,predicted_npw_score,actual_npw_score" > "${COMBINED_CSV}.tmp"
    fi

    # Append new data from bot CSVs (skip headers)
    if [ -f "$bot1_csv" ]; then
        tail -n +2 "$bot1_csv" >> "${COMBINED_CSV}.tmp"
        echo -e "  Added $(tail -n +2 "$bot1_csv" | wc -l | xargs) records from $BOT1_USERNAME"
        rm "$bot1_csv"
    fi

    if [ -f "$bot2_csv" ]; then
        tail -n +2 "$bot2_csv" >> "${COMBINED_CSV}.tmp"
        echo -e "  Added $(tail -n +2 "$bot2_csv" | wc -l | xargs) records from $BOT2_USERNAME"
        rm "$bot2_csv"
    fi

    mv "${COMBINED_CSV}.tmp" "$COMBINED_CSV"

    local total_records=$(($(wc -l < "$COMBINED_CSV") - 1))
    echo -e "  ${GREEN}Total training records: $total_records${NC}"
}

# Function to wait for battle completion
wait_for_battle() {
    echo -e "${YELLOW}→ Waiting for battle to complete...${NC}"

    local max_wait=600  # 10 minutes max
    local elapsed=0
    local check_interval=5
    local last_size=0
    local stall_count=0

    while [ $elapsed -lt $max_wait ]; do
        sleep $check_interval
        elapsed=$((elapsed + check_interval))

        # Check if battle record files exist (battle completed)
        if [ -f "./data/battle_records_${BOT1_USERNAME}.csv" ] || [ -f "./data/battle_records_${BOT2_USERNAME}.csv" ]; then
            # Wait a bit more to ensure files are fully written
            sleep 2
            echo -e "${GREEN}✓ Battle completed!${NC}"
            return 0
        fi

        # Show progress every 15 seconds
        if [ $((elapsed % 15)) -eq 0 ]; then
            echo -e "  Still battling... (${elapsed}s elapsed)"
        fi
    done

    echo -e "${YELLOW}⚠ Battle timeout reached${NC}"
    return 1
}

# Start server window
echo -e "${GREEN}→ Starting Pokémon Showdown server...${NC}"
tmux new-window -n "server" -c "$SHOWDOWN_DIR"
tmux send-keys -t server "node pokemon-showdown start" C-m
echo -e "  Waiting for server to start..."
sleep 8

battle_count=0

# Main battle loop
while true; do
    battle_count=$((battle_count + 1))

    echo ""
    echo -e "${BLUE}════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  Battle #${battle_count}${NC}"
    echo -e "${BLUE}════════════════════════════════════════════════${NC}"

    # Combine training data from previous battles
    if [ $battle_count -gt 1 ]; then
        combine_csvs
    fi

    # Clean up any leftover CSV files from previous battles
    rm -f "./data/battle_records_${BOT1_USERNAME}.csv"
    rm -f "./data/battle_records_${BOT2_USERNAME}.csv"

    # Kill bots window if it exists, create new one
    tmux kill-window -t bots 2>/dev/null || true

    # Start bots in a new window
    echo -e "${GREEN}→ Starting bots...${NC}"
    tmux new-window -n "bots" -c "$BOT_DIR"

    # Bot 1 (accepts challenges)
    tmux send-keys -t bots "uv run python start_warrior.py --local -c data/login.txt" C-m

    sleep 3

    # Bot 2 (sends challenges) - split the bots window
    tmux split-window -h -t bots -c "$BOT_DIR"
    tmux send-keys -t bots "uv run python start_warrior.py --local -c data/login2.txt --challenge $BOT1_USERNAME" C-m

    # Wait for battle to complete
    if ! wait_for_battle; then
        echo -e "${RED}✗ Battle timeout or error${NC}"
        break
    fi

    # Stop the bots (kill the bots window, keep server running)
    echo -e "${GREEN}→ Stopping bots...${NC}"
    tmux kill-window -t bots 2>/dev/null || true

    echo -e "${GREEN}✓ Battle #${battle_count} complete${NC}"

    # Short pause between battles
    sleep 2
done

# Run cleanup on normal exit too
cleanup
