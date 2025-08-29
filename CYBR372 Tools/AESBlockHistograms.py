


from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from collections import Counter
import matplotlib.pyplot as plt

# ---------- Important -----------------
with open("To whoever changes this to your path plaintext.ppm", "rb") as f:
    data = f.read()

# ---------- Important -----------------


block_size = 16
pad_len = block_size - (len(data) % block_size)
data += bytes([pad_len]) * pad_len
key = get_random_bytes(16)
nonce = get_random_bytes(12)
cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
ciphertext = cipher.encrypt(data)
blocks = [ciphertext[i:i+block_size] for i in range(0, len(ciphertext), block_size)]
counts = Counter(blocks)
print(f"Total blocks: {len(blocks)}")
print(f"Unique blocks: {len(counts)}")

top_counts = counts.most_common(100)  # top 50 most frequent blocks
labels = [f"B{i}" for i in range(len(top_counts))]
values = [freq for _, freq in top_counts]

plt.figure(figsize=(14,6))
plt.bar(labels, values, color="steelblue", edgecolor="black")
plt.title("Top 100 Most Repeated Ciphertext Blocks (AES-GCM)", fontsize=14)
plt.xlabel("Distinct Ciphertext Blocks")
plt.ylabel("Occurrences")
plt.xticks(rotation=90)
plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()

