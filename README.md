# AquaNode Pulse pentru Home Assistant

Integrare locală pentru detectorul de pene și monitorul de tensiune AquaNode
Pulse. După instalare, Home Assistant găsește automat dispozitivele Pulse din
aceeași rețea. Nu este necesar Mosquitto, MQTT, Tuya, LocalTuya sau un alt
add-on.

Comunicarea Home Assistant ↔ Pulse rămâne în rețeaua locală. AquaNode Cloud
poate funcționa în paralel, dar cele două conexiuni nu depind una de cealaltă.

## Cerințe

- AquaNode Pulse cu firmware `1.3.0` sau mai nou;
- Home Assistant `2025.1` sau mai nou;
- HACS instalat;
- Home Assistant și Pulse în aceeași rețea sau într-o configurație care permite
  mDNS între VLAN-uri.

## Instalare prin HACS

1. În HACS deschide meniul din dreapta sus și alege **Custom repositories**.
2. Adaugă:
   `https://github.com/BanVictor17/aquanode-pulse-home-assistant`
3. Selectează categoria **Integration**.
4. Caută **AquaNode Pulse** și apasă **Download**.
5. Repornește Home Assistant.

După restart, mergi la **Settings → Devices & services**. Cardul
**AquaNode Pulse discovered** apare automat. Apasă **Configure** și introdu o
singură dată parola de configurare de pe eticheta produsului.

Adăugarea manuală după adresă IP rămâne disponibilă doar ca soluție de rezervă
pentru rețelele care blochează mDNS.

## Ce apare pe pagina produsului

- tensiunea calibrată, cu istoric și statistici Home Assistant;
- semnalul Wi-Fi și timpul de funcționare;
- starea conexiunii opționale AquaNode Cloud;
- avertizare pentru modul absent, semnal saturat sau calibrare necesară;
- avertizare locală pentru tensiune sub prag;
- controlul LED-ului de stare;
- buton de identificare și buton de restart;
- diagnostic descărcabil fără parola dispozitivului.

Entitățile tehnice precum semnalul brut, memoria liberă și numărul de porniri
sunt dezactivate implicit, dar pot fi activate din pagina dispozitivului.

## Calibrarea tensiunii

Deschide integrarea AquaNode Pulse și apasă **Configure → Calibrează
tensiunea**. Măsoară în același moment priza cu un multimetru true-RMS sigur și
introdu valoarea citită.

Factorul este salvat în memoria Pulse, deci rămâne după restart și funcționează
local chiar fără internet. Dacă AquaNode Cloud este disponibil, aceeași
calibrare este sincronizată automat. Dacă modifici potențiometrul modulului,
repetă calibrarea.

Pragul local inițial este `200 V`. Valoarea `0 V` dezactivează avertizarea de
tensiune scăzută din Home Assistant.

## Confidențialitate și securitate

- API-ul de stare și toate comenzile sunt autentificate cu parola de
  configurare de pe etichetă.
- Parola nu este publicată prin mDNS.
- Integrarea nu trimite date către GitHub, HACS sau AquaNode Cloud.
- Endpointul mDNS publică numai modelul, serialul, versiunea și portul API,
  informații necesare descoperirii.

## Probleme frecvente

**Dispozitivul nu este găsit automat**

Verifică dacă Home Assistant și Pulse sunt în aceeași rețea, dacă multicast
DNS este permis și dacă firmware-ul Pulse este cel puțin `1.3.0`. Poți folosi
temporar configurarea manuală după IP.

**Tensiunea nu apare**

Intră în pagina dispozitivului. Entitatea **Calibrare necesară** explică dacă
lipsește calibrarea, iar **Modul tensiune absent** și **Semnal tensiune saturat**
arată problemele de montaj sau reglaj.

**AquaNode Cloud apare deconectat, dar valorile locale funcționează**

Acesta este comportamentul normal când internetul sau serverul AquaNode nu este
disponibil. Home Assistant continuă să citească direct dispozitivul.

## Dezvoltare

```bash
python3 scripts/verify.py
```

Workflow-urile GitHub rulează validarea HACS și Hassfest la fiecare modificare.

## Licență

MIT. AquaNode este marcă AquaNode.
