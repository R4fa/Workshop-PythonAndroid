import android
import mechanize
import ssl

def main():
	global droid
	droid=android.Android()
	
	global detectou
	detectou = False;
	
	line = droid.dialogGetInput("ATENCAO","Insira uma URL:","http://localhost:8080")
	
	url = line.result
	
	br = mechanize.Browser()
	
	#Se quiser testar uma url da internet
	#url = 'http://forum.clubedohardware.com.br/login/'
					
	br.set_handle_robots(False)
	#Configurar o user-agent									
	br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
					
	#IGNORAR SSL - contornar erro SSL: CERTIFICATE_VERIFY_FAILED			
	if hasattr(ssl, '_create_unverified_context'):
		ssl._create_default_https_context = ssl._create_unverified_context
					
	br.open(url)
			
	for link in br.links():
		string_links = str(link)
		print string_links
						
		lista = string_links.split(',')
		str_url = lista[1][6:-1]
		str_txt = lista[2][7:-1]
		
		verificar_links(str_url,str_txt)
	
	if detectou==False:
		droid.makeToast("CLEAN")
		
def verificar_links(url,txt):
	
	#verificar_fake_url
	if ("http://" in txt) & (txt!=url): 
		droid.makeToast("LINK FAKE")
		global detectou
		detectou=True

	#verificar_xss_nao_persistente
	if ("<script>" in url) | ("%3Cscript%3E" in url)  | ("73%63%72%69%70%74" in url):
		droid.makeToast("TAG SCRIPT DETECTED")
		global detectou
		detectou=True
	
	
if __name__=="__main__":
	main()