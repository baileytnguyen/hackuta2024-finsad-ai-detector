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
        # Prepare the system message for OpenAI API
        messages = [
            {"role": "system", "content": "You are a helpful assistant that finds financial scams. I am seeing social engineering scams online that follow the same structure to make people click on a link or look up a person. The scams give sometimes offer financial advice. If you think it's a socially engineered scam, say 'scam' only. If you think it's not a socially engineered scam, say 'bananas' only."},
        ]
        
        # Concatenate all comments into a single block (one entry)
        combined_comments = " ".join([f"User: {comment.username} said: '{comment.comment_text}'"
                                      for comment in request.thread.comments])

        messages_bad = []
        for comment in request.thread.comments:
            messages_bad.append({
                "role": "user",
                "content": f"User: {comment.username} - Comment: {comment.comment_text}"
            })
        
        # Append the concatenated comments as a single message
        messages.append({
            "role": "user",
            "content": f"Here are the comments to analyze:\n{combined_comments}"
        })
        
        # Call the OpenAI API
        completion = client.chat.completions.create(
            model="gpt-4o-mini",  # Specify the model you are using
            messages=messages
        )
        
        # Extract the response from OpenAI
        openai_response = completion.choices[0].message.content
        print('OpenAI response:', openai_response)
        user_id = str(comment.comment_text) ########
        print('USERNAME:', user_id)
        comment = str(comment.comment_text) ########
        print('COMMENT:', comment,'\n')

        # Example of processing the OpenAI response to set the is_scam flag
        is_scam = "scam" in openai_response.lower()  # Detect if 'scam' is mentioned
        message = openai_response
        confidence = 90 if is_scam else 10  # Adjust confidence based on the response
        
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