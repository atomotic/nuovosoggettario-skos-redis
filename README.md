# nuovosoggettario-skos-redis
index "Nuovo Soggettario" SKOS Subjects into Redis Sorted Sets


1. install

		git clone https://github.com/atomotic/nuovosoggettario-skos-redis.git
		cd nuovosoggettario-skos-redis
		pip install -r requirements.txt

2. download SKOS:  **$ make download**
	
		mkdir xml
		wget http://thes.bncf.firenze.sbn.it/dati/NS-SKOS.zip
		unzip NS-SKOS.zip -d xml
		rm NS-SKOS.zip
		
		
3. start redis

		redis-server &
		
		
4. index: **$ make index**   
(install gnu parallel or use xargs)

		$ parallel -j 5 /usr/bin/env python index.py {} ::: xml/*.xml
			
		indexing: xml/NS-SKOS-Azioni-Discipline.xml
		indexing: xml/NS-SKOS-Agenti-Organizzazioni.xml
		...
			
5. play with redis

		$ redis-cli info | grep used_memory_human
		used_memory_human:9.57M
		
		$ redis-cli --raw
		
		127.0.0.1:6379> ZRANGEBYLEX autocomplete [archiv "[archiv\xff" LIMIT 0 5
		archivi capitolari:{"label":"Archivi capitolari", "id":"http://purl.org/bncf/tid/17165"}
		archivi comunali:{"label":"Archivi comunali", "id":"http://purl.org/bncf/tid/32025"}
		archivi correnti:{"label":"Archivi correnti", "id":"http://purl.org/bncf/tid/52282"}
		archivi di autorità di nomi e titoli:{"label":"Archivi di autorità di nomi e titoli", 	"id":"http://purl.org/bncf/tid/2260"}
		archivi di autorità:{"label":"Archivi di autorità", "id":"http://purl.org/bncf/tid/2261"}
