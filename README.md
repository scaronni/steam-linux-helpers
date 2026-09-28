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
- `DXVK_NVAPI_DRS_NGX_DLSS_FG_OVERRIDE_RENDER_PRESET_SELECTION=render_preset_latest`

If no DLSS are found (this means the game does not support DLSS), then exports:

- `NVPRESENT_ENABLE_SMOOTH_MOTION=1` - Enables NVIDIA Smooth Motion

You can add additional Proton settings in `user_settings.py`, for example:

```python
user_settings["DXVK_NVAPI_SET_NGX_DEBUG_OPTIONS"] = "DLSSIndicator=1024,DLSSGIndicator=2"
user_settings["PROTON_LOG"] = "1"
user_settings["DXVK_HUD"] = "devinfo,fps"
user_settings["DXVK_NVAPI_LOG_LEVEL"] = "info"
```

## Custom launcher for ALL games

The `proton-env-setup` file is a script to be passed to **any** game in Steam, to set some logic based on the type of game installed. It works roughly as the auto configuration for Proton, but it supports also native Linux games.

Put the script in your `$PATH` (`.local/bin`, `/usr/local/bin`, etc.) so your shell can find it.

It **must** be set as a startup script for each title, for example:

```
proton-env-setup %command%
```

If you are using SteamRT3 Beta to run the client, you need to set the full path in the game overrides, for example:

```
~/.local/bin/proton-env-setup %command%
```

or:

```
/usr/local/bin/proton-env-setup %command%
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
- `DXVK_NVAPI_DRS_NGX_DLSS_FG_OVERRIDE_RENDER_PRESET_SELECTION=render_preset_latest`

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

## Adjust all launch options for all games at once

The `proton-launch-editor` file is a script to be executed standa alone that will parse your `~/.local/share/Steam/userdata/<steamid>/config/localconfig.vdf` and change the `LaunchOptions` parameter of **all** the games that user has in Steam.

Games that can only be played in VR are skipped, as reported by the `onlyvrsupport` flag in Steam's app info cache (`~/.local/share/Steam/appcache/appinfo.vdf`). Games that can be played both in VR and on a monitor are still updated.

Put the script in your `$PATH` (`.local/bin`, `/usr/local/bin`, etc.) so your shell can find it and adjust the following variables at the top of the script pointing to your Steam User ID and your preferred launch options:

```
STEAM_USER_ID = "XXXXXXXXX"
LAUNCH_OPTION = "proton-env-setup %command%"
```

I use it in combination with the above script. Sample output:

```
$ proton-launch-editor
Processing: Baldur's Gate 3 (ID: 1086940)
Processing: Cyberpunk 2077 (ID: 1091500)
Processing: Mass Effect™ Legendary Edition (ID: 1328670)
Processing: DEATH STRANDING DIRECTOR'S CUT (ID: 1850570)
Processing: Horizon Forbidden West™ Complete Edition (ID: 2420110)
Processing: The Talos Principle (ID: 257510)
Processing: DOOM (ID: 379720)
Processing: Syberia (ID: 46500)
Processing: DOOM Eternal (ID: 782330)

Successfully updated 9 game(s)
Backup saved to: /home/slaanesh/.local/share/Steam/userdata/XXXXXXXXX/config/localconfig.vdf.backup
```

## Find out which preset "latest" actually selects

When `DXVK_NVAPI_DRS_NGX_DLSS_SR_OVERRIDE_RENDER_PRESET_SELECTION` or `DXVK_NVAPI_DRS_NGX_DLSS_RR_OVERRIDE_RENDER_PRESET_SELECTION` are set to `render_preset_latest`, DXVK-NVAPI only passes a special value (`0x00FFFFFF`) to the DLSS library; the library itself decides which preset that means, and the answer changes between DLSS versions and quality modes. It is not documented anywhere.

The `dlss-latest-presets` script reads the DLSS libraries and prints the preset that "latest" resolves to for each quality mode. It works with both Windows DLLs (`nvngx_dlss*.dll`) and native Linux shared objects (`libnvidia-ngx-dlss*.so.*`) and requires only Python and `objdump`.

Pass one or more libraries to the script. For example:

```
$ ./dlss-latest-presets ~/workspace/github/DLSS/lib/Windows_x86_64/rel/nvngx_dlss.dll
== /home/slaanesh/workspace/github/DLSS/lib/Windows_x86_64/rel/nvngx_dlss.dll (version 310.9.1.0)
Super Resolution:
  'latest' = per-mode default preset, resolved per quality mode at evaluation
    Performance        M (13)
    Balanced           K (11)
    Quality            K (11)
    Ultra Performance  L (12)
    Ultra Quality      K (11)
    DLAA               K (11)

$ ./dlss-latest-presets ~/workspace/github/DLSS/lib/Windows_x86_64/rel/nvngx_dlssd.dll
== /home/slaanesh/workspace/github/DLSS/lib/Windows_x86_64/rel/nvngx_dlssd.dll (version 310.9.1.0)
Ray Reconstruction:
  'latest' = fixed preset, independent of quality mode
    Performance        F (6)
    Balanced           F (6)
    Quality            F (6)
    Ultra Performance  F (6)
    Ultra Quality      F (6)
    DLAA               F (6)
```

 When `PROTON_ENABLE_NGX_UPDATER=1` is set, the libraries actually used by the game are the ones downloaded by the NGX updater in the Proton prefix (`pfx/drive_c/ProgramData/NVIDIA/NGX/models`), not the ones shipped with the game. For example:

```
$ dlss-latest-presets ~/.local/share/Steam/steamapps/compatdata/2012840/pfx/drive_c/ProgramData/NVIDIA/NGX/models/*/versions/*/files/*.bin
== .../models/dlssd/versions/20317442/files/160_E658700.bin (version 310.5.2.0)
Ray Reconstruction:
  'latest' = fixed preset, independent of quality mode
    Performance        D (4)
    Balanced           D (4)
    Quality            D (4)
    Ultra Performance  D (4)
    Ultra Quality      D (4)
    DLAA               D (4)

== .../models/dlssg/versions/20317442/files/160_E658700.bin (version 310.5.2.0)
Frame Generation:
  no render preset override setting; 'latest' does not apply

== .../models/dlss/versions/20317442/files/160_E658700.bin (version 310.5.2.0)
Super Resolution:
  'latest' = per-mode default preset, resolved per quality mode at evaluation
    Performance        M (13)
    Balanced           K (11)
    Quality            K (11)
    Ultra Performance  L (12)
    Ultra Quality      K (11)
    DLAA               K (11)
```

The mapping is found by static analysis of the code handling the override value, so a future DLSS release built differently might not be understood; in that case the script prints `could not resolve` instead of guessing.
