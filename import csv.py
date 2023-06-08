import csv

output_data = []  

with open('X:\\New folder\\fixed_file_csv.csv', 'r') as file:
    reader = csv.reader(file, delimiter='\t',)  # Set the delimiter to tab (\t)
    for row in reader:
        value1 = row[0]
        value2 = row[1] 
        value3 = row[2]
        value4 = row[3]
        value5 = row[4]
        output_data.append([value2, value3,value4])  

# Save the output_data as a separate CSV file
with open('output_coords_only.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(output_data)
