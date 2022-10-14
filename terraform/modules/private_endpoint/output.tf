#===========================================================================================================
#      FILE NAME: modules/private_endpoint/output.tf
#      USAGE: To output required values
#      VERSION: 1.0
#      AUTHOR: Sahana Gajanana Acharya
#      DEPARTMENT: Platform Team
#===========================================================================================================

output "private_endpoint_id" {
  description = "The ID of private endpoint"
  value = azurerm_private_endpoint.private_endpoint.id
}

output "private_endpoint_name" {
  description = "The name of private endpoint"
  value = azurerm_private_endpoint.private_endpoint.name
}