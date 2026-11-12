"""
Trade-Bot security hardening layer (Part II: Cryptographic Foundations).

Modules:
  api_signer        — Ed25519 deterministic request signing
  exchange_key_posture — declared exchange-key capability check (live)
  ssrf / tls        — outbound URL guard and TLS posture (live)
  key_lifecycle, at_rest, randomness — not wired into production paths yet
  credential_vault  — BIP-32 HD key derivation for exchange credentials
  constant_time     — Side-channel-safe comparisons
  pq_transport      — Quantum-safe transport stub (Kyber-768)
"""
