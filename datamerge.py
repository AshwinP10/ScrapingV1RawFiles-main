import csv

# Input and output file names
input_file = "massivelist.csv"
output_file = "output.csv"

# Define the columns to extract
columns_to_extract = ["Document Title", "Authors", "Publication Year", "PDF Link"]

# Read data from the input CSV and write the simplified data to the output CSV
with open(input_file, 'r', newline='', encoding='utf-8') as input_csv, \
     open(output_file, 'w', newline='', encoding='utf-8') as output_csv:
    csv_reader = csv.DictReader(input_csv)
    
    # Define the header row for the output CSV
    output_fieldnames = columns_to_extract
    csv_writer = csv.DictWriter(output_csv, fieldnames=output_fieldnames)
    csv_writer.writeheader()

    for row in csv_reader:
        # Extract the data for the selected columns
        simplified_data = {column: row.get(column, "") for column in columns_to_extract}
        
        # Write the simplified data to the output CSV
        csv_writer.writerow(simplified_data)

print("Simplified data has been written to 'output.csv'.")