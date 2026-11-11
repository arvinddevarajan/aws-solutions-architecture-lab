
# ADR-001: IAM Access Strategy for ECS Applications

- **Status:** Accepted (initial lab design)
- **Date:** 2026-11-10

## Context

An enterprise document-processing application running on Amazon ECS
requires access to confidential documents stored in Amazon S3.

The design must:
- Restrict access to necessary S3 objects.
- Avoid long-lived AWS credentials.
- Prevent unnecessary developer access.
- Support auditing of document access.

## Decision

Use an IAM task role for the ECS application with least-privilege
permissions scoped to the required S3 objects.

ECS provides temporary AWS credentials to running tasks.
No permanent credentials will be stored in application code.

## Alternatives Considered

| Option | Decision | Reason |
|---|---|---|
| IAM user access keys | Rejected | Long-lived credential management |
| ECS task role | Selected | Temporary credentials and scoped permissions |
| AdministratorAccess | Rejected | Excessive permissions |
| Public S3 bucket | Rejected | Confidentiality risk |

## Consequences

### Benefits
- Reduces credential exposure.
- Enforces least-privilege access.
- Supports temporary credentials.
- Enables auditing when CloudTrail S3 data events are configured.

### Trade-offs
- IAM policies require maintenance.
- Permissions must evolve with application requirements.
- Application-level vulnerabilities can still misuse granted permissions.

## Implementation Notes

- Configure an ECS task role and appropriate trust policy.
- Grant `s3:GetObject` to the required object ARNs.
- Keep S3 Block Public Access enabled.
- Separate task roles from task execution roles.
- Enable CloudTrail S3 data events when object-level auditing is required.
- Use separate development and production permissions.

## Review Triggers

Revisit this decision when:
- Migrating to a different compute platform.
- Introducing additional AWS services.
- Changing security or compliance requirements.
