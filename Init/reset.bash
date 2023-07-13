# Run this script by type ~/NinjaNIRS_ClientServerTCP/Init/init.bash

# Setup wifi  first
echo ""
echo "sudo chmod 777 /etc/wpa_supplicant/wpa_supplicant.conf"
sudo chmod 777 /etc/wpa_supplicant/wpa_supplicant.conf

echo "sudo ls -l /etc/wpa_supplicant/wpa_supplicant.conf"
sudo ls -l /etc/wpa_supplicant/wpa_supplicant.conf

echo "sudo cp ~/NinjaNIRS_ClientServerTCP/Init/wpa_supplicant_reset.conf /etc/wpa_supplicant/wpa_supplicant.conf"
sudo cp ~/NinjaNIRS_ClientServerTCP/Init/wpa_supplicant_reset.conf /etc/wpa_supplicant/wpa_supplicant.conf

echo "sudo chmod 440 /etc/wpa_supplicant/wpa_supplicant.conf"
sudo chmod 440 /etc/wpa_supplicant/wpa_supplicant.conf

sleep 2

echo ""
echo ""

# Setup ninjaGUIpy server daemon


echo "sudo chmod 777 /etc/crontab"
sudo chmod 777 /etc/crontab

echo "sudo ls -l /etc/crontab"
sudo ls -l /etc/crontab

echo "sudo cp ~/NinjaNIRS_ClientServerTCP/Init/crontab_reset /etc/crontab"
sudo cp ~/NinjaNIRS_ClientServerTCP/Init/crontab_reset /etc/crontab

echo "sudo chmod 440 /etc/crontab"
sudo chmod 440 /etc/crontab

sleep 2

echo ""
echo ""
echo ""
echo ""
echo "===================================================="
echo "Contents of /etc/wpa_supplicant/wpa_supplicant.conf:"
echo "===================================================="
sudo cat /etc/wpa_supplicant/wpa_supplicant.conf
echo ""
echo ""
echo ""
sleep 2
echo "========================="
echo "Contents of /etc/crontab:"
echo "========================="
sudo cat /etc/crontab
echo ""
echo ""

