import pika,  json


def upload(f, fs, channel, access):
    try:
        file_id = fs.put(f)
    except Exception as err:
        print(err)
        return "Internal Server Error", 500

    message_to_send = {
        "video_fid": str(file_id),
        "mp3_fid": None,
        "username": access["username"]
    }

    try:
        channel.basic_publish(
            exchange="",  # setting exchange to "" is to setup to default exchange
            routing_key="video",  # name of the queue to route the message to
            body=json.dumps(message_to_send),
            properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE),
        )

    except Exception as err:
        print(err)  # Print Stack Trace
        fs.delete(file_id)
        return 'Internal Server Error', 500
