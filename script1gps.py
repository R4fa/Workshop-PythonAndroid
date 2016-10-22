import android
import time
import math

global dist
dist=0
droid=android.Android()

def main():
	r = droid.dialogGetInput("ATENCAO","Indique o raio de seguranca (m):","50")
	raio_seguro = float(r.result)
	print raio_seguro

	coord = getLocation()
	lat1=coord[0]
	lon1=coord[1]
	
	#coordenada fatec
	#lat1=-22.739584
	#lon1=-47.350189
		
	while 1:		
		coord = getLocation()
		
		print "Longitude: %s - Latitude: %s" %(coord[1],coord[0]) 
		
		lat2=coord[0]
		lon2=coord[1]

		#calculando distancia do centro ate a localizacao atual
		R = 6371; #Unid.: km - Este e o raio da Terra
		dLat = math.radians(lat2-lat1);
		dLon = math.radians(lon2-lon1);
		lat11 = math.radians(lat1);
		lat22 = math.radians(lat2);

		a = (math.sin(dLat/2) * math.sin(dLat/2)) + (math.sin(dLon/2) * math.sin(dLon/2) * math.cos(lat11) * math.cos(lat22)); 
		c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a)); 
		dist = R * c;

		print "Distance: %s " %(dist)
						
		if (dist*1000)>raio_seguro:
			play = droid.mediaPlay('/sdcard/siren.wav')
			
def getLocation():
	achou_coord = True
	while achou_coord:
		droid.startLocating()
		time.sleep(4) # tempo entre as leituras
		loc = droid.readLocation().result
		if bool(loc)==True:
			achou_coord=False
		if bool(loc)==False:
			print "loc vazio"	
	
	try:
		lon1 = loc['gps']['longitude']
		lat1 = loc['gps']['latitude']
	except KeyError:
		lat1 = loc['network']['latitude']
		lon1 = loc['network']['longitude']
	return lat1,lon1
	
			
if __name__=="__main__":
	main()