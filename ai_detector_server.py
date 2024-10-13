import os
import grpc
import time
from concurrent import futures
from dotenv import load_dotenv
from openai import OpenAI
import comment_scam_detector_pb2
import comment_scam_detector_pb2_grpc

# Load environment variables
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

class ScamDetectionService(comment_scam_detector_pb2_grpc.ScamDetectionServiceServicer):
    def DetectScam(self, request, context):
        # Prepare the messages for OpenAI API
        messages = [
            {"role": "system", "content": "You are a helpful assistant that finds scams. If you think it's a scam, say 'scam' only"},
            {"role": "user", "content": "Analyze the following comments for scams: "},
        ]
        
        # Append each comment to the messages
        for comment in request.thread.comments:
            messages.append({
                "role": "user",
                "content": f"User: {comment.username} - Comment: {comment.comment_text}"
            })
            
        # Call the OpenAI API
        completion = client.chat.completions.create(
            model="gpt-4o-mini",  # Specify the model you are using
            messages=messages
        )
        
        # Extract the response from OpenAI
        openai_response = completion.choices[0].message.content
        print('openai_response:', openai_response)
        # Example of processing the OpenAI response to set the is_scam flag
        # This is a simple implementation; you may want to customize this logic
        #is_scam = "scam" in openai_response  # Detect if 'scam' is mentioned
        is_scam = True
        message = openai_response
        confidence = 0.95 if is_scam else 0.1  # Example confidence levels
        print(message)
        # Create and return the response
        return comment_scam_detector_pb2.ScamDetectionResponse(
            is_scam=is_scam,
            message=message,
            confidence=confidence
        )

def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    comment_scam_detector_pb2_grpc.add_ScamDetectionServiceServicer_to_server(ScamDetectionService(), server)
    server.add_insecure_port('[::]:50051')  # Listen on all interfaces on port 50051
    server.start()
    print("gRPC server is running on port 50051...")
    
    try:
        # Keep the server running
        while True:
            time.sleep(86400)  # Sleep for a day (or replace with a more suitable condition)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()