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
echo "----- Install annoconda and setting env -----"
echo -e "${NC}"

# Install annoconda and setting env
sudo apt-get install curl wget
cd env
wget https://repo.anaconda.com/archive/Anaconda3-2023.03-Linux-x86_64.sh
sudo chmod u+x ./*.sh
./Anaconda3-2023.03-Linux-x86_64.sh
source ~/.bashrc
conda create -n crawler python=3.9 
conda activate crawler
pip install -r requirements.txt
cd ..

# ---------------------------------------------------------
echo -e "${BLUE}"
echo "----- Insatll mariadb -----"
echo -e "${NC}"

USER=$(cat ${USER} | jq -r '.USER')

# Insatll mariadb
sudo apt-key adv --recv-keys --keyserver keyserver.ubuntu.com 0xcbcb082a1bb943db
curl -LsS https://downloads.mariadb.com/MariaDB/mariadb_repo_setup | sudo bash
sudo apt-get install -y apt-transport-https
sudo apt-get update
sudo apt-get install libmariadb3
sudo apt-get install libmariadb-dev
pip3 install mariadb
sudo apt-get install -y mariadb-server
service mariadb start
sudo mysql -u ${USER} -p