# ADR-001: IAM Access Strategy for ECS Applications

**Status:** Accepted (initial lab design)

**Date:** 2026-11-10

## 1. Context

We are designing an enterprise document-processing application running on Amazon ECS. The application needs to retrieve confidential documents stored in Amazon S3.

The architecture must satisfy the following requirements:

- Restrict application access to required S3 objects.
- Avoid storing permanent AWS access keys in application code.
- Prevent unnecessary developer access to production documents.
- Support auditing of document access.

## 2. Decision

We will use an **IAM task role for Amazon ECS**, with an IAM policy granting only the required S3 read permissions.

The ECS task will use temporary AWS credentials associated with the task role.

The application will not store permanent AWS credentials in source code or configuration files.

## 3. Alternatives Considered

### Option A: IAM User with Access Keys

Rejected because long-lived credentials require secure storage, rotation, and lifecycle management.

### Option B: IAM Task Role

Selected because it supports temporary credentials and granular access permissions without requiring embedded access keys.

### Option C: AdministratorAccess

Rejected because unrestricted permissions violate least-privilege principles.

### Option D: Public S3 Bucket

Rejected because making confidential documents publicly readable creates unacceptable exposure risks.

## 4. Consequences and Trade-offs

**Benefits:**
- Reduced risk of credential exposure.
- Permissions scoped to required S3 operations.
- AWS-managed temporary credential delivery.
- Access can be audited through CloudTrail when relevant S3 data events are enabled.

**Trade-offs:**
- IAM policies and role trust relationships require configuration and maintenance.
- Permissions must be updated when application responsibilities change.
- Temporary credentials do not eliminate application vulnerabilities or unauthorized use of the role.

## 5. Implementation Considerations

- Create an ECS task role with the appropriate ECS task-role trust relationship.
- Grant `s3:GetObject` only for the necessary object ARNs.
- Keep S3 Block Public Access enabled.
- Separate application task permissions from ECS task execution permissions.
- Configure CloudTrail S3 data events for required audit coverage.
- Use separate roles and policies for development and production environments.

## 6. Review Trigger

Revisit this decision if the application moves to another compute service, requires new AWS permissions, or introduces additional security and compliance requirements.