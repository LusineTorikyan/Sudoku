import tkinter as tk 
from tkinter import messagebox 
from generate_sudoku import generate_sudoku, remove_easy, remove_medium, remove_hard  # type: ignore 
import json 
import os 
 
cell = [[None for _ in range(9)] for _ in range(9)] 
solution_board = None 
board = None 
mistakes = 0 
SAVE_FILE = os.path.join(os.path.expanduser("~"), "sudoku_solution.json") 
 
# Sudoku Grid  
def draw_sudoku_grid(root, difficulty): 
    global cell, solution_board, board, mistakes 
    mistakes = 0 
 
    for r in range(9): 
        for c in range(9): 
            if cell[r][c] is not None: 
                cell[r][c].destroy() 
            cell[r][c] = None 
 
    if os.path.exists(SAVE_FILE): 
        with open(SAVE_FILE, "r") as f: 
            data = json.load(f) 
            solution_board = data['solution'] 
            board = data['current'] 
        print("Loaded last solved game!") 
    else: 
        full_board = generate_sudoku() 
        solution_board = [row[:] for row in full_board] 
 
        if difficulty == "easy": 
            board = remove_easy(full_board) 
        elif difficulty == "medium": 
            board = remove_medium(full_board) 
        else: 
            board = remove_hard(full_board) 
 
    # Draw board 
    board_frame = tk.Frame(root, bg="white") 
    board_frame.pack(pady=20) 
 
    for row in range(9): 
        for col in range(9): 
            value = board[row][col] 
            top = 3 if row in [0, 3, 6] else 1 
            left = 3 if col in [0, 3, 6] else 1 
 
            if value == 0: 
                widget = tk.Entry( 
                    board_frame, 
                    width=3, 
                    justify="center", 
                    font=("Arial", 14), 
                    fg="blue", 
                    bg="white", 
                    relief="solid", 
                    borderwidth=1 
                ) 
                widget.grid(row=row, column=col) 
                widget.grid_configure(padx=(left, 1), pady=(top, 1)) 
                cell[row][col] = widget 
 
                widget.bind("<Return>", lambda event, r=row, c=col: check_cell(r, c)) 
            else: 
                widget = tk.Label( 
                    board_frame, 
                    text=str(value), 
                    width=4, 
                    height=2, 
                    font=("Arial", 12), 
                    fg="black", 
                    bg="white", 
                    relief="solid", 
                    borderwidth=1 
                ) 
                widget.grid(row=row, column=col) 
                widget.grid_configure(padx=(left, 1), pady=(top, 1)) 
                cell[row][col] = None 
 
def check_cell(row, col): 
    global cell, solution_board, board, mistakes 
    entry = cell[row][col] 
    if entry is None: 
        return 
 
    val = entry.get().strip() 
    if not val.isdigit(): 
        messagebox.showwarning("Error", f"Cell ({row+1},{col+1}) must be a number!") 
        entry.delete(0, tk.END) 
        mistakes += 1 
        return 
 
    number = int(val) 
    if number == solution_board[row][col]: 
        entry.config(fg="green") 
        board[row][col] = number 
        check_game_solved() 
    else: 
        entry.config(fg="red") 
        mistakes += 1 
     
    if mistakes == 3: 
        messagebox.showwarning("Game Over", "You have made 3 mistakes!") 
        for r in range(9): 
            for c in range(9): 
                if cell[r][c] is not None: 
                    cell[r][c].config(state="disabled") 
    else: 
        check_game_solved() 
 
 
 
def check_game_solved(): 
    global board, solution_board 
    for r in range(9): 
        for c in range(9): 
            if board[r][c] != solution_board[r][c]: 
                return 
    messagebox.showinfo("Congratulations!", "You solved the Sudoku! Saving automatically...") 
    with open("sudoku_solution.json", "w") as f: 
            json.dump(solution_board, f) 
 
    loaded_solution = None 
    if os.path.exists("sudoku_solution.json"): 
        with open("sudoku_solution.json", "r") as f:
            loaded_solution = json.load(f) 
 
 
    if loaded_solution: 
        print("Loaded solution board:") 
        for row in loaded_solution: 
            print(row) 
    else: 
        print("No solution file found or file is empty.") 
   
 
 
def create_window(): 
    root = tk.Tk() 
    root.title("Sudoku") 
    root.configure(bg='white') 
    return root 
 
def show_difficulty_buttons(root, start_button): 
    start_button.pack_forget() 
    easy_btn = tk.Button(root, text="Easy", bg="lightgreen", font=("Arial", 12), width=15, height=2) 
    medium_btn = tk.Button(root, text="Medium", bg="khaki", font=("Arial", 12), width=15, height=2) 
    hard_btn = tk.Button(root, text="Hard", bg="lightcoral", fg="white", font=("Arial", 12), width=15, height=2) 
    easy_btn.pack(pady=5) 
    medium_btn.pack(pady=5) 
    hard_btn.pack(pady=5) 
 
    def choose_easy(): 
        easy_btn.pack_forget() 
        medium_btn.pack_forget() 
        hard_btn.pack_forget() 
        draw_sudoku_grid(root, "easy") 
 
    def choose_medium(): 
        easy_btn.pack_forget() 
        medium_btn.pack_forget() 
        hard_btn.pack_forget() 
        draw_sudoku_grid(root, "medium") 
 
    def choose_hard(): 
        easy_btn.pack_forget() 
        medium_btn.pack_forget() 
        hard_btn.pack_forget() 
        draw_sudoku_grid(root, "hard") 
 
    easy_btn.config(command=choose_easy) 
    medium_btn.config(command=choose_medium) 
    hard_btn.config(command=choose_hard) 
 
def run_app(): 
    root = create_window() 
    start_button = tk.Button( 
        root, 
        text="Start", 
        bg="lightgray", 
        fg="black", 
        font=("Arial", 12), 
        width=15, 
        height=2, 
        command=lambda: show_difficulty_buttons(root, start_button) 
    ) 
    start_button.pack(pady=20) 
    root.mainloop()