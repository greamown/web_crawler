#!/bin/bash
# ---------------------------------------------------------

# Color ANIS
RED='\033[1;31m';
BLUE='\033[1;34m';
GREEN='\033[1;32m';
YELLOW='\033[1;33m';
CYAN='\033[1;36m';
NC='\033[0m';
CONF="./common/db.json"
# ---------------------------------------------------------
# Install jq
echo -e "${BLUE}"
echo "----- Installing JQ -----"
echo -e "${NC}"

if ! type jq >/dev/null 2>&1; then
    sudo apt-get install -y jq
else
    echo 'The jq has been installed.';
fi

# ---------------------------------------------------------
echo -e "${BLUE}"
echo "----- Setting env -----"
echo -e "${NC}"

# Setting env
conda activate crawler

# ---------------------------------------------------------
echo -e "${BLUE}"
echo "----- Open mariadb -----"
echo -e "${NC}"

USER=$(cat ${USER} | jq -r '.USER')

# Open mariadb
service mariadb start
sudo mysql -u ${USER} -p