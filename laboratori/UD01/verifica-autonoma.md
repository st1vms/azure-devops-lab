# Verifica Autonoma

WSL2 non installato perché sono su distribuzione linux.

Il percorso Linux del repository

```bash
$ pwd
/var/home/steve/workspace/azure-devops-lab
```

L'URL del remote: `https://github.com/st1vms/azure-devops-lab.git`

Il working tree è la cartella del progetto dove lo sviluppatore apporta modifiche e lavora allo sviluppo del progetto. La staging area è una raccolta di tutte le modifiche da preparare per il commimt. Il commit è uno snapshot delle modifiche nel working tree, il repository remoto è la cartella che racchiude tutti gli snapshots (commit) del progetto e che permette la sincronizzazione delle modifiche tra tutti i working trees.

Per verificare la versione di Azure CLI si usa:

```bash
az version
```

Per verificare il contesto:

```bash
az account show --output table
```

Lo stato dell'invito al docente:

- `Pending`

Un possibile errore di contesto tipico in Azure CLI si verifica quando tenti di gestire una risorsa, ma la CLI sta puntando alla subscription o al tenant sbagliato.

Il comando diagnostico fondamentale è:

```bash
az account show
```

## Autovalutazione

Assegna a ogni capacità `Completato` oppure `Da ripetere`:

| Capacità | Valutazione |
|---|---|
| Distinguo PowerShell dal terminale Ubuntu | Completato |
| Verifico che Ubuntu utilizzi WSL 2 | Completato |
| Riconosco la radice del repository Git | Completato |
| Verifico il remote prima del push | Completato |
| Distinguo file non tracciato e file in staging | Completato |
| Inserisco in staging soltanto il file richiesto | Completato |
| Verifico lo stesso commit in locale e su GitHub | Completato |
| Verifico lo stato dell'invito al docente | Completato |
| Riconosco ed escludo dati riservati | Completato |