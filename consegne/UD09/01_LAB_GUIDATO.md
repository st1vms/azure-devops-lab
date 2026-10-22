# UD09 — Consegna laboratorio guidato

## Organization

- nome: `azdo-st1vms-01`
- geography: `Europe`
- Azure subscription collegata: sì

## Project

- nome: `az900-az104-devops`
- visibility: `Private`
- version control: `Git`
- process: `Agile`

## Gruppi

| Gruppo | Funzione essenziale |
|---|---|
| Project Administrators | I membri di questo gruppo possono svolgere tutte le operazioni nell'ambito del progetto di gruppo. |
| Contributors | I membri di questo gruppo possono aggiungere, modificare ed eliminare elementi all'interno del progetto di gruppo. |
| Readers | I membri di questo gruppo hanno accesso al progetto di gruppo. |
| Build Administrators | I membri di questo gruppo possono creare, modificare ed eliminare le definizioni di build e gestire le build in coda e quelle completate. |

## GitHub

- repository: `st1vms/azure-devops-lab`
- repository privato: no
- `gh auth status`: Effettuato
- `git fetch`: Effettuato
- connessione OAuth/PAT creata in UD09: NO
- metodo raccomandato per CI futura: Azure Pipelines GitHub App

## Parallel jobs

- Microsoft-hosted: Free Tier
- esito hosted: Positivo
- self-hosted: 1 parallel Free Job
- billing verificato: Si

## Agent Pool

- creato da Project settings: sì
- nome: `pool-ud09-wsl`
- tipo: `Self-hosted`
- accesso automatico a tutte le pipeline: No

## Autenticazione registrazione agent

- metodo usato: PAT
- PAT name, se usato:  `ud09-agent-registration`
- PAT scope, se usato: `Agent Pools: Read & manage`
- expiration: `30 days`
- inserito in file/repository: NO
- PAT revocato, se usato: Si

## Agent

- nome: `wsl-ud09-st1vms`
- pool: `pool-ud09-wsl`
- OS: `Linux`
- version: `vsts-agent-linux-x64-5.281.0`
- status: `Online`
- modalità: `Self-hosted`
- credenziale di registrazione chiusa e agent ancora Online: sì

## Capability

- Agent.OS: `Linux`
- Agent.Version: `5.281.0`
- git: `/usr/bin/git`
- python: `/usr/bin/python3`
- PATH verificato: Si

## Readiness

- Organization: `azdo-st1vms-01`
- Project: `az900-az104-devops`
- GitHub: `st1vms/azdo-agent-ud09`
- hosted: No
- self-hosted: Si
- agent: `wsl-ud09-st1vms`
- security: `PAT`
