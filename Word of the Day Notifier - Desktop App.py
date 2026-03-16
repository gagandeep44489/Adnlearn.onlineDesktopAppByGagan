# Word of the Day Notifier - Desktop App in Python
# Purpose:
# Show a daily vocabulary word with definition and example sentence.
# Includes a timer that checks once per minute and notifies at a chosen time.

import json
import random
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk
from urllib.error import URLError
from urllib.request import urlopen


FALLBACK_WORDS = [
    {
        "word": "serendipity",
        "definition": "the occurrence of events by chance in a happy or beneficial way",
        "example": "Meeting her future cofounder at a small café was pure serendipity.",
    },
    {
        "word": "resilient",
        "definition": "able to withstand or recover quickly from difficult conditions",
        "example": "The resilient team adapted quickly after the server outage.",
    },
    {
        "word": "lucid",
        "definition": "expressed clearly; easy to understand",
        "example": "Her lucid explanation made the complex topic feel simple.",
    },
    {
        "word": "meticulous",
        "definition": "showing great attention to detail; very careful and precise",
        "example": "He kept meticulous notes during every stage of the experiment.",
    },
    {
        "word": "ubiquitous",
        "definition": "present, appearing, or found everywhere",
        "example": "Smartphones are now ubiquitous in modern life.",
    },
]


def fetch_word_online(timeout=8):
    """
    Fetch a random word from random-word API, then its meaning/example from dictionary API.
    Returns a dictionary with keys: word, definition, example.
    Raises ValueError if data is incomplete.
    """
    with urlopen("https://random-word-api.herokuapp.com/word", timeout=timeout) as resp:
        word_data = json.loads(resp.read().decode("utf-8"))

    if not word_data or not isinstance(word_data, list):
        raise ValueError("Unexpected random word response")

    word = word_data[0].strip()
    if not word:
        raise ValueError("Empty word received")

    with urlopen(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}", timeout=timeout) as resp:
        detail_data = json.loads(resp.read().decode("utf-8"))

    if not isinstance(detail_data, list) or not detail_data:
        raise ValueError("Unexpected dictionary response")

    entry = detail_data[0]
    meanings = entry.get("meanings", [])
    for meaning in meanings:
        definitions = meaning.get("definitions", [])
        for definition_item in definitions:
            definition = definition_item.get("definition", "").strip()
            example = definition_item.get("example", "").strip()
            if definition:
                return {
                    "word": word,
                    "definition": definition,
                    "example": example or "Example not available for this word.",
                }

    raise ValueError("No usable definition found")


def fallback_word():
    return random.choice(FALLBACK_WORDS)


class WordOfDayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Word of the Day Notifier")
        self.root.geometry("760x520")

        self.last_notified_date = None
        self.running_timer = False

        style = ttk.Style(root)
        style.theme_use("clam")

        container = ttk.Frame(root, padding=12)
        container.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            container,
            text="Word of the Day Notifier",
            font=("Segoe UI", 16, "bold"),
        ).pack(anchor="w", pady=(0, 6))

        ttk.Label(
            container,
            text="Fetch a word instantly or schedule a daily popup reminder.",
        ).pack(anchor="w", pady=(0, 8))

        schedule_frame = ttk.LabelFrame(container, text="Daily Reminder", padding=10)
        schedule_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(schedule_frame, text="Notify at (24h):").grid(row=0, column=0, sticky="w")

        self.hour_var = tk.StringVar(value="09")
        self.minute_var = tk.StringVar(value="00")

        self.hour_spin = ttk.Spinbox(schedule_frame, from_=0, to=23, width=4, textvariable=self.hour_var, wrap=True)
        self.minute_spin = ttk.Spinbox(schedule_frame, from_=0, to=59, width=4, textvariable=self.minute_var, wrap=True)

        self.hour_spin.grid(row=0, column=1, padx=(6, 3))
        ttk.Label(schedule_frame, text=":").grid(row=0, column=2)
        self.minute_spin.grid(row=0, column=3, padx=(3, 12))

        self.toggle_btn = ttk.Button(schedule_frame, text="Start Reminder", command=self.toggle_reminder)
        self.toggle_btn.grid(row=0, column=4, padx=4)

        self.status_var = tk.StringVar(value="Reminder stopped")
        ttk.Label(schedule_frame, textvariable=self.status_var).grid(row=1, column=0, columnspan=5, sticky="w", pady=(8, 0))

        actions = ttk.Frame(container)
        actions.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(actions, text="Get Word Now", command=self.show_word_now).pack(side=tk.LEFT)
        ttk.Button(actions, text="Use Offline Word", command=self.show_offline_word).pack(side=tk.LEFT, padx=8)

        ttk.Label(container, text="Current Word").pack(anchor="w")

        self.output = tk.Text(container, height=16, wrap="word")
        self.output.pack(fill=tk.BOTH, expand=True)
        self.output.insert(
            tk.END,
            "Click 'Get Word Now' to fetch from online dictionary APIs.\n"
            "If there is no internet or API error, use 'Use Offline Word'.",
        )
        self.output.config(state=tk.DISABLED)

    def parse_schedule_time(self):
        try:
            hour = int(self.hour_var.get())
            minute = int(self.minute_var.get())
        except ValueError as exc:
            raise ValueError("Hour and minute must be numbers") from exc

        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            raise ValueError("Hour must be 0-23 and minute must be 0-59")

        return hour, minute

    def set_output(self, text):
        self.output.config(state=tk.NORMAL)
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, text)
        self.output.config(state=tk.DISABLED)

    def render_word(self, word_info, source):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lines = [
            f"Word: {word_info['word']}",
            f"Definition: {word_info['definition']}",
            f"Example: {word_info['example']}",
            f"Source: {source}",
            f"Fetched at: {timestamp}",
        ]
        self.set_output("\n\n".join(lines))

    def get_word(self):
        try:
            return fetch_word_online(), "online API"
        except (URLError, TimeoutError, ValueError, json.JSONDecodeError):
            return fallback_word(), "offline fallback list"

    def show_word_now(self):
        word_info, source = self.get_word()
        self.render_word(word_info, source)

    def show_offline_word(self):
        self.render_word(fallback_word(), "offline fallback list")

    def toggle_reminder(self):
        if self.running_timer:
            self.running_timer = False
            self.toggle_btn.config(text="Start Reminder")
            self.status_var.set("Reminder stopped")
            return

        try:
            hour, minute = self.parse_schedule_time()
        except ValueError as err:
            messagebox.showerror("Invalid Time", str(err))
            return

        self.running_timer = True
        self.toggle_btn.config(text="Stop Reminder")
        self.status_var.set(f"Reminder running for {hour:02d}:{minute:02d} every day")
        self.check_reminder()

    def check_reminder(self):
        if not self.running_timer:
            return

        hour, minute = self.parse_schedule_time()
        now = datetime.now()
        today = now.date()

        if now.hour == hour and now.minute == minute and self.last_notified_date != today:
            word_info, source = self.get_word()
            self.render_word(word_info, source)
            messagebox.showinfo(
                "Word of the Day",
                f"{word_info['word']}\n\n{word_info['definition']}\n\n(From {source})",
            )
            self.last_notified_date = today

        # Check every minute.
        self.root.after(60_000, self.check_reminder)


def main():
    root = tk.Tk()
    WordOfDayApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()