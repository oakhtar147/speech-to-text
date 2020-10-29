with open("./transcript_audiofile.txt", "r") as f:
    text = f.read()

formatted_text = text.replace("  ", "\n\n")

with open("formatted_transcript.txt", "w") as f:
    f.write(formatted_text)
   