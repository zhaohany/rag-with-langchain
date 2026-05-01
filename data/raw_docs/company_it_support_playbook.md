# Company IT Support Playbook

This playbook is used by internal IT support teams to triage, troubleshoot, and escalate issues.
It is intentionally detailed so we can use one real-looking document for ingest and chunking tests.

## Access and Identity Support

Identity incidents are high-impact because they block core work. Always verify user identity before
changing credentials, MFA devices, or permissions. For every request, record request channel,
employee ID, manager confirmation (if required), and exact action taken.

### Password Reset

If a user cannot sign in, start with self-service reset and confirm they are using the corporate
identity domain. If reset email is delayed, verify mailbox health, spam filtering, and mail routing
before manually resetting from admin console. For manual reset, enforce temporary password policy,
force password change at next login, and confirm account is not simultaneously locked by conditional
access policy.

### MFA and Authenticator Issues

For MFA failures, identify whether the problem is push notification delay, device clock drift,
authenticator app corruption, or SIM / number migration. If using TOTP, require user to sync device
time and re-scan seed where policy allows. If using push-based approval, check notification settings,
battery optimization, background app restrictions, and corporate MDM profile state.

### Account Lockout

When account lockout repeats, collect lockout event timeline and source IP/device names. Most repeated
lockouts come from stale credentials in mobile mail clients, mapped network drives, legacy scripts,
or old VPN profiles. Clear cached credentials in keychain/credential manager and rotate service
account secrets if automation is involved.

## VPN and Remote Access

Remote access incidents are common during travel and policy updates. Confirm user location,
network type (home/cellular/hotel), VPN client version, and recent OS updates before deep diagnosis.

### VPN Cannot Connect

Check whether failure occurs at DNS resolution, TCP handshake, authentication, or tunnel negotiation.
Validate endpoint URL, certificate trust chain, and system clock. If TLS handshake fails, compare
device root certificates against baseline image. If auth succeeds but tunnel fails, inspect split
tunnel policy, MTU mismatch, and endpoint security posture checks.

### VPN Connected but Internal Tools Unreachable

If VPN shows connected status but internal apps fail, test reachability in layers: internal DNS,
gateway ping, private HTTP endpoint, and target service health. Confirm split-tunnel routes include
required subnets and that local firewall does not block assigned virtual interface. Verify no conflict
with overlapping home LAN CIDR ranges.

### VPN Client or Certificate Drift

After certificate renewal windows, users may hold expired client certificates in system keychain.
Remove stale certs, reinstall managed profile, and restart network stack. If client version is behind
minimum supported build, upgrade first before escalation.

## Network and Internet Issues

Network reports should capture time, location, affected services, and whether issue reproduces on
multiple devices. Distinguish local device faults from office-wide incidents.

### No Internet in Office

Verify link lights on access switch, DHCP lease assignment, gateway reachability, and DNS response.
If only one VLAN is affected, inspect recent ACL or segmentation policy changes. For widespread outage,
trigger network incident bridge and publish status page update.

### Slow Internet and Packet Loss

Measure baseline latency and jitter to approved internal and external targets. Compare wired vs Wi-Fi,
2.4 GHz vs 5 GHz, and peak-hour congestion patterns. Validate AP channel overlap, rogue AP presence,
and QoS policy drift. Collect traceroute and packet capture when loss is intermittent.

### DNS and Proxy Misconfiguration

If users can access by IP but not hostname, test resolver chain and search domains. For proxy issues,
verify PAC file delivery, proxy auth token validity, and bypass rules for internal domains.

## Endpoint Device Support

Device support should balance speed and data safety. Before invasive fixes, confirm backup status and
business criticality of local files.

### Performance Degradation

Collect CPU, memory, disk IO, and thermal metrics. Check startup items, background sync tools,
browser extensions, endpoint security scans, and pending OS patches. If disk free space is under
threshold, run cleanup workflow and move large archives to approved storage.

### Startup Failures and OS Crashes

For repeated crashes, collect crash logs and recent driver or kernel updates. Boot in safe mode,
isolate third-party kernel extensions, and test with clean user profile. If hardware diagnostics show
memory or disk errors, replace components based on warranty matrix.

### Storage and File System Errors

If users report missing files or corruption, stop write-heavy operations immediately. Validate disk
SMART status, run file system checks, and restore from snapshots where available. Escalate to security
if ransomware indicators appear.

## Email and Collaboration Tools

Communication outages impact many teams quickly. Prioritize broad incidents and publish temporary
workarounds while root cause analysis continues.

### Email Send and Receive Failures

Confirm whether issue is sender-specific, domain-specific, or global. Inspect outbound queue,
mail relay health, spam quarantine, and connector certificates. For delayed delivery, correlate
with upstream provider incidents and retry policy behavior.

### Calendar Sync and Meeting Issues

If calendar updates are delayed, check client cache state, mobile sync policy, and API throttling.
For recurring meetings with wrong timezone, validate organizer timezone settings and daylight-saving
policy updates.

### Chat Platform Connectivity

When chat tools are unreachable, validate websocket connectivity, proxy compatibility, and firewall
rules for required domains and ports. For voice/video degradation, capture MOS metrics and packet loss.

## Business Application Access

Application access issues usually involve IAM groups, environment mismatch, or stale role claims.

### ERP and CRM Permission Denied

Verify user role mapping from HR source of truth through IAM sync to application ACLs. Confirm user is
in correct cost center and department attributes are current. If role propagation is delayed, trigger
manual sync and re-authenticate.

### SSO Redirect Loop

SSO loops often come from cookie domain mismatch, clock skew, or conflicting browser profiles.
Clear session cookies for target domains, verify IdP app config, and test with fresh browser profile.

### Environment-Specific Access Problems

Check whether user is routed to production, staging, or sandbox by URL and role policy. Ensure intended
environment is included in authorization claim and that VPN route allows target environment subnet.

## Security Incident Triage

Security-related tickets require strict chain of custody and timeline logging.

### Phishing Report

Collect original message headers, sender envelope, link targets, and attachment hashes. Quarantine
similar messages tenant-wide where tooling supports bulk action. Notify security operations with IOC
bundle and affected user list.

### Suspicious Login Alert

Validate impossible travel patterns, unusual device fingerprints, and abnormal session duration.
If compromise is likely, force sign-out, rotate credentials, revoke refresh tokens, and review
privileged actions during suspect window.

### Malware Containment

Isolate host from network, preserve forensic artifacts, and avoid reboot unless directed by incident
response lead. Coordinate with endpoint security tooling for scan, quarantine, and reimage decision.

## Escalation and Handoff

Escalate with complete context to reduce ping-pong between teams.

### Severity Matrix

Use standardized severity levels:
- Sev 1: company-wide outage or critical security event
- Sev 2: multi-team impact with major workflow blocked
- Sev 3: single-team issue with workaround available
- Sev 4: individual issue, low urgency

### Required Escalation Package

Every escalation should include:
- business impact summary
- reproduction steps
- timestamps with timezone
- affected users and geographies
- logs, screenshots, and command outputs already collected
- mitigation attempted and result

### Post-Incident Review

For Sev 1 and Sev 2 incidents, run post-incident review within five business days. Document timeline,
root cause, contributing factors, corrective actions, owners, and due dates. Feed recurring failure
patterns back into this playbook.

## Long Structured Section for Chunking Stress Test

This section is intentionally long to test recursive chunking behavior with H2 and H3 boundaries.
It includes multiple dense paragraphs so students can verify: H2 split first, then H3 split,
then fallback to naive chunking when any H3 block remains oversized.

### Large Procedure Block A

Step 1: Gather user report details with exact timestamps, local timezone, network context, and device
identifiers. Step 2: Verify identity and authorization for support actions. Step 3: Reproduce issue
in a controlled environment where possible. Step 4: Check service dashboards for correlated alerts.
Step 5: Compare user environment baseline against golden configuration. Step 6: Test smallest-risk
mitigation first. Step 7: Document outcomes in ticket before moving to next action. Step 8: If issue
persists, gather logs and metrics with retention-safe process. Step 9: Evaluate incident scope and
potential blast radius. Step 10: Escalate with complete package when threshold is met.

### Large Procedure Block B

When root cause is uncertain, use hypothesis-driven triage. Build three likely hypotheses and define
what evidence confirms or disproves each one. Run low-risk tests in sequence, capture command output,
and avoid changing multiple variables at once. If a workaround restores service, mark state as
mitigated and continue root cause analysis until permanent fix is defined. Track rollback plan for
every change, including owner and verification criteria. Close incident only after user validation,
monitoring stabilization, and knowledge base updates.

### Large Procedure Block C

For recurring incidents, correlate by team, region, application, and time window. Identify whether
failure pattern aligns with deployments, certificate rotation windows, identity policy updates,
endpoint agent upgrades, or network maintenance. Convert repeated manual actions into runbooks and
automation where safe. Ensure support handoff notes include pending risks and next checkpoints.
