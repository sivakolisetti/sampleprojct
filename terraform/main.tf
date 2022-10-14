#==========================================================================================================================
#      FILE NAME: main.tf
#      USAGE: Defines required terraform,provider,data blocks and modules to create storage account and private endpoint
#      VERSION: 1.0
#      AUTHOR: Sahana Gajanana Acharya
#      DEPARTMENT: Platform Team
#===========================================================================================================================

#===================================================================================
#Configure terraform block to specify required versions
#===================================================================================
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "2.60"
    }
  }
}
#====================================================================================
# Configure Terraform Backend
#====================================================================================
terraform {
  backend "azurerm" {
  }
}
#====================================================================================
#Configure Azure Resource Manager Provider
#====================================================================================
provider "azurerm" {
  features {}
}
provider "azurerm" {
  features {}  
  alias                            = "hub"
  subscription_id                  = var.hub_sub_id
}

#====================================================================================
#Get details of resource group
#====================================================================================
data "azurerm_resource_group" "rg" {
  name                             = var.resource_group_name
}

#====================================================================================
#Get details of virtual network
#====================================================================================
data "azurerm_virtual_network" "vnet" {
  name                             = var.spoke_vnet
  resource_group_name              = data.azurerm_resource_group.rg.name
}
#====================================================================================
#Get details of subnet
#====================================================================================
data "azurerm_subnet" "subnet" {
    name                           = var.vm_subnet
    virtual_network_name           = data.azurerm_virtual_network.vnet.name
    resource_group_name            = data.azurerm_resource_group.rg.name
}

#====================================================================================
#Get details of private dns zone
#====================================================================================
data "azurerm_private_dns_zone" "example" {
  provider                         = azurerm.hub
  name                             = var.private_dns_zone_name
  resource_group_name              = var.hub_rg_dns_zone
}

#====================================================================================
#Storage account module
#====================================================================================
module "storage_account" {
  source                           = "./modules/storage_account"
  name                             = var.storage_account_name
  location                         = data.azurerm_resource_group.rg.location
  tags                             = var.tags
  resource_group_name              = data.azurerm_resource_group.rg.name
  account_kind                     = var.storage_account_kind
  account_tier                     = var.storage_account_tier
  replication_type                 = var.storage_account_replication_type
  vm_subnet_id                     = data.azurerm_subnet.subnet.id
}

#====================================================================================
#Private endpoint module
#====================================================================================
module "private_endpoint" {
  source                           = "./modules/private_endpoint"
  blob_private_endpoint            = var.blob_private_endpoint
  location                         = data.azurerm_resource_group.rg.location
  resource_group_name              = data.azurerm_resource_group.rg.name
  vm_subnet_id                     = data.azurerm_subnet.subnet.id
  tags                             = var.tags
  storage_account_name             = var.storage_account_name
  privated_dns_zone_id             = data.azurerm_private_dns_zone.example.id
  private_link_enabled_resource_id = module.storage_account.storage_account_id
  depends_on                       = [module.storage_account]
}
