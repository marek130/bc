# Praktická časť k bakalárskej práci: Grafové modely síťových útoků a jejich aplikace
 
 Repozitár obsahuje 7 súborov:
 * matrix.py
 * petriNet.py
 * rulesToJSON.py
 * rulesToNeo4j.py
 * jsonTONeo4j.py
 * createRules.py
 * simulateAttacker.py
 
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
### `RULESTOJSON.PY`
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
- skript berie 2 parametre. Prvý parameter reprezentuje cestu k súboru s bezpečnostnými udalosťami. Druhý parameter slúži ako názov súboru s novo vygenerovanými pravidlami
- **požiadavky**: knižnica bintrees, knižnica Time, knižnica re, knižnica functools, knižnica JSON, knižnica calendar

### `SIMULATEATTACKER.PY`
- skript simulujúci utocníkov v sieti pomocou Petriho sieti. Ako výsledok skriptu sú predpovede postopov útočníka
- skript berie 4 parametre. Prvý parameter reprezentuje cestu k súboru s bezpečnostnými udalosťami. Druhý parameter slúži ako názov súboru s novo vygenerovanými pravidlami. Tretí parameter reprezentuje hraničnú hodnotu podpory (SUPPORT), pre filtrovanie výsledných pravidiel. Posledný parameter reprezentuje hraničnú hodnotu istoty (CONFIDENCE), pre filtrovanie výsledných pravidiel
- - **požiadavky**: knižnica bintrees, knižnica Time, knižnica re, knižnica functools, knižnica JSON, knižnica calendar, knižnica random

 
