import json
import re
import time
from pathlib import Path

import feedparser
import openai
import requests
from urllib.parse import unquote
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Podcast(models.Model):
	title = models.CharField(max_length=200)
	description = models.TextField()
	rss_feed_url = models.URLField()
	cover = models.URLField(null=False, blank=False, default='')
	users = models.ManyToManyField(User, related_name='subscriptions')

	def __str__(self):
		return self.title


class Episode(models.Model):
	podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE, related_name='episodes')
	title = models.CharField(max_length=200)
	description = models.TextField()
	audio_file = models.FileField(upload_to='podcast_episodes/')
	published_date = models.DateTimeField()
	duration = models.DurationField()
	ad_timestamps = models.JSONField(null=True, blank=True)
	transcription = models.JSONField(null=True, blank=True)
	scanned_transcripts = models.TextField(null=False, blank=True, default="")
	cuts = models.JSONField(null=True, blank=True)
	link = models.CharField(max_length=512, null=True, blank=True)
	def __str__(self):
		return self.title

	@property
	def audio_link(self):
		if self.link is None:
			return self.audio_file.name
		else:
			return self.link


	def transcribe_episode(self):
		p = Path(__file__).with_name('access_token.txt')
		with p.open() as f:
			token = f.read()
		# Transcribe each episode using rev.ai batch transcription
		# Submit the transcription job to rev.ai
		headers = {
			'Authorization': f'Bearer {token}',
			'Content-Type': 'application/json'
		}

		if self.link is None:
			link = self.audio_file.name # self.audio_file.url doesn't work for some reason
		else:
			link = self.link

		data = {
			'media_url': link,
			'metadata': f'Transcription for {self}'
		}
		response = requests.post('https://api.rev.ai/speechtotext/v1/jobs',
								 headers=headers, data=json.dumps(data))
		try:
			job_id = response.json()['id']
		except KeyError:
			print(self.audio_file.name)
			print(response.json())
			raise KeyError

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
		self.transcription = transcript_result
		self.save()
		return transcript_result

	def scan_for_ads(self):
		def mark_ads(transcript, offset=0):
			openai.api_key_path = Path(__file__).with_name('openai_api_key.txt')
			# Set the model to use
			model = "gpt-4"

			# Set the system message to instruct the model
			system_message = "You are an assistant that can identify and mark advertisements in a podcast transcript. " \
							"Surround all the advertisments with [BEGIN AD] and [END AD] while leaving the text " \
							"unchanged. Do not surround text that is not part of an advertisement with " \
							"[BEGIN AD] and [END AD]."

			split_text = transcript.split(" ")
			user_prompt = " ".join(split_text[offset:offset + 1000])
			print(user_prompt)
			# Create a chat completion request with the messages and model parameters
			response = openai.ChatCompletion.create(
				model=model,
				messages=[
					{"role": "system", "content": system_message},
					# just run on first 1k words
					{"role": "user", "content": user_prompt}
				],
				temperature=0,
				top_p=1,
				max_tokens=4000,
			)

			# Get the assistant message from the response
			assistant_message = response["choices"][0]["message"]["content"]

			# Return the assistant message as the output
			return assistant_message, len(split_text) >= offset + 1000

		transcript_text = "\n".join(
			["".join([x["value"] for x in elem["elements"]]) for elem in self.transcription["monologues"]])

		# Call the mark_ads function to mark the ads
		oset = 0
		done = False
		while not done:
			assistant_message, done = mark_ads(transcript_text, oset)
			if self.scanned_transcripts is None:
				self.scanned_transcripts = ""
			self.scanned_transcripts += assistant_message
			print(assistant_message)
			oset += 500

			self.save()
		self.save()
	def determine_cut_times(self):
		# detect sections surrounded by [BEGIN AD] and [END AD] in the edited transcript
		regex = re.compile(r'\[BEGIN AD\](.*?)\[END AD\]', re.DOTALL | re.IGNORECASE)
		ads = regex.findall(self.scanned_transcripts)
		print(ads)
		flattened_transcript = []
		for elem in self.transcription["monologues"]:
			flattened_transcript.extend(elem["elements"])

		string_transcript_full = "".join([elem['value'] for elem in flattened_transcript])
		print(string_transcript_full)

		def locate(start: int, end: int, ad: str):
			# locate in flattened transcript
			# use modified binary search
			# start and end are indices in flattened_transcript
			# working area is in [start, end]
			# ad is the ad to locate

			string_transcript_full = "".join([elem['value'] for elem in flattened_transcript[start:end]])
			assert ad in string_transcript_full, f"ad {ad} not in working area"
			# print(f"ad {ad} in working area")
			midpoint = (start + end) // 2

			string_transcript_first_half = "".join([elem['value'] for elem in flattened_transcript[start:midpoint]])
			if ad in string_transcript_first_half:
				return locate(start, midpoint, ad)

			string_transcript_second_half = "".join([elem['value'] for elem in flattened_transcript[midpoint:end]])
			if ad in string_transcript_second_half:
				return locate(midpoint, end, ad)

			# ad is split between first and second half
			string_transcript_middle_half = "".join(
				[elem['value'] for elem in flattened_transcript[start + midpoint // 2:end - midpoint // 2]])
			if ad in string_transcript_middle_half:
				return locate(start + midpoint // 2, end - midpoint // 2, ad)

			# brute force, change by 1 char
			for i in range(start, end):
				for j in range(i, end):
					string_transcript = "".join([elem['value'] for elem in flattened_transcript[i:j]])
					if ad in string_transcript:
						return i, j

		cuts = []
		for ad in ads:
			cuts.append(locate(0, len(flattened_transcript), ad.strip()))

		# sometimes we start or end on a token with no [ts] tag, so we need to go forward/back until we find one
		for i in range(len(cuts)):
			cut_start = cuts[i][0]
			cut_end = cuts[i][1]
			while flattened_transcript[cut_start].get('ts') is None:
				cut_start += 1
			while flattened_transcript[cut_end].get('end_ts') is None:
				cut_end -= 1
			cuts[i] = (cut_start, cut_end)
		print(cuts)
		cut_times = []
		for cut in cuts:
			cut_times.append((flattened_transcript[cut[0]]['ts'], flattened_transcript[cut[1]]['end_ts']))
		self.cuts = cut_times
		self.save()

	def full_scan(self):
		self.transcribe_episode()
		print("transcribed")
		self.scan_for_ads()
		print("scanned")
		self.determine_cut_times()
		print("determined cuts")
