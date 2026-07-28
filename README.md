# AquaNode Pulse pentru Home Assistant

Integrare locală completă pentru detectorul de pene și monitorul de tensiune
AquaNode Pulse. Home Assistant găsește automat dispozitivul, citește starea la
fiecare secundă și păstrează local evenimentele și graficele.

Nu este necesar Mosquitto, MQTT, Tuya, LocalTuya sau un alt add-on. AquaNode
Cloud poate funcționa în paralel, dar integrarea Home Assistant nu depinde de
el.

## Ce primești

- panou AquaNode Pulse în meniul lateral, cu o interfață apropiată de aplicația
  produsului;
- pagină principală cu toate dispozitivele și starea lor;
- trei secțiuni pentru fiecare Pulse: **Stare**, **Tensiune** și
  **Dispozitiv**;
- actualizare locală la o secundă pentru stare, tensiune, Wi-Fi și diagnostic;
- clasificarea întreruperii ca pană de curent, problemă de rețea, cauză
  necunoscută sau repornire planificată;
- jurnal persistent, păstrat după restartul Home Assistant;
- grafice pentru 24 de ore, 7 zile, 30 de zile și un an;
- minimul, media și maximul tensiunii pentru fiecare interval;
- incidente de tensiune scăzută cu prag și histerezis;
- notificări automate în centrul Home Assistant;
- blueprint separat pentru notificări push pe telefon;
- redenumire locală și notificare de test;
- control pentru LED, identificare, restart, praguri și calibrare;
- diagnostic cu IP, firmware, semnal Wi-Fi, uptime, memorie, număr de porniri
  și stare AquaNode Cloud.

## Cum este salvat istoricul

Valorile live sunt citite la o secundă. Pentru a nu umple inutil memoria și
discul Home Assistant, graficele sunt salvate sub formă de agregate:

- câte un punct pe minut pentru ultimele 24 de ore;
- câte un punct la 15 minute pentru 7 și 30 de zile;
- câte un punct la 6 ore pentru un an.

Fiecare punct păstrează minimul, media și maximul. Evenimentele sunt salvate
separat, cu ora de început, ora de final, durata și cauza. Sunt păstrate până
la 400 de zile, în limita a 2.000 de evenimente pentru fiecare dispozitiv.

Datele sunt în `.storage/aquanode_pulse.history` din Home Assistant. Nu sunt
trimise către GitHub, HACS sau AquaNode Cloud.
Salvarea este administrată direct de integrare, independent de Recorder, astfel
încât graficele și jurnalul rămân disponibile după restarturi și actualizări.

## Cerințe

- AquaNode Pulse cu firmware `1.3.0` sau mai nou;
- Home Assistant `2025.1` sau mai nou;
- HACS instalat;
- Home Assistant și Pulse în aceeași rețea locală.

Descoperirea automată folosește mDNS. Pentru Home Assistant instalat în Docker
fără `network_mode: host`, integrarea încearcă și o căutare locală unicast.
Adăugarea manuală după IP rămâne disponibilă.

## Instalare prin HACS

1. Deschide **HACS**.
2. Intră în meniul din dreapta sus și alege **Custom repositories**.
3. Adaugă:
   `https://github.com/BanVictor17/aquanode-pulse-home-assistant`
4. Alege categoria **Integration**.
5. Caută **AquaNode Pulse** și apasă **Download**.
6. Repornește Home Assistant.
7. Deschide **Setări → Dispozitive și servicii**.
8. Pe cardul **AquaNode Pulse discovered**, apasă **Configure**.
9. Introdu parola de configurare de pe eticheta produsului.

După adăugare apare automat secțiunea **AquaNode Pulse** în meniul lateral.

## Notificări

### Notificări Home Assistant

Sunt active implicit. Nu trebuie creată nicio automatizare. Apar în centrul de
notificări Home Assistant pentru:

- posibilă pană sau pierdere de rețea;
- revenire, cu cauza confirmată și durata;
- tensiune sub limită;
- revenirea tensiunii.

În pagina **Dispozitiv** poți opri aceste notificări sau poți seta timpul minim.
Valoarea implicită este `0 secunde`, adică notificare imediată. Incidentele mai
scurte decât pragul rămân în jurnal și grafice.

Butonul **Trimite o notificare de test** verifică centrul de notificări fără să
simuleze o pană reală.

### Notificări push pe telefon

Home Assistant trebuie să știe pe ce telefon să trimită mesajul, de aceea
această alegere se face o singură dată:

1. Instalează aplicația oficială Home Assistant pe telefon.
2. Permite notificările în aplicație și în setările telefonului.
3. În panoul AquaNode Pulse, deschide dispozitivul.
4. Intră în **Dispozitiv → Notificări pe telefon**.
5. Apasă **Importă automatizarea**.
6. În Home Assistant, confirmă importul blueprint-ului.
7. Creează automatizarea.
8. Alege entitatea **Conexiune locală** a dispozitivului Pulse.
9. La serviciul telefonului introdu, de exemplu,
   `notify.mobile_app_telefonul_meu`.
10. Salvează automatizarea.

Serviciul corect poate fi găsit în **Developer tools → Actions**, căutând
`notify.mobile_app`.

Blueprint-ul trimite imediat mesajul de posibilă pană când pragul este `0`,
apoi un al doilea mesaj la revenire, cu pană de curent sau problemă de rețea.
Poate trimite și alertele de tensiune.

## Calibrarea tensiunii

1. Conectează Pulse și un multimetru true-RMS sigur la aceeași alimentare.
2. Deschide **AquaNode Pulse → dispozitiv → Dispozitiv**.
3. Apasă **Calibrează tensiunea**.
4. Introdu valoarea măsurată în acel moment.
5. Apasă **Salvează**.

Factorul este salvat în memoria Pulse și rămâne după restart. Dacă modifici
potențiometrul modulului de măsurare, repetă calibrarea.

Pragul inițial pentru tensiune scăzută este `200 V`. Valoarea `0 V`
dezactivează alerta. Revenirea este confirmată după ce tensiunea trece cu
`3 V` peste prag, pentru a evita notificările repetate la limita setată.

## Comenzi și siguranță

- **Identifică dispozitivul** face LED-ul să clipească.
- **LED albastru în repaus** oprește doar lumina continuă. Semnalele de setup
  și eroare rămân active.
- **Repornește dispozitivul** creează o fereastră de mentenanță locală, astfel
  încât restartul cerut nu este raportat ca pană.
- **Șterge evenimentele** șterge evenimentele încheiate, dar păstrează incidentele
  active și graficele de tensiune.
- **Redenumește dispozitivul** schimbă numele numai în Home Assistant și în
  notificările locale.

Accesul la panou și dispozitive este gestionat de utilizatorii și permisiunile
Home Assistant. Integrarea locală nu cere și nu folosește un cont AquaNode
Cloud pentru partajare.

## Probleme frecvente

**Dispozitivul nu este găsit automat**

Verifică dacă Home Assistant și Pulse sunt în aceeași rețea. Pentru Docker,
folosește `network_mode: host` sau adaugă dispozitivul manual după IP.

**Tensiunea nu apare**

În pagina dispozitivului verifică **Modul tensiune absent**, **Semnal tensiune
saturat** și **Calibrare necesară**.

**AquaNode Cloud apare deconectat**

Este normal dacă internetul sau serverul AquaNode nu este disponibil.
Integrarea Home Assistant continuă să citească local dispozitivul.

**Graficele sunt goale după instalare**

Istoricul începe în momentul în care integrarea este instalată. Primul punct
apare după prima măsurătoare calibrată, iar graficul se completează în timp.

## Dezvoltare

```bash
ruff check custom_components/aquanode_pulse scripts/verify.py tests
python3 scripts/verify.py
python3 -m pytest -q
node --check custom_components/aquanode_pulse/frontend/aquanode-pulse-panel.js
```

Workflow-urile GitHub rulează verificarea reală cu Home Assistant, HACS și
Hassfest la fiecare modificare.

## Licență

MIT. AquaNode este marcă AquaNode.
