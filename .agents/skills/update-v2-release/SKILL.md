# Update Skupper Release Version

Automates the process of updating the skupper-website to reference a new Skupper V2 release version.

## Prerequisites

- New Skupper version must be published as a GitHub release at https://github.com/skupperproject/skupper/releases
- You must be in the skupper-website repository root directory
- The `./plano` build tool must be functional

## Overview

The skupper-website repository tracks version numbers in multiple locations. The update process combines automated scripts (for GitHub-sourced data) with manual edits (for configuration). This ensures consistency between GitHub releases and website content.

## Update Process

### Step 1: Run Automated Release Generation

```bash
./plano generate-releases
```

**What this does:**
- Fetches release metadata from GitHub API
- Updates `input/data/releases.json` with new version entry
- Updates "latest" pointer to new version
- Updates `input/data/install.json` version field
- Downloads install YAML from GitHub release to `input/install.yaml`
- Updates container image tags (e.g., `quay.io/skupper/controller:X.Y.Z`)

**Files automatically updated:**
- `input/data/releases.json`
- `input/data/install.json`
- `input/install.yaml`

### Step 2: Update MkDocs Configuration

Manually edit `mkdocs.yml` to update version variables:

```yaml
# Change these lines (around line 8-9):
skupper_version: "X.Y.Z"      # Update to new version
skupper_cli_version: "X.Y.Z"  # Update to new version
```

**Why manual?**
These are configuration variables used throughout the documentation templates and cannot be automatically inferred from GitHub releases alone.

### Step 3: Regenerate Website Output

```bash
./plano render --force
```

**What this does:**
- Processes all input files through the site generator
- Updates all generated files in `output/` directory
- Propagates version changes to deployment-ready files

**Files regenerated:**
- `output/install.yaml`
- `output/v2/install.yaml`
- `output/data/install.json`
- `output/data/releases.json`
- All documentation HTML pages

## Verification Checklist

After completing the update, verify:

### 1. Release Data Updated
```bash
# Check releases.json contains new version
grep -A 5 '"X.Y.Z"' input/data/releases.json

# Verify "latest" points to new version
grep -A 3 '"latest"' input/data/releases.json
```

### 2. Install Files Updated
```bash
# Check install.json version
grep '"version"' input/data/install.json

# Check install.yaml image tags
grep 'quay.io/skupper' input/install.yaml | head -5
```

### 3. MkDocs Configuration Updated
```bash
# Verify version variables
grep 'skupper.*version:' mkdocs.yml
```

### 4. Output Files Match Input
```bash
# Verify output files exist and are recent
ls -lh output/install.yaml output/data/*.json
```

### 5. (Optional) Preview Site Locally
```bash
./plano serve
# Visit http://localhost:8000 and spot-check version numbers
```

## Troubleshooting

### `generate-releases` fails
- **Cause**: Network issue or GitHub API rate limit
- **Solution**: Wait a few minutes and retry, or check GitHub release exists

### `render` fails
- **Cause**: Template syntax error or missing dependencies
- **Solution**: Check error output, ensure Python dependencies installed

### Version numbers don't appear on site
- **Cause**: Browser cache or dev server not reloaded
- **Solution**: Hard refresh (Ctrl+Shift+R) or restart `./plano serve`

## Quick Reference: Files by Update Method

### Automated (via `./plano generate-releases`):
- `input/data/releases.json` - Release metadata
- `input/data/install.json` - Install script version
- `input/install.yaml` - Kubernetes install manifest

### Manual:
- `mkdocs.yml` - Documentation version variables (lines 8-9)

### Generated (via `./plano render --force`):
- `output/` directory - All deployment files

## Complete Example

Updating from version 2.2.1 to 2.2.2:

```bash
# Step 1: Automated update
./plano generate-releases

# Step 2: Manual edit
# Edit mkdocs.yml:
#   skupper_version: "2.2.1"  →  "2.2.2"
#   skupper_cli_version: "2.2.1"  →  "2.2.2"

# Step 3: Regenerate
./plano render --force

# Verification
grep '2.2.2' input/data/releases.json
grep 'skupper_version: "2.2.2"' mkdocs.yml
ls -lh output/install.yaml
```

## Related Files and Scripts

- `python/skupper_website/__main__.py` - Main build script entry point
- `python/skupper_website/__init__.py` - Contains `generate_releases()` function
- `README.md` - General build and deployment documentation

## Notes

- The `output/` directory is generated and should not be edited directly
- Version updates should be committed as atomic changes (all files together)
- Always verify the new GitHub release exists before running `generate-releases`
- The "latest" pointer in `releases.json` is important for install scripts and API clients
