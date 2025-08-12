import csv

def write_header(output_file):
    # Write the header for the output file (sales, date, region)
    with open(output_file, 'w', newline='') as output:
        fieldnames = ['sales', 'date', 'region']
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()

def process_sales_data(input_file, product_filter):
    processed_rows = []

    # Open the input file for reading
    with open(input_file, 'r') as infile:
        reader = csv.DictReader(infile)

        # Process each row from the input file
        for row in reader:
            # Ensure that 'product' matches exactly (strip spaces and check case)
            if row['product'].strip().lower() == product_filter.lower():
                try:
                    # Calculate sales as price * quantity
                    price = float(row['price'].replace('$', '').strip())  # Remove '$' and convert to float
                    quantity = float(row['quantity'])
                    sales = price * quantity

                    # Append processed data (sales, date, region)
                    processed_rows.append({
                        'sales': sales,
                        'date': row['date'].strip(),
                        'region': row['region'].strip()
                    })
                except (ValueError, KeyError) as e:
                    print(f"Skipping row due to error: {e}")
                    continue  # Skip rows with errors

    return processed_rows

# Main Logic
output_file = '../data/pink_morsels_data.csv'

# Write the header once before processing any data
write_header(output_file)

# Collect all processed data
all_processed_data = []
all_processed_data.extend(process_sales_data('../data/daily_sales_data_0.csv', 'pink morsel'))
all_processed_data.extend(process_sales_data('../data/daily_sales_data_1.csv', 'pink morsel'))
all_processed_data.extend(process_sales_data('../data/daily_sales_data_2.csv', 'pink morsel'))

# Write all the processed rows to the output file at once
if all_processed_data:
    with open(output_file, 'a', newline='') as output:
        fieldnames = ['sales', 'date', 'region']
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writerows(all_processed_data)
