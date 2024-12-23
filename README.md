# ChronoPulse
ChronoPulse is an automated news aggregation and summarization system designed to generate simplified news articles from YouTube video transcripts. It leverages Zapier, Telegram, and advanced AI models to deliver concise news updates directly to a Telegram group. The project is fully automated and deployed on Google Compute Engine during its free trial period.

---

## Features
1. **YouTube Monitoring via Zapier**
   - Zapier tracks new video uploads to specific news channels on YouTube.
   - Sends a message to the `admin-source` Telegram group containing:
     - The video title.
     - The video URL.
     - The video duration.

2. **YouTube Transcript Extraction**
   - The Python script listens for incoming messages in the `admin-source` group.
   - Extracts the video URL and retrieves its transcript using the YouTube Transcript API.

3. **AI-Powered Summarization**
   - The transcript is summarized into simple English using the Gemini AI API.
   - Ensures the summary is concise and easy to understand.

4. **Automated News Delivery**
   - Sends the summarized news, along with the video’s thumbnail, to the `ChronoPulse` Telegram group.
   - Fully automated with no manual intervention required.

5. **Deployment on Google Compute Engine**
   - The Python script runs continuously on Google Compute Engine, leveraging the free trial for cost efficiency.

---

## How It Works
1. **Zapier Integration**
   - Monitors specified YouTube channels.
   - Triggers an alert when a new video is uploaded.
   - Posts the video details (title, URL, duration) to the `admin-source` Telegram group.

2. **Telegram Bot (d_bot)**
   - Listens for new messages in the `admin-source` group.
   - Processes messages containing YouTube video URLs.

3. **Transcript Retrieval and Summarization**
   - Extracts the video ID from the URL.
   - Retrieves the transcript using the YouTube Transcript API.
   - Summarizes the transcript using the Gemini AI API with rotating API keys for reliability.

4. **News Delivery**
   - Generates a concise news summary.
   - Downloads the video’s thumbnail.
   - Sends the summary and thumbnail to the `ChronoPulse` Telegram group.

---

## System Architecture
### Components
- **Zapier**: For monitoring YouTube uploads and sending alerts to Telegram.
- **Telegram**: Used as the communication platform for both receiving video details and delivering news summaries.
- **Python Script**: Core logic for transcript extraction, summarization, and news delivery.
- **Google Compute Engine**: Hosting environment for the Python script.
- **Gemini AI API**: Summarizes video transcripts into simple English.
- **YouTube Transcript API**: Retrieves transcripts from YouTube videos.

---

## Prerequisites
- **Zapier Account**: To monitor YouTube channels.
- **Telegram Bot API Token**: For the d_bot functionality.
- **Google API Keys**: For accessing the Gemini AI API.
- **YouTube Transcript API**: For fetching video transcripts.
- **Google Compute Engine Account**: For deployment.

---

## Installation and Setup
### 1. Clone the Repository
```bash
$ git clone https://github.com/Dhurkesh-B/Chrono-Pulse
$ cd ChronoPulse
```

### 2. Install Dependencies
```bash
$ pip install -r requirements.txt
```

### 3. Set Environment Variables
Create a `.env` file and add the following variables:
```
TELEGRAM_API_ID=<Your Telegram API ID>
TELEGRAM_API_HASH=<Your Telegram API Hash>
TELEGRAM_BOT_TOKEN=<Your Telegram Bot Token>
SOURCE_GROUP_ID=<Admin-Source Telegram Group ID>
DESTINATION_GROUP_ID=<Admin-Source Telegram Group ID>
GEMINI_KEY_1=<Gemini API Key 1>
GEMINI_KEY_2=<Gemini API Key 2>
GEMINI_KEY_3=<Gemini API Key 3>
GEMINI_KEY_4=<Gemini API Key 4>
```

### 4. Run the Script
```bash
$ python app.py
```

---

## Deployment on Google Compute Engine
1. **Create a Compute Instance**
   - Choose a lightweight instance to stay within the free trial limits.
   - Install Python and necessary libraries on the instance.

2. **Upload the Project**
   - SCP or upload the project files to the instance.

3. **Run the Script**
   - Use a process manager like `tmux` or `screen` to keep the script running.

---

## Limitations
- **Transcript Availability**: Videos without transcripts cannot be processed.
- **API Key Quota**: Limited by the usage quotas of the Gemini AI API and YouTube API.

---

## Future Enhancements
- Add support for multilingual summarization.
- Enhance error handling and retry logic.
- Introduce scheduling for periodic summaries.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

## Acknowledgments
- [Zapier](https://zapier.com): For seamless YouTube monitoring.
- [Telegram](https://core.telegram.org/): For providing the bot API.
- [Google Gemini AI](https://cloud.google.com/ai): For AI-powered summarization.
- [YouTube Transcript API](https://pypi.org/project/youtube-transcript-api/): For transcript extraction.

