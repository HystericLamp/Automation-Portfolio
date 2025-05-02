from ai_gmail_agent import AiGmailAgent

agent = AiGmailAgent()

def lambda_handler(event, context):
    emails = agent.get_unread_mail()
    result = agent.process_emails(emails)
    if result:
        return {
            "statusCode": 200,
            "body": "Processed email(s)."
        }
    else:
        return {
            "statusCode": 200,
            "body": "Failed to process email(s)."
        }