#!/bin/bash
set -e

echo "Ensuring buildozer has initialized the python-for-android toolchain..."
# Run a quick buildozer command to ensure it downloads python-for-android if it hasn't already
buildozer android update || true

P4A_BUILD_SCRIPT=".buildozer/android/platform/python-for-android/pythonforandroid/build.py"

if [ -f "$P4A_BUILD_SCRIPT" ]; then
    echo "Checking if python-for-android needs patching..."
    
    # 1. Patch python -m venv to use --clear
    if grep -q "shprint(host_python, '-m', 'venv', 'venv')" "$P4A_BUILD_SCRIPT"; then
        echo "Patching venv creation to use --clear..."
        sed -i "s/shprint(host_python, '-m', 'venv', 'venv')/shprint(host_python, '-m', 'venv', '--clear', 'venv')/" "$P4A_BUILD_SCRIPT"
    fi

    # 2. Patch pip install to use --platform for cross-compiled wheels
    if ! grep -q "platform_args =" "$P4A_BUILD_SCRIPT"; then
        echo "Patching pip install to support cross-compiled android wheels..."
        awk '
        /shprint\(sh\.bash, '"'"'-c'"'"', \(/ {
            print "            from pythonforandroid.recipe import PyProjectRecipe"
            print "            tags = PyProjectRecipe.get_wheel_platform_tags(arch.arch, ctx)"
            print "            platform_args = \" \" + \" \".join([f\"--platform={tag}\" for tag in tags]) + \" \""
        }
        /install -v --target '"'"'{0}'"'"' --no-deps -r requirements.txt/ {
            sub(/"install -v --target '"'"'{0}'"'"' --no-deps -r requirements.txt"/, "\"install -v --target '"'"'{0}'"'"' --no-deps\" + platform_args + \"-r requirements.txt\"")
        }
        { print }
        ' "$P4A_BUILD_SCRIPT" > "${P4A_BUILD_SCRIPT}.tmp"
        mv "${P4A_BUILD_SCRIPT}.tmp" "$P4A_BUILD_SCRIPT"
    fi
    echo "python-for-android is patched and ready."
else
    echo "Warning: $P4A_BUILD_SCRIPT not found. The patch couldn't be applied. If the build fails, run this script again."
fi

echo "Starting buildozer..."
buildozer android debug

