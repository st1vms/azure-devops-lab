# Nota operativa — UD01

La cartella di lavoro si nella cartella home del mio utente, nella mia distribuzione secureblue Fedora kinoite. VSCode installato su distrobox Ubuntu 26.04.1 LTS.

Il controllo che ha dimostrato il corretto contesto di esecuzione è:

```bash
pwd
```

Output: `/var/home/<USER>/workspace`

*Nota: su fedora immutabile, le cartelle ~/ e /home sono linkate a /var/home/*

L'output indicava un percorso interno alla home Linux e non un percorso `/mnt/c`.

## Comando più utile incontrato nell'unità

Il comando che ho trovato più utile in questa unità è decisamente `git`, permette lo sviluppo efficiente di codice grazie al version control.
