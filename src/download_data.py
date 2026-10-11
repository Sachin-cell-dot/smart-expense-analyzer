

import kagglehub
import os

dataset_id = "rajatsurana979/comprehensive-credit-card-transactions-dataset"

path = kagglehub.dataset_download(dataset_id)

print("Download completed!")
print("Dataset location:", path)

print("\nAvailable files:")
for file in os.listdir(path):
    print(file)
