# Vetralla Tekneko per Home Assistant

Integrazione non ufficiale per consultare in Home Assistant il calendario della
raccolta rifiuti e le notizie pubblicate tramite la piattaforma Innovambiente.

## Funzioni

- prossima raccolta programmata;
- raccolte previste oggi;
- sensori binari per ciascun tipo di rifiuto disponibile;
- ultime notizie del comune;
- supporto alle zone domestiche e non domestiche;
- aggiornamento automatico ogni ora.

## Installazione con HACS

1. In HACS apri **Repository personalizzati**.
2. Aggiungi `https://github.com/fcaloro-beep/tekneko-ha` come **Integrazione**.
3. Installa **Vetralla Tekneko** e riavvia Home Assistant.
4. Vai in **Impostazioni → Dispositivi e servizi → Aggiungi integrazione** e
   cerca **Vetralla Tekneko**.

Per Vetralla usa `1341` come ID comune e `1` per le utenze domestiche oppure
`2` per quelle non domestiche.

## Note

Il progetto usa endpoint web pubblici ma non ufficialmente documentati. Cambi
alla piattaforma Innovambiente potrebbero richiedere un aggiornamento.

