import pika, sys, os, time
from pymongo import MongoClient
import gridfs
from convert import to_mp3

def setup():
    client = MongoClient('host.minikube.internal',27017)
    db_videos = client.videos
    db_mp3s = client.mp3s

    #GridFS setup

    fs_videos = gridfs.GridFS(db_videos)
    fs_mp3s = gridfs.GridFS(db_mp3s)

    #RabbitMQ configuration

    connection = pika.BlockingConnection( pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()

    #CAllBack Function for RabbitMQ channel

    def videocallback(ch, method, properties, body):
        err = to_mp3.start(body, fs_videos, fs_mp3s, ch)
        if err:
            ch.basic_nack(delivery_tag=method.delivery_tag)
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(
        queue=os.environ.get("VIDEO_QUEUE"), on_message_callback=videocallback
    )

    print('Waiting for messages. Exit using Ctrl-C')

    channel.start_consuming()


if __name__ == "__main__":
    try:
        setup()
    except KeyboardInterrupt:
        print("Interrupt")
        try:
            sys.exit(0)
        except:
            os._exit(0)
