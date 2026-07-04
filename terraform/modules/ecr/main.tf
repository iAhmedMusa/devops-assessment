# IMMUTABLE tags tie directly to the pipeline's no-`latest` policy
# (docs/ci-cd.md, section 3): once a tag is pushed it can never be
# overwritten, so a tag always points at exactly one image forever, in ECR
# just as it already does on Docker Hub.
resource "aws_ecr_repository" "this" {
  for_each             = toset(var.repository_names)
  name                 = "${var.name_prefix}-${each.value}"
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  encryption_configuration {
    encryption_type = "AES256"
  }

  tags = merge(var.tags, {
    Name = "${var.name_prefix}-${each.value}"
  })
}

# Keep the last 20 tagged images (enough history for rollback without
# unbounded storage growth) and expire untagged images after 7 days
# (dangling layers from superseded builds -- safe to reclaim quickly since
# nothing running references an untagged image).
resource "aws_ecr_lifecycle_policy" "this" {
  for_each   = aws_ecr_repository.this
  repository = each.value.name

  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Keep last 20 tagged images"
        selection = {
          tagStatus     = "tagged"
          tagPrefixList = ["v"]
          countType     = "imageCountMoreThan"
          countNumber   = 20
        }
        action = {
          type = "expire"
        }
      },
      {
        rulePriority = 2
        description  = "Expire untagged images after 7 days"
        selection = {
          tagStatus   = "untagged"
          countType   = "sinceImagePushed"
          countUnit   = "days"
          countNumber = 7
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
}
