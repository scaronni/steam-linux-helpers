"""
DLSS and NVAPI auto-configuration module for Proton user_settings.py
(Simplified version - Windows DLSS DLLs only)

Usage in user_settings.py:
    from dlss_nvapi_setup_simple import get_settings
    user_settings = get_settings()
"""

import os
import glob


def get_game_dir():
    """Get the game installation directory from environment."""
    return os.environ.get("STEAM_COMPAT_INSTALL_PATH", "")


def get_prefix_dir():
    """Get the Proton prefix directory (pfx subfolder)."""
    compat_data = os.environ.get("STEAM_COMPAT_DATA_PATH", "")
    if compat_data:
        return os.path.join(compat_data, "pfx")
    return ""


def find_files_matching(directory, pattern):
    """Find files matching a glob pattern in directory and subdirectories."""
    if not directory or not os.path.isdir(directory):
        return []

    search_path = os.path.join(directory, "**", pattern)
    return glob.glob(search_path, recursive=True)


def has_nvngx_dlss_dll():
    """Check if nvngx_dlss*.dll files exist in game folder or prefix."""
    game_dir = get_game_dir()
    prefix_dir = get_prefix_dir()

    # Check game directory
    if game_dir:
        dll_files = find_files_matching(game_dir, "nvngx_dlss*.dll")
        if dll_files:
            return True

    # Check prefix directory
    if prefix_dir:
        dll_files = find_files_matching(prefix_dir, "nvngx_dlss*.dll")
        if dll_files:
            return True

    return False


def get_settings():
    """
    Generate Proton environment settings based on DLSS/NVAPI detection.

    Returns:
        dict: Dictionary of environment variables to set
    """
    settings = {}

    # 1. Always enable DXVK NVAPI Reflex
    settings["DXVK_NVAPI_VKREFLEX"] = "1"

    # 2. Check for nvngx_dlss*.dll files
    has_dll = has_nvngx_dlss_dll()

    if has_dll:
        # Enable NGX DLSS overrides for Windows DLSS DLLs
        settings["PROTON_ENABLE_NGX_UPDATER"] = "1"
        settings["DXVK_NVAPI_DRS_NGX_DLSS_SR_OVERRIDE"] = "on"
        settings["DXVK_NVAPI_DRS_NGX_DLSS_RR_OVERRIDE"] = "on"
        settings["DXVK_NVAPI_DRS_NGX_DLSS_FG_OVERRIDE"] = "on"
        settings["DXVK_NVAPI_DRS_NGX_DLSS_SR_OVERRIDE_RENDER_PRESET_SELECTION"] = "render_preset_latest"
        settings["DXVK_NVAPI_DRS_NGX_DLSS_RR_OVERRIDE_RENDER_PRESET_SELECTION"] = "render_preset_latest"
        settings["DXVK_NVAPI_DRS_NGX_DLSS_FG_OVERRIDE_RENDER_PRESET_SELECTION"] = "render_preset_latest"
    else:
        # If no DLSS DLLs found, enable smooth motion
        settings["NVPRESENT_ENABLE_SMOOTH_MOTION"] = "1"

    return settings


# Auto-generate settings when module is imported
# This allows: import dlss_nvapi_setup_simple; user_settings = dlss_nvapi_setup_simple.user_settings
user_settings = get_settings()
