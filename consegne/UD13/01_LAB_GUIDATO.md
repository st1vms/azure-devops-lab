# UD13 — Consegna LAB guidato

## Terraform

- network.tf: Copiato
- plan:

```bash
Plan: 4 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + resource_group_name           = "rg-ud12-tf"
  + storage_account_name          = "stud13793266087"
  + storage_primary_blob_endpoint = (known after apply)
```

- apply: Completato: `Resources: 4 added, 0 changed, 0 destroyed`
- VNet verificata:

```bash
az network vnet show \
  --resource-group rg-ud12-tf \
  --name vnet-ud13 \
  --query "{Name:name,Address:addressSpace.addressPrefixes}" \
  --output jsonc

{
  "Address": [
    "10.13.0.0/16"
  ],
  "Name": "vnet-ud13"
}
```

- subnet verificata:

```bash
az network vnet subnet show \
--resource-group rg-ud12-tf \
--vnet-name vnet-ud13 \
--name snet-app \
--query "{Name:name,Prefix:addressPrefixes[0]}" \
--output table
Name      Prefix
--------  ------------
snet-app  10.13.1.0/24
```

- destroy: Eseguito: `Resources: 4 destroyed`
- RG Terraform eliminato: Si

## Delivery persistente

- Resource Group:

```bash
$ az group create \
  --name "$DELIVERY_RG" \
  --location "$DELIVERY_LOCATION" \
  --tags Course=AZ104 Purpose=FinalDelivery \
  --output table
Location    Name
----------  -------------------
italynorth  rg-ud13-15-delivery
```

- service connection: Creata
- WIF: Si
- scope: Subscription
- accesso globale a tutte le pipeline: NO

## Pipeline

- YAML: Copiato
- agent pool: `pool-ud09-wsl`
- Validate: Completato con successo
- Deploy: Completato con successo
- What-If: Completato con successo
- deployment: Completato con successo
- ACR:

```bash
az acr list \
  --resource-group "$DELIVERY_RG" \
  --query "[].{Name:name,SKU:sku.name,Admin:adminUserEnabled}" \
  --output table
Name                    SKU    Admin
----------------------  -----  -------
acrud1315vanpejrkpcmd6  Basic  False
```

```bash
ACR_NAME=$(az acr list \
  --resource-group "$DELIVERY_RG" \
  --query "[0].name" \
  --output tsv)

az acr show \
  --name "$ACR_NAME" \
  --resource-group "$DELIVERY_RG" \
  --query roleAssignmentMode \
  --output tsv
LegacyRegistryPermissions
```

```bash
az acr list \
  --resource-group "$DELIVERY_RG" \
  --query "[0].loginServer" \
  --output tsv
acrud1315vanpejrkpcmd6.azurecr.io
```

- SKU: `Basic`
- admin user: No

## Fine UD13

- risorse delivery conservate: sì
