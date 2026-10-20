# Threat model

## Assets and boundaries

Assets include organization control plane, account membership, identity assignments, CloudTrail/Config history, KMS keys, archive objects, Terraform state and future CI identity. Trust boundaries are developer workstation, source control CI, management/security/log archive accounts, AWS Organizations delegated services, and archive storage.

## Threats and controls

| Threat | Reference mitigation | Residual work |
|---|---|---|
| Unauthorized CI role assumption | Narrow sample GitHub OIDC subject/audience | Provision no role here; bind exact repo/ref/environment and least privilege |
| Audit trail tampering | Example SCP denies selected stop/delete/update operations | SCP can disrupt operators/services; test exceptions and recovery path |
| Evidence disclosure/deletion | Public access block, TLS denial, versioning, KMS, prevent_destroy | Add service delivery policy, Object Lock/retention, replication and tested recovery |
| State leakage | No backend/state configured | Choose encrypted, access-controlled backend and locking before init |
| Provider/module supply chain | No external modules | Pin reviewed providers/actions and verify checksums/releases |
| Human lockout | No automatic SCP attachment in environment | Simulate policy, preserve tested break-glass identity, staged rollout |

This document is a design aid, not a compliance attestation or deployed-control claim.
