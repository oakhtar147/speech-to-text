from google.cloud import speech
import io, os
import utils
from tqdm import tqdm

DIR = r"C:\Users\Dell\Desktop\speech"

def transcribe_gcs(gcs_uri, duration):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""

    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding="LINEAR16",
        sample_rate_hertz=44100,
        language_code="en-US",
    )

    operation = client.long_running_recognize(
        request={"config": config, "audio": audio}
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=duration + 100)


    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    transcript = ""

    for result in response.results:
        # The first alternative is the most likely one for this portion.
        transcript += (result.alternatives[0].transcript + " ") 

    audio_fname = os.path.basename(gcs_uri)

    with open(f"transcript_{audio_fname}.txt", "w") as f:
        f.write(transcript)   

if __name__ == "__main__":

    fname = os.path.join(DIR, "audiofile.wav")
    duration = utils.get_duration(fname)

    gcs_uri = "gs://audiofiles_bucket/audiofile.wav"
    transcribe_gcs(gcs_uri, duration)