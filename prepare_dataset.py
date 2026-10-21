import pandas as pd


NORMAL_FILE = "normal_dataset.csv"
LEAK_FILE = "leak_dataset.csv"
OUTPUT_FILE = "training_dataset.csv"


def prepare_dataset():

    print("=" * 70)
    print("PREPARING FD LEAK DETECTION DATASET")
    print("=" * 70)

    # -----------------------------------------
    # Load normal dataset
    # -----------------------------------------

    normal = pd.read_csv(NORMAL_FILE)

    print(f"Normal samples loaded: {len(normal)}")

    # Label normal workload as 0
    normal["label"] = 0

    # -----------------------------------------
    # Load leak dataset
    # -----------------------------------------

    leak = pd.read_csv(LEAK_FILE)

    print(f"Leak samples loaded: {len(leak)}")

    # Label leak workload as 1
    leak["label"] = 1

    # -----------------------------------------
    # Combine datasets
    # -----------------------------------------

    dataset = pd.concat(
        [normal, leak],
        ignore_index=True
    )

    # -----------------------------------------
    # Remove unnecessary columns
    # -----------------------------------------

    columns_to_remove = [
        "timestamp",
        "pid"
    ]

    dataset = dataset.drop(
        columns=columns_to_remove
    )

    # -----------------------------------------
    # Shuffle dataset
    # -----------------------------------------

    dataset = dataset.sample(
        frac=1,
        random_state=42
    ).reset_index(drop=True)

    # -----------------------------------------
    # Save final dataset
    # -----------------------------------------

    dataset.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print()
    print("Dataset preparation completed.")
    print()

    print(f"Total samples: {len(dataset)}")

    print()
    print("Class distribution:")
    print(
        dataset["label"].value_counts()
    )

    print()
    print("Final features:")

    for column in dataset.columns:

        print(f" - {column}")

    print()
    print(
        f"Dataset saved as: {OUTPUT_FILE}"
    )

    print("=" * 70)


if __name__ == "__main__":

    prepare_dataset()