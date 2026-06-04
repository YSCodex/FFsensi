#!/usr/bin/env bash
set -e

echo "========================================="
echo "  YS SENSI ENGINE AUTO SETUP"
echo "  Owner: @ysyuvrajyt"
echo "========================================="

echo "[*] Updating packages..."
pkg update -y && pkg upgrade -y

echo "[*] Installing Python and Git..."
pkg install python git -y

echo "[*] Granting storage permissions..."
termux-setup-storage

echo "[*] Starting Sensi Engine..."
python3 main.py