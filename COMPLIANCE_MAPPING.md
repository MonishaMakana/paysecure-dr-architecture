# Compliance Mapping: PaySecure Gateway DR Architecture

This document maps each major design decision to relevant regulatory standards for Indian payment aggregators.

## RBI Master Direction on Payment Systems

1. Operational resilience
   - Multi-region deployment across `ap-south-1` and `ap-south-2` supports business continuity and disaster recovery.
   - Route 53 failover and health checks satisfy ongoing availability expectations.

2. Business continuity planning
   - 12 runbooks provide documented procedures for region failure, split-brain, and peak-load failover.
   - Systems Manager Automation documents and runbooks ensure recoverability within RTO < 5 minutes.

3. System integrity
   - Aurora Global Database and DynamoDB Global Tables provide consistent replication and transactional integrity.
   - Kafka replication ensures event continuity for settlement and fraud detection.

4. Data localisation
   - All data remains within India by using only AWS Mumbai and Hyderabad regions.
   - Cross-region replication is restricted to Indian regions only.

## PCI-DSS v4.0

1. Requirement 1: Network segmentation
   - Dedicated VPCs, subnet segmentation, and WAF protect the payment environment.

2. Requirement 3: Protect stored cardholder data
   - Aurora, DynamoDB, and S3 encryption at rest with AWS KMS.
   - Sensitive fields tokenized and stored with strict access controls.

3. Requirement 4: Encrypt transmission
   - TLS 1.2+ and mTLS for all merchant and internal traffic.

4. Requirement 6: Secure systems and applications
   - IaC with Terraform / CloudFormation and automated deployment pipelines.

5. Requirement 10: Logging and monitoring
   - CloudTrail, CloudWatch, GuardDuty, and AWS Config capture audit trails.

6. Requirement 11: Regular testing and incident response
   - DR runbooks, fire drills, and simulated failover exercises.

## NPCI UPI Technical Standards

1. Transaction integrity
   - Kafka replication of payment events and idempotent transaction processing.

2. Data confidentiality
   - End-to-end encryption on gateway APIs and secure storage of sensitive UPI metadata.

3. Settlement and reconciliation
   - Durable event streams and audit logs for settlement processing.

4. Availability
   - Active-active architecture and regional failover satisfy NPCI uptime expectations.

## India Data Localisation Requirements

- All payment-related data is stored and processed only within Indian AWS regions.
- AWS services selected are available in `ap-south-1` and `ap-south-2`.
- No cross-border replication or storage of regulated payment data outside India.

## Design Decisions Mapped to Standards

| Design Decision | RBI | PCI-DSS | NPCI UPI | Data Localisation |
|---|---|---|---|---|
| Multi-region active-active application | Yes | Yes | Yes | Yes |
| Aurora Global DB | Yes | Yes | Yes | Yes |
| DynamoDB Global Tables | Yes | Yes | Yes | Yes |
| ElastiCache Global Datastore | Yes | Yes | Yes | Yes |
| MSK MirrorMaker 2 | Yes | Indirect | Yes | Yes |
| Route 53 failover | Yes | Yes | Yes | Yes |
| CloudTrail / Config / GuardDuty | Yes | Yes | Yes | Yes |
| GitHub Pages documentation | No | No | No | N/A |

## Audit and Reporting

- Provide the Board with documented evidence that data residency is maintained.
- Use AWS Config and AWS CloudTrail exports for post-failure audits.
- Capture DR exercise results and remediation steps.

## Compliance Notes

- The architecture is designed for a payment aggregator; specific implementations should be reviewed by the compliance team before production.
- Reference the latest RBI circulars and NPCI Technical Standards at delivery time.
