
# ADR-002: Application Configuration, Logging, and Error Handling

## Status
Accepted

## Context

The AWS S3 presigned URL application requires reliable configuration management, consistent logging, and predictable error handling.

Without these controls, invalid configuration, expired AWS credentials, and AWS API failures can lead to unexpected application behavior and difficult troubleshooting.

## Decision

### 1. Centralized Configuration Management

- Load application settings from environment variables.
- Use a frozen Python dataclass to represent application configuration.
- Validate required configuration values before making AWS API requests.
- Exclude local `.env` files from version control.

### 2. Structured Logging

- Use Python's built-in logging framework.
- Format application logs as JSON.
- Include timestamps, severity levels, service names, and messages.
- Avoid logging AWS credentials, tokens, or presigned URLs.

### 3. Exception Handling

- Handle configuration validation errors explicitly.
- Distinguish AWS authentication failures from AWS service errors.
- Return nonzero exit codes when application execution fails.
- Provide actionable error messages without unnecessarily exposing sensitive information.

### 4. AWS Authentication

- Use temporary AWS credentials for local development.
- Use AWS IAM roles for applications deployed on AWS.
- Avoid hardcoding AWS access keys or secrets in application source code.

## Alternatives Considered

### Hardcoded Configuration
Rejected because it reduces portability and increases security risks.

### Unstructured Logging
Rejected because plain-text logs are less convenient for automated searching, filtering, and analysis.

### Generic Exception Handling
Rejected because catching all exceptions without distinguishing failure types makes troubleshooting more difficult.

### Long-Lived AWS Access Keys
Not selected because temporary credentials reduce the risks associated with persistent credentials.

## Consequences

### Benefits

- Early detection of invalid application configuration.
- Consistent, machine-readable application logs.
- Improved troubleshooting and operational visibility.
- Better separation between application code and environment-specific settings.
- Reduced risk of exposing sensitive AWS credentials.

### Trade-offs

- Additional configuration and logging code.
- More exception-handling logic to maintain.
- JSON logs require compatible log collection and analysis tools.
- AWS SDK internal diagnostic messages may still require separate filtering.

## Future Improvements

- Implement automated unit tests.
- Introduce request correlation IDs.
- Add application execution metrics.
- Integrate application logs with Amazon CloudWatch.
- Implement least-privilege IAM permissions.
- Add automated security checks in CI/CD.

## Related Decisions

- ADR-001: IAM Access and Authentication
