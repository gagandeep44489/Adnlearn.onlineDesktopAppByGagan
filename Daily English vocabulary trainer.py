import random
import tkinter as tk
from tkinter import messagebox, ttk


VOCAB_WORDS = [
    {
        "word": "Abundant",
        "definition": "Existing in large quantities; plentiful.",
        "example": "Fresh water is abundant in this region during the rainy season.",
    },
    {
        "word": "Candid",
        "definition": "Truthful and straightforward; frank.",
        "example": "She gave a candid review of the presentation.",
    },
    {
        "word": "Diligent",
        "definition": "Showing careful and persistent effort.",
        "example": "He is a diligent student who studies every day.",
    },
    {
        "word": "Eloquent",
        "definition": "Fluent or persuasive in speaking or writing.",
        "example": "The speaker gave an eloquent speech about education.",
    },
    {
        "word": "Frugal",
        "definition": "Careful with money and resources; economical.",
        "example": "Being frugal helped her save for college.",
    },
    {
        "word": "Impeccable",
        "definition": "In accordance with the highest standards; flawless.",
        "example": "His manners were impeccable at the formal dinner.",
    },
    {
        "word": "Meticulous",
        "definition": "Showing great attention to detail; very careful.",
        "example": "The designer was meticulous about every measurement.",
    },
    {
        "word": "Novice",
        "definition": "A person new to or inexperienced in a field.",
        "example": "Even as a novice, she learned quickly.",
    },
    {
        "word": "Pragmatic",
        "definition": "Dealing with things realistically and sensibly.",
        "example": "They took a pragmatic approach to solve the problem.",
    },
    {
        "word": "Resilient",
        "definition": "Able to recover quickly from difficulties.",
        "example": "Children can be surprisingly resilient after setbacks.",
    },
    {
        "word": "Sporadic",
        "definition": "Occurring at irregular intervals; scattered.",
        "example": "The internet connection was sporadic during the storm.",
    },
    {
        "word": "Vivid",
        "definition": "Producing powerful feelings or clear images in the mind.",
        "example": "The novel gives a vivid description of village life.",
    },
]


class VocabularyTrainerApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Daily English Vocabulary Trainer")
        self.root.geometry("760x520")
        self.root.minsize(700, 480)

        self.correct_answers = 0
        self.attempts = 0
        self.current_word = None
        self.question_type = tk.StringVar(value="Definition")

        self._build_ui()
        self.load_new_word()

    def _build_ui(self):
        title_label = ttk.Label(
            self.root,
            text="Daily English Vocabulary Trainer",
            font=("Segoe UI", 20, "bold"),
        )
        title_label.pack(pady=(18, 8))

        subtitle = ttk.Label(
            self.root,
            text="Learn one word at a time, then test yourself!",
            font=("Segoe UI", 11),
        )
        subtitle.pack(pady=(0, 14))

        self.word_label = ttk.Label(
            self.root,
            text="",
            font=("Segoe UI", 22, "bold"),
            foreground="#0b5394",
        )
        self.word_label.pack(pady=(4, 10))

        info_frame = ttk.Frame(self.root)
        info_frame.pack(fill="x", padx=24)

        ttk.Label(info_frame, text="Definition:", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.definition_label = ttk.Label(
            info_frame,
            text="",
            font=("Segoe UI", 11),
            wraplength=680,
            justify="left",
        )
        self.definition_label.pack(anchor="w", pady=(2, 10))

        ttk.Label(info_frame, text="Example:", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.example_label = ttk.Label(
            info_frame,
            text="",
            font=("Segoe UI", 11, "italic"),
            wraplength=680,
            justify="left",
        )
        self.example_label.pack(anchor="w", pady=(2, 12))

        quiz_frame = ttk.LabelFrame(self.root, text="Quick Quiz")
        quiz_frame.pack(fill="x", padx=24, pady=8)

        type_frame = ttk.Frame(quiz_frame)
        type_frame.pack(anchor="w", padx=12, pady=(8, 4))
        ttk.Label(type_frame, text="Question Type:").pack(side="left", padx=(0, 8))
        ttk.Radiobutton(
            type_frame,
            text="Definition",
            value="Definition",
            variable=self.question_type,
            command=self.update_prompt,
        ).pack(side="left", padx=4)
        ttk.Radiobutton(
            type_frame,
            text="Word",
            value="Word",
            variable=self.question_type,
            command=self.update_prompt,
        ).pack(side="left", padx=4)

        self.question_prompt = ttk.Label(
            quiz_frame,
            text="",
            font=("Segoe UI", 10),
            wraplength=660,
            justify="left",
        )
        self.question_prompt.pack(anchor="w", padx=12, pady=(2, 6))

        self.answer_entry = ttk.Entry(quiz_frame, font=("Segoe UI", 11))
        self.answer_entry.pack(fill="x", padx=12)
        self.answer_entry.bind("<Return>", lambda event: self.check_answer())

        button_frame = ttk.Frame(quiz_frame)
        button_frame.pack(fill="x", padx=12, pady=10)

        ttk.Button(button_frame, text="Check Answer", command=self.check_answer).pack(side="left")
        ttk.Button(button_frame, text="Show Answer", command=self.show_answer).pack(side="left", padx=8)
        ttk.Button(button_frame, text="Next Word", command=self.load_new_word).pack(side="left")

        self.feedback_label = ttk.Label(self.root, text="", font=("Segoe UI", 11, "bold"))
        self.feedback_label.pack(pady=(8, 6))

        self.score_label = ttk.Label(self.root, text="Score: 0 / 0", font=("Segoe UI", 11))
        self.score_label.pack(pady=(0, 12))

    def load_new_word(self):
        self.current_word = random.choice(VOCAB_WORDS)
        self.word_label.config(text=self.current_word["word"])
        self.definition_label.config(text=self.current_word["definition"])
        self.example_label.config(text=self.current_word["example"])
        self.feedback_label.config(text="")
        self.answer_entry.delete(0, tk.END)
        self.update_prompt()
        self.answer_entry.focus_set()

    def update_prompt(self):
        if self.question_type.get() == "Definition":
            self.question_prompt.config(text="Type the definition of this word in your own words.")
        else:
            self.question_prompt.config(
                text=(
                    "Type the word that matches this definition:\n"
                    f"{self.current_word['definition']}"
                )
            )

    def check_answer(self):
        user_answer = self.answer_entry.get().strip()
        if not user_answer:
            messagebox.showinfo("Input Needed", "Please type an answer first.")
            return

        self.attempts += 1

        if self.question_type.get() == "Definition":
            is_correct = self._check_definition_answer(user_answer)
        else:
            is_correct = user_answer.lower() == self.current_word["word"].lower()

        if is_correct:
            self.correct_answers += 1
            self.feedback_label.config(text="✅ Correct! Great job.", foreground="#1b5e20")
        else:
            self.feedback_label.config(
                text=f"❌ Not quite. Correct answer: {self.current_word['word']}"
                if self.question_type.get() == "Word"
                else "❌ Not quite. Try including key idea words from the definition.",
                foreground="#8b0000",
            )

        self.score_label.config(text=f"Score: {self.correct_answers} / {self.attempts}")

    def _check_definition_answer(self, user_answer: str) -> bool:
        expected_words = {
            token.strip(".,;:!?\"'()[]{}").lower()
            for token in self.current_word["definition"].split()
            if len(token) > 3
        }
        answer_words = {
            token.strip(".,;:!?\"'()[]{}").lower() for token in user_answer.split()
        }
        overlap = expected_words.intersection(answer_words)
        return len(overlap) >= max(2, len(expected_words) // 4)

    def show_answer(self):
        if self.question_type.get() == "Definition":
            messagebox.showinfo("Definition", self.current_word["definition"])
        else:
            messagebox.showinfo("Word", self.current_word["word"])


if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    if "clam" in style.theme_names():
        style.theme_use("clam")
    app = VocabularyTrainerApp(root)
    root.mainloop()