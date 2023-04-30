import json

import openai

openai.api_key_path = "openai_api_key.txt"


def mark_ads(transcript):
	# Set the model to use
	model = "gpt-4"

	# Set the system message to instruct the model
	system_message = "You are an assistant that can identify and mark advertisements in a podcast transcript. Surround all the advertisments with [BEGIN AD] and [END AD] while leaving the text unchanged."

	# Create a chat completion request with the messages and model parameters
	response = openai.ChatCompletion.create(
		model=model,
		messages=[
			{"role": "system", "content": system_message},
			# just run on first 1k words
			{"role": "user", "content": " ".join(transcript.split()[:1000])}
		],
		temperature=0.1,
		stop=["\n"]
	)

	# Get the assistant message from the response
	assistant_message = response["choices"][0]["message"]["content"]

	# Return the assistant message as the output
	return assistant_message


if __name__ == "__main__":
	# Read the transcript from the transcript.txt file
	with open("transcript.json") as f:
		transcript = json.load(f)

	transcript_text = "\n".join(
		["".join([x["value"] for x in elem["elements"]]) for elem in transcript["monologues"]])

	# Call the mark_ads function to mark the ads
	output = mark_ads(transcript_text)

	# Print the output
	print(output)
	# save output to file
	with open("ads_marked.txt", "w") as f:
		f.write(output)
