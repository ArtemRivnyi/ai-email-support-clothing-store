variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

variable "gemini_api_key" {
  description = "API Key for Google Gemini"
  type        = string
  sensitive   = true
}

variable "openai_api_key" {
  description = "API Key for OpenAI"
  type        = string
  sensitive   = true
}

variable "master_api_key" {
  description = "Master API Key for external webhook integrations"
  type        = string
  sensitive   = true
  default     = "super-secure-production-key-123"
}

variable "jwt_secret" {
  description = "Secret key for JWT generation"
  type        = string
  sensitive   = true
  default     = "production-jwt-secret-do-not-share"
}
