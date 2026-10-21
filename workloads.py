import time
import socket
import sys


def normal_workload(duration=150):
    """
    Normal workload:
    Resources are opened and properly closed.
    FD usage should remain relatively stable.
    """

    print("=" * 60)
    print("NORMAL FD WORKLOAD")
    print("=" * 60)

    print(f"Running for {duration} seconds...")
    print("Files and sockets will be properly closed.")
    print()

    end_time = time.time() + duration
    counter = 0

    while time.time() < end_time:

        # Open and close a file
        with open("/tmp/fd_normal_test.txt", "w") as file:
            file.write(
                f"Normal workload iteration {counter}\n"
            )

        # Create and close a socket
        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        sock.close()

        counter += 1

        print(
            f"[NORMAL] Iteration: {counter}"
        )

        time.sleep(0.5)

    print()
    print("[NORMAL] Workload completed.")


def leaking_workload(duration=150):
    """
    Intentional FD leak:
    Files and sockets are opened but deliberately
    NOT closed.

    This should cause FD count to increase over time.
    """

    print("=" * 60)
    print("INTENTIONAL FD LEAK WORKLOAD")
    print("=" * 60)

    print(f"Running for {duration} seconds...")
    print("Files and sockets will NOT be closed.")
    print()

    end_time = time.time() + duration

    leaked_files = []
    leaked_sockets = []

    counter = 0

    while time.time() < end_time:

        # -----------------------------
        # INTENTIONAL FILE LEAK
        # -----------------------------

        file = open(
            "/tmp/fd_leak_test.txt",
            "w"
        )

        file.write(
            f"Leaked file {counter}\n"
        )

        # DO NOT CLOSE THE FILE
        leaked_files.append(file)

        # -----------------------------
        # INTENTIONAL SOCKET LEAK
        # -----------------------------

        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        # DO NOT CLOSE THE SOCKET
        leaked_sockets.append(sock)

        counter += 1

        print(
            f"[LEAK] Iteration: {counter} | "
            f"Leaked files: {len(leaked_files)} | "
            f"Leaked sockets: {len(leaked_sockets)}"
        )

        time.sleep(0.5)

    print()
    print("[LEAK] Workload completed.")

    print(
        f"Total leaked files: {len(leaked_files)}"
    )

    print(
        f"Total leaked sockets: {len(leaked_sockets)}"
    )


def main():

    if len(sys.argv) < 2:

        print()
        print("Usage:")
        print()
        print("Normal workload:")
        print("python3 workloads.py normal")
        print()
        print("Leak workload:")
        print("python3 workloads.py leak")
        print()

        return

    mode = sys.argv[1].lower()

    if mode == "normal":

        normal_workload()

    elif mode == "leak":

        leaking_workload()

    else:

        print(
            f"Unknown workload: {mode}"
        )

        print()
        print("Use:")
        print("python3 workloads.py normal")
        print("python3 workloads.py leak")


if __name__ == "__main__":
    main()