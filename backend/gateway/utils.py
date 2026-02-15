import pika
import os
import json

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
VIDEO_QUEUE = "video_queue"

def get_rabbitmq_connection():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        return connection
    except Exception as e:
        print(f"Error connecting to RabbitMQ: {e}")
        return None

def publish_video_job(video_path: str, job_id: str):
    connection = get_rabbitmq_connection()
    if not connection:
        return False
    
    try:
        channel = connection.channel()
        channel.queue_declare(queue=VIDEO_QUEUE, durable=True)
        
        message = json.dumps({"video_path": video_path, "job_id": job_id})
        
        channel.basic_publish(
            exchange='',
            routing_key=VIDEO_QUEUE,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ))
        print(f" [x] Sent video job: {job_id}")
        connection.close()
        return True
    except Exception as e:
        print(f"Error publishing message: {e}")
        return False
