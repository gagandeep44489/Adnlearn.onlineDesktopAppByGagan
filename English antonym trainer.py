# English Antonym Trainer - Desktop App in Python
# Purpose:
# Help users practice English antonyms with instant feedback, hints, and scoring.

import random
import tkinter as tk
from tkinter import ttk, messagebox


ANTONYM_BANK = {
    "ancient": {"modern", "new"},
    "arrive": {"depart", "leave"},
    "ascent": {"descent"},
    "bold": {"timid", "shy"},
    "brave": {"cowardly", "timid"},
    "broad": {"narrow"},
    "calm": {"agitated", "nervous"},
    "chaos": {"order"},
    "cheap": {"expensive", "costly"},
    "clean": {"dirty"},
    "complex": {"simple"},
    "create": {"destroy"},
    "dawn": {"dusk"},
    "deep": {"shallow"},
    "early": {"late"},
    "empty": {"full"},
    "expand": {"contract", "shrink"},
    "famous": {"unknown", "obscure"},
    "fragile": {"sturdy", "strong"},
    "generous": {"stingy", "selfish"},
    "genuine": {"fake", "false"},
    "harsh": {"gentle", "mild"},
    "include": {"exclude", "omit"},
    "increase": {"decrease", "reduce"},
    "inner": {"outer"},
    "junior": {"senior"},
    "kind": {"cruel", "mean"},
    "loud": {"quiet", "silent"},
    "major": {"minor"},
    "optimistic": {"pessimistic"},
    "permit": {"forbid", "prohibit"},
    "protect": {"endanger", "harm"},
    "rapid": {"slow"},
    "regular": {"irregular"},
    "reward": {"punish", "penalty"},
    "scarce": {"abundant", "plentiful"},
    "secure": {"unsafe", "insecure"},
    "solid": {"liquid"},
    "temporary": {"permanent"},
    "victory": {"defeat", "loss"},
    "visible": {"invisible", "hidden"},
    "wisdom": {"ignorance"},
}


class AntonymTrainerApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("English Antonym Trainer")
        self.root.geometry("760x520")

        self.words = list(ANTONYM_BANK.keys())
        self.used_words = set()

        self.current_word = ""
        self.current_answers = set()

        self.total_questions = 0
        self.correct_answers = 0
        self.streak = 0

        self._build_ui()
        self.next_question()

    def _build_ui(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")

        frame = ttk.Frame(self.root, padding=14)
        frame.pack(fill=tk.BOTH, expand=True)

        title = ttk.Label(frame, text="English Antonym Trainer", font=("Segoe UI", 18, "bold"))
        title.pack(anchor="w")

        subtitle = ttk.Label(
            frame,
            text="Type an antonym for the shown word. Multiple correct answers are accepted.",
        )
        subtitle.pack(anchor="w", pady=(2, 12))

        quiz_box = ttk.LabelFrame(frame, text="Question", padding=12)
        quiz_box.pack(fill=tk.X)

        self.word_label = ttk.Label(quiz_box, text="Word: -", font=("Segoe UI", 16, "bold"))
        self.word_label.pack(anchor="w")

        entry_row = ttk.Frame(quiz_box)
        entry_row.pack(fill=tk.X, pady=(10, 2))

        ttk.Label(entry_row, text="Your antonym:").pack(side=tk.LEFT)
        self.answer_var = tk.StringVar()
        self.answer_entry = ttk.Entry(entry_row, textvariable=self.answer_var, width=40)
        self.answer_entry.pack(side=tk.LEFT, padx=8)
        self.answer_entry.bind("<Return>", lambda _event: self.check_answer())

        self.feedback_var = tk.StringVar(value="Enter your answer and click Check.")
        feedback_label = ttk.Label(quiz_box, textvariable=self.feedback_var, foreground="#174ea6")
        feedback_label.pack(anchor="w", pady=(8, 0))

        controls = ttk.Frame(frame)
        controls.pack(fill=tk.X, pady=12)

        ttk.Button(controls, text="Check", command=self.check_answer).pack(side=tk.LEFT)
        ttk.Button(controls, text="Next", command=self.next_question).pack(side=tk.LEFT, padx=8)
        ttk.Button(controls, text="Hint", command=self.show_hint).pack(side=tk.LEFT)
        ttk.Button(controls, text="Restart", command=self.restart).pack(side=tk.RIGHT)

        progress = ttk.LabelFrame(frame, text="Progress", padding=12)
        progress.pack(fill=tk.X)

        self.score_var = tk.StringVar(value="Score: 0/0")
        self.streak_var = tk.StringVar(value="Current Streak: 0")
        self.accuracy_var = tk.StringVar(value="Accuracy: 0.0%")

        ttk.Label(progress, textvariable=self.score_var, font=("Segoe UI", 11, "bold")).pack(anchor="w")
        ttk.Label(progress, textvariable=self.streak_var).pack(anchor="w", pady=2)
        ttk.Label(progress, textvariable=self.accuracy_var).pack(anchor="w")

        tip = ttk.Label(
            frame,
            text="Tip: Answers are case-insensitive. Example: antonym of 'early' is 'late'.",
            foreground="#555555",
        )
        tip.pack(anchor="w", pady=(12, 0))

    def _normalize(self, text: str) -> str:
        return text.strip().lower()

    def _update_progress_labels(self):
        self.score_var.set(f"Score: {self.correct_answers}/{self.total_questions}")
        self.streak_var.set(f"Current Streak: {self.streak}")
        accuracy = (self.correct_answers / self.total_questions * 100) if self.total_questions else 0.0
        self.accuracy_var.set(f"Accuracy: {accuracy:.1f}%")

    def next_question(self):
        if len(self.used_words) == len(self.words):
            self.used_words.clear()

        remaining = [w for w in self.words if w not in self.used_words]
        self.current_word = random.choice(remaining)
        self.current_answers = ANTONYM_BANK[self.current_word]
        self.used_words.add(self.current_word)

        self.word_label.config(text=f"Word: {self.current_word}")
        self.answer_var.set("")
        self.feedback_var.set("Enter your answer and click Check.")
        self.answer_entry.focus_set()

    def check_answer(self):
        answer = self._normalize(self.answer_var.get())
        if not answer:
            messagebox.showwarning("Missing Answer", "Please type an antonym before checking.")
            return

        self.total_questions += 1
        if answer in self.current_answers:
            self.correct_answers += 1
            self.streak += 1
            self.feedback_var.set("✅ Correct! Great job.")
        else:
            self.streak = 0
            accepted = ", ".join(sorted(self.current_answers))
            self.feedback_var.set(f"❌ Not quite. Accepted antonym(s): {accepted}")

        self._update_progress_labels()

    def show_hint(self):
        if not self.current_answers:
            return
        sample = sorted(self.current_answers)[0]
        if len(sample) <= 1:
            hint = sample
        else:
            hint = sample[0] + "_" * (len(sample) - 1)
        self.feedback_var.set(f"Hint: starts with '{hint[0]}' and has {len(sample)} letters.")

    def restart(self):
        self.total_questions = 0
        self.correct_answers = 0
        self.streak = 0
        self.used_words.clear()
        self._update_progress_labels()
        self.next_question()


if __name__ == "__main__":
    root = tk.Tk()
    app = AntonymTrainerApp(root)
    root.mainloop()