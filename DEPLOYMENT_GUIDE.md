# Deployment Guide - Project Mind APK Build via GitHub Actions

## Current Status

✓ **Code is ready for deployment**
- All import errors fixed
- Validation script passes
- All 21 Python files syntactically valid
- buildozer.spec configured correctly
- GitHub Actions workflow (.github/workflows/build-apk.yml) is configured

✓ **Local commits prepared**
```
fac7b11 docs: add comprehensive release notes for v1.0.0
43839ea fix: resolve import path errors and improve module structure
```

## STEP 1: Push Commits to GitHub

### Option A: Using Git Command Line (Recommended)

**Prerequisites:**
- Git installed and configured
- SSH key configured for GitHub OR GitHub CLI installed

**Steps:**
```bash
cd /path/to/Project-Mind

# Verify commits are ready
git log --oneline -2

# Push to master branch
git push origin master
```

### Option B: Using GitHub CLI (Easiest)

If you don't have GitHub CLI:
1. Download from: https://cli.github.com
2. Install and run: `gh auth login`
3. Follow prompts to authenticate
4. Then push: `git push origin master`

### Option C: Using SSH Key (If not set up)

1. Generate SSH key (if needed):
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

2. Add public key to GitHub:
   - Go to: https://github.com/settings/keys
   - Click "New SSH key"
   - Paste your public key

3. Test connection:
   ```bash
   ssh -T git@github.com
   ```

4. Push:
   ```bash
   git push origin master
   ```

### Option D: Using HTTPS with Personal Access Token

1. Create Personal Access Token:
   - Go to: https://github.com/settings/tokens/new
   - Select: `repo` scope
   - Copy the token

2. Update remote URL:
   ```bash
   git remote set-url origin https://github.com/Vishal7728/Project-Mind.git
   ```

3. Push (will prompt for token):
   ```bash
   git push origin master
   # Enter your GitHub username
   # Paste your Personal Access Token as password
   ```

---

## STEP 2: Monitor GitHub Actions Build

Once commits are pushed, the CI/CD pipeline will automatically start:

1. **Go to GitHub Actions:**
   - Visit: https://github.com/Vishal7728/Project-Mind/actions

2. **Watch the build progress:**
   - You'll see a new workflow run: "Build APK - Production"
   - Monitor these stages:
     - ✓ Validate Project Setup (runs validate_build.py)
     - ✓ Build Android APK (runs buildozer android release)
     - ✓ Upload Artifact (APK file)

3. **Expected build time:**
   - First run: ~15-20 minutes (downloading SDK/NDK)
   - Subsequent runs: ~10-15 minutes (cached)

---

## STEP 3: Retrieve the Built APK

### If Build Succeeds:

1. **Download from GitHub Actions:**
   - Go to: https://github.com/Vishal7728/Project-Mind/actions
   - Click the latest successful "Build APK" workflow
   - Scroll to "Artifacts"
   - Download `projectmind-*.apk`

2. **Install on Android device:**
   ```bash
   adb install projectmind-*.apk
   ```

3. **Or use Play Console:**
   - Upload APK to Google Play Console
   - Configure store listing
   - Submit for review

### If Build Fails:

1. **Check the logs:**
   - Click the failed workflow run
   - Expand the "Build Android APK" step
   - Look for error messages (usually at the bottom)

2. **Common issues:**
   - `android.ndk not found` → NDK download may have failed (retry)
   - Memory issues → Gradle memory limit too low (increase in buildozer.spec)
   - Permission errors → Check Android SDK path configuration
   - Cython errors → Ensure Cython 0.29.33 is pinned in requirements

3. **Troubleshooting:**
   - For NDK/SDK issues: Rerun workflow (may be network transient)
   - For code errors: Fix locally, commit, and push again
   - Check `buildozer.spec` for configuration issues

---

## STEP 4: Configure Release Signing (Optional - For Play Store)

If you want to publish to Google Play Store, configure signing:

### Generate Keystore (One-time):

```bash
keytool -genkey -v -keystore projectmind.jks \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000 \
  -alias projectmind_key
```

### Add to GitHub Secrets:

1. Encode keystore to base64:
   ```bash
   base64 projectmind.jks > projectmind.jks.b64
   cat projectmind.jks.b64
   ```

2. Go to: https://github.com/Vishal7728/Project-Mind/settings/secrets/actions

3. Add these secrets:
   - `RELEASE_KEYSTORE_BASE64` → Contents of .jks.b64 file
   - `RELEASE_KEYSTORE_PASSWORD` → Your keystore password
   - `RELEASE_KEY_ALIAS` → projectmind_key
   - `RELEASE_KEY_PASSWORD` → Your key password

4. The GitHub Actions workflow will automatically use these for signing

---

## STEP 5: Test the APK

### On Emulator:
```bash
# List available emulators
emulator -list-avds

# Start emulator
emulator @emulator_name

# Wait for it to boot, then install APK
adb install projectmind-*.apk

# Launch app
adb shell am start -n org.projectmind/org.renpy.android.PythonActivity
```

### On Physical Device:
1. Connect device via USB
2. Enable USB Debugging (Developer Options)
3. Install: `adb install projectmind-*.apk`
4. Open app from home screen

### Verify Features:
- App launches without crashes
- Permissions are requested correctly
- All UI elements load
- No runtime errors in logs: `adb logcat`

---

## Workflow Configuration

The GitHub Actions workflow is already configured in `.github/workflows/build-apk.yml`:

**What it does:**
1. Validates Python syntax and buildozer.spec
2. Sets up Java 17, Android SDK, and NDK
3. Installs Python dependencies (including Cython 0.29.33)
4. Runs `buildozer android release`
5. Uploads the resulting APK as an artifact
6. Caches Gradle and SDK for faster rebuilds

**Triggered on:**
- Push to master/main/develop branches
- Pull requests to these branches
- Manual workflow dispatch (via Actions tab)

---

## Pushing Locally Without SSH/GitHub CLI

If you can't use SSH or GitHub CLI, use this workaround:

```bash
# Create a temporary HTTPS remote
git remote add https-origin https://github.com/Vishal7728/Project-Mind.git

# Push via HTTPS (will prompt for credentials)
git push https-origin master

# Optional: Make HTTPS the default
git remote set-url origin https://github.com/Vishal7728/Project-Mind.git
git push origin master
```

---

## Current Build Status

**Repository:** https://github.com/Vishal7728/Project-Mind
**Branch:** master
**Latest Commit:** fac7b11 (Release notes added)
**Status:** Ready for deployment

**To start the build:**
1. Push commits to GitHub
2. Visit Actions tab
3. Monitor the build progress
4. Download APK when complete

---

## Troubleshooting Checklist

| Issue | Solution |
|-------|----------|
| **SSH Key Error** | Use HTTPS or GitHub CLI instead |
| **Build Timeout** | Increase timeout or split build into smaller jobs |
| **NDK Download Fails** | Rerun workflow (network transient) |
| **Code Errors** | Fix locally and push again |
| **Permission Denied** | Check GitHub repository access |
| **Keystore Not Found** | Add secrets to GitHub if doing signed release |

---

## Next Steps After Successful Build

1. **Test the APK** on device/emulator
2. **Verify permissions** are working
3. **Check all features** function correctly
4. **Review logs** for any warnings/errors
5. **Deploy to Play Store** (if applicable):
   - Upload to Google Play Console
   - Fill out store listing
   - Submit for review

---

## Support

For issues:
1. Check GitHub Actions logs
2. Review `buildozer.spec` configuration
3. Check `RELEASE_NOTES.md` for version info
4. See `APK_BUILD_GUIDE.md` for detailed build instructions
5. See `ANDROID_DEVOPS_AUDIT.md` for technical details

---

**Last Updated:** December 10, 2025
**Status:** Ready for deployment
