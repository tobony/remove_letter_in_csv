import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import os
from pathlib import Path

string_version = "2024-10-26"  # 버전 정보


def remove_character(input_file, output_file, character):
    total_removed = 0
    with open(input_file, "r", newline="", encoding="utf-8") as infile, open(
        output_file, "w", newline="", encoding="utf-8"
    ) as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for row in reader:
            cleaned_row = []
            for field in row:
                removed = field.count(character)
                total_removed += removed
                cleaned_field = field.replace(character, "")
                cleaned_row.append(cleaned_field)
            writer.writerow(cleaned_row)

    return total_removed


def process_csv_files(directory, character, progress_text):
    total_files_processed = 0
    total_characters_removed = 0

    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".csv") and not file.startswith("clean_"):
                input_path = Path(root) / file
                output_path = input_path.with_name(f"clean_{file}")

                removed_count = remove_character(input_path, output_path, character)

                total_files_processed += 1
                total_characters_removed += removed_count

                progress_text.insert(
                    tk.END,
                    f"Processed {input_path}\n"
                    f"Saved results to {output_path}\n"
                    f"Number of '{character}' characters removed: {removed_count}\n"
                    f"{'-' * 50}\n\n",  # 빈 줄 추가",
                )
                progress_text.yview(tk.END)  # 항상 최신 상태를 스크롤 보기

    messagebox.showinfo(
        "Processing Complete",
        f"Total CSV files processed: {total_files_processed}\nTotal number of '{character}' characters removed across all files: {total_characters_removed}",
    )


def select_directory(entry):
    directory = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, directory)


def start_processing(entry_dir, entry_char, progress_text):
    directory = entry_dir.get()
    character = entry_char.get()
    if not directory:
        messagebox.showwarning("Input Error", "Please select a directory")
        return
    if not character:
        messagebox.showwarning("Input Error", "Please enter a character to remove")
        return

    proceed = messagebox.askyesno("Confirm Process", "Are you sure you want to start processing the files?")
    if proceed:
        progress_text.delete(1.0, tk.END)  # 새로운 작업 전 기존 텍스트 초기화
        process_csv_files(directory, character, progress_text)


def create_gui():
    root = tk.Tk()
    root.title(f"CSV Character Remover {string_version}")
    # 기본 창 크기 설정
    root.geometry("500x350")
    
    # 최소 창 너비 설정
    root.minsize(300, 350)

    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

    # Grid에 빈 공간을 균일하게 분배하기 위한 설정
    frame.columnconfigure(1, weight=1)
    frame.columnconfigure(2, weight=1)

    label_dir = tk.Label(frame, text="Select Directory")
    label_dir.grid(row=0, column=0, sticky="w")

    entry_dir = tk.Entry(frame, width=50)
    entry_dir.grid(row=0, column=1, padx=5, pady=5, sticky="we", columnspan=2)

    button_browse = tk.Button(
        frame, text="Browse", command=lambda: select_directory(entry_dir)
    )
    button_browse.grid(row=0, column=3, padx=5, pady=5)

    label_char = tk.Label(frame, text="Character to Remove")
    label_char.grid(row=1, column=0, sticky="w")

    entry_char = tk.Entry(frame, width=50)  # width 값을 50으로 설정
    entry_char.grid(row=1, column=1, padx=5, pady=5, sticky="we", columnspan=2)

    button_start = tk.Button(
        frame,
        text="Start Processing",
        command=lambda: start_processing(entry_dir, entry_char, progress_text),
    )
    button_start.grid(row=2, column=0, columnspan=4, pady=10)

    # 스크롤바 상태를 위한 설정
    scrollbar = tk.Scrollbar(frame)
    scrollbar.grid(row=3, column=4, sticky="ns")

    progress_text = tk.Text(frame, wrap="word", yscrollcommand=scrollbar.set, height=15)
    progress_text.grid(row=3, column=0, columnspan=4)
    scrollbar.config(command=progress_text.yview)

    root.mainloop()


if __name__ == "__main__":
    create_gui()
