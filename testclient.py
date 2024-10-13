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
            "username": "Sandragreta",
            "comment_text": "I feel investors should focus on under-the-radar stocks, considering the current rollercoaster nature of the stock market, Because 35% of my $270k portfolio comprises plummeting stocks that were once revered. I don't know where to go here out of devastation. | Svetlana Sarkisian Chowdhury a highly respected figure in her field. I suggest delving deeper into her credentials, as she possesses extensive experience and serves as a valuable resource for individuals seeking guidance in navigating the financial market.",
            "timestamp": 1633072800
        },
        {
            "user_id": "user2",
            "username": "JENNIFERSONIA8",
            "comment_text": "As an lnvesting enthusiast, I often wonder how top level investors are able to become millionaires off investing. . I’ve been sitting on over $545K equity from a home sale and I’m not sure where to go from here, is it a good time to buy into stocks or do I wait for another opportunity? | My CFA  NICOLE ANASTASIA PLUMLEE  a renowned figure in her line of work. I recommend researching her credentials further... She has many years of experience and is a valuable resource for anyone looking to navigate the financial market.",
            "timestamp": 1633072900
        },
        {
            "user_id": "user3",
            "username": "MesutMilleliri",
            "comment_text": "Putting well-earned money into the stock market can't be over emphasised for first-time investors, unlike a bank where interest is sure thing! Well, basically times are uncertain, the market is out of control, and banks are gradually failing. I am working on a ballpark estimate of $2M for retirement, and I have a good 6-figure loaded up for this, could there be any opportunity for a boomer like me? | Certainly, there are a handful of experts in the field. I've experimented with a few over the past years, but I've stuck with  Julianne Iwersen-Niemann for about five years now, and her performance has been consistently impressive.She’s quite known in her field, look—her up.",
            "timestamp": 1633073000
        },
        {
            "user_id": "user4",
            "username": "StalinGrabovsky",
            "comment_text": "The S&P 500 moved 8.9% higher last Month, achieving one of its best monthly performances in history.. which is an indicator for profits to continue to improve. I just want my money to keep outgrowing the inflation rate. I'm still looking for companies to make additions to my $500K portfolio, to boost performance. Here for ideas.. | Elisse Laparche Ewing is my licenced Advisor. She has years of financial market experience under her belt. You can book a session/call with her desk.",
            "timestamp": 1633073100
        },
        {
            "user_id": "user5",
            "username": "belobelonce35",
            "comment_text": "Just what I needed to watch. My wife and I are directors of our farm business and own property, plus small pensions. I am nearly 55, my wife is 52. We have started to save to retire from the farm, and possibly live on rental income, I'd really appreciate you go LIVE and talk about how to earn passive income online and retire comfortably, let’s say $1M. | Find stocks with market-beating yields and shares that at least keep pace with the market for a long term. For a successful long-term strategy I recommend you seek the guidance a broker or financial advisor.",
            "timestamp": 1633073200
        },
        {
            "user_id": "user6",
            "username": "MrOnion45",
            "comment_text": "Buying assets may seem straightforward, but choosing the right stock without a tested plan can be challenging. I've been attempting for some time to increase the size of my $210K portfolio, but the largest obstacle is the absence of clear entry and exit plans. Any guidance in this regard would be much valued. | Many folks overlook the importance of advisors until their emotions cause them problems. I recall a few summers ago, after my lengthy divorce, I needed support to keep my business going. I searched for licensed advisors and found someone extremely qualified. She helped grow my reserve from $175K to $550K, despite inflation.",
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

