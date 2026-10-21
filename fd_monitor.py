import os
import sys
import time
import csv
from datetime import datetime


def count_file_descriptors(pid):
    """
    Count the number of open file descriptors
    belonging to a Linux process.
    """

    fd_path = f"/proc/{pid}/fd"

    try:
        return len(os.listdir(fd_path))

    except FileNotFoundError:
        return None

    except PermissionError:
        print("Permission denied while reading process FDs.")
        return None


def get_fd_types(pid):
    """
    Categorize file descriptors using /proc/PID/fd.
    """

    fd_path = f"/proc/{pid}/fd"

    counts = {
        "file_count": 0,
        "socket_count": 0,
        "pipe_count": 0,
        "device_count": 0,
        "unknown_count": 0
    }

    try:

        for fd in os.listdir(fd_path):

            full_path = os.path.join(fd_path, fd)

            try:
                target = os.readlink(full_path)

            except (FileNotFoundError, PermissionError):
                continue

            if target.startswith("socket:"):
                counts["socket_count"] += 1

            elif target.startswith("pipe:"):
                counts["pipe_count"] += 1

            elif target.startswith("/dev/"):
                counts["device_count"] += 1

            elif target.startswith("/"):

                counts["file_count"] += 1

            else:

                counts["unknown_count"] += 1

    except FileNotFoundError:
        return None

    return counts


def monitor_process(pid, output_file, interval=1):
    """
    Monitor a Linux process using /proc/PID/fd.
    """

    print("=" * 70)
    print("AI-BASED FILE DESCRIPTOR MONITOR")
    print("=" * 70)

    print(f"Monitoring PID: {pid}")
    print(f"Output file: {output_file}")
    print(f"Sampling interval: {interval} second(s)")
    print()

    # Check process
    if not os.path.exists(f"/proc/{pid}"):

        print(f"ERROR: Process {pid} does not exist.")

        return

    # CSV columns
    fieldnames = [
        "timestamp",
        "pid",
        "fd_count",
        "fd_delta",
        "fd_growth_rate",
        "file_count",
        "socket_count",
        "pipe_count",
        "device_count",
        "unknown_count",
        "fd_limit",
        "fd_utilization"
    ]

    previous_count = None
    previous_time = None

    with open(
        output_file,
        "w",
        newline=""
    ) as csv_file:

        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        try:

            while True:

                current_count = count_file_descriptors(pid)

                if current_count is None:

                    print()
                    print("Process no longer exists.")
                    break

                resource_counts = get_fd_types(pid)

                if resource_counts is None:

                    break

                current_time = time.time()

                # -----------------------------
                # Calculate FD delta
                # -----------------------------

                if previous_count is None:

                    fd_delta = 0
                    growth_rate = 0.0

                else:

                    fd_delta = current_count - previous_count

                    time_difference = (
                        current_time - previous_time
                    )

                    if time_difference > 0:

                        growth_rate = (
                            fd_delta / time_difference
                        )

                    else:

                        growth_rate = 0.0

                # -----------------------------
                # Get Linux FD limit
                # -----------------------------

                try:

                    with open(
                        f"/proc/{pid}/limits",
                        "r"
                    ) as limits_file:

                        limits_text = limits_file.read()

                    fd_limit = 0

                    for line in limits_text.splitlines():

                        if "Max open files" in line:

                            parts = line.split()

                            if len(parts) >= 5:

                                fd_limit = int(parts[3])

                            break

                except Exception:

                    fd_limit = 0

                # -----------------------------
                # FD utilization
                # -----------------------------

                if fd_limit > 0:

                    utilization = (
                        current_count / fd_limit
                    ) * 100

                else:

                    utilization = 0.0

                timestamp = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                # -----------------------------
                # Save dataset row
                # -----------------------------

                writer.writerow({

                    "timestamp": timestamp,

                    "pid": pid,

                    "fd_count": current_count,

                    "fd_delta": fd_delta,

                    "fd_growth_rate": round(
                        growth_rate,
                        4
                    ),

                    "file_count":
                        resource_counts["file_count"],

                    "socket_count":
                        resource_counts["socket_count"],

                    "pipe_count":
                        resource_counts["pipe_count"],

                    "device_count":
                        resource_counts["device_count"],

                    "unknown_count":
                        resource_counts["unknown_count"],

                    "fd_limit":
                        fd_limit,

                    "fd_utilization":
                        round(
                            utilization,
                            6
                        )
                })

                csv_file.flush()

                # -----------------------------
                # Display information
                # -----------------------------

                print(
                    f"Time={timestamp} | "
                    f"FDs={current_count} | "
                    f"Delta={fd_delta:+d} | "
                    f"Growth={growth_rate:.2f}/s | "
                    f"Files={resource_counts['file_count']} | "
                    f"Sockets={resource_counts['socket_count']}"
                )

                previous_count = current_count
                previous_time = current_time

                time.sleep(interval)

        except KeyboardInterrupt:

            print()
            print("Monitoring stopped by user.")

    print()
    print(f"Dataset saved to: {output_file}")


def main():

    if len(sys.argv) < 3:

        print()
        print("Usage:")
        print(
            "python3 fd_monitor.py <PID> <output.csv>"
        )
        print()
        print("Example:")
        print(
            "python3 fd_monitor.py 12345 leak_dataset.csv"
        )
        print()

        return

    pid = int(sys.argv[1])

    output_file = sys.argv[2]

    monitor_process(
        pid,
        output_file
    )


if __name__ == "__main__":

    main()