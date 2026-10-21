import os
import sys
import time
import joblib
import psutil
import pandas as pd


MODEL_FILE = "fd_leak_model.pkl"

FEATURES = [
    "fd_count",
    "fd_delta",
    "fd_growth_rate",
    "file_count",
    "socket_count",
    "pipe_count",
    "device_count",
    "unknown_count",
    "fd_limit",
    "fd_utilization",
]


def get_fd_count(pid):
    """Return number of open file descriptors for a process."""
    try:
        return len(os.listdir(f"/proc/{pid}/fd"))
    except (FileNotFoundError, PermissionError):
        return None


def get_process_stats(pid):
    """Collect FD-related statistics for the target process."""

    fd_count = get_fd_count(pid)

    if fd_count is None:
        return None

    file_count = 0
    socket_count = 0
    pipe_count = 0
    device_count = 0
    unknown_count = 0

    try:
        for fd in os.listdir(f"/proc/{pid}/fd"):
            try:
                target = os.readlink(f"/proc/{pid}/fd/{fd}")

                if target.startswith("socket:"):
                    socket_count += 1
                elif target.startswith("pipe:"):
                    pipe_count += 1
                elif target.startswith("/dev/"):
                    device_count += 1
                elif target.startswith("/"):
                    file_count += 1
                else:
                    unknown_count += 1

            except (FileNotFoundError, PermissionError):
                continue

    except (FileNotFoundError, PermissionError):
        pass

    fd_limit = 0

    try:
        limits = psutil.Process(pid).rlimit(psutil.RLIMIT_NOFILE)
        fd_limit = limits[0]
    except Exception:
        fd_limit = 1048576

    fd_utilization = fd_count / fd_limit if fd_limit > 0 else 0

    return {
        "fd_count": fd_count,
        "file_count": file_count,
        "socket_count": socket_count,
        "pipe_count": pipe_count,
        "device_count": device_count,
        "unknown_count": unknown_count,
        "fd_limit": fd_limit,
        "fd_utilization": fd_utilization,
    }


def main():

    if len(sys.argv) != 2:
        print("Usage:")
        print("python3 live_ai_monitor.py <PID>")
        return

    pid = int(sys.argv[1])

    print("=" * 70)
    print("LIVE AI FILE DESCRIPTOR LEAK MONITOR")
    print("=" * 70)
    print(f"Monitoring PID: {pid}")
    print(f"AI Model: {MODEL_FILE}")
    print("Sampling interval: 1 second")
    print("=" * 70)

    if not psutil.pid_exists(pid):
        print(f"ERROR: Process {pid} does not exist.")
        return

    # Load trained AI model
    try:
        model = joblib.load(MODEL_FILE)
    except Exception as e:
        print(f"ERROR: Could not load model: {e}")
        return

    print("\nAI model loaded successfully.")
    print("Monitoring started...\n")

    previous_fd = None
    previous_time = None

    try:

        while psutil.pid_exists(pid):

            current_time = time.time()

            stats = get_process_stats(pid)

            if stats is None:
                print("Unable to read process statistics.")
                break

            current_fd = stats["fd_count"]

            if previous_fd is None:
                fd_delta = 0
                growth_rate = 0.0
            else:
                fd_delta = current_fd - previous_fd

                time_delta = current_time - previous_time

                if time_delta > 0:
                    growth_rate = fd_delta / time_delta
                else:
                    growth_rate = 0.0

            stats["fd_delta"] = fd_delta
            stats["fd_growth_rate"] = growth_rate

            # Arrange features in exactly the same order used during training
            X = pd.DataFrame(
                [[stats[feature] for feature in FEATURES]],
                columns=FEATURES
            )

            prediction = model.predict(X)[0]

            # Get confidence if supported by the model
            confidence = None

            if hasattr(model, "predict_proba"):
                probabilities = model.predict_proba(X)[0]
                confidence = max(probabilities) * 100

            if prediction == 1:
                result = "LEAK DETECTED"
            else:
                result = "NORMAL"

            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

            if confidence is not None:
                print(
                    f"{timestamp} | "
                    f"FDs={current_fd} | "
                    f"Delta={fd_delta:+d} | "
                    f"Growth={growth_rate:.2f}/s | "
                    f"Files={stats['file_count']} | "
                    f"Sockets={stats['socket_count']} | "
                    f"Prediction={result} | "
                    f"Confidence={confidence:.2f}%"
                )
            else:
                print(
                    f"{timestamp} | "
                    f"FDs={current_fd} | "
                    f"Delta={fd_delta:+d} | "
                    f"Growth={growth_rate:.2f}/s | "
                    f"Files={stats['file_count']} | "
                    f"Sockets={stats['socket_count']} | "
                    f"Prediction={result}"
                )

            previous_fd = current_fd
            previous_time = current_time

            time.sleep(1)

    except KeyboardInterrupt:
        print("\n\nMonitoring stopped by user.")

    print("\n" + "=" * 70)
    print("LIVE AI MONITOR STOPPED")
    print("=" * 70)


if __name__ == "__main__":
    main()