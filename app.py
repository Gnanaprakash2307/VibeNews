import tkinter as tk
from tkinter import messagebox, scrolledtext
from news_fetch import fetch_news
from gemini_ai import summarize_news
from text_to_speech import speak_text
from pdf_gen import save_summary_to_pdf

# -------------------- Constants -------------------- #
HACKER_GREEN = "#00FF41"
BG_BLACK = "black"
FONT_TITLE = ("Courier New", 18, "bold")
FONT_BODY = ("Courier New", 11)

# -------------------- Main Window Setup -------------------- #
root = tk.Tk()
root.title("VibeNews | Dev Terminal Edition")
root.geometry("850x700")
root.configure(bg=BG_BLACK)

# -------------------- ASCII Header -------------------- #
ascii_art = r"""
    ____  _     _            _   _                 
  |  _ \(_)___| |_ ___ _ __| \ | | ___ _ __  _ __  
  | | | | / __| __/ _ \ '__|  \| |/ _ \ '_ \| '_ \ 
  | |_| | \__ \ ||  __/ |  | |\  |  __/ | | | | | |
  |____/|_|___/\__\___|_|  |_| \_|\___|_| |_|_| |_|   Vibe News
"""
ascii_label = tk.Label(root, text=ascii_art, font=("Courier", 9), fg=HACKER_GREEN, bg=BG_BLACK, justify="left")
ascii_label.pack(pady=(10, 5))

# -------------------- Blinking Cursor -------------------- #
cursor_label = tk.Label(root, text=">", font=("Courier", 12), fg=HACKER_GREEN, bg=BG_BLACK)
cursor_label.pack()


def blink_cursor():
    current = cursor_label.cget("text")
    cursor_label.config(text=">" if current == "" else "")
    root.after(500, blink_cursor)


blink_cursor()

# -------------------- Input Section -------------------- #
input_frame = tk.Frame(root, bg=BG_BLACK)
input_frame.pack(pady=10)

entry_label = tk.Label(input_frame, text="Enter news topic ↓", font=FONT_BODY, fg=HACKER_GREEN, bg=BG_BLACK)
entry_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

query_entry = tk.Entry(input_frame, width=60, font=FONT_BODY, fg=HACKER_GREEN, bg="#111")
query_entry.grid(row=1, column=0, padx=5, pady=5)

# -------------------- Suggestion Box -------------------- #
# Popular topics for auto-suggest
popular_topics = ["Technology", "Sports", "World", "Business", "Health", "Science", "Entertainment"]


# Function to update suggestions based on input
def update_suggestions(event):
    query = query_entry.get()
    filtered_topics = [topic for topic in popular_topics if query.lower() in topic.lower()]
    suggestion_box.delete(0, tk.END)
    for topic in filtered_topics:
        suggestion_box.insert(tk.END, topic)


# Display suggestion box below the entry
suggestion_box = tk.Listbox(root, height=5, width=60, font=("Courier New", 11), bg="#111", fg=HACKER_GREEN,
                            selectmode=tk.SINGLE)
suggestion_box.pack(pady=5)

query_entry.bind('<KeyRelease>', update_suggestions)


# -------------------- Trending News Buttons -------------------- #
def set_trending_topic(topic):
    query_entry.delete(0, tk.END)
    query_entry.insert(tk.END, topic)


btn_trending_frame = tk.Frame(root, bg=BG_BLACK)
btn_trending_frame.pack(pady=10)

trending_buttons = ["Technology", "Sports", "World", "Business", "Health"]
for idx, topic in enumerate(trending_buttons):
    trending_btn = tk.Button(btn_trending_frame, text=topic, command=lambda t=topic: set_trending_topic(t),
                             font=("Courier", 10, "bold"), bg="#111", fg=HACKER_GREEN)
    trending_btn.grid(row=0, column=idx, padx=12)

# -------------------- Output Section -------------------- #
output_label = tk.Label(root, text="Generated Summary ↓", font=FONT_BODY, fg=HACKER_GREEN, bg=BG_BLACK)
output_label.pack(pady=(15, 5))

result_box = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    height=20,
    width=100,
    font=FONT_BODY,
    bg="#111",
    fg=HACKER_GREEN,
    insertbackground=HACKER_GREEN
)
result_box.pack(padx=15, pady=5)


# -------------------- Loading Indicator -------------------- #
def show_loading_message():
    result_box.delete("1.0", tk.END)
    result_box.insert(tk.END, "[...] Fetching news & summarizing...\n")
    root.update()


def hide_loading_message(summary):
    result_box.delete("1.0", tk.END)
    result_box.insert(tk.END, summary)


# -------------------- Sentiment Analysis -------------------- #
def get_sentiment_color(summary):
    # Sentiment logic (Placeholder)
    sentiment = "Positive"  # For now, assume positive sentiment
    sentiment_color = {"Positive": "#00FF00", "Negative": "#FF0000", "Neutral": "#FFFFFF"}.get(sentiment, "#FFFFFF")
    return sentiment_color


# -------------------- Functions -------------------- #
def handle_text_input():
    query = query_entry.get()
    if not query.strip():
        messagebox.showwarning("🚨 Empty Input", "You need to type something.")
        return

    show_loading_message()

    news_text = fetch_news(query)
    summary = summarize_news(news_text)

    # Clean the summary by removing asterisks
    cleaned_summary = summary.replace("*", "")

    sentiment_color = get_sentiment_color(cleaned_summary)

    result_box.delete("1.0", tk.END)
    result_box.insert(tk.END, cleaned_summary, sentiment_color)


def handle_speak():
    root.bell()  # Terminal beep
    speak_text(result_box.get("1.0", tk.END))


def handle_pdf():
    save_summary_to_pdf(result_box.get("1.0", tk.END))
    messagebox.showinfo("PDF Saved", "The summary has been saved as a PDF!")


# -------------------- Buttons -------------------- #
btn_frame = tk.Frame(root, bg=BG_BLACK)
btn_frame.pack(pady=20)

button_style = {
    "font": ("Courier New", 10, "bold"),
    "bg": "#111",
    "fg": HACKER_GREEN,
    "activebackground": "#00aa33",
    "activeforeground": "black",
    "padx": 10,
    "pady": 6,
    "bd": 1,
    "relief": "solid"
}

search_btn = tk.Button(btn_frame, text="> Search", command=handle_text_input, **button_style)
search_btn.grid(row=0, column=0, padx=10)

speak_btn = tk.Button(btn_frame, text="> Speak", command=handle_speak, **button_style)
speak_btn.grid(row=0, column=1, padx=10)

save_btn = tk.Button(btn_frame, text="> Save as PDF", command=handle_pdf, **button_style)
save_btn.grid(row=0, column=2, padx=10)

# -------------------- Bind Enter Key -------------------- #
root.bind('<Return>', lambda event: handle_text_input())

# -------------------- Run the App -------------------- #
root.mainloop()
