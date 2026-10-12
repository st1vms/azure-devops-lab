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

## Verifica — Preparazione dell'ambiente e metodo di lavoro

## Parte A — Scelte operative

### 1

In PowerShell git --version restituisce 2.53.0, mentre nel terminale Ubuntu restituisce 2.43.0. Qual è la spiegazione più corretta?

B. Windows e Ubuntu possono possedere installazioni distinte di Git.

### 2

Quale comando mostra se la distribuzione Ubuntu sta usando WSL 1 o WSL 2?

C. `wsl --list --verbose`

### 3

Perché il progetto viene conservato in `~/workspace`?

C. Per lavorare nel file system Linux, più adatto al successivo workflow con Docker e bind mount.

### 4

Git è presente e la sua versione è compatibile. Qual è l'azione corretta?

C. Verificarne il funzionamento e proseguire senza reinstallazione.

### 5

Dopo `git commit` la pagina GitHub non mostra la modifica. Quale spiegazione è più probabile?

A. Il commit esiste localmente, ma non è ancora stato eseguito git push.

### 6

Qual è il controllo più diretto per capire quali file entreranno nel prossimo commit?

A. `git status` dopo `git add`

### 7

Durante `az login --use-device-code` il terminale mostra un codice temporaneo. Che cosa devi fare?

C. Usarlo nella pagina di autenticazione e non conservarlo nel repository.

### 8

Quale indizio dimostra meglio che VS Code sta operando dentro Ubuntu?

B. L'indicatore `WSL: Ubuntu` e un terminale con percorso Linux.

### 9

Perché il docente deve essere aggiunto come collaboratore al repository personale pubblico?

C. Per partecipare alle attività di scrittura, revisione e collaborazione previste dal percorso.

## Parte B — Risposte brevi

### 10

Spiega in non più di quattro righe la differenza fra Git e GitHub.

Git è il sistema di versionamento, che permette di tenere traccia delle modifiche apportate ai progetti (repository). Fornisce gli strumenti da command line e GUI per poter interagire col sistema di versionamento.
Github invece è la piattaforma Cloud che permette di pubblicare le repository online, e permettere a chiunque di visualizzarle, gestendo anche la collaborazione tra sviluppatori, funziona più come una piattaforma social per il codice.

### 11

Scrivi la sequenza minima di comandi che useresti per osservare le modifiche, preparare un singolo file, creare un commit e inviarlo al remote.

```bash
# Visualizzare lo stato della directory di lavoro e dell'area di staging
git status

# Aggiungere il file specificato all'area di staging
git add path/file.ext

# Registra le modifiche in fase di preparazione nel repository
git commit -m "Descrivi le modifiche apportate al file"

# Trasmetti i commit del ramo locale al repository remoto
git push
```

### 12

Si propone di eseguire immediatamente `wsl --update` su tutte le postazioni. Quali due controlli devono precedere la decisione?

```bash
# Verificare prima i nomi disponibili:
wsl --list --verbose

# Creare un backup nel caso ci siano problemi di incompatibilità con le versioni successive di WSL
wsl --export <NOME_DISTRIBUZIONE> "$env:USERPROFILE\Downloads\backup-wsl.tar"
```

### 13

Il comando `code .` apre VS Code, ma il terminale integrato mostra un percorso `C:\Users\...`. Quale problema sospetti e quale verifica esegui?

Il comando potrebbe essere stato eseguito su un terminale di Windows (CMD, Powershell) invece che sul terminale di WSL.
Per verificare, controllare se il terminale integrato presenta l'indicatore `WSL: Ubuntu`.

### 14

Hai pubblicato per errore un vero token in un commit e poi hai cancellato la riga con un secondo commit. Perché il problema non è risolto?

Il primo commit con il token rimarrà tracciato nello storico dei commit, ed effetuando il push verrà sincronizzato con il remote, indipendemente dal fatto che il secondo commit lo modifichi.
