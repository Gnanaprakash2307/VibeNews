import google.generativeai as genai

API_KEY = "AIzaSyCQwmLtnOvE5i8MjdAAd0lYl51sPEC082k"
genai.configure(api_key=API_KEY)


def summarize_news(news_text):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")

        # Enhanced prompt with more structure and specific instructions
        prompt = (
            "You are a news summarizer and sentiment analyzer. Given the news article below, "
            "please perform the following tasks:\n\n"
            "1. Provide a concise summary of the news in **two lines**.\n"
            "2. Classify the sentiment of the news article as either **Positive**, **Neutral**, or **Negative**.\n"
            "3. Suggest **who would benefit** or be most interested in this news (e.g., professionals, students, specific industries, etc.).\n"
            "4. Ensure your response is formatted in **markdown**, with clear headings and bullet points.\n\n"
            "Here is the news article:\n\n"
            f"{news_text}\n\n"
            "Response Format:\n"
            "### Summary\n"
            "- Brief summary of the news (max 2 lines).\n"
            "### Sentiment\n"
            "- Positive/Neutral/Negative.\n"
            "### Audience\n"
            "- Who should care? (professionals, industry, group of people, etc.)"
        )

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"❌ Gemini error: {str(e)}"
