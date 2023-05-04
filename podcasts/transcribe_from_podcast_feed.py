import json
import time

import requests as requests
import feedparser

# read token from access_token.txt
with open("../podcast_app/access_token.txt") as f:
	token = f.read()


def parse_rss_feed(rss_feed: str):
	# Parse the RSS feed using feedparser
	feed = feedparser.parse(rss_feed)

	# Extract the episode URLs from the parsed feed
	episode_audio_urls = []
	for entry in feed.entries:
		episode_urls = entry.links
		for episode_url in episode_urls:
			if episode_url.type == 'audio/mpeg':
				episode_audio_urls.append(episode_url.href)

	return episode_audio_urls


def transcribe_podcast(rss_feed_url: str, rev_ai_api_key: str, max_transcriptions: int = 1):
	# Get the podcast episodes from the RSS feed
	response = requests.get(rss_feed_url)
	rss_feed = response.text

	# Parse the RSS feed to get the episode URLs
	episode_urls = parse_rss_feed(rss_feed)

	# limit the number of episodes to transcribe
	episode_urls = episode_urls[:max_transcriptions]

	return _transcribe_episodes(episode_urls, rev_ai_api_key)


def _transcribe_episodes(episode_urls: list, rev_ai_api_key: str):
	# Transcribe each episode using rev.ai batch transcription
	for episode_url in episode_urls:
		# Submit the transcription job to rev.ai
		headers = {
			'Authorization': f'Bearer {rev_ai_api_key}',
			'Content-Type': 'application/json'
		}
		data = {
			'media_url': episode_url,
			'metadata': f'Transcription for {episode_url}'
		}
		response = requests.post('https://api.rev.ai/speechtotext/v1/jobs', headers=headers, data=json.dumps(data))
		job_id = response.json()['id']

		# Wait for the transcription job to complete
		while True:
			response = requests.get(f'https://api.rev.ai/speechtotext/v1/jobs/{job_id}', headers=headers)
			job_status = response.json()['status']

			if job_status == 'transcribed':
				break
			if job_status == 'failed':
				raise Exception('Transcription failed')
			time.sleep(10)
			print(f'Job {job_id} is {job_status}')
			print(response.json())

		# Get the transcription result with timestamps
		headers['Accept'] = 'application/vnd.rev.transcript.v1.0+json'
		response = requests.get(f'https://api.rev.ai/speechtotext/v1/jobs/{job_id}/transcript', headers=headers)
		transcript_result = response.json()
		return transcript_result


if __name__ == '__main__':
	# transcript_result = transcribe_podcast('https://www.thisamericanlife.org/podcast/rss.xml', token)
	transcript_result = _transcribe_episodes(
		["https://drive.google.com/uc?export=download&id=16aJlhmpJSF3lKRGl8cTgXAGUMRB-yb9d"], token)
	# save transcript_result to file as json blob
	with open("transcript_tal_excerpt.json", "w") as f:
		json.dump(transcript_result, f)
