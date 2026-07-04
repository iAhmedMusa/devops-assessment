output "cluster_log_group_name" {
  description = "CloudWatch log group name for the EKS control plane."
  value       = aws_cloudwatch_log_group.cluster.name
}

output "application_log_group_name" {
  description = "CloudWatch log group name for application logs."
  value       = aws_cloudwatch_log_group.application.name
}
