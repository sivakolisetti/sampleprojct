#====================================================================================================================
#      FILE NAME: modules/storage_account/variables.tf
#      USAGE: Specifies required variables for the resource block specified in modules/storage_account/main.tf
#      VERSION: 1.0
#      AUTHOR: Sahana Gajanana Acharya
#      DEPARTMENT: Platform Team
#=====================================================================================================================

variable "name" {
  description = "(Required) Specifies the name of the storage account"
  type        = string
  default = ""
}

variable "resource_group_name" {
  description = "(Required) Specifies the resource group name of the storage account"
  type        = string
  default = ""
}

variable "location" {
  description = "(Required) Specifies the location of the storage account"
  type        = string
  default = ""
}

variable "account_kind" {
  description = "(Optional) Specifies the account kind of the storage account"
  default     = "StorageV2"
  type        = string

   validation {
    condition = contains(["Storage", "StorageV2"], var.account_kind)
    error_message = "The account kind of the storage account is invalid."
  }
}

variable "account_tier" {
  description = "(Optional) Specifies the account tier of the storage account"
  default     = "Standard"
  type        = string

   validation {
    condition = contains(["Standard", "Premium"], var.account_tier)
    error_message = "The account tier of the storage account is invalid."
  }
}

variable "replication_type" {
  description = "(Optional) Specifies the replication type of the storage account"
  default     = "LRS"
  type        = string

  validation {
    condition = contains(["LRS", "ZRS", "GRS", "GZRS", "RA-GRS", "RA-GZRS"], var.replication_type)
    error_message = "The replication type of the storage account is invalid."
  }
}
variable "is_hns_enabled" {
  description = "(Optional) Specifies the replication type of the storage account"
  default     = false
  type        = bool
}

variable "tags" {
  description = "(Optional) Specifies the tags"
  default     = {}
}

variable "ip_rules" {
    description = "Specifies IP rules for the storage account"
    default     = []
    type        = list(string)  
}
variable "vm_subnet_id" {
  description = "Specifies the vn subnet id"
  default     = ""
}
