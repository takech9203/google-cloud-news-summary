#!/usr/bin/env bash
# Deploy OIDC provider and IAM role for Google Cloud News Summary CI/CD.
#
# Usage:
#   # GitHub Actions (role: GitHubActions-GoogleCloudNewsSummary, stack: google-cloud-news-summary-github-iam)
#   ./scripts/deploy-iam.sh -o myorg -r google-cloud-news-summary
#
#   # Custom role name and region
#   ./scripts/deploy-iam.sh -o myorg -r google-cloud-news-summary -n MyRole -R us-west-2
#
#   # Use existing OIDC provider
#   ./scripts/deploy-iam.sh -o myorg -r google-cloud-news-summary -p arn:aws:iam::123456789012:oidc-provider/token.actions.githubusercontent.com

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
STACK_NAME="google-cloud-news-summary-github-iam"
REGION="us-east-1"
ROLE_NAME="GitHubActions-GoogleCloudNewsSummary"
GITHUB_ORG=""
GITHUB_REPO=""
OIDC_PROVIDER_ARN=""

usage() {
  cat <<EOF
Usage: $0 -o ORG -r REPO [OPTIONS]

Required:
  -o, --org ORG               GitHub owner/org
  -r, --repo REPO             GitHub repository name

Optional:
  -n, --role-name NAME        IAM role name (default: GitHubActions-GoogleCloudNewsSummary)
  -s, --stack-name NAME       CloudFormation stack name (default: google-cloud-news-summary-github-iam)
  -R, --region REGION         AWS region (default: us-east-1)
  -p, --oidc-provider-arn ARN Existing OIDC Provider ARN (auto-detected if not specified)
  -h, --help                  Show this help

Examples:
  # Auto-detect existing OIDC provider or create new one
  $0 -o myorg -r google-cloud-news-summary

  # Explicitly specify OIDC provider ARN
  $0 -o myorg -r google-cloud-news-summary \\
    -p arn:aws:iam::123456789012:oidc-provider/token.actions.githubusercontent.com

Note:
  The script automatically checks for existing GitHub OIDC provider.
  If found, it will be used. Otherwise, a new provider will be created.
  Use -p option to override auto-detection.
EOF
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -o|--org)                GITHUB_ORG="$2"; shift 2 ;;
    -r|--repo)               GITHUB_REPO="$2"; shift 2 ;;
    -n|--role-name)          ROLE_NAME="$2"; shift 2 ;;
    -s|--stack-name)         STACK_NAME="$2"; shift 2 ;;
    -R|--region)             REGION="$2"; shift 2 ;;
    -p|--oidc-provider-arn)  OIDC_PROVIDER_ARN="$2"; shift 2 ;;
    -h|--help)               usage ;;
    *)                       echo "Error: Unknown option: $1"; usage ;;
  esac
done

# Validate
if [[ -z "$GITHUB_ORG" ]]; then
  echo "Error: -o/--org is required."
  usage
fi

if [[ -z "$GITHUB_REPO" ]]; then
  echo "Error: -r/--repo is required."
  usage
fi

TEMPLATE="${SCRIPT_DIR}/cfn-github-oidc-iam.yaml"
PARAMS="RoleName=${ROLE_NAME} GitHubOrg=${GITHUB_ORG} GitHubRepo=${GITHUB_REPO}"

# Auto-detect existing OIDC provider if not specified
if [[ -z "$OIDC_PROVIDER_ARN" ]]; then
  echo "Checking for existing GitHub OIDC provider..."
  DETECTED_ARN=$(aws iam list-open-id-connect-providers \
    --region "$REGION" \
    --query 'OpenIDConnectProviderList[?contains(Arn, `token.actions.githubusercontent.com`)].Arn' \
    --output text 2>/dev/null || echo "")

  if [[ -n "$DETECTED_ARN" ]]; then
    OIDC_PROVIDER_ARN="$DETECTED_ARN"
    echo "Found existing OIDC provider: ${OIDC_PROVIDER_ARN}"
  else
    echo "No existing OIDC provider found. Will create new one."
  fi
fi

if [[ -n "$OIDC_PROVIDER_ARN" ]]; then
  PARAMS="${PARAMS} OIDCProviderArn=${OIDC_PROVIDER_ARN}"
fi

echo "=== Google Cloud News Summary IAM Setup ==="
echo "Platform: GitHub Actions"
echo "Repo:     ${GITHUB_ORG}/${GITHUB_REPO}"
echo "Stack:    ${STACK_NAME}"
echo "Region:   ${REGION}"
echo "Role:     ${ROLE_NAME}"
if [[ -n "$OIDC_PROVIDER_ARN" ]]; then
  echo "OIDC:     ${OIDC_PROVIDER_ARN} (existing)"
else
  echo "OIDC:     Will create new provider"
fi
echo ""

export AWS_PAGER=""

echo "Deploying CloudFormation stack..."
aws cloudformation deploy \
  --template-file "$TEMPLATE" \
  --stack-name "$STACK_NAME" \
  --region "$REGION" \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides $PARAMS

echo ""
echo "=== Stack Outputs ==="
aws cloudformation describe-stacks \
  --stack-name "$STACK_NAME" \
  --region "$REGION" \
  --query 'Stacks[0].Outputs[*].[OutputKey,OutputValue]' \
  --output table

echo ""
echo "Done. Set the RoleArn above as AWS_ROLE_ARN in your GitHub Actions variables."
