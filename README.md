# Steam helpers for Linux

This repository contains some ideas of stuff I've been using in my Steam installation with an NVIDIA GPU.

## DLSS and NVAPI Auto-Configuration for Proton

Python modules that automatically configure NVIDIA DLSS and NVAPI settings for games running through Proton.

- **`dlss_nvapi_setup.py`** - Full version with native Linux DLSS library auto-updater
- **`user_settings.py`** - Proton configuration file that imports one of the above modules

Users should place the two python files in the Proton Installation directory (for example `~/.local/share/Steam/steamapps/common/Proton - Experimental`). Just launch your games through Steam and the appropriate settings will be applied automatically.

### What It Does

- `DXVK_NVAPI_VKREFLEX=1` - Enables NVIDIA Reflex support

Searches for Windows DLSS DLLs in:

- Game installation folder (`~/.local/share/Steam/steamapps/common/<game>`)
- Proton prefix (`~/.local/share/Steam/steamapps/compatdata/<appid>/pfx`)

If found, enables NGX (DLSS) updates and applies the latest preset with overrides:

- `PROTON_ENABLE_NGX_UPDATER=1`
- `DXVK_NVAPI_DRS_NGX_DLSS_SR_OVERRIDE=on` (Super Resolution)
- `DXVK_NVAPI_DRS_NGX_DLSS_RR_OVERRIDE=on` (Ray Reconstruction)
- `DXVK_NVAPI_DRS_NGX_DLSS_FG_OVERRIDE=on` (Frame Generation)
- `DXVK_NVAPI_DRS_NGX_DLSS_SR_OVERRIDE_RENDER_PRESET_SELECTION=render_preset_latest`
- `DXVK_NVAPI_DRS_NGX_DLSS_RR_OVERRIDE_RENDER_PRESET_SELECTION=render_preset_latest`

If no DLSS are found (this means the game does not support DLSS), then exports:

- `NVPRESENT_ENABLE_SMOOTH_MOTION=1` - Enables NVIDIA Smooth Motion

You can add additional Proton settings in `user_settings.py`, for example:

```python
user_settings["DXVK_NVAPI_SET_NGX_DEBUG_OPTIONS"] = "DLSSIndicator=1024,DLSSGIndicator=2"
user_settings["PROTON_LOG"] = "1"
user_settings["DXVK_HUD"] = "devinfo,fps"
user_settings["DXVK_NVAPI_LOG_LEVEL"] = "info"
```

## Custom launcher for ALL games at once

The `proton-env-setup` file is a script to be passed to **any** game in Steam, to set some logic based on the type of game installed. It works roughly as the auto configuration for Proton, but it supports also native Linux games.

Put the script in your `$PATH` (`.local/bin`, `/usr/local/bin`, etc.) so your shell can find it.

It **must** be set as a startup script for each title, for example:

```
proton-env-setup %command%
```

### What It Does

Runs the Steam `%command%` with `gamemoderun`. In my case, it's helpful for disabling standby and some power management features when playing with a controller or on a laptop.

- `DXVK_NVAPI_VKREFLEX=1` - Enables NVIDIA Reflex support

Searches for the DLSS libraries for both Windows (DLLs) and Linux (shared objects) in:

- Game installation folder (`~/.local/share/Steam/steamapps/common/<game>`)
- Proton prefix (`~/.local/share/Steam/steamapps/compatdata/<appid>/pfx`)

If Windows DLLs are found, enables NGX (DLSS) updates and applies the latest preset with overrides:

- `PROTON_ENABLE_NGX_UPDATER=1`
- `DXVK_NVAPI_DRS_NGX_DLSS_SR_OVERRIDE=on` (Super Resolution)
- `DXVK_NVAPI_DRS_NGX_DLSS_RR_OVERRIDE=on` (Ray Reconstruction)
- `DXVK_NVAPI_DRS_NGX_DLSS_FG_OVERRIDE=on` (Frame Generation)
- `DXVK_NVAPI_DRS_NGX_DLSS_SR_OVERRIDE_RENDER_PRESET_SELECTION=render_preset_latest`
- `DXVK_NVAPI_DRS_NGX_DLSS_RR_OVERRIDE_RENDER_PRESET_SELECTION=render_preset_latest`

If native Linux shared objects are found, it downloads the latest DLSS libraries from the [NVIDIA DLSS Github repository](https://github.com/NVIDIA/DLSS/tree/main/lib/Linux_x86_64/rel) and places them along the game provided ones. For example:

```
$ ls -hs1 Baldurs\ Gate\ 3/bin/libnvidia-ngx*
53M 'Baldurs Gate 3/bin/libnvidia-ngx-dlss.so.310.5.3'
42M 'Baldurs Gate 3/bin/libnvidia-ngx-dlss.so.3.7.20'
```

If no libraries are found (this means the game does not support DLSS), then exports:

- `NVPRESENT_ENABLE_SMOOTH_MOTION=1` - Enables NVIDIA Smooth Motion

### Testing

It can be tested with any command to see what it does (in this case `uname`):

```
$ STEAM_COMPAT_INSTALL_PATH=~/.local/share/Steam/steamapps/common/Cyberpunk\ 2077/ \
  STEAM_COMPAT_DATA_PATH=~/.local/share/Steam/steamapps/compatdata/1091500/ \
  proton-env-setup uname
Set DXVK_NVAPI_VKREFLEX=1
Set PROTON_ENABLE_NGX_UPDATER=1
Set DXVK_NVAPI_DRS_NGX_DLSS_SR_OVERRIDE=on
Set DXVK_NVAPI_DRS_NGX_DLSS_RR_OVERRIDE=on
Set DXVK_NVAPI_DRS_NGX_DLSS_FG_OVERRIDE=on
Set DXVK_NVAPI_DRS_NGX_DLSS_SR_OVERRIDE_RENDER_PRESET_SELECTION=render_preset_latest
Set DXVK_NVAPI_DRS_NGX_DLSS_RR_OVERRIDE_RENDER_PRESET_SELECTION=render_preset_latest
Launching: gamemoderun uname

Linux
```
```
$ STEAM_COMPAT_INSTALL_PATH=~/.local/share/Steam/steamapps/common/Baldurs\ Gate\ 3 \
  STEAM_COMPAT_DATA_PATH=~/.local/share/Steam/steamapps/compatdata/1086940 \
  proton-env-setup uname
Found libnvidia-ngx-dlss.so.3.7.20 (41.7 MB)
Found libnvidia-ngx-dlss.so.310.5.3 (52.7 MB)
Set DXVK_NVAPI_VKREFLEX=1
Launching: gamemoderun uname

Linux
```
```
$ STEAM_COMPAT_INSTALL_PATH=~/.local/share/Steam/steamapps/common/The\ Talos\ Principle \
  STEAM_COMPAT_DATA_PATH=~/.local/share/Steam/steamapps/compatdata/257510 \
  proton-env-setup uname
Set DXVK_NVAPI_VKREFLEX=1
Set NVPRESENT_ENABLE_SMOOTH_MOTION=1
Launching: gamemoderun uname

Linux
```
