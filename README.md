# Praktická časť k bakalárskej práci: Grafové modely síťových útoků a jejich aplikace
 
 Repozitár obsahuje 7 súborov:
 * matrix.py
 * petriNet.py
 * rulesToJSON.py
 * rulesToNeo4j.py
 * jsonTONeo4j.py
 * createRules.py
 * simulateAttackers.py
 
# Všetky skripty boli testované na:
* Elementary OS 5
* python 2.7.12

# Postup: 
 ![postup](https://raw.githubusercontent.com/marek130/bc/master/postup.jpg "Logo Title Text 1")

# Popisy jednotlivých súborov
 ---
## Skripty na transformáciu pravidiel do grafovych modelov
### `MATRIX.PY`
- skript na generovanie matice susednosti z pravidiel SABU
- skript berie ako argument cestu k súboru so SABU pravidlami

### `PETRINET.PY`
- skript na transformáciu pravidiel do petriho sieti
- skript berie 1 argument a to cestu k súboru s pravidlami
- **požiadavky**: knižnica SNAKES

### `RULESTOJSON.PY`
- transformovanie pravidel do formátu JSON
- skript berie 1 argument a to cestu k súboru s pravidlami
- **požiadavky**: knižnica JSON

## Skripty na vizualizáciu
### `RULESTONEO4J.PY`
- skript na vizualizáciu SABU pravidel do grafovej databáze Neo4j
- skript berie 1 argument a to cestu k súboru s pravidlami
- **požiadavky**: knižnica py2neo

### `JSONTONEO4J.PY`
- skript na vizualizáciu grafu útoku vo formáte JSON do grafovej databáze Neo4j
- skript požaduje k behu súbor ./jsonData , obsahujúci graf útoku vygenerovaný skriptom `rulesToJSON.py`
- **požiadavky**: knižnica py2neo, knižnica JSON

## Skripty na generovanie pravidiel
### `CREATERULES.PY`
- skript na vygenerovanie pravidiel z bezpečnostných udalostí
- skript berie 4 parametre. Prvý parameter reprezentuje cestu k súboru s bezpečnostnými udalosťami. Druhý parameter slúži ako názov súboru s novo vygenerovanými pravidlami. Hraničnú hodnotu podpory (SUPPORT) zastupuje tretí parameter, ktorý je použitý pre filtrovanie výsledných pravidiel. Posledný parameter reprezentuje hraničnú hodnotu istoty (CONFIDENCE), pre filtrovanie výsledných pravidiel.
- **požiadavky**: knižnica bintrees, knižnica time, knižnica re, knižnica functools, knižnica JSON, knižnica calendar

### `SIMULATEATTACKERS.PY`
- skript simulujúci útočníkov v sieti pomocou Petriho sieti. Ako výsledok skriptu sú predpovede postupov útočníka
- skript berie 6 argumentov. Prvý argument reprezentuje cestu k súboru s bezpečnostnými udalosťami. Druhý argument slúži ako názov súboru s novo vygenerovanými pravidlami. Tretí argument reprezentuje počet útočníkov v simulácií. Ďalší argument reprezentuje maximálnu dĺžku sekvencie útoku u útočníka. Hraničnú hodnotu podpory (SUPPORT) zastupuje piaty argument, ktorý je použitý pre filtrovanie výsledných pravidiel. Posledný argument reprezentuje hraničnú hodnotu istoty (CONFIDENCE), pre filtrovanie výsledných pravidiel.
-  **požiadavky**: knižnica bintrees, knižnica time, knižnica re, knižnica functools, knižnica JSON, knižnica calendar, knižnica random

 
