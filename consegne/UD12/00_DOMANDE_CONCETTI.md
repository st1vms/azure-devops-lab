# UD12 — Domande sui concetti

Rispondere dopo avere studiato `00_CONCETTI.md`. Non limitarsi a definizioni di una riga: quando possibile aggiungere un piccolo esempio.

## 1. Quale problema risolve l'Infrastructure as Code rispetto a una configurazione esclusivamente manuale?

**Risposta:**
L'Infrastructure as Code risolve il problema di dover ripetere le operazioni a mano ogni volta. Se creiamo una risorsa tramite il Portale Azure, è difficile ricordarsi tutti i passaggi esatti se dobbiamo ricrearla uguale domani o in un altro ambiente. Con l'IaC scriviamo tutto in un file, così il lavoro diventa ripetibile, tracciabile e automatizzabile.

## 2. Spiega con parole semplici la differenza tra approccio imperativo e dichiarativo

**Risposta:**
L'approccio imperativo significa dire passo dopo passo cosa fare, come quando diamo una lista di comandi uno alla volta. L'approccio dichiarativo significa invece descrivere come vogliamo che sia il risultato finale. Con il secondo metodo noi diciamo cosa vogliamo ottenere e lo strumento pensa a capire quali azioni compiere per arrivarci.

## 3. Perché continuiamo a usare Azure CLI anche se introduciamo IaC?

**Risposta:**
Usiamo ancora Azure CLI perché ci serve per verificare le risorse, fare controlli, interrogare Azure o preparare i prerequisiti necessari prima di lanciare i file IaC. Non serve a sostituirli, ma ad aiutarci a controllare che tutto funzioni bene.

## 4. Che cos'è Bicep?

**Risposta:**
Bicep è un linguaggio semplice e dichiarativo creato apposta per descrivere le risorse su Azure. I file Bicep hanno l'estensione `.bicep` e ci permettono di scrivere l'infrastruttura in modo più chiaro e leggibile rispetto ai vecchi template.

## 5. Bicep sostituisce Azure Resource Manager?

**Risposta:**
No, Bicep non sostituisce Azure Resource Manager. Bicep è solo un modo più comodo e pulito per scrivere il codice che poi sarà comunque interpretato e distribuito da Azure Resource Manager.

## 6. Che cosa significa `param location string`?

**Risposta:**
Significa che stiamo dichiarando un parametro chiamato `location` che accetta un valore di tipo testo (`string`). Serve a rendere il file riutilizzabile, ad esempio per decidere in quale regione creare la risorsa senza dover riscrivere tutto il codice.

## 7. A cosa serve un parametro?

**Risposta:**
Un parametro serve a passare dei valori dall'esterno al nostro file di codice, così possiamo riusare lo stesso template in situazioni diverse. Ad esempio, possiamo cambiare il nome o la regione dello Storage Account senza toccare la struttura principale del codice.

## 8. A cosa servono `@minLength` e `@maxLength`?

**Risposta:**
Servono a mettere dei paletti sulla lunghezza del testo che possiamo inserire in un parametro. Ad esempio, `@minLength(3)` e `@maxLength(24)` dicono che il nome dello Storage Account deve avere almeno 3 lettere e al massimo 24.

## 9. Nella riga `resource storage 'Microsoft.Storage/storageAccounts@2023-05-01'`, che cosa significa `storage`?

**Risposta:**
Significa che `storage` è il nome simbolico interno che usiamo dentro il file Bicep per riferirci a quella specifica risorsa. Non è il nome reale che la risorsa avrà in Azure, ma serve solo al nostro codice per riconoscerla.

## 10. Che cosa significa `Microsoft.Storage/storageAccounts`?

**Risposta:**
Indica il tipo esatto di risorsa che vogliamo creare su Azure. `Microsoft.Storage` è il nome del provider che gestisce il servizio, mentre `storageAccounts` specifica che stiamo creando proprio uno Storage Account.

## 11. Che cosa significa `@2023-05-01`?

**Risposta:**
È la versione dell'API di Azure che vogliamo usare per interpretare le proprietà di quella risorsa. Dice allo strumento quale versione del contratto usare per dialogare correttamente con Azure.

## 12. È la data di creazione dello Storage Account?

**Risposta:**
No, non c'entra nulla con la data in cui creiamo lo Storage Account o con la data in cui abbiamo scritto il file. È solo la versione del linguaggio con cui Azure riconosce le regole di quella risorsa.

## 13. Qual è la differenza tra nome simbolico Bicep e nome reale Azure?

**Risposta:**
Il nome simbolico è un etichetta che usiamo solo dentro il file di codice per collegare le varie parti tra loro. Il nome reale invece è quello vero che apparirà sul Portale Azure e che useremo per identificare la risorsa nel cloud.

## 14. A cosa servono gli output Bicep?

**Risposta:**
Gli output servono a restituire dei valori utili dopo che il deployment è stato completato. Ad esempio, ci permettono di stampare a schermo il nome reale dello Storage Account appena creato o l'indirizzo per collegarci.

## 15. Che cosa fa `az bicep lint`?

**Risposta:**
Fa un controllo di base sul nostro file Bicep per trovare eventuali errori di scrittura o problemi prima ancora di avviare il deployment vero e proprio su Azure.

## 16. Che cosa fa What-If?

**Risposta:**
What-If ci mostra in anticipo che cosa succederebbe se facessimo partire il deployment. Analizza la situazione attuale e ci elenca le modifiche, come le nuove risorse che verranno create.

## 17. What-If crea realmente le risorse?

**Risposta:**
No, What-If serve solo a fare una previsione. Non crea e non modifica niente su Azure, ci fa solo vedere in anticipo quali cambiamenti avverranno.

## 18. Qual è la differenza tra What-If e deployment `create`?

**Risposta:**
Il What-If serve solo a guardare la previsione di quello che succederà, un po' come un'anteprima. Il comando `create` invece prende quel codice e lo applica davvero, creando o modificando le risorse in modo definitivo su Azure.

## 19. Perché Bicep non richiede un file equivalente a `terraform.tfstate`?

**Risposta:**
Perché Bicep si appoggia direttamente ad Azure Resource Manager, che memorizza e gestisce lo stato reale delle risorse direttamente nel cloud. Non abbiamo bisogno di un file locale separato per tenere traccia di cosa è stato creato.

## 20. Che cos'è Terraform?

**Risposta:**
Terraform è uno strumento IaC dichiarativo che serve a descrivere e creare l'infrastruttura. A differenza di Bicep, non funziona solo con Azure, ma può gestire molte piattaforme diverse grazie ai suoi componenti di collegamento.

## 21. Perché Terraform usa provider?

**Risposta:**
Terraform usa i provider perché il programma principale non conosce tutte le piattaforme del mondo. Ogni provider è come un adattatore speciale che insegna a Terraform come comunicare con un servizio specifico, come ad esempio Azure, AWS o GitHub.

## 22. Che ruolo ha AzureRM?

**Risposta:**
AzureRM è il provider specifico per Azure. Il suo ruolo è tradurre le richieste di Terraform in comandi che la piattaforma Azure è in grado di capire per creare le risorse.

## 23. Che cosa contiene `versions.tf`?

**Risposta:**
Contiene le regole sulle versioni che stiamo usando, ad esempio la versione minima di Terraform necessaria e la versione esatta del provider che vogliamo scaricare per far funzionare il progetto.

## 24. A cosa serve `providers.tf`?

**Risposta:**
Serve ad attivare e configurare il provider che vogliamo usare, dicendo a Terraform con quale sistema principale dovrà dialogare durante il lavoro.

## 25. Perché credenziali e codice IaC devono restare separati?

**Risposta:**
Devono restare separati per motivi di sicurezza. Il codice descrive come è fatta l'infrastruttura e va salvato nel repository, mentre password, token e chiavi private devono restare fuori dal codice ed essere passati dall'ambiente di esecuzione.

## 26. Che cosa contiene `variables.tf`?

**Risposta:**
Contiene la dichiarazione delle variabili del nostro progetto, cioè quei valori che possiamo personalizzare, come la regione di Azure o i nomi delle risorse, specificando anche dei valori predefiniti.

## 27. Che differenza c'è tra `azurerm_resource_group`, `lab`, `var.resource_group_name` e `rg-ud12-tf`?

**Risposta:**
`azurerm_resource_group` è il tipo di risorsa Terraform, `lab` è il nome interno che usiamo noi nel codice, `var.resource_group_name` è la variabile che legge il nome, e `rg-ud12-tf` è il nome reale e definitivo che la risorsa avrà su Azure.

## 28. Nella riga `resource "azurerm_resource_group" "lab"`, che cos'è `lab`?

**Risposta:**
`lab` è semplicemente il nome logico interno che Terraform usa per riconoscere quella risorsa all'interno del file di configurazione.

## 29. Il Resource Group reale si chiamerà `lab`?

**Risposta:**
No, il nome reale non c'entra con la parola `lab`. Il nome vero viene preso dalla variabile collegata, come ad esempio `rg-ud12-tf`.

## 30. Da dove arriva il nome reale `rg-ud12-tf`?

**Risposta:**
Arriva dal valore impostato nella variabile corrispondente all'interno del file di configurazione o passato tramite l'ambiente di lavoro.

## 31. Che cosa significa `azurerm_resource_group.lab.name`?

**Risposta:**
Significa che stiamo prendendo la risorsa logica chiamata `lab` gestita da Terraform e stiamo leggendo la sua proprietà che contiene il nome reale.

## 32. Perché lo Storage Account usa `azurerm_resource_group.lab.name`?

**Risposta:**
Lo usa per collegarsi al Resource Group giusto senza dover scrivere il nome a mano, dicendo a Terraform di inserire lo Storage Account dentro quel gruppo specifico.

## 33. Che cosa significa `azurerm_resource_group.lab.location`?

**Risposta:**
Significa che vogliamo leggere la regione geografica in cui si trova il Resource Group logico `lab`, così da mettere lo Storage Account esattamente nello stesso posto.

## 34. Perché Terraform può dedurre la dipendenza fra Resource Group e Storage Account?

**Risposta:**
Perché nello Storage Account scriviamo che il gruppo di risorse si collega a `azurerm_resource_group.lab.name`. In questo modo Terraform capisce da solo che prima deve creare il Resource Group e poi lo Storage Account.

## 35. A cosa serve la validazione di `storage_account_name`?

**Risposta:**
Serve a controllare subito, prima di fare qualsiasi altra cosa, che il nome scelto rispetti le regole di Azure, come avere la giusta lunghezza ed essere composto solo da lettere minuscole e numeri.

## 36. A cosa servono gli output Terraform?

**Risposta:**
Servono a mostrare sullo schermo i dati importanti delle risorse create, come i loro nomi reali o i loro indirizzi, una volta che il comando di applicazione è terminato.

## 37. Che cosa fa `terraform init`?

**Risposta:**
Prepara la cartella di lavoro scaricando i componenti necessari, come il provider AzureRM, e crea i file di servizio locali per poter eseguire i comandi successivi.

## 38. Che differenza c'è tra `.terraform/` e `.terraform.lock.hcl`?

**Risposta:**
La cartella `.terraform/` contiene tutti i file di lavoro scaricati localmente, mentre il file `.terraform.lock.hcl` serve a bloccare le versioni precise dei provider usati per fare in modo che siano sempre gli stessi.

## 39. Che cosa fa `terraform fmt`?

**Risposta:**
Sistema e formatta automaticamente il testo dei file di configurazione seguendo le regole estetiche standard di Terraform, rendendo il codice ordinato.

## 40. Che cosa fa `terraform validate`?

**Risposta:**
Controlla che i file di configurazione siano scritti senza errori di sintassi e che siano coerenti tra loro prima di provare a comunicare con il cloud.

## 41. Che cosa fa `terraform plan`?

**Risposta:**
Legge lo stato attuale e il codice per calcolare e mostrare in anticipo tutte le modifiche che Terraform intende fare sul sistema, come le risorse che verranno create.

## 42. Perché il piano va letto prima dell'apply?

**Risposta:**
Va letto per essere sicuri che Terraform non stia per fare modifiche sbagliate o inattese, dandoci la possibilità di controllare tutto prima di passare all'azione vera e propria.

## 43. Perché nel LAB salviamo il piano in `ud12.tfplan`?

**Risposta:**
Lo salviamo in un file per essere sicuri di applicare esattamente quella previsione che abbiamo appena controllato, senza che nel frattempo cambino le condizioni.

## 44. Che cosa fa `terraform apply`?

**Risposta:**
Prende il piano che abbiamo preparato e lo esegue davvero, creando o modificando le risorse reali sulla piattaforma cloud.

## 45. Che cos'è lo state Terraform?

**Risposta:**
È un file speciale che Terraform usa per tenere traccia di tutto ciò che ha creato, collegando il codice scritto alle risorse reali presenti nel cloud.

## 46. Quale relazione mantiene lo state?

**Risposta:**
Mantiene il legame tra gli oggetti definiti nel nostro codice e le risorse effettive che si trovano su Azure, così sa sempre quale risorsa aggiornare o eliminare quando modifichiamo il file.

## 47. Perché `terraform.tfstate` non va trattato come normale codice sorgente?

**Risposta:**
Perché contiene dati operativi delicati e informazioni sensibili sulle risorse, e se venisse modificato per errore o gestito male potrebbe rompere il collegamento con il cloud.

## 48. Che cosa mostra `terraform state list`?

**Risposta:**
Mostra l'elenco di tutte le risorse che Terraform sta gestendo in quel momento attraverso il proprio file di stato.

## 49. `terraform state list` mostra tutte le risorse della Subscription?

**Risposta:**
No, mostra solo ed esclusivamente gli oggetti gestiti da quel preciso progetto Terraform, non tutto quello che esiste nell'intera Subscription di Azure.

## 50. `terraform destroy` elimina anche i file `.tf`?

**Risposta:**
No, elimina solo le risorse reali che erano state create su Azure, ma lascia intatti i file di codice sorgente all'interno del computer.

## 51. Qual è la differenza principale nel percorso Bicep→Azure rispetto a Terraform→Azure?

**Risposta:**
Con Bicep il codice passa direttamente attraverso Azure Resource Manager per arrivare alle risorse, mentre con Terraform il codice passa prima attraverso il provider AzureRM e usa un file di stato locale.

## 52. In che cosa What-If e Plan sono simili?

**Risposta:**
Sono simili nello scopo perché servono entrambi a mostrarci in anteprima che cosa succederà prima di applicare le modifiche reali.

## 53. Perché non sono lo stesso meccanismo?

**Risposta:**
Perché What-If è uno strumento interno di Azure Resource Manager, mentre Plan è un meccanismo proprio di Terraform che confronta il codice con il file di stato locale.

## 54. In quale tipo di organizzazione Bicep può essere particolarmente naturale?

**Risposta:**
Può essere molto naturale in un'azienda che lavora quasi esclusivamente all'interno dell'ecosistema Azure e usa già i servizi nativi di Microsoft.

## 55. In quale tipo di organizzazione Terraform può essere particolarmente naturale?

**Risposta:**
Può essere naturale in un'azienda che gestisce più piattaforme diverse nello stesso momento, come Azure, AWS e sistemi locali, usando un unico strumento universale.

## 56. Perché non ha senso dire in assoluto che uno dei due è sempre migliore?

**Risposta:**
Perché ogni strumento ha i suoi punti di forza e la scelta dipende dalle esigenze dell'azienda, dalle competenze delle persone e dalle piattaforme che già si utilizzano.

## 57. Perché i file IaC devono rimanere nel repository?

**Risposta:**
Devono rimanere nel repository perché sono il codice sorgente della nostra infrastruttura, così possiamo modificarli, storicizzarli con Git e riutilizzarli nel tempo.

## 58. Le directory `infra/bicep/` e `infra/terraform/` verranno ricreate da zero in UD13?

**Risposta:**
No, non verranno ricreate da zero, ma saranno mantenute e arricchite con nuovi file e nuove configurazioni nelle giornate successive.

## 59. Perché installare Terraform nel WSL2 è utile per le UD successive?

**Risposta:**
Perché ci permette di avere già pronti gli strumenti necessari per eseguire i comandi direttamente dentro l'ambiente di lavoro che useremo per le pipeline e i laboratori futuri.

## 60. Su quale componente vengono realmente eseguiti i comandi di una pipeline?

**Risposta:**
I comandi vengono eseguiti sui programmi installati all'interno dell'Agent che sta facendo girare quel determinato lavoro.

## 61. Che cosa rappresenta il WSL2 del partecipante nel modello self-hosted?

**Risposta:**
Rappresenta l'ambiente locale che usiamo per simulare un Agent autogestito, utile per capire come funzionano i computer che eseguono le operazioni.

## 62. Qual è la differenza principale fra persistenza self-hosted e ambiente Microsoft-hosted?

**Risposta:**
Il self-hosted usa una macchina che mantiene i file e i programmi installati nel tempo, mentre l'ambiente Microsoft-hosted usa una macchina temporanea nuova che viene buttata via alla fine di ogni singolo lavoro.

## 63. Perché eliminare le risorse Azure non significa eliminare il codice IaC?

**Risposta:**
Perché le risorse sul cloud sono temporanee e si possono cancellare quando non servono più, mentre il codice scritto nei file rimane salvato nel repository e pronto per essere riutilizzato in seguito.
