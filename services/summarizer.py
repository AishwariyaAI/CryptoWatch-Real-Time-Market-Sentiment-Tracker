from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def summarize_news(text):

    try:

        prompt = f"""
Analyze the following cryptocurrency news headlines.

Provide:

1. Overall Market Sentiment
2. Key Events
3. Risks
4. Opportunities
5. Investor Insight

News:
{text}
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=500
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"AI Summary unavailable: {str(e)}"