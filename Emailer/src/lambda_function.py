from ai_gmail_agent import AiGmailAgent

agent = AiGmailAgent()

def lambda_handler(event, context):
    agent.check_for_unread_mail()
    agent.read_email()
    agent.send_email()
    return {
        "statusCode": 200,
        "body": "Processed email."
    }