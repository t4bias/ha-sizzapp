"""Constants for the SizzApp integration."""

DOMAIN = "sizzapp"

# Config entry keys
CONF_SHARE_URL = "share_url"

# API
API_BASE_URL = "https://api.sizzapp.com/app/location_sharing/info"
SHARE_BASE_URL = "https://sizzapp.com/location/"

# Update interval in seconds
DEFAULT_SCAN_INTERVAL = 30

# Data keys from API response
DATA_UNIT_ID = "unit_id"
DATA_NAME = "name"
DATA_SPEED = "speed"
DATA_LAT = "lat"
DATA_LNG = "lng"
DATA_IN_TRIP = "in_trip"
DATA_DT_UNIT = "dt_unit"
DATA_IMAGE_FILENAME = "image_filename"
