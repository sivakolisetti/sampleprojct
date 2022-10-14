#===========================================================================================================
#      FILE NAME: modules/storage_account/main.tf
#      USAGE: Defines resource block to create storage account
#      VERSION: 1.0
#      AUTHOR: Sahana Gajanana Acharya
#      DEPARTMENT: Platform Team
#===========================================================================================================

#===========================================================================================================
#Create storage account
#===========================================================================================================
resource "azurerm_storage_account" "storage_account" {
  name                     = var.name
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_kind             = var.account_kind
  account_tier             = var.account_tier
  account_replication_type = var.replication_type
  is_hns_enabled           = var.is_hns_enabled
  tags                     = var.tags
  
  network_rules {
    default_action         = "Deny" 
    ip_rules               = var.ip_rules
  }
}
