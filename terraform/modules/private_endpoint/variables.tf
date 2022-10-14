#=======================================================================================================================
#      FILE NAME: modules/private_endpoint/variables.tf
#      USAGE: Specifies required variables for the resource block specified in modules/private_endpoint/main.tf
#      VERSION: 1.0
#      AUTHOR: Sahana Gajanana Acharya
#      DEPARTMENT: Platform Team
#=======================================================================================================================

variable "blob_private_endpoint" {
  type        = string
  description = "Private Endpoint Name"
  default = ""
}
variable "location" {
  description = "(Required) Specifies the location of the storage account"
  type        = string
  default = ""
}
variable "resource_group_name" {
  description = "Specifies the resource group name"
  default     = ""
  type        = string
}
variable "vm_subnet_id" {
  description = "Specifies the vn subnet id"
  default     = ""
}
variable "tags" {
  description = "(Optional) Specifies tags for all the resources"
  default     = ""
}

variable "storage_account_name" {
  description = "Specifies the storage account name"
  default     = ""
  type        = string
}
variable "private_link_enabled_resource_id"{
  description = "storage_account_id"
  default = ""
}
variable "privated_dns_zone_id"{
  description = "id of private dns zone created in hub"
  default = ""
}

