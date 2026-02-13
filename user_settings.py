# Proton User Settings with auto DLSS/NVAPI configuration
from dlss_nvapi_setup import get_settings

# Get auto-configured settings based on DLSS detection
user_settings = get_settings()

# You can add additional manual settings here:
# user_settings["PROTON_LOG"] = "1"
# user_settings["DXVK_HUD"] = "devinfo,fps"
