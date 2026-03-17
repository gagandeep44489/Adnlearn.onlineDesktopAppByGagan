import importlib.util
import tkinter as tk
from tkinter import ttk, messagebox
import nltk
nltk.download('wordnet')


WORDNET_AVAILABLE = importlib.util.find_spec("nltk") is not None
if WORDNET_AVAILABLE:
    from nltk.corpus import wordnet  # type: ignore


FALLBACK_THESAURUS = {
    "happy": ["cheerful", "content", "delighted", "joyful", "pleased"],
    "sad": ["downcast", "gloomy", "melancholy", "sorrowful", "unhappy"],
    "fast": ["brisk", "quick", "rapid", "speedy", "swift"],
    "smart": ["bright", "clever", "intelligent", "sharp", "wise"],
    "small": ["compact", "little", "miniature", "petite", "tiny"],
    "big": ["enormous", "gigantic", "huge", "large", "massive"],
}


def get_synonyms_from_wordnet(word: str) -> list[str]:
    if not WORDNET_AVAILABLE:
        return []

    synonyms: set[str] = set()
    for synset in wordnet.synsets(word):
        for lemma in synset.lemmas():
            synonym = lemma.name().replace("_", " ").strip().lower()
            if synonym and synonym != word:
                synonyms.add(synonym)
    return sorted(synonyms)


def get_synonyms(word: str) -> list[str]:
    normalized = word.strip().lower()
    if not normalized:
        return []

    wordnet_results = get_synonyms_from_wordnet(normalized)
    if wordnet_results:
        return wordnet_results

    return FALLBACK_THESAURUS.get(normalized, [])


class SynonymFinderApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("English Synonym Finder")
        self.root.geometry("520x430")
        self.root.resizable(False, False)

        self.word_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Type a word and click Find Synonyms.")

        self._build_ui()

    def _build_ui(self) -> None:
        main = ttk.Frame(self.root, padding=18)
        main.pack(fill="both", expand=True)

        title = ttk.Label(
            main,
            text="English Synonym Finder",
            font=("Segoe UI", 16, "bold"),
        )
        title.pack(anchor="w", pady=(0, 10))

        subtitle = ttk.Label(
            main,
            text="Get synonyms for English words (WordNet + built-in fallback).",
            font=("Segoe UI", 10),
        )
        subtitle.pack(anchor="w", pady=(0, 12))

        input_frame = ttk.Frame(main)
        input_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(input_frame, text="Word:", font=("Segoe UI", 10, "bold")).pack(
            side="left", padx=(0, 8)
        )

        entry = ttk.Entry(input_frame, textvariable=self.word_var, width=32)
        entry.pack(side="left", padx=(0, 8))
        entry.bind("<Return>", self.find_synonyms)

        find_button = ttk.Button(
            input_frame,
            text="Find Synonyms",
            command=self.find_synonyms,
        )
        find_button.pack(side="left")

        self.results_listbox = tk.Listbox(main, height=14, font=("Segoe UI", 10))
        self.results_listbox.pack(fill="both", expand=True)

        status = ttk.Label(main, textvariable=self.status_var, foreground="#555")
        status.pack(anchor="w", pady=(10, 0))

    def find_synonyms(self, _event=None) -> None:
        word = self.word_var.get().strip()
        self.results_listbox.delete(0, tk.END)

        if not word:
            messagebox.showinfo("Input Required", "Please enter an English word.")
            self.status_var.set("No word entered.")
            return

        synonyms = get_synonyms(word)
        if not synonyms:
            self.status_var.set(f"No synonyms found for '{word}'.")
            return

        for item in synonyms:
            self.results_listbox.insert(tk.END, item)

        self.status_var.set(f"Found {len(synonyms)} synonym(s) for '{word}'.")


def main() -> None:
    root = tk.Tk()
    SynonymFinderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()