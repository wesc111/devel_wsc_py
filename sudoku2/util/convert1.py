# conversion script to read old sudoku text files and convert to new format
# Werner Schoegler, 11-Nov-2025

import sys, os

input_file = ""
output_file = ""
python_dir = "C:/Users/werne/OneDrive/devel_wsc_private/python"

if __name__ == '__main__':

    input_file = python_dir + "/sudoku2/data/hardest.txt"
    output_file = python_dir + "/sudoku2/data/hardest_new.txt"
    easy_counter = 0
    medium_counter = 0
    hard_counter = 0
    evil_counter = 0
    unknown_counter = 0
    counter = 0
    
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        f_out.write("trialSudokus = {\n")
        for line in f_in:
            line1 = line.strip()
            sudoku = line1.split("#", 1)[0].strip()  # Remove comments
            comment = line1.split("#", 1)[1].strip() if "#" in line1 else "no comment"
            if len(sudoku) == 0:
                continue
            # Convert line to new format if needed
            # Here we assume the old format is the same as the new format for simplicity
            if len(sudoku) != 81:
                print(f"Skipping invalid line (not 81 chars): {line1}")
                continue
            if "leicht" in comment.lower() or "easy" in comment.lower():
                category = "easy"
                easy_counter += 1
                counter = easy_counter
            elif "mittel" in comment.lower() or "medium" in comment.lower() or "normal" in comment.lower():
                category = "medium"
                medium_counter += 1
                counter = medium_counter
            elif "schwer" in comment.lower() or "schwierig" in comment.lower() or "expert" in comment.lower() or "hard" in comment.lower():
                category = "hard"
                hard_counter += 1
                counter = hard_counter
            elif "teuflisch" in comment.lower() or "knifflig" in comment.lower() \
                or "extrem" in comment.lower() or "evil" in comment.lower() or "hardest" in comment.lower() :
                category = "evil"
                evil_counter += 1
                counter = evil_counter
            else:
                category = "unknown"  
                unknown_counter += 1
                counter = unknown_counter         
            f_out.write(f"    \"{category} {counter}\" :  \"{sudoku}\",  # {comment}\n")
            counter += 1
        f_out.write("}\n")
    print(f"Converted {counter} lines \n    from {input_file} \n    to {output_file}")