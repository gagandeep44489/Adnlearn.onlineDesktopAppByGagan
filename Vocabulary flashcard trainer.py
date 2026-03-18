import json
import random
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog


class FlashcardTrainer(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Vocabulary Flashcard Trainer")
        self.geometry("760x520")
        self.minsize(680, 480)

        self.deck_path = Path("vocabulary_deck.json")
        self.cards: list[dict[str, str]] = []
        self.current_index: int | None = None
        self.showing_answer = False
        self.correct_count = 0
        self.reviewed_count = 0

        self._build_ui()
        self._load_default_deck()

    def _build_ui(self) -> None:
        self.configure(padx=14, pady=14)

        toolbar = tk.Frame(self)
        toolbar.pack(fill="x", pady=(0, 10))

        tk.Button(toolbar, text="Add Card", command=self.add_card).pack(side="left")
        tk.Button(toolbar, text="Edit Current", command=self.edit_current_card).pack(side="left", padx=6)
        tk.Button(toolbar, text="Delete Current", command=self.delete_current_card).pack(side="left")

        tk.Button(toolbar, text="Shuffle", command=self.shuffle_cards).pack(side="left", padx=(18, 0))
        tk.Button(toolbar, text="Load Deck", command=self.load_deck).pack(side="left", padx=6)
        tk.Button(toolbar, text="Save Deck", command=self.save_deck).pack(side="left")

        self.progress_var = tk.StringVar(value="Reviewed: 0 | Correct: 0 | Accuracy: 0%")
        tk.Label(self, textvariable=self.progress_var, anchor="w").pack(fill="x")

        self.word_var = tk.StringVar(value="No cards yet. Add one to begin.")
        word_card = tk.Label(
            self,
            textvariable=self.word_var,
            relief="groove",
            bg="#F8FAFC",
            fg="#0F172A",
            font=("Segoe UI", 22, "bold"),
            wraplength=690,
            justify="center",
            padx=16,
            pady=28,
        )
        word_card.pack(fill="both", expand=True, pady=12)

        self.definition_var = tk.StringVar(value="")
        self.definition_label = tk.Label(
            self,
            textvariable=self.definition_var,
            relief="ridge",
            bg="#ECFEFF",
            fg="#155E75",
            font=("Segoe UI", 13),
            wraplength=690,
            justify="left",
            padx=12,
            pady=12,
        )
        self.definition_label.pack(fill="x")

        controls = tk.Frame(self)
        controls.pack(fill="x", pady=(12, 0))

        self.flip_button = tk.Button(controls, text="Show Definition", command=self.flip_card)
        self.flip_button.pack(side="left")

        self.correct_button = tk.Button(
            controls, text="I was Correct", command=lambda: self.score_answer(True), state="disabled"
        )
        self.correct_button.pack(side="left", padx=6)

        self.incorrect_button = tk.Button(
            controls, text="I was Incorrect", command=lambda: self.score_answer(False), state="disabled"
        )
        self.incorrect_button.pack(side="left")

        tk.Button(controls, text="Next Card", command=self.next_card).pack(side="right")

    def _load_default_deck(self) -> None:
        if self.deck_path.exists():
            self.cards = self._read_deck(self.deck_path)
        else:
            self.cards = [
                {"word": "ephemeral", "definition": "lasting for a very short time"},
                {"word": "meticulous", "definition": "showing careful attention to detail"},
                {"word": "ubiquitous", "definition": "existing or appearing everywhere"},
                {"word": "alleviate", "definition": "to make pain or a problem less severe"},
                {"word": "candid", "definition": "truthful and straightforward; frank"},
            ]
            self._write_deck(self.deck_path)

        self.next_card(first=True)

    def _read_deck(self, path: Path) -> list[dict[str, str]]:
        try:
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            parsed = [
                {"word": str(item["word"]).strip(), "definition": str(item["definition"]).strip()}
                for item in data
                if isinstance(item, dict) and item.get("word") and item.get("definition")
            ]
            return parsed
        except (OSError, json.JSONDecodeError) as exc:
            messagebox.showerror("Load error", f"Could not read deck:\n{exc}")
            return []

    def _write_deck(self, path: Path) -> None:
        try:
            with path.open("w", encoding="utf-8") as f:
                json.dump(self.cards, f, indent=2, ensure_ascii=False)
        except OSError as exc:
            messagebox.showerror("Save error", f"Could not save deck:\n{exc}")

    def _update_progress(self) -> None:
        accuracy = (self.correct_count / self.reviewed_count * 100) if self.reviewed_count else 0
        self.progress_var.set(
            f"Reviewed: {self.reviewed_count} | Correct: {self.correct_count} | Accuracy: {accuracy:.0f}%"
        )

    def _render_current_card(self) -> None:
        if self.current_index is None or not self.cards:
            self.word_var.set("No cards available.")
            self.definition_var.set("")
            self.flip_button.config(state="disabled")
            self.correct_button.config(state="disabled")
            self.incorrect_button.config(state="disabled")
            return

        card = self.cards[self.current_index]
        self.word_var.set(card["word"])
        if self.showing_answer:
            self.definition_var.set(card["definition"])
            self.flip_button.config(text="Hide Definition")
            self.correct_button.config(state="normal")
            self.incorrect_button.config(state="normal")
        else:
            self.definition_var.set("Try to recall the definition, then click Show Definition.")
            self.flip_button.config(text="Show Definition", state="normal")
            self.correct_button.config(state="disabled")
            self.incorrect_button.config(state="disabled")

    def next_card(self, first: bool = False) -> None:
        if not self.cards:
            self.current_index = None
            self.showing_answer = False
            self._render_current_card()
            return

        if self.current_index is None or first:
            self.current_index = random.randrange(len(self.cards))
        else:
            if len(self.cards) == 1:
                self.current_index = 0
            else:
                prev = self.current_index
                while self.current_index == prev:
                    self.current_index = random.randrange(len(self.cards))

        self.showing_answer = False
        self._render_current_card()

    def flip_card(self) -> None:
        if self.current_index is None:
            return
        self.showing_answer = not self.showing_answer
        self._render_current_card()

    def score_answer(self, was_correct: bool) -> None:
        self.reviewed_count += 1
        if was_correct:
            self.correct_count += 1
        self._update_progress()
        self.next_card()

    def add_card(self) -> None:
        word = simpledialog.askstring("New word", "Enter vocabulary word:")
        if not word:
            return
        definition = simpledialog.askstring("Definition", f"Enter definition for '{word}':")
        if not definition:
            return

        self.cards.append({"word": word.strip(), "definition": definition.strip()})
        self.current_index = len(self.cards) - 1
        self.showing_answer = False
        self._render_current_card()

    def edit_current_card(self) -> None:
        if self.current_index is None:
            messagebox.showinfo("No card", "There is no current card to edit.")
            return

        card = self.cards[self.current_index]
        word = simpledialog.askstring("Edit word", "Update word:", initialvalue=card["word"])
        if not word:
            return
        definition = simpledialog.askstring(
            "Edit definition", "Update definition:", initialvalue=card["definition"]
        )
        if not definition:
            return

        card["word"] = word.strip()
        card["definition"] = definition.strip()
        self._render_current_card()

    def delete_current_card(self) -> None:
        if self.current_index is None:
            return
        card = self.cards[self.current_index]
        if not messagebox.askyesno("Delete card", f"Delete '{card['word']}'?"):
            return

        del self.cards[self.current_index]
        if self.cards:
            self.current_index %= len(self.cards)
        else:
            self.current_index = None
        self.showing_answer = False
        self._render_current_card()

    def shuffle_cards(self) -> None:
        if len(self.cards) < 2:
            return
        random.shuffle(self.cards)
        self.current_index = 0
        self.showing_answer = False
        self._render_current_card()

    def load_deck(self) -> None:
        path = filedialog.askopenfilename(
            title="Open deck",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )
        if not path:
            return

        loaded = self._read_deck(Path(path))
        if loaded:
            self.cards = loaded
            self.current_index = None
            self.correct_count = 0
            self.reviewed_count = 0
            self._update_progress()
            self.next_card(first=True)

    def save_deck(self) -> None:
        path = filedialog.asksaveasfilename(
            title="Save deck",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )
        if not path:
            return
        self._write_deck(Path(path))
        messagebox.showinfo("Saved", "Deck saved successfully.")


if __name__ == "__main__":
    app = FlashcardTrainer()
    app.mainloop()