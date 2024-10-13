import grpc
import comment_scam_detector_pb2
import comment_scam_detector_pb2_grpc

def test_scam_detection(stub, comments):
    # Prepare the CommentThread for the gRPC request
    comment_thread = comment_scam_detector_pb2.CommentThread(comments=comments)
    request = comment_scam_detector_pb2.ScamDetectionRequest(thread=comment_thread)

    # Call the DetectScam method
    response = stub.DetectScam(request)
    return response

def main():
    # Create a gRPC channel to connect to the server
    channel = grpc.insecure_channel('localhost:50051')  # Adjust the port if necessary
    stub = comment_scam_detector_pb2_grpc.ScamDetectionServiceStub(channel)

    # Test cases
    test_comments = [
        {
            "user_id": "user1",
            "username": "User One",
            "comment_text": "This is a great product!",
            "timestamp": 1633072800
        },
        {
            "user_id": "user2",
            "username": "User Two",
            "comment_text": "Click here to win a free iPhone!",
            "timestamp": 1633072900
        },
        {
            "user_id": "user3",
            "username": "User Three",
            "comment_text": "Get rich quick!",
            "timestamp": 1633073000
        },
        {
            "user_id": "user4",
            "username": "User Four",
            "comment_text": "Just a regular comment.",
            "timestamp": 1633073100
        },
        {
            "user_id": "user5",
            "username": "User Five",
            "comment_text": "Earn money now!",
            "timestamp": 1633073200
        },
        {
            "user_id": "user6",
            "username": "User Six",
            "comment_text": "",
            "timestamp": 1633073300
        }
    ]

    for comment in test_comments:
        # Prepare the comment for the request
        comments = [comment_scam_detector_pb2.Comment(
            user_id=comment["user_id"],
            username=comment["username"],
            comment_text=comment["comment_text"],
            timestamp=comment["timestamp"]
        )]

        # Call the scam detection function
        response = test_scam_detection(stub, comments)

        # Print the response
        print(f"Comment: {comment['comment_text']}")
        print("Is Scam:", response.is_scam)
        print("Message:", response.message)
        print("Confidence:", response.confidence)
        print("-" * 50)

if __name__ == "__main__":
    main()