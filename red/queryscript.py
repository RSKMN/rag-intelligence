import csv

# Define your queries as a list of dictionaries
queries = [
    {
        "query": "What are the current sensor readings at home?",
        "k": 3,
        "metadata_filter": "",
        "filepath_globpattern": ""
    },
    # You can add more queries here if needed
    {
        "query": "How many sensor events occurred in the last hour?",
        "k": 5,
        "metadata_filter": "",
        "filepath_globpattern": ""
    },
]

# Specify the filename for the CSV file
filename = "queries.csv"

# Write the queries to the CSV file with the required headers
with open(filename, "w", newline="") as csvfile:
    fieldnames = ["query", "k", "metadata_filter", "filepath_globpattern"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write header row
    writer.writeheader()

    # Write each query row
    for q in queries:
        writer.writerow(q)

print(f"{filename} generated successfully.")
