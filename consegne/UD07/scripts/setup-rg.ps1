$RgName = "rg-ud07-auto"
$Location = "westeurope"

$rg = Get-AzResourceGroup `
  -Name $RgName `
  -ErrorAction SilentlyContinue

if (-not $rg) {
    $rg = New-AzResourceGroup `
      -Name $RgName `
      -Location $Location
}

Update-AzTag `
  -ResourceId $rg.ResourceId `
  -Tag @{ ManagedBy="Autonomo"; UD="07"} `
  -Operation Merge | Out-Null

Get-AzResourceGroup `
  -Name $RgName |
  Select-Object ResourceGroupName, Location, ProvisioningState, Tags