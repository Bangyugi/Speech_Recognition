import requests
from api_secrets import API_KEY_ASSEMBLYAI
import time


# upload
upload_enpoint = "https://api.assemblyai.com/v2/upload"
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"
headers = {"authorization": API_KEY_ASSEMBLYAI}


def upload(filename):
    def read_file(filename, chunk_size=5242880):
        with open(filename, "rb") as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data

    urlresponse = requests.post(
        upload_enpoint, headers=headers, data=read_file(filename)
    )

    # print(urlresponse.json())

    audio_url = urlresponse.json()["upload_url"]
    return audio_url


# transcribe
def transcribe(audio_url):
    transcript_request = {"audio_url": audio_url}
    transcript_response = requests.post(
        transcript_endpoint, json=transcript_request, headers=headers
    )

    job_id = transcript_response.json()["id"]
    return job_id


# poll
def poll(transcript_id):
    polling_endpoint = transcript_endpoint + "/" + transcript_id
    polling_response = requests.get(polling_endpoint, headers=headers)
    return polling_response.json()


def get_transcription_result_url(audio_url):
    transcript_id = transcribe(audio_url)
    print("Waiting 30 seconds...")
    while True:
        data = poll(transcript_id)
        # polling_response = requests.get(polling_endpoint, headers=headers)
        if data["status"] == "completed":
            return data, None
        elif data["status"] == "error":
            return data, data["error"]

        # time.sleep(30)


# save transcript
def save_transcript(audio_url, filename):
    data, error = get_transcription_result_url(audio_url)
    print(data)

    if data:
        text_filename = filename + ".txt"
        with open(text_filename, "w") as f:
            f.write(data["text"] + "\n")
            for i in data["words"]:
                f.write(
                    "Word: "
                    + i.get("text", "")
                    + ", Confidence: "
                    + str(i.get("confidence", ""))
                    + "\n"
                )
        print("Transcription saved!!")
    elif error:
        print("Error!!", error)
