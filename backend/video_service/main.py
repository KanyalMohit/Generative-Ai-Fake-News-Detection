import pika
import redis
import json
import os
import sys
import time
from dotenv import load_dotenv

load_dotenv()

# Ensure services module can be found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.video_analyzer import analyze_video

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
VIDEO_QUEUE = "video_queue"
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Redis Client
try:
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
except Exception as e:
    print(f"Failed to connect to Redis: {e}")
    sys.exit(1)

def callback(ch, method, properties, body):
    job_data = json.loads(body)
    job_id = job_data.get("job_id")
    video_path = job_data.get("video_path")
    
    print(f" [x] Received Job {job_id} for video {video_path}")
    
    # Update status to PROCESSING
    r.hset(f"job:{job_id}", mapping={"status": "PROCESSING"})
    
    try:
        # Simulate processing or call actual analyzer
        # In a real deployed env, video_path needs to be accessible (shared volume)
        # For local dev, we assume we are running relative to backend root or similar
        
        # Check if file exists (path might be relative to gateway, need to adjust if services run in different dirs locally)
        # For this boilerplate, we assume 'uploads/' is in the mapped volume or common root
        
        if not os.path.exists(video_path):
             # Try adjusting path if running from inside video_service
             # Assuming uploads is at ../uploads
             alt_path = os.path.join("..", video_path)
             if os.path.exists(alt_path):
                 video_path = alt_path
        
        result = analyze_video(video_path)
        
        # Save result
        r.hset(f"job:{job_id}", mapping={"status": "COMPLETED", "result": json.dumps(result)})
        print(f" [x] Job {job_id} Completed")

    except Exception as e:
        print(f" [!] Job {job_id} Failed: {e}")
        r.hset(f"job:{job_id}", mapping={"status": "FAILED", "error": str(e)})

    # Acknowledge message
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    print(" [*] Waiting for video jobs. To exit press CTRL+C")
    
    connection = None
    while not connection:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        except pika.exceptions.AMQPConnectionError:
            print("RabbitMQ not ready, retrying in 5s...")
            time.sleep(5)

    channel = connection.channel()
    channel.queue_declare(queue=VIDEO_QUEUE, durable=True)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=VIDEO_QUEUE, on_message_callback=callback)

    channel.start_consuming()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
