<p align="center">
  <img src="https://raw.githubusercontent.com/fcaloro-beep/tekneko-ha/main/assets/tekneko-logo.svg" alt="Tekneko Raccolta" width="420">
</p>

# Tekneko Raccolta per Home Assistant

Integrazione non ufficiale per consultare in Home Assistant il calendario della
raccolta rifiuti e le notizie pubblicate tramite la piattaforma Innovambiente.

## Funzioni

- calendario mensile delle raccolte, visibile nel pannello Calendario di Home Assistant;
- prossima raccolta programmata;
- raccolte previste oggi;
- sensori binari per ciascun tipo di rifiuto disponibile;
- ultime notizie del comune;
- supporto alle zone domestiche e non domestiche;
- aggiornamento automatico ogni ora.

## Calendario mensile

Dopo aver configurato l'integrazione, apri **Calendario** nella barra laterale
di Home Assistant e seleziona **Calendario raccolte**. La stessa entità può
essere aggiunta a una dashboard con la scheda Calendario.

## Installazione con HACS

1. In HACS apri **Repository personalizzati**.
2. Aggiungi `https://github.com/fcaloro-beep/tekneko-ha` come **Integrazione**.
3. Installa **Tekneko Raccolta** e riavvia Home Assistant.
4. Vai in **Impostazioni → Dispositivi e servizi → Aggiungi integrazione** e
   cerca **Tekneko Raccolta**.

La configurazione permette di scegliere tra oltre 300 comuni presenti sulla
piattaforma Innovambiente e carica automaticamente le relative zone. Il
percorso **Altro comune** consente anche di inserire manualmente un ID non
ancora incluso nel catalogo.

## Note

Il progetto usa endpoint web pubblici ma non ufficialmente documentati. Cambi
alla piattaforma Innovambiente potrebbero richiedere un aggiornamento.
