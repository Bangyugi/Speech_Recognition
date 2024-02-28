import requests
import json
import time
from api_secrets import API_KEY_ASSEMBLYAI


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
def transcribe(audio_url, sentiment_analysis):
    transcript_request = {
        "audio_url": audio_url,
        "sentiment_analysis": sentiment_analysis,
    }
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


def get_transcription_result_url(audio_url, sentiment_analysis):
    transcript_id = transcribe(audio_url, sentiment_analysis)
    while True:
        data = poll(transcript_id)
        # polling_response = requests.get(polling_endpoint, headers=headers)
        if data["status"] == "completed":
            return data, None
        elif data["status"] == "error":
            return data, data["error"]

        print("Waiting 30 seconds...")
        # time.sleep(30)


def save_transcript(url, title, sentiment_analysis = False):
    data, error = get_transcription_result_url(url, sentiment_analysis)
    print (data)
    if data:
        filename = title + ".txt"
        with open(filename, "w") as f:
            f.write(data["text"])

        if sentiment_analysis:
            filename = title + "_sentiments.json"
            with open(filename, "w") as f:
                sentiments = data["sentiment_analysis_results"]
                json.dump(sentiments, f, indent=4)
        print("Transcript saved")
        return True
    elif error:
        print("Error!!!", error)
        return False
