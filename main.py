import asyncio
from flask import Flask, jsonify
from telethon import TelegramClient, events
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import requests
import re
import os
import sqlite3
import time

# Load environment variables from the .env file

# Initialize Flask app
app = Flask(__name__)

# Store processed message IDs to avoid duplicate processing
processed_messages = set()

# Helper Function: SQLite Retry Logic
def execute_query_with_retries(query, params=(), retries=5, delay=0.1):
    for attempt in range(retries):
        try:
            with sqlite3.connect("database.db", check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return cursor.fetchall()
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e):
                time.sleep(delay)
            else:
                raise
    raise RuntimeError("Failed to execute query after multiple retries.")

# Helper Function: Extract Video ID
def get_video_id(video_url):
    video_id_match = re.search(r"v=([a-zA-Z0-9_-]{11})", video_url)
    if video_id_match:
        return video_id_match.group(1)
    raise ValueError("Invalid YouTube video URL")

# Helper Function: Download Thumbnail
def download_thumbnail(url, filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        return filename
    raise ValueError("Unable to download thumbnail image.")

# Helper Function: Fetch and Format Transcript
def print_youtube_transcripts(video_url):
    try:
        video_id = get_video_id(video_url)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        formatter = TextFormatter()
        return formatter.format_transcript(transcript), video_id
    except Exception as e:
        return f"Error: {str(e)}", None

# Helper Function: Simplify Transcript
def simplify_text(article_text,keyList):
    try:
        llm = ChatGoogleGenerativeAI(
            model='gemini-1.5-pro',
            temperature=0,
            max_tokens=None,
            Timeout=None,
            max_retries=2,
            api_key=keyList[0]
        )
        prompt_template = ChatPromptTemplate.from_messages([
            ('system', 'You are a chatbot trained on the following data:\n{data}'),
            ('human', 'This is the transcript of a news video. Simplify it in the simple english (summary) without no advanced english words\n\n{article}')
        ])
        output_parse = StrOutputParser()
        chain = prompt_template | llm | output_parse
        response = chain.invoke({'article': article_text, 'data': "Article content"})
        return response
    except Exception as e:
        keyList.append(keyList.pop(0))
        try:
            llm = ChatGoogleGenerativeAI(
                model='gemini-1.5-pro',
                temperature=0,
                max_tokens=None,
                Timeout=None,
                max_retries=2,
                api_key=keyList[0]
            )
            prompt_template = ChatPromptTemplate.from_messages([
                ('system', 'You are a chatbot trained on the following data:\n{data}'),
                ('human', 'This is the transcript of a news video. Simplify it in the simple english (summary) without no advanced english words\n\n{article}')
            ])
            output_parse = StrOutputParser()
            chain = prompt_template | llm | output_parse
            response = chain.invoke({'article': article_text, 'data': "Article content"})
            return response
        except Exception as e:
            return 'Breaking News'

# Telegram Bot Logic
async def run_bot():
    api_id = 28495580
    api_hash = "6efae95830517f82bc82defd5a494b8e"
    bot_token = "7127397315:AAEZFg76GSHO1dR8tYi2kns8qmS1RM6yLm0"
    source_group_id = -1002168741674
    destination_group_id = -1002249855375

    # Create a unique session for the bot
    session_name = f"session_{int(time.time())}"
    client = TelegramClient(session_name, api_id, api_hash)

    @client.on(events.NewMessage)
    async def handler(event):
        chat_id = event.chat_id
        message_id = event.id  # Get message ID to track duplicates
        message_text = event.raw_text

        if chat_id == source_group_id:
            # Skip already processed messages
            if message_id in processed_messages:
                return

            # Mark message as processed
            processed_messages.add(message_id)

            try:
                message_text = message_text.split('$')
                video_url = message_text[1].strip()
                transcript, video_id = print_youtube_transcripts(video_url)
                gemini_keys = ['AIzaSyAHwYOOvw5VDNRuRf_OxXILMXfQ-1iozzM','AIzaSyDxO1TwIBaDZ1JUfKZw6IuB8oVmWCZ9hD0',
                            'AIzaSyAk9X-cF3QnRlokL200nxgrqq8yVNPXmVU','AIzaSyAcrxUWi1MWQYErCae_GWXTGW7SCChmPhk']
                if video_id:
                    thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
                    thumbnail_path = download_thumbnail(thumbnail_url, f"{video_id}_thumbnail.jpg")
                    simplified_content = simplify_text(transcript,gemini_keys)
                    while len(simplified_content)>=1000:
                        gemini_keys.append(gemini_keys.pop(0))
                        simplified_content = simplify_text(simplified_content,gemini_keys)

                    await client.send_file(destination_group_id, thumbnail_path, caption=simplified_content)
                    os.remove(thumbnail_path)
            except Exception as e:
                print(f"Error processing message: {e}")

    # Start the bot
    await client.start(bot_token=bot_token)
    print("Bot started and listening for messages...")
    await client.run_until_disconnected()

# Flask Route
@app.route("/")
def home():
    return jsonify({"status": "Bot is running", "message": "Telegram bot with Flask API is active!"})

# Run Flask App
if __name__ == "__main__":
    # Start the bot
    asyncio.run(run_bot())

    # Start the Flask app
    listen_port = int(os.getenv('X_ZOHO_CATALYST_LISTEN_PORT', 9000))
    app.run(host="0.0.0.0", port=listen_port, debug=True)
