import json
import re


def determine_cut_times(edited_transcript_section, timestamped_transcript):
	# detect sections surrounded by [BEGIN AD] and [END AD] in the edited transcript
	regex = re.compile(r'\[BEGIN AD\](.*?)\[END AD\]', re.DOTALL)
	ads = regex.findall(edited_transcript_section)

	flattened_transcript = []
	for elem in timestamped_transcript["monologues"]:
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
	cut1_start = cuts[0][0]
	cut1_end = cuts[0][1]
	print("".join([elem['value'] for elem in flattened_transcript[cut1_start:cut1_end]]))
	print(flattened_transcript[cut1_start])
	print(flattened_transcript[cut1_end])


if __name__ == "__main__":
	# load edited_transcript_section from marked_transcript0.txt
	with open("marked_transcript_tal_excerpt0.txt") as f:
		edit_transcript_section = f.read()

	# load timestamped_transcript from transcript.json
	with open("transcript_tal_excerpt.json") as f:
		timestamped_transcript = json.load(f)

	determine_cut_times(edit_transcript_section, timestamped_transcript)
