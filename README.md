# SizzApp Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)
[![Add to HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=t4bias&repository=ha-sizzapp&category=integration)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/t4bias)

Integrate your [SizzApp](https://sizzapp.com) tracked vehicles into [Home Assistant](https://www.home-assistant.io/) using public tracking links — no account credentials required.

---

## Features

- 📍 **Live GPS tracking** via HA device tracker
- 🚗 **Trip detection** (binary sensor: in trip / not in trip)
- 💨 **Speed sensor**
- 🕒 **Last update timestamp**
- 🔄 **Automatic polling** every 30 seconds
- 🛡️ **No password required** – uses SizzApp's share link feature

---

## Requirements

- A SizzApp account with at least one active tracking link
- HACS (recommended for installation)

---

## Installation

### Via HACS (recommended)

1. Click the button below to add this repository directly to HACS:

   [![Add to HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=t4bias&repository=ha-sizzapp&category=integration)

2. Search for **SizzApp** in HACS and install it
3. Restart Home Assistant

> **Manual alternative:** Go to **HACS → Integrations** → click the three-dot menu → **Custom repositories**, add `https://github.com/t4bias/ha-sizzapp` as an **Integration**, then install.

### Manual

1. Copy the `custom_components/sizzapp` folder into your Home Assistant `custom_components` directory
2. Restart Home Assistant

---

## Configuration

1. In Home Assistant, go to **Settings → Devices & Services → Add Integration**
2. Search for **SizzApp**
3. Enter your **SizzApp tracking link**
   - Open the SizzApp smartphone app
   - Navigate to **Tracking Links**
   - Create or copy an existing link (e.g. `https://sizzapp.com/location/your-code`)
4. Click **Submit** — the device will be added automatically

### Reconfiguration

If your tracking link changes, you can update it via **Settings → Devices & Services → SizzApp → Configure**.

---

## Entities

Depending on your device, the following entities will be created:

### Device Tracker
| Entity | Description |
|---|---|
| `device_tracker.<name>` | Live GPS position of the tracked device |

### Sensors
| Entity | Description |
|---|---|
| `sensor.<name>_speed` | Current speed in km/h |
| `sensor.<name>_last_update` | Timestamp of the last data update from the API *(disabled by default)* |

### Binary Sensors
| Entity | Description |
|---|---|
| `binary_sensor.<name>_in_trip` | `on` when the device is currently on a trip, `off` when stationary |

---

## Polling & Updates

The integration polls the SizzApp API every **30 seconds** automatically. The data displayed depends on how frequently SizzApp updates the location on their servers — this is controlled by the SizzApp app and device, not this integration.

---

## Troubleshooting

**"Invalid tracking link" error during setup**
Make sure you paste the full URL from the SizzApp app, e.g. `https://sizzapp.com/location/abc123`. Alternatively, you can enter just the code portion (`abc123`) directly.

**Entities show as unavailable**
Check that your tracking link is still active in the SizzApp app. Links can be deactivated or expire. You can update the link via the integration's reconfigure option.

**Cannot connect to API**
Verify your Home Assistant instance has internet access and can reach `api.sizzapp.com`.

---

## Removal

1. Go to **Settings → Devices & Services → SizzApp**
2. Click the three-dot menu → **Delete**
3. Restart Home Assistant
4. If installed manually, remove the `custom_components/sizzapp` folder from your Home Assistant configuration directory

---

## Contributing

Pull requests and bug reports are welcome! Please open an issue at [github.com/t4bias/ha-sizzapp/issues](https://github.com/t4bias/ha-sizzapp/issues).

---

## Support

If this integration saves you some time and you'd like to say thanks:

[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/t4bias)

---

## Disclaimer

This integration is an unofficial, community-developed project and is not affiliated with or supported by SizzApp. Use at your own risk.
