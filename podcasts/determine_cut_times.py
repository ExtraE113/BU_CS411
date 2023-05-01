import json
import re


def determine_cut_times(edited_transcript_section, timestamped_transcript):
	# detect sections surrounded by [BEGIN AD] and [END AD] in the edited transcript
	regex = re.compile(r'\[BEGIN AD\](.*?)\[END AD\]', re.DOTALL)
	ads = regex.findall(edited_transcript_section)

	for ad in ads:
		# locate that string in the timestamped_transcript
		raise NotImplemented


if __name__ == "__main__":
	# load edited_transcript_section from marked_transcript0.txt
	with open("marked_transcript0.txt") as f:
		edit_transcript_section = f.read()

	# load timestamped_transcript from transcript.json
	with open("transcript.json") as f:
		timestamped_transcript = json.load(f)

	determine_cut_times(edit_transcript_section, timestamped_transcript)
