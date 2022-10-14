#===========================================================================================================
#      FILE NAME: modules/storage_account/output.tf
#      USAGE: To output required values
#      VERSION: 1.0
#      AUTHOR: Sahana Gajanana Acharya
#      DEPARTMENT: Platform Team
#===========================================================================================================

output "storage_account_id" {
  description = "The ID of storage account"
  value = azurerm_storage_account.storage_account.id
}
output "primary_blob_endpoint" {
  description = "The endpoint URL for blob storage in the primary location."
  value = azurerm_storage_account.storage_account.primary_blob_endpoint
}
output "primary_file_endpoint" {
  description = "The endpoint URL for file storage in the primary location."
  value = azurerm_storage_account.storage_account.primary_file_endpoint
}
output "primary_queue_endpoint" {
  description = "The endpoint URL for queue storage in the primary location."
  value = azurerm_storage_account.storage_account.primary_queue_endpoint
}
output "primary_table_endpoint" {
  description = "The endpoint URL for table storage in the primary location." 
  value = azurerm_storage_account.storage_account.primary_table_endpoint
}