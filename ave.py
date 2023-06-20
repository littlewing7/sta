import glob

# Create a list to store all the file paths
file_paths = glob.glob('backtest/results/*')  # Replace 'path/to/files/' with the actual path to your files

results = {}  # Dictionary to store the results

# Process each file
for file_path in file_paths:
    with open(file_path, 'r') as file:
        lines = file.readlines()[:20]  # Read the first 20 lines from the file
        for line in lines:
            # Split the line by multiple spaces
            parts = line.split()
            if len(parts) >= 4:
                name = parts[0]
                percentage = float(parts[2])
                # Update the results dictionary
                if name in results:
                    results[name].append(percentage)
                else:
                    results[name] = [percentage]

# Sort the results by name
sorted_results = sorted(results.items())

# Calculate the average percentage for each name and print the results
for name, percentages in sorted_results:
    average_percentage = sum(percentages) / len(percentages)
    average_percentage = int(average_percentage)
    print(f"Script: {name} | Average Percentage: {average_percentage}")

