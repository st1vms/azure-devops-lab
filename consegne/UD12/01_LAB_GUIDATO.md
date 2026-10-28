# UD12 — Consegna LAB guidato

## Preparazione

- materiali UD12: Presenti
- repository personale: Presente
- directory `infra/bicep`: Presente
- directory `infra/terraform`: Presente
- directory consegne: Presente

## Azure

- subscription verificata: Si
- identità verificata: Si

## Bicep

- Bicep version: `0.48.1 (cec7951cf6)`
- lint: Disponibile, nessun errore
- Resource Group: `rg-ud12-bicep`
- Storage Account: `stud12b93193517`
- What-If change type: `Microsoft.Storage/storageAccounts`
- deployment:

```bash
az deployment group create \
  --name ud12-bicep-deploy \
  --resource-group "$BICEP_RG" \
  --template-file main.bicep \
  --parameters \
      location="$LAB_LOCATION" \
      storageName="$BICEP_STG" \
  --output table
Name               State      Timestamp                         Mode         ResourceGroup
-----------------  ---------  --------------------------------  -----------  ---------------
ud12-bicep-deploy  Succeeded  2026-10-28T13:24:32.096562+00:00  Incremental  rg-ud12-bicep
```

- output `storageAccountName`: `stud12b93193517`
- output `blobEndpoint`: `https://stud12b93193517.blob.core.windows.net/`
- verifica CLI:

```bash
$ az storage account show \
  --resource-group "$BICEP_RG" \
  --name "$BICEP_STG" \
  --query "{
    Name:name,
    Location:location,
    SKU:sku.name,
    TLS:minimumTlsVersion,
    PublicBlob:allowBlobPublicAccess
  }" \
  --output table
Name             Location    SKU           TLS     PublicBlob
---------------  ----------  ------------  ------  ------------
stud12b93193517  italynorth  Standard_LRS  TLS1_2  False
```

- Resource Group Bicep eliminato: Si
- `az group exists`: `false`

## Terraform

- Terraform version: `v1.17.0`
- provider AzureRM: `hashicorp/azurerm`
- `terraform init`:

```bash
$ terraform init
Initializing the backend...

Initializing provider plugins...
- Finding hashicorp/azurerm versions matching "~> 5.4"...
- Installing hashicorp/azurerm v5.11.0...
- Installed hashicorp/azurerm v5.11.0 (signed by HashiCorp)

Terraform has created a lock file .terraform.lock.hcl to record the provider
selections it made above. Include this file in your version control repository
so that Terraform can guarantee to make the same selections by default when
you run "terraform init" in the future.

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.
```

- `terraform fmt -check`: Eseguito, nessun output.
- `terraform validate`:

```bash
$ terraform validate
Success! The configuration is valid.
```

- plan add: `2`
- plan change: `0`
- plan destroy: `0`
- apply: `Apply complete! Resources: 2 added, 0 changed, 0 destroyed.`
- output Resource Group: `rg-ud12-tf`
- output Storage: `stud12t93194552`
- verifica CLI:

```bash
az group show \
  --name rg-ud12-tf \
  --query "{Name:name,Location:location,Tags:tags}" \
  --output jsonc

{
  "Location": "italynorth",
  "Name": "rg-ud12-tf",
  "Tags": {
    "Course": "AZ104",
    "ManagedBy": "Terraform",
    "UD": "12"
  }
}
```

```bash
az storage account show \
  --resource-group rg-ud12-tf \
  --name "$TF_VAR_storage_account_name" \
  --query "{Name:name,SKU:sku.name,Location:location}" \
  --output table
Name             SKU           Location
---------------  ------------  ----------
stud12t93194552  Standard_LRS  italynorth
```

- `terraform state list`:

```bash
$ terraform state list
azurerm_resource_group.lab
azurerm_storage_account.lab
```

## Fine LAB guidato

- risorse Terraform mantenute per LAB autonomo: sì
