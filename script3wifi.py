import android
import time
import os.path

from script1gps import getLocation

def main():
	global droid
	droid=android.Android()
	global networks
	networks={}
	global continuar
	continuar = True
	
	global lista_ssids
	lista_ssids = ['rede','teste','default','free','gratis','open','aberto','convidado','guest',
					'INTELBRAS','Dlink','D-LINK','3Com','belkin','ConnectionPoint','linksys',
					'NETGEAR','TP-LINK','Link_One','Wi-Fi TIM','Thomson','link-one','multilaser',
					'Micromax','rtl','Nextel','Samsung','motorola','netvirtua','net virtua',
					'oi wifi','live tim','tim wifi']
	
	while continuar:
		executar_scan()
		
		#print type(networks)
		
		#key eh o BSSID, que eh repetido em values
		for value in networks.iteritems():
			
			res = verifica_lista(value[0])
			#print type(value[1])
			
			if (res==False):
				print "REDE DETECTADA - NAO ESTA NO ARQUIVO"
				#Redes WEP - frageis
				if (("WEP" in value[1].get("capabilities")) |
				#SSID eh igual ou subtring dos relacionados em lista_ssids
				(any(value[1].get("ssid").upper() in s for s in [name.upper() for name in lista_ssids])==True) |
				#SSID eh igual ou contem alguma das redes em lista_ssids
				any(n in value[1].get("ssid").upper() for n in [nome.upper() for nome in lista_ssids])):
					
					print "REDE DETECTADA - ATENDE AOS REQUISITOS"
					#pegar coordenadas GPS
					coord = getLocation()
					
					lat=coord[0]
					lon=coord[1]
					
					print "bssid "+value[1].get("bssid")
					print "ssid "+value[1].get("ssid")
					print "cap "+value[1].get("capabilities")
					print "level "+str(value[1].get("level"))
					print "coord "+str(lat)+","+str(lon)
												
					with open('/sdcard/redes.txt', 'a') as myfile:
						myfile.write("BSSID="+value[1].get("bssid")+
									 ";SSID="+value[1].get("ssid")+
									 ";CAPABILITIES="+value[1].get("capabilities")+
									 ";LEVEL="+str(value[1].get("level"))+
									 ";LOCATION="+str(lat)+","+str(lon)+"\n")
				
			else:
				print "REDE JA INSERIDA"
				
		time.sleep(3)
		

	
def executar_scan():
	global networks
	networks={}
	while not droid.wifiStartScan().result:
		time.sleep(0.25)
		print "aguardando inicio..."
	while not networks:
		for ap in droid.wifiGetScanResults().result:
			networks[ap['bssid']]=ap.copy()
			print "procurando redes"
			#print ap
			
def verifica_lista(bssid):

	if os.path.exists('/sdcard/redes.txt'):
		if bssid in open('/sdcard/redes.txt').read():
			return True
		else:
			return False
			print "false"
	else:
		print "arquivo de redes nao existe"
		open('/sdcard/redes.txt','w').close()
		return False
	
if __name__=="__main__":
	main()