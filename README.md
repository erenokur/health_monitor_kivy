# Health Monitor Kivy

This project is a small Kivy app that tracks user blood pressure and medicine.

## Development Environment Setup

### Prerequisites

- **Python 3.12+**
- **pip** and **virtualenv**

### Windows, macOS, and Linux

Create a virtual environment and install the required dependencies:

```bash
# 1. Create a virtual environment
python -m venv .venv

# 2. Activate the virtual environment
# On Linux / macOS:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

## Running the App Locally

Start the app from within your active virtual environment:

```bash
python main.py
```

## Building & Deploying

This project uses [Buildozer](https://buildozer.readthedocs.io/en/latest/) for compiling and packaging the app for mobile and desktop platforms.

### Android Deployment (Linux / macOS)

We have provided a custom build script (`build_android.sh`) to automatically patch a known issue in the `python-for-android` toolchain regarding pip 26 platform compatibility when building for multiple architectures.

1. Ensure your virtual environment is active.
2. Ensure you have the Android SDK/NDK dependencies installed (Buildozer usually downloads these automatically).
3. Run the custom build script:
   ```bash
   ./build_android.sh
   ```
4. The generated APK will be placed in the `bin/` directory.
5. To deploy and run directly on an Android device connected via USB (with USB Debugging enabled):
   ```bash
   buildozer android deploy run
   ```

### macOS Deployment

To build a standalone macOS application bundle:

1. Ensure you are on a macOS machine.
2. Run buildozer targeting macOS:
   ```bash
   buildozer osx debug
   ```
3. The generated `.app` bundle will be located in the `bin/` directory.

## Files

- `main.py`: Kivy application entrypoint
- `health_monitor.db`: SQLite database for storing readings
- `buildozer.spec`: Buildozer configuration file for packaging
- `build_android.sh`: Custom build script to resolve pip cross-compilation errors
