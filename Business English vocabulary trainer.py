import random
import tkinter as tk
from tkinter import messagebox


VOCABULARY = [
    {
        "word": "Agenda",
        "definition": "A list of topics to be discussed at a meeting.",
        "example": "Please review the agenda before the client call.",
    },
    {
        "word": "Benchmark",
        "definition": "A standard used to compare business performance.",
        "example": "Our sales benchmark for Q2 is 15% growth.",
    },
    {
        "word": "Deadline",
        "definition": "The latest time or date by which something must be finished.",
        "example": "The proposal deadline is Friday at 5 PM.",
    },
    {
        "word": "Revenue",
        "definition": "Income generated from normal business operations.",
        "example": "Monthly revenue increased after the marketing campaign.",
    },
    {
        "word": "Stakeholder",
        "definition": "A person or group with an interest in a business decision.",
        "example": "We need stakeholder approval before launch.",
    },
    {
        "word": "Leverage",
        "definition": "To use something to maximum advantage.",
        "example": "We can leverage customer feedback to improve the product.",
    },
    {
        "word": "Negotiation",
        "definition": "Discussion aimed at reaching an agreement.",
        "example": "The contract negotiation took three meetings.",
    },
    {
        "word": "Forecast",
        "definition": "A prediction of future business outcomes.",
        "example": "The finance team shared a quarterly forecast.",
    },
    {
        "word": "Minutes",
        "definition": "The official written record of a meeting.",
        "example": "I emailed the meeting minutes to the team.",
    },
    {
        "word": "Onboarding",
        "definition": "The process of integrating a new employee into a company.",
        "example": "Our onboarding program lasts two weeks.",
    },
    {
        "word": "Pipeline",
        "definition": "A series of potential opportunities in progress.",
        "example": "The sales pipeline looks strong this month.",
    },
    {
        "word": "ROI",
        "definition": "Return on Investment; a measure of profitability.",
        "example": "This project delivered an excellent ROI.",
    },
]


class BusinessEnglishTrainer:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Business English Vocabulary Trainer")
        self.root.geometry("700x460")
        self.root.minsize(650, 420)

        self.cards = VOCABULARY[:]
        random.shuffle(self.cards)
        self.index = 0
        self.correct_answers = 0
        self.questions_asked = 0
        self.is_definition_visible = False

        self.word_var = tk.StringVar()
        self.definition_var = tk.StringVar()
        self.example_var = tk.StringVar()
        self.score_var = tk.StringVar()

        self._build_ui()
        self._show_card()
        self._update_score()

    def _build_ui(self) -> None:
        title = tk.Label(
            self.root,
            text="Business English Vocabulary Trainer",
            font=("Segoe UI", 18, "bold"),
            fg="#143B66",
        )
        title.pack(pady=(18, 8))

        card_frame = tk.Frame(self.root, bd=2, relief="groove", padx=20, pady=16)
        card_frame.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(card_frame, text="Word", font=("Segoe UI", 12, "bold")).pack(anchor="w")
        tk.Label(
            card_frame,
            textvariable=self.word_var,
            font=("Segoe UI", 24, "bold"),
            fg="#0B5E8E",
            pady=8,
        ).pack(anchor="w")

        tk.Label(card_frame, text="Definition", font=("Segoe UI", 12, "bold")).pack(anchor="w")
        tk.Label(
            card_frame,
            textvariable=self.definition_var,
            font=("Segoe UI", 12),
            wraplength=620,
            justify="left",
            pady=4,
        ).pack(anchor="w")

        tk.Label(card_frame, text="Example", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(8, 0))
        tk.Label(
            card_frame,
            textvariable=self.example_var,
            font=("Segoe UI", 11, "italic"),
            fg="#37474F",
            wraplength=620,
            justify="left",
            pady=4,
        ).pack(anchor="w")

        quiz_frame = tk.Frame(self.root, padx=20, pady=8)
        quiz_frame.pack(fill="x")

        tk.Label(quiz_frame, text="Type the vocabulary word:", font=("Segoe UI", 11)).pack(anchor="w")
        self.answer_entry = tk.Entry(quiz_frame, font=("Segoe UI", 12), width=35)
        self.answer_entry.pack(anchor="w", pady=6)
        self.answer_entry.bind("<Return>", self._check_answer)

        controls = tk.Frame(self.root, pady=6)
        controls.pack(fill="x")

        tk.Button(controls, text="Show/Hide Meaning", command=self._toggle_definition, width=18).pack(
            side="left", padx=20
        )
        tk.Button(controls, text="Check Answer", command=self._check_answer, width=14).pack(side="left", padx=4)
        tk.Button(controls, text="Next Word", command=self._next_card, width=12).pack(side="left", padx=4)
        tk.Button(controls, text="Shuffle", command=self._shuffle_cards, width=10).pack(side="left", padx=4)

        tk.Label(
            self.root,
            textvariable=self.score_var,
            font=("Segoe UI", 11, "bold"),
            fg="#2E7D32",
            pady=8,
        ).pack(anchor="w", padx=20)

    def _current_card(self) -> dict:
        return self.cards[self.index]

    def _show_card(self) -> None:
        card = self._current_card()
        self.word_var.set(card["word"])
        if self.is_definition_visible:
            self.definition_var.set(card["definition"])
            self.example_var.set(card["example"])
        else:
            self.definition_var.set("(Hidden) Click 'Show/Hide Meaning' to reveal.")
            self.example_var.set("(Hidden until meaning is shown.)")

    def _toggle_definition(self) -> None:
        self.is_definition_visible = not self.is_definition_visible
        self._show_card()

    def _check_answer(self, _event=None) -> None:
        user_answer = self.answer_entry.get().strip()
        correct_word = self._current_card()["word"]

        if not user_answer:
            messagebox.showinfo("Input required", "Please type your answer before checking.")
            return

        self.questions_asked += 1
        if user_answer.lower() == correct_word.lower():
            self.correct_answers += 1
            messagebox.showinfo("Correct", f"Great! '{correct_word}' is right.")
            self._next_card()
        else:
            messagebox.showwarning(
                "Try Again",
                f"Not quite. Correct word: {correct_word}\nHint: reveal the meaning if needed.",
            )
        self._update_score()

    def _next_card(self) -> None:
        self.index = (self.index + 1) % len(self.cards)
        self.answer_entry.delete(0, tk.END)
        self.is_definition_visible = False
        self._show_card()

    def _shuffle_cards(self) -> None:
        random.shuffle(self.cards)
        self.index = 0
        self.answer_entry.delete(0, tk.END)
        self.is_definition_visible = False
        self._show_card()

    def _update_score(self) -> None:
        accuracy = (self.correct_answers / self.questions_asked * 100) if self.questions_asked else 0.0
        self.score_var.set(
            f"Score: {self.correct_answers}/{self.questions_asked} correct  |  Accuracy: {accuracy:.1f}%"
        )


def main() -> None:
    root = tk.Tk()
    app = BusinessEnglishTrainer(root)
    _ = app
    root.mainloop()


if __name__ == "__main__":
    main()