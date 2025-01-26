
import requests


from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "uwefgiwjfowjnowiyfonscmnamndlaijdipdjpdjwifjcn"  # This will be used to verify your webhook

# Step 1: Webhook Verification
@app.route('/webhook', methods=['GET'])
def verify_webhook():
    # When Facebook sends a GET request to verify the webhook
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if mode == 'subscribe' and token == VERIFY_TOKEN:
        print("Webhook verified!")
        return challenge, 200  # Return the challenge to confirm verification
    else:
        return "Forbidden", 403

# Step 2: Handle Incoming Messages
@app.route('/webhook', methods=['POST'])
def receive_message():
    data = request.json  # Incoming data from Facebook

    # Extract sender ID and the message text
    for entry in data.get('entry', []):
        for event in entry.get('messaging', []):
            sender_id = event['sender']['id']  # This is the user ID
            if 'message' in event:
                message_text = event['message'].get('text')
                print(f"Message from {sender_id}: {message_text}")

                # Respond to the user (you can send a reply here)
                send_message(sender_id, "Received your message!")

    return "EVENT_RECEIVED", 200

def send_message(recipient_id, text):
    import requests

    url = "https://graph.facebook.com/v16.0/me/messages"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": text}
    }
    headers = {
        "Content-Type": "application/json"
    }

    access_token = "EAAGwRF2lGTMBO1kt4IZAJwmsir0MZAR0rBAZAricKlh5dZBDvGcjP21kH7C3wrdEX691fsronmTeVJHB4lZC6lRGSv4b7IFhdCHbEZA9mGNDJLUxOqrZAWCr2aXrUNmHTxUnMZCnDnMKRPMz0dowv5npZC7Bha7O5tziw0AcFLm1iK8uidZAFvuZCcgZCujsIZAl3eS6x"  # Replace with your Page Access Token

    response = requests.post(url, json=payload, headers=headers, params={"access_token": access_token})
    if response.status_code != 200:
        print("Error sending message:", response.json())

if __name__ == "__main__":
    app.run(port=5000)


