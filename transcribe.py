from google.cloud import speech
import io, os, json
from audiofile import AudioFile
from tqdm import tqdm
import time
import warnings

warnings.filterwarnings('ignore')

DIR = r"C:\Users\Dell\Desktop\speech"

def transcribe_gcs(gcs_uri, duration):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""

    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding="LINEAR16",
        sample_rate_hertz=44100,
        language_code="en-US",
        enable_word_time_offsets=True
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
    chunk_timestamps = []
    srt_idx = 1

    for result in response.results: 
        # The first alternative is the most likely one for this portion. It is the only one containing word offsets 
        alternative = result.alternatives[0]
        # using \n\n as a delimiter when adding the timestamps

        transcript += (alternative.transcript.strip() + "\n\n") 

        response_start_time = alternative.words[0].start_time
        response_end_time = alternative.words[-1].end_time

        # print(alternative.words[0].start_time.total_seconds())
        start_time = time.strftime('%H:%M:%S', time.gmtime(int(response_start_time.total_seconds())))
        end_time = time.strftime('%H:%M:%S', time.gmtime(int(response_end_time.total_seconds())))
        
        # get the ms part in ss.s and convert to ss,ms where ms == .s * 100 
        start_ms = int(str(response_start_time.total_seconds()).split('.')[-1]) * 100
        end_ms = int(str(response_end_time.total_seconds()).split('.')[-1]) * 100

        # we get the start and end time of the first and last word respectively in chunk, in hh:mm:ss format 
        start_time = str(start_time).split('.')[0]
        end_time = str(end_time).split('.')[0]
        time_for_chunk = f"{srt_idx}\n{start_time},{start_ms} --> {end_time},{end_ms}\n" # this is the srt format we need

        # for each chunk we append its timestamp so we can add it later
        chunk_timestamps.append(time_for_chunk) 
        srt_idx += 1

    # get the basename of the file so each transript.txt file is unique when generated
    audio_fname = os.path.basename(gcs_uri).strip(".wav")
 
    # modify transcript to include the timestamp at the start of each chunk of transcription.
    transcript = "\n\n".join([f"{x}"  + y for (x, y) in zip(chunk_timestamps, transcript.split("\n\n"))]) # here we add timestamps to each chunk of speech

    # write the stream of chunk to a txt file once the whole audio is transcribed.
    with open(f"FINAL_TRANSCRIPT_{audio_fname}.txt", "w") as f:
        f.write(transcript) 

    print("Transcripted the audio")      

if __name__ == "__main__":

    # we would need the same file locally (and in GCS bucket if size > 10mb and > 1 minute) so as to get the duration and transcribe it.
    file_path = r"C:\Users\Dell\Desktop\speech\audiofile.wav"

    audio = AudioFile(file_path)
    audio.stereo_to_mono()
    duration = audio.get_duration()

    # this is the uri of the bucket in GCS
    gcs_uri = "gs://audiofiles_bucket/audiofile.wav"
    transcribe_gcs(gcs_uri, duration)