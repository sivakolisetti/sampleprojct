#===================================================================================================
#      FILE NAME: variables.tf
#      USAGE: Specifies required variables for the data blocks and modules specified in main.tf
#      VERSION: 1.0
#      AUTHOR: Sahana Gajanana Acharya
#      DEPARTMENT: Platform Team
#===================================================================================================

variable "storage_account_name" {
  description = "Specifies the storage account name"
  default     = ""
  type        = string
}

variable "location" {
  description = "Specifies the location for the resource group and all the resources"
  default     = "westeurope"
  type        = string
}

variable "tags" {
  description = "(Optional) Specifies tags for all the resources"
  default     = ""
}

variable "resource_group_name" {
  description = "Specifies the resource group name"
  default     = ""
  type        = string
}

variable "storage_account_kind" {
  description = "(Optional) Specifies the account kind of the storage account"
  default     = "StorageV2"                     #provides all storage services(blob,queue,tables,files)
  type        = string

   validation {
    condition = contains(["Storage", "StorageV2"], var.storage_account_kind)
    error_message = "The account kind of the storage account is invalid."
  }
}

variable "storage_account_tier" {
  description = "(Optional) Specifies the account tier of the storage account"
  default     = "Standard"
  type        = string

   validation {
    condition = contains(["Standard", "Premium"], var.storage_account_tier)
    error_message = "The account tier of the storage account is invalid."
  }
}

variable "storage_account_replication_type" {
  description = "(Optional) Specifies the replication type of the storage account"
  default     = "LRS"
  type        = string

  validation {
    condition = contains(["LRS", "ZRS", "GRS", "GZRS", "RA-GRS", "RA-GZRS"], var.storage_account_replication_type)
    error_message = "The replication type of the storage account is invalid."
  }
}
variable "spoke_vnet" {
  description = "Specifies the spoke vnet name"
  default     = ""
}
variable "vm_subnet" {
  description = "Specifies the vn subnet name"
  default     = ""
}
variable "blob_private_endpoint" {
  type        = string
  description = "Private Endpoint Name"
  default = ""
}
variable "hub_sub_id" {
  type        = string
  description = "hub Subscription Id"
  default = ""
}
variable "hub_rg_dns_zone" {
  type        = string
  description = "rg name where dns zone exists"
  default = ""
}

variable "private_dns_zone_name" {
  type        = string
  description = "Private DNS zone name for blob storage existing in hub"
  default = "privatelink.blob.core.windows.net"
}