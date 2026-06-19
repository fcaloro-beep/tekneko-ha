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

La configurazione permette di scegliere tra oltre 300 comuni presenti sulla
piattaforma Innovambiente e carica automaticamente le relative zone. Il
percorso **Altro comune** consente anche di inserire manualmente un ID non
ancora incluso nel catalogo.

## Note

Il progetto usa endpoint web pubblici ma non ufficialmente documentati. Cambi
alla piattaforma Innovambiente potrebbero richiedere un aggiornamento.
