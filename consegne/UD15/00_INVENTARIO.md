# UD15 — Inventario aggiornato

Partecipante: Stefano Raneri
Data/ora e fuso: 09:20 CET
Repository operativo e commit prima della prova: Si

| Elemento | Versione / stato osservato | Intervento necessario ed esito |
|---|---|---|
| WSL/architettura, memoria e spazio | Assente (Uso Linux) | Nessuno, Positivo |
| Docker Client/Server e context | Assente (Uso podman 5.8.3) | Nessuno, Positivo |
| kubectl Client/Server | Client Version: v1.37.2/Kustomize Version: v5.8.1 | Nessuno |
| Minikube e profilo | v1.39.0/Creato | Nessuno |
| Context e nodo | Assenti | Configurarli |
| Porte 8081/8082 | Assenti | Configurarle |

## Comandi aggiuntivi per driver=podman

```bash
minikube config set driver podman
minikube config set rootless true
```

## Comandi aggiuntivi per fedora secureblue

```bash
sudo sysctl -w fs.inotify.max_user_watches=524288
sudo sysctl -w fs.inotify.max_user_instances=8192
```

Tempo setup effettivo, con download/attese: 10 minuti
Controllo funzionale cluster, output essenziale: Effettuato
Modifiche Git preesistenti conservate: Si

Non inserire kubeconfig, certificati o token. Se un controllo non è stato possibile, scriverlo.

### Ambiente iniziale

```text
2026-11-04T09:59:27+01:00
/home/steve/Scrivania/workspace/azure-devops-lab
a4c8980 UD14 Consegna Lab Autonomo
x86_64
               total        used        free      shared  buff/cache   available
Mem:            61Gi        23Gi       1,3Gi       230Mi        38Gi        38Gi
Swap:          8,0Gi       8,0Ki       8,0Gi
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme0n1p3  1,9T 1014G  846G  55% /home/steve
Client:        Podman Engine
Version:       5.8.3
API Version:   5.8.3
Go Version:    go1.26.4-X:nodwarf5
Git Commit:    93dbfd0d86ee57f8f91801f61ce57dd880a4725f
Built:         Fri Jun 12 02:00:00 2026
Build Origin:  Fedora Project
OS/Arch:       linux/amd64
Client Version: v1.37.2
Kustomize Version: v5.8.1
minikube version: v1.39.0
commit: 7a9f6a841470a207de8cf4bafcccee0969d8ba10
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured

CURRENT   NAME       CLUSTER    AUTHINFO   NAMESPACE
*         minikube   minikube   minikube   default
NAME       STATUS     ROLES           AGE   VERSION   INTERNAL-IP    EXTERNAL-IP   OS-IMAGE                         KERNEL-VERSION                   CONTAINER-RUNTIME
minikube   NotReady   control-plane   12m   v1.37.0   192.168.49.2   <none>        Debian GNU/Linux 12 (bookworm)   7.0.14-201.fc44.x86_64 (amd64)   containerd://2.3.4
```
