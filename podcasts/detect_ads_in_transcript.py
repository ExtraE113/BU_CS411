import json
import openai

openai.api_key_path = "openai_api_key.txt"


def mark_ads(transcript, offset=0):
	# Set the model to use
	model = "gpt-4"

	# Set the system message to instruct the model
	system_message = "You are an assistant that can identify and mark advertisements in a podcast transcript. Surround all the advertisments with [BEGIN AD] and [END AD] while leaving the text unchanged."

	split_text = transcript.split(" ")

	# Create a chat completion request with the messages and model parameters
	response = openai.ChatCompletion.create(
		model=model,
		messages=[
			{"role": "system", "content": system_message},
			# just run on first 1k words
			{"role": "user", "content": " ".join(split_text[offset:offset+1000])}
		],
		temperature=0,
		max_tokens=4000,
	)

	# Get the assistant message from the response
	assistant_message = response["choices"][0]["message"]["content"]

	# Return the assistant message as the output
	return assistant_message, len(split_text) >= offset+1000


if __name__ == "__main__":
	# Read the transcript from the transcript.txt file
	with open("transcript_tal_excerpt.json") as f:
		transcript = json.load(f)

	transcript_text = "\n".join(
		["".join([x["value"] for x in elem["elements"]]) for elem in transcript["monologues"]])

	print(len(transcript_text.split(" ")) / 1000)

	# Call the mark_ads function to mark the ads
	offset = 0
	done = False
	while not done:
		assistant_message, done = mark_ads(transcript_text, offset)

		# write to file
		with open(f"marked_transcript_tal_excerpt{offset}.txt", "w") as f:
			f.write(assistant_message)

		print(f"writing part {offset} of transcript to file")
		offset += 500

