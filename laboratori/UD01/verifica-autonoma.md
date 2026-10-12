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
