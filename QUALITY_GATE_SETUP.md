# Quality Gate Configuration Guide

This document explains how to configure Quality Gate as a mandatory requirement for PR status validation in the CI flow.

## 🎯 What Has Been Implemented

### Layer 1: Quality Gate Check in GitHub Actions Workflow ✅

The workflow now includes:
- **Quality Gate Check Action**: Waits for SonarCloud to process the quality gate
- **Automatic Failure**: Workflow fails if quality gate does not pass
- **Email Notifications**: Includes quality gate status in success/failure emails
- **5-minute timeout**: Ensures timely response

**How it works:**
- After SonarCloud scan completes, the workflow waits for the quality gate result
- If quality gate status is "FAILED", the workflow exits with error code 1
- This prevents PRs from being merged if code quality standards are not met

---

## 📋 Additional Setup Required

### Layer 2: Enable SonarCloud PR Decoration (Automatic Status Checks)

SonarCloud can automatically add status checks to your PRs with detailed quality information.

#### Steps:

1. **Go to SonarCloud Project Settings:**
   - Visit: https://sonarcloud.io/project/configuration?id=neolisto_simple_python_parser

2. **Navigate to General Settings → Pull Requests:**
   - Or use direct link: https://sonarcloud.io/project/configuration/branches?id=neolisto_simple_python_parser

3. **Enable PR Decoration:**
   - Ensure "Decorate Pull Requests" is enabled
   - This will automatically post quality gate status as a GitHub status check

4. **Configure Quality Gate:**
   - Go to: https://sonarcloud.io/organizations/neolisto/quality_gates/show/1
   - Review and adjust quality gate conditions:
     - Coverage threshold
     - Duplicated lines
     - Maintainability rating
     - Reliability rating
     - Security rating
     - Code smells, bugs, vulnerabilities

---

### Layer 3: GitHub Branch Protection Rules (Prevent Merge on Failure)

This is the final layer that **enforces** quality gate checks before allowing PR merges.

#### Steps:

1. **Go to Repository Settings:**
   - Visit: https://github.com/neolisto/simple_python_parser/settings/branches

2. **Add Branch Protection Rule:**
   - Click "Add rule" or "Add branch protection rule"

3. **Configure Protection for Main Branch:**
   - **Branch name pattern**: `main` (or `master` if that's your default branch)
   
4. **Enable Required Status Checks:**
   - ✅ Check "Require status checks to pass before merging"
   - ✅ Check "Require branches to be up to date before merging"
   
5. **Select Required Checks:**
   - Search for and select: **"SonarCloud"** (this appears after the first PR with SonarCloud)
   - Also select: **"SonarCloud Code Analysis"** or similar status checks from SonarCloud
   
6. **Additional Recommended Settings:**
   - ✅ "Require a pull request before merging"
   - ✅ "Require approvals" (set to 1 or more)
   - ✅ "Dismiss stale pull request approvals when new commits are pushed"
   - ✅ "Require review from Code Owners" (optional)
   - ✅ "Include administrators" (enforces rules for everyone)

7. **Save Changes:**
   - Click "Create" or "Save changes"

8. **Repeat for Dev Branch (Optional but Recommended):**
   - Add similar protection for `dev` branch
   - **Branch name pattern**: `dev`
   - Enable the same status checks

---

## 🔧 Testing the Configuration

### Test 1: Create a Test PR with Poor Quality Code

1. Create a new branch:
   ```bash
   git checkout -b test-quality-gate
   ```

2. Add some intentionally problematic code:
   ```python
   # Add to a Python file
   def bad_function():
       x = 1
       y = 2
       z = 3
       # Unused variables, code smells
       pass
   ```

3. Commit and push:
   ```bash
   git add .
   git commit -m "Test: intentionally poor code quality"
   git push origin test-quality-gate
   ```

4. Create a Pull Request to `dev` or `main`

5. **Expected Results:**
   - GitHub Actions workflow runs
   - SonarCloud analyzes the code
   - If quality gate fails:
     - Workflow shows red ❌
     - PR cannot be merged (if branch protection is configured)
     - You receive failure email notification
   - If quality gate passes:
     - Workflow shows green ✅
     - PR can be merged
     - You receive success email notification

---

## 📊 SonarCloud Quality Gate Conditions

Default quality gate conditions typically include:

| Metric | Condition | Description |
|--------|-----------|-------------|
| Coverage | < 80% | Code coverage must be at least 80% |
| Duplicated Lines | > 3% | Less than 3% code duplication allowed |
| Maintainability Rating | Worse than A | Code must maintain A rating |
| Reliability Rating | Worse than A | No bugs in new code |
| Security Rating | Worse than A | No vulnerabilities in new code |
| Security Hotspots | Not Reviewed | All security hotspots must be reviewed |

You can customize these at:
https://sonarcloud.io/organizations/neolisto/quality_gates

---

## 🚨 Troubleshooting

### Issue: Quality Gate Check Times Out

**Solution:**
- Increase timeout in workflow (currently 5 minutes)
- Check SonarCloud project processing queue
- Ensure SONAR_TOKEN has proper permissions

### Issue: SonarCloud Status Check Not Appearing in PR

**Solution:**
1. Verify SonarCloud app is installed on GitHub
2. Check PR decoration is enabled in SonarCloud
3. Ensure GitHub-SonarCloud integration is active
4. Run at least one successful analysis first

### Issue: Branch Protection Not Blocking Merges

**Solution:**
1. Verify status check name matches exactly
2. Ensure "Include administrators" is checked
3. Check that the workflow completed at least once
4. Status checks only appear after first run

---

## 📧 Email Notification Details

Email notifications now include:

**On Success:**
- ✅ Quality Gate PASSED status
- Repository and branch information
- Links to workflow run and SonarCloud dashboard

**On Failure:**
- ❌ Quality Gate FAILED status
- Failure details
- Links to troubleshoot and view detailed analysis

---

## 🔐 Security Considerations

1. **SONAR_TOKEN**: Ensure token has appropriate permissions
   - Generate Tokens: https://sonarcloud.io/account/security
   - Required scope: Execute analysis

2. **Email Credentials**: Store securely in GitHub Secrets
   - Never commit credentials to repository
   - Use app passwords, not actual passwords

3. **Branch Protection**: Enforce for administrators too
   - Prevents accidental bypass of quality checks
   - Ensures consistency across team

---

## 📝 Summary Checklist

- [x] Quality Gate check added to GitHub Actions workflow
- [ ] Disable Automatic Analysis in SonarCloud
- [ ] Enable SonarCloud PR Decoration
- [ ] Configure SonarCloud Quality Gate conditions
- [ ] Add GitHub Branch Protection rules for `main` branch
- [ ] Add GitHub Branch Protection rules for `dev` branch (optional)
- [ ] Add email secrets (EMAIL_USERNAME, EMAIL_PASSWORD, EMAIL_TO)
- [ ] Test with a sample PR
- [ ] Document process for team members

---

## 📚 Additional Resources

- [SonarCloud Documentation](https://docs.sonarcloud.io/)
- [GitHub Branch Protection Rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/about-protected-branches)
- [Quality Gate Best Practices](https://docs.sonarcloud.io/improving/quality-gates/)
- [GitHub Actions - SonarCloud](https://github.com/SonarSource/sonarcloud-github-action)

---

## 🎉 Benefits

Once fully configured, this setup provides:

1. **Automated Quality Enforcement**: No manual review needed for basic quality checks
2. **Consistent Standards**: Everyone follows same quality bar
3. **Early Detection**: Issues caught before merge
4. **Visibility**: Team sees quality metrics on every PR
5. **Accountability**: Clear feedback on code quality
6. **Documentation**: Quality trends tracked over time

---

## 🤝 Need Help?

If you encounter issues:
1. Check GitHub Actions logs for detailed error messages
2. Review SonarCloud project dashboard for analysis results
3. Verify all secrets are configured correctly
4. Consult the troubleshooting section above

