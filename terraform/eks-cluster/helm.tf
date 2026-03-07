resource "helm_release" "ai_email_support" {
  name       = "ai-email-support"
  chart      = "../../k8s/ai-email-support"
  namespace  = "ai-email-support"
  create_namespace = true

  # Wait for the EKS cluster to be active before deploying
  depends_on = [module.eks]

  set {
    name  = "secret.geminiApiKey"
    value = var.gemini_api_key
  }

  set {
    name  = "secret.openaiApiKey"
    value = var.openai_api_key
  }

  set {
    name  = "secret.masterApiKey"
    value = var.master_api_key
  }

  set {
    name  = "secret.jwtSecret"
    value = var.jwt_secret
  }

  set {
    name  = "api.replicaCount"
    value = "2" # Example of overriding values for production
  }
}
