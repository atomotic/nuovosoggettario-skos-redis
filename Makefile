download:
	mkdir xml
	wget http://thes.bncf.firenze.sbn.it/dati/NS-SKOS.zip
	unzip NS-SKOS.zip -d xml
	rm NS-SKOS.zip

index:
	parallel -j 5 /usr/local/bin/python index.py {} ::: xml/*.xml
