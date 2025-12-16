# Wi-Fi Sensing Experiments

Small experimental repository to explore Wi-Fi signal behavior using RSSI measurements extracted from live 802.11 captures.

This repo contains:
- Live RSSI visualization using `tshark` + Python
- LOS vs NLOS signal analysis
- Simple signal plots for exploratory purposes

## Scope

Part of this experiment comes from an exercise conducted at The Osaka University - Graduate School of Information Science and Technology in Mobile Communication course.

> This is **not** a production-ready project and **not** CSI-based sensing.
> The goal is to keep a trace of experiments and observations.

## Setup

- macOS
- Wireshark / tshark
- Python 3

Example capture command:
```bash
tshark -I -i en0 -Y 'wlan.ssid=="<SSID>"' \
  -T fields -e frame.time_epoch -e wlan_radio.signal_dbm
```

## Notes

Experiments were conducted in controlled indoor environments.
Results are indicative and environment-dependent.
