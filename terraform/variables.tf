variable "cloudwatch_group" {
  type = string
  default = "rent-service"
}

variable "name_prefix" {
  description = "Name prefix of each resources"
  type = string
  default = "rent-service"
}

variable "LINE_TOKEN" {
  type = string
  default = "line_token"
}

variable "YU_LINE_TOKEN" {
  type = string
  default = "yu_line_token"
}
