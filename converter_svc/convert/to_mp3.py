import pika, json, tempfile, os
from bson.objectid import ObjectId
import moviepy.editor

def start(message, fs_videos, fs_mp3s, channel):
    message = json.loads(message) # Convert Python object to JSON
    
    #Create Tempoarary File
    temp_file = tempfile.NamedTemporaryFile()

    #VideoContents
    out_file = fs_videos.get(ObjectId(message["video_fid"]))

    #Add Video Contents to Empty File created Above

    temp_file.write(out_file.read())

    #Extracting Audio from temp video file
    audio = moviepy.editor.VideoFileClip(temp_file.name).audio

    #Write Audio to the final file
    temp_file_path = tempfile.gettempdir() + f"/{message['video_fid']}.mp3"

    audio.write_audiofile(temp_file_path)

    # Save the file to MongoDB

    with open(temp_file_path, "rb") as f:
        data = f.read()
        file_id = fs_mp3s.put(data)
    
    os.remove(temp_file_path)
    
    message["mp3_fid"] = str(file_id)

    try:
        channel.basic_publish(
            exchange="",  # setting exchange to "" is to setup to default exchange
            routing_key=os.environ.get("MP3_QUEUE"),  # name of the queue to route the message to
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE),

        )
    except Exception as e:
        fs_mp3s.delete(file_id)
        return "Failed to publish message"

    
