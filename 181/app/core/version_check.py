# app/core/version_check.py

import pkg_resources

def check_versions_auto(required_versions=None):
    """
    بررسی نسخه پکیج‌ها در محیط فعلی.

    required_versions: dict (نام پکیج: نسخه مورد نیاز)
    اگر None باشد، فقط نسخه‌های نصب شده را نشان می‌دهد.
    """
    installed_packages = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
    results = []

    for pkg_name, installed_version in installed_packages.items():
        status = "OK"
        required_version = None

        if required_versions and pkg_name in required_versions:
            required_version = required_versions[pkg_name]
            if installed_version != required_version:
                status = "MISMATCH"

        results.append({
            "package": pkg_name,
            "installed_version": installed_version,
            "required_version": required_version,
            "status": status
        })

    return results
