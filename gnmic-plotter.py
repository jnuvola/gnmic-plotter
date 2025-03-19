#!/usr/bin/env python3
import json
import subprocess
import sys
from datetime import datetime
import matplotlib.pyplot as plt


def run_gnmic_command(cmd):
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1
    )
    return process


def parse_json_stream(process):
    buffer = ""
    for line in process.stdout:
        line = line.strip()
        if not line:
            continue
        buffer += line
        try:
            obj = json.loads(buffer)
            yield obj
            buffer = ""
        except json.JSONDecodeError:
            continue


def update_plot(metric_data):

    plt.clf()

    fig = plt.gcf()
    fig.patch.set_facecolor("black")
    ax = plt.gca()
    ax.set_facecolor("black")

    for metric, data in metric_data.items():
        if not data:
            continue
        times, values = zip(*data)
        ax.plot_date(times, values, "-", color="green", label=metric)

    ax.set_xlabel("Time", color="white")
    ax.set_ylabel("Value", color="white")
    ax.set_title("gnmic Plotter", color="white")

    ax.tick_params(axis="x", colors="white")
    ax.tick_params(axis="y", colors="white")

    for spine in ax.spines.values():
        spine.set_edgecolor("white")

    leg = ax.legend()
    leg.get_frame().set_facecolor("black")
    leg.get_frame().set_edgecolor("black")
    for text in leg.get_texts():
        text.set_color("white")

    plt.gcf().autofmt_xdate()
    plt.draw()
    plt.pause(0.01)


def main():

    if len(sys.argv) < 2:
        print("Usage: {} <gnmic command arguments>".format(sys.argv[0]))
        sys.exit(1)

    cmd = ["gnmic"] + sys.argv[1:]
    process = run_gnmic_command(cmd)

    metric_data = {}

    plt.ion()
    plt.figure()

    for obj in parse_json_stream(process):
        if obj.get("sync-response"):
            continue
        if "updates" not in obj:
            continue

        try:
            time_str = obj.get("time")
            if time_str:
                timestamp = datetime.fromisoformat(time_str)
            else:
                timestamp = datetime.fromtimestamp(obj["timestamp"] / 1e9)
        except Exception as e:
            print("Error parsing time:", e)
            continue

        for update in obj.get("updates", []):
            values = update.get("values", {})
            if values:
                metric_name = list(values.keys())[0]
                try:
                    value = float(values[metric_name])
                except ValueError:
                    continue

                if metric_name not in metric_data:
                    metric_data[metric_name] = []
                metric_data[metric_name].append((timestamp, value))
                print(f"Updated {metric_name}: {timestamp} -> {value}")

        update_plot(metric_data)

    process.stdout.close()
    process.wait()


if __name__ == "__main__":
    main()
