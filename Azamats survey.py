"""
Keyword Highlighting in Texts and Quick Review Efficiency Survey
================================================================
A psychological state survey program for assessing cognitive habits
related to keyword highlighting and review efficiency.

Author: Student Submission
Module: Fundamentals of Programming, 4BUIS008C (Level 4)
"""
import streamlit as st
import json
import csv
import os
import re
from datetime import datetime


# ──────────────────────────────────────────────
#  DATA: Survey questions stored as a list of dicts
#  (also loadable from external file)
# ──────────────────────────────────────────────

DEFAULT_QUESTIONS = [
    {
        "id": 1,
        "text": "How consistently do you highlight keywords while reading academic or professional texts?",
        "options": [
            ("Always – I highlight every key term systematically", 0),
            ("Often – I highlight most important terms", 1),
            ("Sometimes – I highlight when I remember to", 2),
            ("Rarely – I almost never highlight", 3),
            ("Never – I do not highlight at all", 4),
        ],
    },
    {
        "id": 2,
        "text": "When reviewing highlighted material, how quickly can you reconstruct the main ideas?",
        "options": [
            ("Very quickly – within seconds per page", 0),
            ("Quickly – within a minute per page", 1),
            ("Moderately – takes a few minutes", 2),
            ("Slowly – takes considerable time", 3),
            ("Very slowly – I struggle to recall ideas", 4),
        ],
    },
    {
        "id": 3,
        "text": "How well do your highlights reflect the actual key concepts of the text?",
        "options": [
            ("Extremely well – they capture all core ideas", 0),
            ("Well – they capture most ideas", 1),
            ("Adequately – they capture some ideas", 2),
            ("Poorly – they miss many key ideas", 3),
            ("Very poorly – they are mostly irrelevant", 4),
        ],
    },
    {
        "id": 4,
        "text": "How often do you over-highlight (marking too much text, reducing efficiency)?",
        "options": [
            ("Never – my highlights are concise", 0),
            ("Rarely – I occasionally over-highlight", 1),
            ("Sometimes – I over-highlight moderately", 2),
            ("Often – most of my text ends up highlighted", 3),
            ("Always – I highlight almost everything", 4),
        ],
    },
    {
        "id": 5,
        "text": "How effectively do you use colour-coding to categorise different types of information?",
        "options": [
            ("Very effectively – I have a clear colour system", 0),
            ("Effectively – I use colours with some consistency", 1),
            ("Somewhat effectively – my system is inconsistent", 2),
            ("Ineffectively – I rarely use colour-coding", 3),
            ("Not at all – I use a single colour or none", 4),
        ],
    },
    {
        "id": 6,
        "text": "How confident are you in identifying which terms are truly 'keywords' in a passage?",
        "options": [
            ("Very confident – I reliably identify key terms", 0),
            ("Confident – I am usually correct", 1),
            ("Moderately confident – I am sometimes unsure", 2),
            ("Low confidence – I often misjudge", 3),
            ("Not confident at all – I struggle greatly", 4),
        ],
    },
    {
        "id": 7,
        "text": "How often do you review your highlighted notes before an exam or presentation?",
        "options": [
            ("Always – thorough review every time", 0),
            ("Often – review most of the time", 1),
            ("Sometimes – review occasionally", 2),
            ("Rarely – almost never review highlights", 3),
            ("Never – I do not review highlights", 4),
        ],
    },
    {
        "id": 8,
        "text": "How much does your highlighting strategy improve your understanding of complex material?",
        "options": [
            ("Greatly – it significantly aids comprehension", 0),
            ("Considerably – noticeable improvement", 1),
            ("Somewhat – minor improvement", 2),
            ("Barely – little to no improvement", 3),
            ("Not at all – it makes no difference or hinders", 4),
        ],
    },
    {
        "id": 9,
        "text": "How often do you combine keyword highlighting with margin notes or annotations?",
        "options": [
            ("Always – I always annotate alongside highlights", 0),
            ("Often – I annotate most of the time", 1),
            ("Sometimes – occasional annotations", 2),
            ("Rarely – I seldom add notes", 3),
            ("Never – I never annotate", 4),
        ],
    },
    {
        "id": 10,
        "text": "How efficiently can you locate specific information in a text using only your highlights?",
        "options": [
            ("Very efficiently – I find it immediately", 0),
            ("Efficiently – I find it quickly", 1),
            ("Moderately – it takes some time", 2),
            ("Inefficiently – it takes a long time", 3),
            ("Very inefficiently – I cannot locate it", 4),
        ],
    },
    {
        "id": 11,
        "text": "How regularly do you adapt your highlighting technique based on the type of text?",
        "options": [
            ("Always – I tailor my approach every time", 0),
            ("Often – I adapt most of the time", 1),
            ("Sometimes – I adapt occasionally", 2),
            ("Rarely – I use the same approach always", 3),
            ("Never – I never consider adapting", 4),
        ],
    },
    {
        "id": 12,
        "text": "How well do your highlights help you create summaries or study guides afterwards?",
        "options": [
            ("Extremely well – summaries are easy to build", 0),
            ("Well – summaries are mostly straightforward", 1),
            ("Adequately – some effort required", 2),
            ("Poorly – significant effort still needed", 3),
            ("Very poorly – highlights are of no use", 4),
        ],
    },
    {
        "id": 13,
        "text": "How aware are you of evidence-based best practices for effective keyword highlighting?",
        "options": [
            ("Very aware – I actively apply research-based methods", 0),
            ("Aware – I know and apply some practices", 1),
            ("Somewhat aware – I know a little", 2),
            ("Barely aware – I have little knowledge", 3),
            ("Not aware – I have never studied the topic", 4),
        ],
    },
    {
        "id": 14,
        "text": "How often does re-reading your highlights feel insufficient, making you re-read the full text?",
        "options": [
            ("Never – highlights are always sufficient", 0),
            ("Rarely – almost always sufficient", 1),
            ("Sometimes – occasionally insufficient", 2),
            ("Often – frequently insufficient", 3),
            ("Always – I always have to re-read fully", 4),
        ],
    },
    {
        "id": 15,
        "text": "How satisfied are you with your current highlighting and quick-review strategy overall?",
        "options": [
            ("Very satisfied – it works excellently for me", 0),
            ("Satisfied – it works well", 1),
            ("Neutral – it works adequately", 2),
            ("Dissatisfied – it needs improvement", 3),
            ("Very dissatisfied – it does not work for me", 4),
        ],
    },
]

# Score-to-psychological-state mapping
SCORE_BANDS = [
    (0,  15, "Excellent Highlighter",
     "Your keyword highlighting and quick-review skills are outstanding. "
     "You demonstrate highly efficient cognitive reading habits. No intervention needed."),
    (16, 25, "Proficient Reviewer",
     "You have strong highlighting habits with minor room for refinement. "
     "Continue your current practices and explore colour-coding strategies."),
    (26, 35, "Adequate Practitioner",
     "Your skills are functional but inconsistent. Consider adopting a structured "
     "highlighting system to improve review speed and retention."),
    (36, 45, "Developing Learner",
     "Your highlighting efficiency is below average. Significant improvement is possible "
     "through deliberate practice and study-skills workshops."),
    (46, 55, "Struggling Reviewer",
     "You are experiencing notable difficulty with keyword identification and review. "
     "Seeking academic support or attending literacy skill sessions is advisable."),
    (56, 60, "Inefficient Processor",
     "Your current highlighting approach may be actively hindering comprehension. "
     "Professional academic coaching is strongly recommended."),
]

# ──────────────────────────────────────────────
#  UTILITY FUNCTIONS
# ──────────────────────────────────────────────

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_banner():
    """Print the programme title banner."""
    banner = """
╔══════════════════════════════════════════════════════════════════╗
║   KEYWORD HIGHLIGHTING & QUICK REVIEW EFFICIENCY SURVEY         ║
║   Psychological State Assessment Tool  v1.0                      ║
╚══════════════════════════════════════════════════════════════════╝
"""
    print(banner)


def print_separator(char: str = "─", width: int = 66):
    """Print a horizontal separator line."""
    print(char * width)


# ──────────────────────────────────────────────
#  INPUT VALIDATION FUNCTIONS
# ──────────────────────────────────────────────

def validate_name(name: str) -> bool:
    """
    Validate that a name contains only letters, hyphens,
    apostrophes, and spaces.  Covers O'Connor, Smith-Jones, Mary Ann.
    Returns True if valid, False otherwise.
    """
    pattern = r"^[A-Za-z][A-Za-z\s\-']*$"
    return bool(re.match(pattern, name.strip())) and len(name.strip()) >= 1


def validate_date_of_birth(dob: str) -> bool:
    """
    Validate date of birth in DD/MM/YYYY format.
    Checks format correctness, valid calendar date, and sensible age range.
    Returns True if valid, False otherwise.
    """
    try:
        date_obj = datetime.strptime(dob.strip(), "%d/%m/%Y")
        today = datetime.today()
        # Must be in the past and person must be ≤ 120 years old
        if date_obj >= today:
            return False
        age_years = (today - date_obj).days / 365.25
        return 0 < age_years <= 120
    except ValueError:
        return False


def validate_student_id(sid: str) -> bool:
    """
    Validate student ID: must contain digits only.
    Returns True if valid, False otherwise.
    """
    return sid.strip().isdigit() and len(sid.strip()) > 0


def get_valid_input(prompt: str, validator, error_msg: str,
                    max_attempts: int = 5) -> str:
    """
    Generic input collector with validation loop (for loop variant).
    Returns the validated input string.
    """
    # for loop attempt — used for a fixed number of retries
    for attempt in range(max_attempts):
        value = input(prompt).strip()
        if validator(value):
            return value
        remaining = max_attempts - attempt - 1
        if remaining > 0:
            print(f"  ✗  {error_msg}  ({remaining} attempt(s) remaining)")
        else:
            print(f"  ✗  {error_msg}  No more attempts. Exiting.")
            raise ValueError(f"Validation failed after {max_attempts} attempts.")
    return ""   # unreachable but satisfies linter


def get_valid_input_while(prompt: str, validator, error_msg: str) -> str:
    """
    Generic input collector with while loop (unlimited retries).
    Returns the validated input string.
    """
    # while loop — used when we want unlimited retries
    while True:
        value = input(prompt).strip()
        if validator(value):
            return value
        print(f"  ✗  {error_msg}")


# ──────────────────────────────────────────────
#  FILE I/O FUNCTIONS
# ──────────────────────────────────────────────

def load_questions_from_file(filepath: str) -> list:
    """
    Load survey questions from an external JSON file.
    Falls back to DEFAULT_QUESTIONS on any error.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        print(f"  ✓  Questions loaded from '{filepath}'.")
        return data
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        print(f"  ⚠  Could not load questions from file ({exc}). "
              "Using built-in questions.")
        return DEFAULT_QUESTIONS


def save_results_txt(result: dict, filepath: str) -> bool:
    """Save survey results to a plain text file."""
    try:
        with open(filepath, "w", encoding="utf-8") as fh:
            fh.write("KEYWORD HIGHLIGHTING & QUICK REVIEW EFFICIENCY SURVEY\n")
            fh.write("=" * 60 + "\n")
            fh.write(f"Name          : {result['name']}\n")
            fh.write(f"Date of Birth : {result['dob']}\n")
            fh.write(f"Student ID    : {result['student_id']}\n")
            fh.write(f"Date Taken    : {result['date_taken']}\n")
            fh.write(f"Total Score   : {result['score']}\n")
            fh.write(f"State         : {result['state']}\n")
            fh.write(f"Description   : {result['description']}\n")
            fh.write("-" * 60 + "\n")
            fh.write("Answers:\n")
            for i, ans in enumerate(result['answers'], 1):
                fh.write(f"  Q{i:02d}: {ans['option_text']} (score: {ans['points']})\n")
        return True
    except IOError as exc:
        print(f"  ✗  Error saving TXT: {exc}")
        return False


def save_results_csv(result: dict, filepath: str) -> bool:
    """Save survey results to a CSV file."""
    try:
        with open(filepath, "w", newline="", encoding="utf-8") as fh:
            # Header row
            fieldnames = [
                "name", "dob", "student_id", "date_taken",
                "score", "state", "description"
            ]
            writer = csv.DictWriter(fh, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({
                "name": result["name"],
                "dob": result["dob"],
                "student_id": result["student_id"],
                "date_taken": result["date_taken"],
                "score": result["score"],
                "state": result["state"],
                "description": result["description"],
            })
            # Answers section
            fh.write("\nQuestion,Selected Option,Points\n")
            for i, ans in enumerate(result["answers"], 1):
                fh.write(f"Q{i:02d},{ans['option_text']},{ans['points']}\n")
        return True
    except IOError as exc:
        print(f"  ✗  Error saving CSV: {exc}")
        return False


def save_results_json(result: dict, filepath: str) -> bool:
    """Save survey results to a JSON file."""
    try:
        with open(filepath, "w", encoding="utf-8") as fh:
            json.dump(result, fh, indent=4, ensure_ascii=False)
        return True
    except IOError as exc:
        print(f"  ✗  Error saving JSON: {exc}")
        return False


def display_loaded_result(filepath: str) -> None:
    """Load and display a previously saved result file."""
    ext = os.path.splitext(filepath)[1].lower()
    try:
        if ext == ".json":
            with open(filepath, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            print_separator()
            print("  LOADED SURVEY RESULT")
            print_separator()
            print(f"  Name          : {data.get('name', 'N/A')}")
            print(f"  Date of Birth : {data.get('dob', 'N/A')}")
            print(f"  Student ID    : {data.get('student_id', 'N/A')}")
            print(f"  Date Taken    : {data.get('date_taken', 'N/A')}")
            print(f"  Total Score   : {data.get('score', 'N/A')}")
            print(f"  State         : {data.get('state', 'N/A')}")
            print(f"  Description   : {data.get('description', 'N/A')}")
            answers = data.get("answers", [])
            if answers:
                print_separator("-")
                print("  Answers:")
                for i, ans in enumerate(answers, 1):
                    print(f"    Q{i:02d}: {ans.get('option_text','?')} "
                          f"(score: {ans.get('points','?')})")
        elif ext == ".csv":
            with open(filepath, "r", encoding="utf-8") as fh:
                content = fh.read()
            print_separator()
            print("  LOADED SURVEY RESULT (CSV)")
            print_separator()
            print(content)
        elif ext == ".txt":
            with open(filepath, "r", encoding="utf-8") as fh:
                content = fh.read()
            print_separator()
            print(content)
        else:
            print("  ⚠  Unsupported file format. Supported: .json, .csv, .txt")
    except (FileNotFoundError, json.JSONDecodeError, IOError) as exc:
        print(f"  ✗  Could not load result file: {exc}")


# ──────────────────────────────────────────────
#  CORE SURVEY CLASS
# ──────────────────────────────────────────────

class Survey:
    """
    Encapsulates the entire survey workflow:
    - Storing questions and score bands
    - Collecting and validating user details
    - Running the questionnaire
    - Scoring and interpreting results
    - Saving / loading results
    """

    def __init__(self, questions: list = None):
        # Variable types used: list, dict, tuple, int, str, float, bool, set, frozenset, range
        self.questions: list = questions if questions else DEFAULT_QUESTIONS
        self.score_bands: list = SCORE_BANDS
        self.answers: list = []          # list of dicts
        self.total_score: int = 0
        self.state: str = ""
        self.description: str = ""
        self.name: str = ""
        self.dob: str = ""
        self.student_id: str = ""
        self.date_taken: str = datetime.now().strftime("%d/%m/%Y %H:%M")

        # Demonstrate set, frozenset, tuple, range, float, bool usage
        self._valid_formats: set = {"txt", "csv", "json"}
        self._immutable_formats: frozenset = frozenset({"txt", "csv", "json"})
        self._score_range: range = range(0, 61)
        self._version: float = 1.0
        self._is_complete: bool = False

    # ── User detail collection ─────────────────

    def collect_user_details(self) -> None:
        """Prompt for and validate user personal details."""
        print_separator()
        print("  PARTICIPANT DETAILS")
        print_separator()

        # Surname — for loop validation (get_valid_input uses for internally)
        self.name = get_valid_input(
            "  Surname and Given Name : ",
            validate_name,
            "Name may only contain letters, hyphens (-), apostrophes ('), and spaces."
        )

        # Date of birth — while loop validation (get_valid_input_while)
        self.dob = get_valid_input_while(
            "  Date of Birth (DD/MM/YYYY): ",
            validate_date_of_birth,
            "Invalid date. Use DD/MM/YYYY format with a valid past date."
        )

        # Student ID — for loop validation
        self.student_id = get_valid_input(
            "  Student ID (digits only) : ",
            validate_student_id,
            "Student ID must contain digits only (no letters or symbols)."
        )

    # ── Question runner ────────────────────────

    def run(self) -> None:
        """
        Present all questions to the user and collect answers.
        Uses a for loop to iterate questions and a while loop for
        answer validation.
        """
        print_separator()
        print(f"  SURVEY  ({len(self.questions)} questions)")
        print("  For each question, enter the number of your answer.\n")
        print_separator()

        self.answers = []
        self.total_score = 0

        for q in self.questions:          # for loop: iterating questions
            print(f"\n  Q{q['id']:02d}. {q['text']}")
            options: list = q["options"]

            for idx, (opt_text, _pts) in enumerate(options, 1):
                print(f"       {idx}. {opt_text}")

            # while loop: answer input validation
            choice: int = 0
            while True:
                raw = input(f"       Your choice (1–{len(options)}): ").strip()
                if raw.isdigit():
                    choice = int(raw)
                    if 1 <= choice <= len(options):
                        break
                print(f"       ✗  Please enter a number between 1 and {len(options)}.")

            chosen_text, chosen_pts = options[choice - 1]
            self.answers.append({
                "question_id": q["id"],
                "option_text": chosen_text,
                "points": chosen_pts,
            })
            self.total_score += chosen_pts

        self._is_complete = True
        self._interpret_score()

    # ── Score interpretation ───────────────────

    def _interpret_score(self) -> None:
        """Determine psychological state from total score using if/elif/else."""
        score: int = self.total_score
        # Conditional statements (if / elif / else)
        if score < 0:
            self.state = "Invalid Score"
            self.description = "Score is out of range."
        elif score <= 15:
            self.state = self.score_bands[0][2]
            self.description = self.score_bands[0][3]
        elif score <= 25:
            self.state = self.score_bands[1][2]
            self.description = self.score_bands[1][3]
        elif score <= 35:
            self.state = self.score_bands[2][2]
            self.description = self.score_bands[2][3]
        elif score <= 45:
            self.state = self.score_bands[3][2]
            self.description = self.score_bands[3][3]
        elif score <= 55:
            self.state = self.score_bands[4][2]
            self.description = self.score_bands[4][3]
        else:
            self.state = self.score_bands[5][2]
            self.description = self.score_bands[5][3]

    # ── Results display ────────────────────────

    def display_results(self) -> None:
        """Print a formatted results summary."""
        print_separator("═")
        print("  SURVEY RESULTS")
        print_separator("═")
        print(f"  Name          : {self.name}")
        print(f"  Date of Birth : {self.dob}")
        print(f"  Student ID    : {self.student_id}")
        print(f"  Date Taken    : {self.date_taken}")
        print(f"  Total Score   : {self.total_score}  (max possible: {4 * len(self.questions)})")
        print_separator()
        print(f"  Psychological State : {self.state}")
        print(f"  Assessment          : {self.description}")
        print_separator("═")

    # ── Build result dict ─────────────────────

    def _build_result_dict(self) -> dict:
        """Assemble a dictionary of all result data for serialisation."""
        return {
            "name": self.name,
            "dob": self.dob,
            "student_id": self.student_id,
            "date_taken": self.date_taken,
            "score": self.total_score,
            "state": self.state,
            "description": self.description,
            "answers": self.answers,
        }

    # ── Save results ──────────────────────────

    def save_results(self) -> None:
        """Prompt the user to choose a file format and save the results."""
        print("\n  Save results?")
        print("  1. Yes – TXT")
        print("  2. Yes – CSV")
        print("  3. Yes – JSON")
        print("  4. No  – Skip")

        while True:
            choice = input("  Your choice (1–4): ").strip()
            if choice in {"1", "2", "3", "4"}:
                break
            print("  ✗  Please enter 1, 2, 3, or 4.")

        if choice == "4":
            print("  Results not saved.")
            return

        # Build safe filename
        safe_name = re.sub(r"[^\w]", "_", self.name)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        fmt_map = {"1": "txt", "2": "csv", "3": "json"}
        fmt: str = fmt_map[choice]
        filepath: str = f"result_{safe_name}_{timestamp}.{fmt}"

        result: dict = self._build_result_dict()

        if fmt == "txt":
            success: bool = save_results_txt(result, filepath)
        elif fmt == "csv":
            success = save_results_csv(result, filepath)
        else:
            success = save_results_json(result, filepath)

        if success:
            print(f"  ✓  Results saved to '{filepath}'.")
        else:
            print("  ✗  Failed to save results.")


# ──────────────────────────────────────────────
#  MAIN MENU & ENTRY POINT
# ──────────────────────────────────────────────

def main_menu() -> str:
    """Display the main menu and return the user's choice."""
    print_separator()
    print("  MAIN MENU")
    print_separator()
    print("  1. Start a new survey")
    print("  2. Load existing results from file")
    print("  3. Exit")
    print_separator()

    # while loop for menu input validation
    while True:
        choice = input("  Select option (1–3): ").strip()
        if choice in {"1", "2", "3"}:
            return choice
        print("  ✗  Invalid option. Please enter 1, 2, or 3.")


def choose_question_source() -> list:
    """Ask user whether to use built-in or file-based questions."""
    print_separator()
    print("  QUESTION SOURCE")
    print_separator()
    print("  1. Use built-in questions (hardcoded)")
    print("  2. Load questions from external file")

    while True:
        choice = input("  Select option (1–2): ").strip()
        if choice in {"1", "2"}:
            break
        print("  ✗  Please enter 1 or 2.")

    if choice == "2":
        path = input("  Enter path to questions JSON file: ").strip()
        return load_questions_from_file(path)
    return DEFAULT_QUESTIONS


def run_new_survey() -> None:
    """Orchestrate a complete new survey session."""
    questions: list = choose_question_source()
    survey = Survey(questions)
    survey.collect_user_details()
    survey.run()
    survey.display_results()
    survey.save_results()


def load_existing_result() -> None:
    """Prompt for a file path and display the stored result."""
    print_separator()
    print("  LOAD EXISTING RESULT")
    print_separator()
    filepath = input("  Enter path to result file (.json / .csv / .txt): ").strip()
    display_loaded_result(filepath)


def main() -> None:
    """Main programme entry point."""
    print_banner()

    while True:
        choice: str = main_menu()

        if choice == "1":
            run_new_survey()
        elif choice == "2":
            load_existing_result()
        else:
            print("\n  Goodbye!\n")
            break

        input("\n  Press Enter to return to the main menu…")
        clear_screen()
        print_banner()


# ──────────────────────────────────────────────
#  Script entry guard
# ──────────────────────────────────────────────
if __name__ == "__main__":
    main()
