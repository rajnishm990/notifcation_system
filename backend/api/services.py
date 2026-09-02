import os, requests

def send_notification(channel, content, user_data):
    if channel == 'email':
        requests.post(
            "https://api.brevo.com/v3/smtp/email",
            headers={'api-key': os.getenv('BREVO_API_KEY')},
            json={
                "sender": {"email": os.getenv('SENDER_EMAIL')},
                "to": [{"email": user_data.get('email')}],
                "subject": "System Notification",
                "textContent": content
            }
        )
    elif channel == 'wa':
        requests.post(
            f"https://graph.facebook.com/v17.0/{os.getenv('PHONE_NUMBER_ID')}/messages",
            headers={'Authorization': f"Bearer {os.getenv('WHATSAPP_ACCESS_TOKEN')}"},
            json={"messaging_product": "whatsapp", "to": user_data.get('phone'), "type": "text", "text": {"body": content}}
        )
    elif channel == 'push':
        requests.post(
            "https://onesignal.com/api/v1/notifications",
            headers={"Authorization": f"Basic {os.getenv('ONESIGNAL_REST_API_KEY')}"},
            json={
                "app_id": os.getenv('ONESIGNAL_APP_ID'),
                "included_segments": ["Subscribed Users"], 
                "contents": {"en": content}
            }
        )