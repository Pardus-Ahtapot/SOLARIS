#!/bin/bash
#parser.sh

source $(find /var/opt -name portscan.conf)
DATE=$(date +%F)
touch $LOG_DIR/alarm.log
compare()
{	previous_scan=$1
	target=$2
	ip_adresleri=$(cat $previous_scan | grep Up | sort -u  | egrep -o '([0-9]{1,3}[\.]){3}[0-9]{1,3}')
	while IFS= read -r line 
	do				
		ip_adresi=$line
	        cat $previous_scan  | grep -e "\<$ip_adresi\>" | grep -o '[0-9]*\/open/\tcp' | sed 's/\/open.*//' | sed 's/ $//g' | sort -n >  tcp_tarama.txt
	        cat $previous_scan  | grep -e "\<$ip_adresi\>" | grep -o '[0-9]*\/open/\udp' | sed 's/\/open.*//' | sed 's/ $//g' | sort -n >  udp_tarama.txt
		port_from_alarm=$(sqlite3 $DB_DIR/db.ahtapotps "SELECT tcp,udp FROM portscan_alarm WHERE ip_address='$ip_adresi';")
		port_from_whitelist=$(sqlite3 $DB_DIR/db.ahtapotps "SELECT tcp,udp  FROM portscan_assetlist WHERE ip_address='$ip_adresi';")
		db_stat2=$?
		if [ "$db_stat2" -eq 0 ];then
			if ! [ -z "$port_from_whitelist" ] ;then
				echo "$port_from_whitelist" | awk '{split($0,p,"|"); print p[1]}' | tr ',' '\n' | sed '/^\s*$/d' | sort -n >  tcp_veritabani.txt 
				echo "$port_from_whitelist" | awk '{split($0,p,"|"); print p[2]}' | tr ',' '\n' | sed '/^\s*$/d' | sort -n >  udp_veritabani.txt
				alarm_tcp_port=$(comm -13 tcp_veritabani.txt tcp_tarama.txt | tr '\n' ',' | sed 's/,$//')
				alarm_udp_port=$(comm -13 udp_veritabani.txt udp_tarama.txt | tr '\n' ',' | sed 's/,$//')
				
                		if ! [ -z "$alarm_tcp_port" ];then
					echo "$DATE::Alert::$target::Bu network'te bulunan $ip_adresi IP adresine ait $alarm_tcp_port numarali TCP port/portlar whitelist'te degildir." >> $LOG_DIR/alarm.log
				fi
				if ! [ -z "$alarm_udp_port" ];then
					echo "$DATE::Alert::$target::Bu network'te bulunan $ip_adresi IP adresine ait $alarm_udp_port numarali UDP port/portlar whitelist'te degildir." >> $LOG_DIR/alarm.log
				fi
				# eger ip adresine ait alarm yoksa  ekle
				if [ -z "$port_from_alarm" ];then
					sqlite3 $DB_DIR/db.ahtapotps "INSERT INTO portscan_alarm (ip_address,tcp,udp) VALUES('$ip_adresi','$alarm_tcp_port','$alarm_udp_port');"
				fi
				# eger ip adresine ait bir alarm varsa duzenle
				if ! [ -z "$port_from_alarm" ];then
					sqlite3 $DB_DIR/db.ahtapotps "UPDATE portscan_alarm SET tcp='$alarm_tcp_port', udp='$alarm_udp_port' WHERE ip_address='$ip_adresi';"
				fi	 
			fi
		elif [ "$db_stat2" -eq 1 ] ;then
			echo "DEBUG: Aranan bilgiler veritabaninda yok.-->$port_from_whitelist, $ip_adresi" >> $LOG_DIR/portscan.log
		fi
	done <<< "$ip_adresleri"
	if [ -e tcp_veritabani.txt ];then
		rm tcp_veritabani.txt
	fi
	if [ -e udp_veritabani.txt ];then
		rm udp_veritabani.txt
	fi
	rm tcp_tarama.txt udp_tarama.txt
}


pushd $OUTPUT_DIR
paths=$(find . -name previous-scan)
echo "$paths" | while read -r path
do
	target=$(echo "$path" | cut -d '/' -f3)
	compare "$path" $target
done
