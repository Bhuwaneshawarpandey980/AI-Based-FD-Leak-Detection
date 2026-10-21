import pandas as pd
import matplotlib.pyplot as plt


# Load datasets
normal = pd.read_csv("normal_dataset.csv")
leak = pd.read_csv("leak_dataset.csv")


# ==============================
# GRAPH 1: FD COUNT COMPARISON
# ==============================

plt.figure(figsize=(10, 6))

plt.plot(
    normal["fd_count"],
    label="Normal Workload"
)

plt.plot(
    leak["fd_count"],
    label="Leak Workload"
)

plt.xlabel("Sample")
plt.ylabel("File Descriptor Count")
plt.title("File Descriptor Count: Normal vs Leak")

plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig("fd_count_comparison.png", dpi=300)

plt.show()


# ==============================
# GRAPH 2: FD GROWTH RATE
# ==============================

plt.figure(figsize=(10, 6))

plt.plot(
    normal["fd_growth_rate"],
    label="Normal Workload"
)

plt.plot(
    leak["fd_growth_rate"],
    label="Leak Workload"
)

plt.xlabel("Sample")
plt.ylabel("FD Growth Rate (FDs/sec)")
plt.title("File Descriptor Growth Rate: Normal vs Leak")

plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig("fd_growth_comparison.png", dpi=300)

plt.show()


# ==============================
# GRAPH 3: SOCKET COUNT
# ==============================

plt.figure(figsize=(10, 6))

plt.plot(
    normal["socket_count"],
    label="Normal Workload"
)

plt.plot(
    leak["socket_count"],
    label="Leak Workload"
)

plt.xlabel("Sample")
plt.ylabel("Socket Count")
plt.title("Socket Count: Normal vs Leak")

plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig("socket_comparison.png", dpi=300)

plt.show()


print("\n" + "=" * 60)
print("VISUALIZATION COMPLETED")
print("=" * 60)

print("\nGenerated files:")
print("1. fd_count_comparison.png")
print("2. fd_growth_comparison.png")
print("3. socket_comparison.png")