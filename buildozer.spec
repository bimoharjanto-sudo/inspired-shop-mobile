[app]

# Nama aplikasi
title = Inspired Shop

# Package
package.name = inspiredshop
package.domain = com.bjards

# Source
source.dir = app
source.include_exts = py,png,jpg,jpeg,kv,atlas

# Versi
version = 0.1.0

# Dependency minimal
requirements = python3,kivy

# Orientation
orientation = portrait

# Android
fullscreen = 0

# Android API
android.api = 35
android.minapi = 24
android.accept_sdk_license = True

# Permissions
android.permissions = INTERNET

# Build
android.archs = arm64-v8a

# Logging
log_level = 2

[buildozer]

log_level = 2
warn_on_root = 1
