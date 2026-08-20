[app]

# (str) Title of your application
title = Link 5 Dots

# (str) Package name
package.name = link5dots

# (str) Package domain (needed for android/ios packaging)
package.domain = org.link5dots

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas,ttf,wav,json

# (list) List of inclusions using pattern matching
source.include_patterns = assets/*,game/*,ui/*,settings/*,ai/*

# (str) Application versioning
version = 1.0

# (list) Application requirements
requirements = python3==3.11.10,kivy==2.3.0

# (list) Supported orientations
orientation = portrait

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color
android.presplash_color = #DCE5D6

# (list) Permissions
android.permissions = VIBRATE

# (int) Target Android API
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (bool) Automatically accept SDK license agreements
android.accept_sdk_license = True

# (str) The Android arch to build for
android.archs = arm64-v8a, armeabi-v7a

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 0
