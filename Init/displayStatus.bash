# Display wifi  first
echo ""
sudo chmod 777 /etc/wpa_supplicant/wpa_supplicant.conf
echo "===================================================="
echo "Contents of /etc/wpa_supplicant/wpa_supplicant.conf:"
echo "===================================================="
sudo cat /etc/wpa_supplicant/wpa_supplicant.conf
echo ""

# Display ninjaGUIpy server daemon
sudo chmod 777 /etc/crontab
sleep 1
echo "========================="
echo "Contents of /etc/crontab:"
echo "========================="
sudo cat /etc/crontab
echo ""
sudo chmod 440 /etc/crontab
sudo chmod 440 /etc/wpa_supplicant/wpa_supplicant.conf


