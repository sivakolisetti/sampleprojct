#===============================================================================
#      FILE NAME: output.tf
#      USAGE: To output required values
#      VERSION: 1.0
#      AUTHOR: Sahana Gajanana Acharya
#      DEPARTMENT: Platform Team
#===============================================================================

output "storage_account_id"{
  description = "The id of storage account."
  value = module.storage_account.storage_account_id
}
