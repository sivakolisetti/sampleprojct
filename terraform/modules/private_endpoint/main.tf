#===========================================================================================================
#      FILE NAME: modules/private_endpoint/main.tf
#      USAGE: Defines resource block to create private endpoint
#      VERSION: 1.0
#      AUTHOR: Sahana Gajanana Acharya
#      DEPARTMENT: Platform Team
#===========================================================================================================

#===========================================================================================================
#Create Private endpoint
#===========================================================================================================
resource "azurerm_private_endpoint" "private_endpoint" {
  name                = var.blob_private_endpoint
  location            = var.location
  resource_group_name = var.resource_group_name
  subnet_id           = var.vm_subnet_id
  tags                = var.tags
  private_service_connection {
    name                           = "${var.storage_account_name}.privateEndpoint"
    private_connection_resource_id = var.private_link_enabled_resource_id
    is_manual_connection           = false
    subresource_names               = ["blob"]
  }
  private_dns_zone_group {
    name    = "BlobPrivateDnsZoneGroup"
    private_dns_zone_ids     = [var.privated_dns_zone_id]
  
  }
  
}



