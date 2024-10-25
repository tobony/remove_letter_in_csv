import csv
import os
from pathlib import Path

def remove_question_marks(input_file, output_file):
    total_removed = 0
    with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for row in reader:
            cleaned_row = []
            for field in row:
                removed = field.count('?')
                total_removed += removed
                cleaned_field = field.replace('?', '')
                cleaned_row.append(cleaned_field)
            writer.writerow(cleaned_row)

    return total_removed

def process_csv_files(directory):
    total_files_processed = 0
    total_question_marks_removed = 0

    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.csv'):
                input_path = Path(root) / file
                output_path = input_path.with_name(f"_{file}")
                # output_path = input_path.with_name(f"{input_path.stem}_clean{input_path.suffix}")
            
                removed_count = remove_question_marks(input_path, output_path)

                total_files_processed += 1
                total_question_marks_removed += removed_count
                
                print(f"Processed {input_path}")
                print(f"Saved results to {output_path}")
                print(f"Number of '?' characters removed: {removed_count}")
                print("-" * 50)

    return total_files_processed, total_question_marks_removed

if __name__ == "__main__":
    current_directory = Path.cwd()
    files_processed, total_removed = process_csv_files(current_directory)

    print(f"\nTotal CSV files processed: {files_processed}")
    print(f"Total number of '?' characters removed across all files: {total_removed}")