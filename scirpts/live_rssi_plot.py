import subprocess
import time
from collections import deque

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

INTERFACE = "en0"
SSID = "XXXXXX"
WINDOW_SECONDS = 30
MAX_POINTS = 2000

display_filter = f'wlan.ssid=="{SSID}"'

cmd = [
    "tshark",
    "-I",
    "-i", INTERFACE,
    "-l",
    "-Y", display_filter,
    "-T", "fields",
    "-E", "separator=\t",
    "-e", "frame.time_epoch",
    "-e", "wlan_radio.signal_dbm",
]

proc = subprocess.Popen(
    cmd,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    bufsize=1
)

print(
    f"Started tshark (PID {proc.pid}) on interface {INTERFACE}, SSID='{SSID}'")

t0 = time.time()
xs = deque(maxlen=MAX_POINTS)
ys = deque(maxlen=MAX_POINTS)

fig, ax = plt.subplots()
(line,) = ax.plot([], [])
ax.set_xlabel("Time (s)")
ax.set_ylabel("RSSI (dBm)")
ax.set_title(f"Live RSSI (SSID={SSID})")
ax.set_ylim(-100, -10)

stdout_iter = iter(proc.stdout.readline, "")

last_data_time = time.time()


def update(_):
    global last_data_time

    line_raw = next(stdout_iter, None)

    if line_raw is None or line_raw == "":
        return

    parts = line_raw.rstrip("\n").split("\t")
    if len(parts) < 2:
        return

    ts_str, rssi_str = parts[0], parts[1]

    if not rssi_str:
        return

    try:
        ts = float(ts_str)
        rssi = float(rssi_str)
    except ValueError:
        return

    print(f"ts={ts} rssi={rssi}")

    xs.append(ts - t0)
    ys.append(rssi)
    last_data_time = time.time()

    if time.time() - last_data_time > 2.0:
        ax.set_title(
            f"Live RSSI (SSID={SSID}) — no data (check tshark fields/monitor mode)")
    else:
        ax.set_title(f"Live RSSI (SSID={SSID})")

    if xs:
        latest = xs[-1]
        while xs and (latest - xs[0] > WINDOW_SECONDS):
            xs.popleft()
            ys.popleft()

        line.set_data(xs, ys)
        ax.set_xlim(max(0, latest - WINDOW_SECONDS),
                    max(WINDOW_SECONDS, latest))

    return (line,)


ani = FuncAnimation(fig, update, interval=100,
                    blit=True, cache_frame_data=False)

plt.show()

print("Exiting...")
proc.terminate()
proc.wait()
