import pandas as pd

# Read the CSV file
df = pd.read_csv('datasets/cyber/cyberner.csv')

# Get unique tags from the 'Tag' column
unique_tags = sorted(df['Tag'].unique())

# Write to output file
with open('unique_tags_output.txt', 'w', encoding='utf-8') as f:
    f.write("Unique Tags in cyberner.csv:\n")
    f.write("=" * 50 + "\n")
    for tag in unique_tags:
        f.write(f"{tag}\n")
    
    f.write("\n" + "=" * 50 + "\n")
    f.write(f"Total unique tags: {len(unique_tags)}\n")

print(f"Output saved to unique_tags_output.txt")
print(f"Found {len(unique_tags)} unique tags")
