# PaySecure Gateway Multi-Region Disaster Recovery Architecture

## Executive Summary

PaySecure Gateway currently operates in a single AWS Mumbai region with 99.92% uptime. The target is 99.99% uptime by Q3 2026, with an RPO under 1 minute and RTO under 5 minutes. This architecture delivers a resilient, India-only multi-region solution using AWS Mumbai (`ap-south-1`) and AWS Hyderabad (`ap-south-2`).

Key design decisions:
- Active-active application and API plane across Mumbai and Hyderabad
- Active-passive Redis cache with automated failover for ElastiCache
- Aurora PostgreSQL Global Database for sub-minute replication
- DynamoDB Global Tables for multi-region writes and low-latency reads
- Apache Kafka with dual-cluster replication using MirrorMaker 2 for event continuity
- Route 53 latency-weighted failover and health checks
- Data localisation compliant with Indian regulatory requirements

## Architecture Goals

- RTO < 5 minutes for service continuity
- RPO < 1 minute for transactional data
- 99.99% availability across two Indian regions
- Regulatory compliance: RBI Payment Systems, PCI-DSS v4.0, NPCI UPI, India data localisation
- Operational readiness for region failure, partition, and peak volume events

## Target AWS Regions

- Primary: AWS Mumbai (`ap-south-1`)
- Secondary: AWS Hyderabad (`ap-south-2`)

Both regions are within India and satisfy data localisation mandates while enabling geographic redundancy.

## Core Architecture Components

### 1. Networking and Edge

- Amazon Route 53 with latency-based routing and health checks for global DNS failover.
- AWS WAF and AWS Shield Advanced protecting external payment endpoints.
- VPC peering and AWS PrivateLink for secure cross-region service connectivity.
- AWS Transit Gateway with inter-region peering for internal replication traffic.

### 2. Application Layer

- ECS Fargate / EKS in both regions, running identical PaySecure microservices.
- AWS Application Load Balancer in each region with cross-zone load balancing enabled.
- Active-active service routing for API traffic, supported by regional weights and health checks.
- Regional blue-green deployment pipelines with AWS CodePipeline / CodeDeploy.

### 3. API and Payment Gateway

- API Gateway for tokenized external endpoints in each region.
- Region-aware gateway endpoints using Route 53 health checks and failover.
- Mutual TLS and API key controls for merchant integrations.

### 4. Aurora PostgreSQL Strategy

- Primary cluster in Mumbai with Aurora Global Database replicating to Hyderabad.
- Aurora PostgreSQL Global DB configured for cross-region read replicas.
- Writer endpoint resides in Mumbai; Hyderabad offers fast read replica and recovery target.
- Promoted replica failover procedure for region failure.
- Continuous Backup to Amazon S3 with point-in-time recovery.

### 5. DynamoDB Strategy

- DynamoDB Global Tables spanning Mumbai and Hyderabad.
- Global Table replication configured for active-active writes in both regions.
- On conflict, use last-writer-wins with application-level reconciliation for payment idempotency.
- Secondary indexes in each region for local query performance.

### 6. ElastiCache Redis Strategy

- Primary ElastiCache Redis cluster in Mumbai with Global Datastore to Hyderabad.
- Active-passive topology ensures a single writable primary and a secondary read replica.
- Auto-failover and DNS endpoint swap to maintain RTO under 5 minutes.
- Cache warming and application-level retry logic for failover scenarios.

### 7. Apache Kafka Strategy

- AWS MSK cluster in Mumbai and AWS MSK cluster in Hyderabad.
- Dual-cluster active-active design using MirrorMaker 2 for topic replication.
- Critical payment event topics replicated with exactly-once semantics where possible.
- Consumer groups configured with geo-aware failover.
- Cross-region replication for transaction events, settlement events, fraud alerts, and audit streams.

### 8. Storage and Backup

- Amazon S3 for secure payment logs, settlement artifacts, and backups.
- S3 replication within India using `ap-south-1` to `ap-south-2` replication and encryption at rest.
- AWS Backup for centralized snapshot retention across Aurora, DynamoDB, and EFS.

### 9. Security and Compliance

- AWS KMS keys per region and cross-region key replication for crypto operations.
- Payment data encrypted in transit and at rest.
- PCI-DSS network segmentation, logging, and monitoring built into the architecture.
- Audit trails in AWS CloudTrail and AWS Config.

### 10. Observability and Automation

- Amazon CloudWatch metrics, alarms, dashboards, and cross-region dashboards.
- AWS X-Ray distributed tracing across both regions.
- Automated failover runbooks implemented through AWS Systems Manager Automation documents.
- AWS Config rules and GuardDuty for compliance monitoring.

## Component-Specific Replication

### Aurora PostgreSQL

- Global Database with sub-second replication for committed transaction metadata.
- Secondary region configured as a read-only Aurora replica for analytics and standby.
- Recovery procedure:
  1. Detect failover using CloudWatch `AuroraGlobalClusterStatus` and Route 53 health checks.
  2. Promote Hyderabad replica using `PromoteReadReplicaDBCluster`.
  3. Redirect application writer connections to Hyderabad writer endpoint.

### DynamoDB

- Multi-region active-active global tables across Mumbai and Hyderabad.
- Writes are accepted in both regions, minimizing latency for merchants across India.
- Conflict resolution uses a combination of DynamoDB conditional writes and application-level reconciliation.
- Global tables guarantee replication within seconds for operational metadata and merchant state.

### ElastiCache Redis

- Primary Redis cluster in Mumbai with Global Datastore replication to Hyderabad.
- Data replication uses asynchronous propagation and supports primary failover.
- Failover steps:
  1. Promote Hyderabad read replica to primary.
  2. Update application Redis endpoint to Hyderabad primary DNS alias.
  3. Validate data consistency with query and cache warming.

### Apache Kafka

- Dual MSK clusters in Mumbai and Hyderabad.
- MirrorMaker 2 replicates topics in both directions.
- Consumer applications subscribe to the local region cluster and fail over to remote cluster if local cluster becomes unavailable.
- Topic partition design is aligned with 45,000 merchants and transaction volume spikes.

## Deployment Pattern

- Use Infrastructure as Code (Terraform / CloudFormation) for reproducible environment creation.
- Deploy identical stacks in both regions.
- Use canary deployment pipelines in each region.
- Update DNS weights to shift traffic gradually during maintenance or failover.

## Failover Strategy

- Normal operation: active-active with weighted routing for Mumbai and Hyderabad.
- Regional outage: automatic Route 53 failover to healthy region.
- Database failover: Aurora promotion in secondary region, DynamoDB global table automatic conflict reconciliation, Kafka consumer failover.
- Cache failover: ElastiCache Global Datastore promotion to Hyderabad.

## Compliance and Risk Control

- RBI Master Direction on Payment Systems: ensures operational resilience and business continuity.
- PCI-DSS v4.0: segmentation, encryption, access control, incident response, and audit logging.
- NPCI UPI Technical Standards: transaction integrity, message-level security, and settlement audit.
- India data localisation: all payment data stays in Indian AWS regions; cross-region replication inside India only.

## Summary

This architecture delivers a resilient, compliant, India-only multi-region disaster recovery design for PaySecure Gateway. It supports the required uptime improvement, recovery targets, and regulatory controls needed for a payment aggregator serving tens of thousands of merchants.
