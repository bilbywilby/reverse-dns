# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-09-10
### Added
- Core `reverse_dns.py` analyzer with concurrent lookup logic.
- Raw-IP fallback for DLT_USBPCAP (Type 228) compatibility.
- Synthetic fixture generator for smoke testing.
- Virtual environment integration and dependency pinning.
- MIT License and Contribution guidelines.
- GitHub Actions CI pipeline for automated smoke tests.

### Fixed
- False negative in protocol aggregation validation regex.


## [0.2.1] - 2026-09-11
### Fixed
- CI Smoke Test runner failure caused by missing `tests/fixtures` directory on fresh clones.
- Self-provisioning directory added at runtime via `os.makedirs` and `mkdir -p` (commit `6e2ea8d`).
