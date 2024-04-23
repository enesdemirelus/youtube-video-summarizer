import re
import sys
import time
import textwrap
from youtube_transcript_api import YouTubeTranscriptApi
import openai

def progress_bar(duration, start_text, end_text):
    total_steps = 30

    print(start_text)
    for i in range(total_steps + 1):
        time.sleep(duration / total_steps)
        percent_complete = int((i / total_steps) * 100)
        progress_bar = '#' * i + '-' * (total_steps - i)
        sys.stdout.write(f"\r[{progress_bar}] {percent_complete}%")
        sys.stdout.flush()
    print(f"\n{end_text}\n")

def print_formatted_text(title, content):
    print(f"\n{title}\n")
    print(textwrap.fill(content, width=80))
    print("\n" + "=" * 80 + "\n")

url = input("Please enter the link of the YouTube video: ")

progress_bar(2, "Getting the transcript out of the video...", "Transcript successfully extracted!")

regex = r"v=([^\s&]+)"
video_id = re.findall(regex, url)[0]
transcript = YouTubeTranscriptApi.get_transcript(video_id)
complete_transcript = " ".join([entry["text"] for entry in transcript])

openai.api_key = "OPEN AI API KEY HERE"

prompt = f"Can you summarize this video for me in 200 words? :\n{complete_transcript}"

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
)

summary = response['choices'][0]['message']['content']

progress_bar(2, "Creating the summary...", "Summary successfully created!")

print_formatted_text("Summary of the video you provided:", summary)
