# Decisions log

## Block 0 (2026-09-08)

### D1. Scaffold lives in an existing repository; no nested `git init`
Block 0 Step 2 says "git init; first commit". The session's binding branch
requirement is to develop and push on `claude/stock-picker-scaffold-probe-1eccnt`
in `fredcover33/foundryonesciences`, which is already a git repository. Running
`git init` inside it would create an embedded repository whose commits could not
be pushed to that branch. The scaffold was therefore created as the
`stock-picker/` subdirectory of the existing repository and committed to the
designated branch. Reported to Fred as a divergence.

### D2. Step 3 documentation survey BLOCKED — massive.com denied by egress policy
Every documentation URL required by Step 3 is unreachable from this session.
The denial is at the organization egress proxy (HTTP 403 to CONNECT), not at
massive.com, and it is not host-specific to massive.com: a control request to
example.com is denied identically, i.e. general outbound web access is off for
this session.

Evidence, verbatim:

    $ curl -sS -o /dev/null -w "%{http_code}\n" https://massive.com/docs/llms.txt
    curl: (56) CONNECT tunnel failed, response 403
    000

    $ curl -sS -o /dev/null -w "example.com -> HTTP %{http_code}\n" https://example.com
    curl: (56) CONNECT tunnel failed, response 403
    example.com -> HTTP 000

    $ curl -sS "$HTTPS_PROXY/__agentproxy/status"
    ...
    "recentRelayFailures": [
        {
          "ts": "2026-09-08T10:36:53.510Z",
          "kind": "connect_rejected",
          "detail": "gateway answered 403 to CONNECT (policy denial or upstream failure)",
          "host": "massive.com:443"
        }
    ]

The harness's own fetch tool uses a separate egress path and is denied too:

    WebFetch https://massive.com/docs/llms.txt
    -> {"error_type":"EGRESS_BLOCKED","domain":"massive.com",
        "message":"Access to massive.com is blocked by the network egress proxy."}

The proxy's own documentation (/root/.ccr/README.md) states of this failure
class: "The destination host is not allowed by your organization's egress
policy for this session. Do not retry or route around it — report the blocked
host."

Consequence: `docs/DATA_SOURCES.md` is left EMPTY. Conduct rule 1 forbids
supplying the S3 endpoint, bucket prefixes, path formats, column lists,
timestamp units, plan access/history/recency tables, prices, or pre-market
coverage from anywhere other than a page actually fetched in this session.
None was fetched, so none is recorded. No substitute data source was used
(conduct rule 5).

Unblocking requires either an egress-policy allowance for `massive.com` in
this environment, or Fred supplying the documentation content directly.

## Block 0-R (2026-09-08)

### D3. Step 2 egress verification FAILED — massive.com still denied
Block 0-R states egress is restored. It is not, in this session. The
verification required by Step 2 was run and refused, on both available egress
paths, in a container distinct from the Block 0 one (the agent proxy's local
port changed from 36541 to 41941, i.e. a new container process, so this is not
a stale result carried over).

    $ curl -sS -w "\n[HTTP %{http_code}] [%{size_download} bytes]\n" \
        -o .../llms.txt https://massive.com/docs/llms.txt
    curl: (56) CONNECT tunnel failed, response 403
    [HTTP 000] [0 bytes]

    $ curl -sS "$HTTPS_PROXY/__agentproxy/status"
      "recentRelayFailures": [
        {
          "ts": "2026-09-08T11:03:57.051Z",
          "kind": "connect_rejected",
          "detail": "gateway answered 403 to CONNECT (policy denial or upstream failure)",
          "host": "massive.com:443"
        }
      ]

    $ curl -sS -o /dev/null -w "example.com -> HTTP %{http_code}\n" https://example.com
    curl: (56) CONNECT tunnel failed, response 403
    example.com -> HTTP 000

    WebFetch https://massive.com/docs/llms.txt
    -> {"error_type":"EGRESS_BLOCKED","domain":"massive.com",
        "message":"Access to massive.com is blocked by the network egress proxy."}

The control request to example.com is refused identically, so this is not a
massive.com-specific rule: general outbound web access is off for this session.
The denial is issued by the organization egress gateway at CONNECT time,
before any URL path is seen, so the ".md variant first" instruction in Step 3
is untestable — no path on that host resolves.

Steps 3 onward are not attempted. docs/DATA_SOURCES.md remains EMPTY: conduct
rule 1 forbids recording an endpoint, prefix, column list, timestamp unit, plan
table, price or licensing term from anywhere but a page actually fetched here.

### D4. GIVEN FACTS F1-F4 are recorded as UNVERIFIED
Conduct rule 10 requires F1-F4 be verified against the documentation, and that
any difference be reported and stopped on. No documentation could be fetched,
so every VERIFY in Step 3 returns NOT VERIFIED — neither confirmed nor
contradicted. F1-F4 are carried forward as Fred's instruction only. In
particular F2 (plan access and history) and F3 (directory sizes) remain
unchecked, and F5 warns those tables render with headings offset from their
values, which is exactly the kind of error a second reading exists to catch.

### D5. config.toml updated to the Block 0-R schema
`probe.trades_parse_sample_rows` was replaced by
`probe.trades_stream_sample_seconds = 60`; REQUIRED_KEYS in src/picker/config.py
was updated to match. This does not depend on egress, so it was completed
before stopping. Verified: deleting each required key in turn yields the
mandated message.
