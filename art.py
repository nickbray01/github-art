from datetime import datetime, timedelta
import os, subprocess

REPO_PATH = "."
COMMITS_PER_PIXEL = 3

# GitHub graph covers 52 weeks (columns)
COLUMNS = 52
ROWS = 7

# Define characters to print
TEXT = "HELLO WORLD"

# Define simplified 5x7 font
CHAR_MAP = {
    'H': ["101", "101", "111", "101", "101"],
    'E': ["111", "100", "110", "100", "111"],
    'L': ["100", "100", "100", "100", "111"],
    'O': ["010", "101", "101", "101", "010"],
    'W': ["10101", "10101", "10101", "10101", "01010"],
    'R': ["110", "101", "110", "101", "101"],
    'D': ["110", "101", "101", "101", "110"],
    ' ': ["000", "000", "000", "000", "000"]
}

def render_text_to_grid(text):
    grid = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
    col = 0
    for char in text:
        bitmap = CHAR_MAP.get(char.upper(), CHAR_MAP[' '])
        for y, row in enumerate(bitmap):
            for x, pixel in enumerate(row.replace(" ", "")):
                if col + x < COLUMNS and int(pixel):
                    grid[y+1][col + x] = 1  # Rows 1–5 for message
        col += len(bitmap[0].replace(" ", "")) + 1  # Space between letters
    # Add solid weekend lines (rows 0 and 6)
    for x in range(COLUMNS):
        grid[0][x] = 1
        grid[6][x] = 1
    return grid

def make_commit(commit_date):
    os.environ['GIT_AUTHOR_DATE'] = commit_date.isoformat()
    os.environ['GIT_COMMITTER_DATE'] = commit_date.isoformat()
    subprocess.run(["git", "commit", "--allow-empty", "-m", "graph art"], cwd=".")

def main():
    start_date = datetime.today() - timedelta(days=365)
    start_date -= timedelta(days=(start_date.weekday() + 1) % 7)

    grid = render_text_to_grid(TEXT)

    for x in range(COLUMNS):
        for y in range(ROWS):
            if grid[y][x]:
                day = start_date + timedelta(weeks=x, days=y)
                for _ in range(COMMITS_PER_PIXEL):
                    make_commit(day)

    subprocess.run(["git", "push"], cwd=REPO_PATH)

if __name__ == "__main__":
    main()
