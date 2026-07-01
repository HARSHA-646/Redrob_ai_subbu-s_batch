import pandas as pd

old = pd.read_csv("submission_v1.csv")
new = pd.read_csv("submission_test.csv")

print("=" * 80)
print("OLD SHAPE :", old.shape)
print("NEW SHAPE :", new.shape)
print("=" * 80)

# Candidate ID comparison
old_ids = old["candidate_id"].tolist()
new_ids = new["candidate_id"].tolist()

common = set(old_ids) & set(new_ids)

print(f"Common IDs     : {len(common)}")
print(f"Old IDs        : {len(old_ids)}")
print(f"New IDs        : {len(new_ids)}")

print("=" * 80)

# Exact order match
exact_match = old_ids == new_ids

print("Exact Order Match:", exact_match)

print("=" * 80)

# Show mismatches by rank
mismatches = []

for i in range(min(len(old_ids), len(new_ids))):

    if old_ids[i] != new_ids[i]:

        mismatches.append(
            (
                i + 1,
                old_ids[i],
                new_ids[i]
            )
        )

print("Mismatch Count:", len(mismatches))

print("=" * 80)

if len(mismatches) > 0:

    print("FIRST 20 MISMATCHES\n")

    for rank, old_id, new_id in mismatches[:20]:

        print(
            f"Rank {rank}"
            f" | OLD={old_id}"
            f" | NEW={new_id}"
        )

else:

    print("PERFECT MATCH")

print("=" * 80)

# Missing from new
missing_from_new = list(
    set(old_ids) - set(new_ids)
)

missing_from_old = list(
    set(new_ids) - set(old_ids)
)

print(
    "Missing From NEW:",
    len(missing_from_new)
)

print(
    "Missing From OLD:",
    len(missing_from_old)
)

print("=" * 80)

if missing_from_new:

    print("\nSample Missing From NEW:")

    for x in missing_from_new[:10]:
        print(x)

if missing_from_old:

    print("\nSample Missing From OLD:")

    for x in missing_from_old[:10]:
        print(x)

print("=" * 80)