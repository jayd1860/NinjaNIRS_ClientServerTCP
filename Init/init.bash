# Run this script by type ~/NinjaNIRS_ClientServerTCP/Init/init.bash

# Setup wifi  first
echo ""
r=`sudo grep -n "ninjaGUIpy" /etc/wpa_supplicant/wpa_supplicant.conf`
if [ -z "$r" ]; then
	echo "Step 1. Wifi is NOT set up. Adding ninjaGUIpy WiFi"
	sleep 1

	echo "cp ~/NinjaNIRS_ClientServerTCP/Init/wpa_supplicant_reset.conf ~/NinjaNIRS_ClientServerTCP/Init/wpa_supplicant_reset_temp.conf"
	cp ~/NinjaNIRS_ClientServerTCP/Init/wpa_supplicant_reset.conf ~/NinjaNIRS_ClientServerTCP/Init/wpa_supplicant_reset_temp.conf
	sleep 1

	echo "echo \" \" >> ~/NinjaNIRS_ClientServerTCP/Init/wpa_supplicant_reset_temp.conf"
	echo "echo \"network={\" >> ~/NinjaNIRS_ClientServerTCP/Init/wpa_supplicant_reset_temp.conf"
	echo "echo \"	ssid=\"ninjaGUIpy\"\" >> ~/NinjaNIRS_ClientServerTCP/Init/wpa_supplicant_reset_temp.conf"
	echo "echo \"	psk=\"ninjaGUIpy2023\"\"  >> ~/NinjaNIRS_ClientServerTCP/Init/wpa_supplicant_reset_temp.conf"
	echo "echo \"	key_mgmt=WPA-PSK\" >> ~/NinjaNIRS_ClientServerTCP/Init/wpa_supplicant_reset_temp.conf"
	echo "echo \"}\" >> ~/NinjaNIRS_ClientServerTCP/Init/wpa_supplicant_reset_temp.conf"
	echo "echo \" \" >> ~/NinjaNIRS_ClientServerTCP/Init/wpa_supplicant_reset_temp.conf"
	echo " " >> ~/NinjaNIRS_ClientServerTCP/Init/wpa_supplicant_reset_temp.conf 
	echo "network={" >> ~/NinjaNIRS_ClientServerTCP/Init/wpa_supplicant_reset_temp.conf
	echo "	ssid=\"ninjaGUIpy\"" >> ~/NinjaNIRS_ClientServerTCP/Init/wpa_supplicant_reset_temp.conf
	echo "	psk=\"ninjaGUIpy2023\""  >> ~/NinjaNIRS_ClientServerTCP/Init/wpa_supplicant_reset_temp.conf
	echo "	key_mgmt=WPA-PSK" >> ~/NinjaNIRS_ClientServerTCP/Init/wpa_supplicant_reset_temp.conf
	echo "}" >> ~/NinjaNIRS_ClientServerTCP/Init/wpa_supplicant_reset_temp.conf
	echo " " >> ~/NinjaNIRS_ClientServerTCP/Init/wpa_supplicant_reset_temp.conf 
	sleep 1

	echo "sudo chmod 777 /etc/wpa_supplicant/wpa_supplicant.conf"
	sudo chmod 777 /etc/wpa_supplicant/wpa_supplicant.conf
	echo "sudo ls -l /etc/wpa_supplicant/wpa_supplicant.conf"
	sudo ls -l /etc/wpa_supplicant/wpa_supplicant.conf
	echo "sudo cp ~/NinjaNIRS_ClientServerTCP/Init/wpa_supplicant_reset_temp.conf /etc/wpa_supplicant/wpa_supplicant.conf"
	sudo cp ~/NinjaNIRS_ClientServerTCP/Init/wpa_supplicant_reset_temp.conf /etc/wpa_supplicant/wpa_supplicant.conf
	sleep 1

	echo "sudo chmod 440 /etc/wpa_supplicant/wpa_supplicant.conf"
	sudo chmod 440 /etc/wpa_supplicant/wpa_supplicant.conf
	sleep 1

	echo "rm -rf ~/NinjaNIRS_ClientServerTCP/Init/wpa_supplicant_reset_temp.conf"
	rm -rf ~/NinjaNIRS_ClientServerTCP/Init/wpa_supplicant_reset_temp.conf
	sleep 2
else
	echo "Step 1. NOTHING TO DO:  ninjaGUIpy WiFi is already set up."
	sleep 2
fi

echo ""
echo ""

# Setup ninjaGUIpy server daemon
r=`sudo grep -n "@reboot jayd1860 ~/NinjaNIRS_ClientServerTCP/runServer.bash" /etc/crontab`
if [ -z "$r" ]; then
	echo "Step 2. ninjaGUIpy server is NOT set up will add it to /etc/crontab"
	sleep 1

	echo "cp ~/NinjaNIRS_ClientServerTCP/Init/crontab_reset ~/NinjaNIRS_ClientServerTCP/Init/crontab_reset_temp"
	cp ~/NinjaNIRS_ClientServerTCP/Init/crontab_reset ~/NinjaNIRS_ClientServerTCP/Init/crontab_reset_temp
	sleep 1

	echo "echo \" \" >> ~/NinjaNIRS_ClientServerTCP/Init/crontab_reset_temp"
	echo "echo \"@reboot jayd1860 ~/NinjaNIRS_ClientServerTCP/runServer.bash\" >> ~/NinjaNIRS_ClientServerTCP/Init/crontab_reset_temp"
	echo "echo \" \" >> ~/NinjaNIRS_ClientServerTCP/Init/crontab_reset_temp"
	echo " " >> ~/NinjaNIRS_ClientServerTCP/Init/crontab_reset_temp
	echo "@reboot jayd1860 ~/NinjaNIRS_ClientServerTCP/runServer.bash" >> ~/NinjaNIRS_ClientServerTCP/Init/crontab_reset_temp
	echo " " >> ~/NinjaNIRS_ClientServerTCP/Init/crontab_reset_temp
	sleep 1

	echo "sudo chmod 777 /etc/crontab"
	sudo chmod 777 /etc/crontab
	echo "sudo ls -l /etc/crontab"
	sudo ls -l /etc/crontab
	echo "sudo cp ~/NinjaNIRS_ClientServerTCP/Init/crontab_reset_temp /etc/crontab"
	sudo cp ~/NinjaNIRS_ClientServerTCP/Init/crontab_reset_temp /etc/crontab
	sleep 1

	echo "sudo chmod 440 /etc/crontab"
	sudo chmod 440 /etc/crontab
	sleep 1

	rm -rf ~/NinjaNIRS_ClientServerTCP/Init/crontab_reset_temp
	sleep 2
else
	echo "Step 2. NOTHING TO DO:  ninjaGUIpy server daemon is already set up."
	sleep 2
fi

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
