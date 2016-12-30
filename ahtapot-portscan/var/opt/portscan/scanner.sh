#!/bin/bash
#scanner.sh

source $(find /var/opt -name portscan.conf)
OPTIONS="-Pn -T4 -sSU -n -p- -d --min-rate 7000 --max-scan-delay 1ms --max-retries 1 --min-hostgroup 1024 --min-parallelism 256"
DATE=$(date +%s)
OUTPUT="-oA"                                
NMAP=$(which nmap)
IPV4_REGEX="\b(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\b"
NETMASK_REGEX="\b([1-9]|[1-2][0-9]|3[0-2])\b"

# taranacak hedeflerin parametre olarak verilebilmesi icin
while getopts "t:" opt; do 
	case $opt in
	t)
		TARGETS=${OPTARG}
	;;
	esac
done
if ! [ $(pwd) = "$LOG_DIR" ];then
	pushd $LOG_DIR
fi
touch portscan.log
chown ahtapotops:ahtapotops portscan.log
# birden fazla TARGET degiskeni kullanilacaksa, aralaria virgul koyulmali
echo "$TARGETS" | tr ',' '\n' | grep -v '^$' | while read -r TARGET
do 
	netmask=$(echo "$TARGET" | cut -d "/" -f2)
	address=$(echo "$TARGET" | cut -d "/" -f1)
	if ! [[ $address =~ $IPV4_REGEX ]];then
		echo "Hedef adres 192.168.0.1/22 şeklinde belirtilmeli, sadece sayi ve nokta(.) kullanilmali" >> $LOG_DIR/portscan.log
		exit 11;
		if ! [[ $netmask =~ $NETMASK_REGEX ]];then
			echo "Netmask 1-32 arasinda bir deger olmali" >> $LOG_DIR/portscan.log
			exit 11;
		fi
	fi
	echo "$DATE::$TARGET::Tarama baslatiliyor" >> $LOG_DIR/portscan.log
	if ! [ -d $OUTPUT_DIR ];then
		mkdir $OUTPUT_DIR
		chown ahtapotops:ahtapotops $OUTPUT_DIR
	fi
	pushd $OUTPUT_DIR
	if ! [ -d "$netmask" ];then
		mkdir "$netmask"
	fi
	if ! [ -d "$netmask/$address" ];then
		mkdir "$netmask/$address"
	fi
	pushd "$netmask/$address"
	$NMAP $TARGET $OPTIONS $OUTPUT scan-$DATE 
	nmap_exit_status=$(echo $?)
	echo "nmap_exit_status: $nmap_exit_status"
	if [ "$nmap_exit_status" -eq 0 ];then
	        echo "$DATE::$TARGET::Tarama bitti" >> $LOG_DIR/portscan.log
	elif [ "$nmap_exit_status" -eq 1 ];then
        	echo "$DATE::$TARGET::Network ile ilgili hata olustu" >> $LOG_DIR/portscan.log
	        exit "$nmap_exit_status";
	fi

	ln -sf scan-$DATE.gnmap  previous-scan
done
