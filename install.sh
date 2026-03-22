pkg update -y && pkg upgrade -y
pkg install python -y
pip install flask
pkg install termux-api
pkg install openssh
pkg install curl
pkg install jq
echo "[*]finished installing run by typing python Haxx.py"
