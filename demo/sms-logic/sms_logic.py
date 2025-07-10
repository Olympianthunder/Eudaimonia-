import os
from twilio.rest import Client
import gradio as gr

ACCOUNT_SID = os.getenv("TWILIO_SID", "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
AUTH_TOKEN  = os.getenv("TWILIO_TOKEN", "your_auth_token")
FROM_NUMBER = os.getenv("TWILIO_FROM", "+15551234567")
TO_NUMBER   = os.getenv("EMERGENCY_CONTACT", "+15557654321")

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def send_sms():
    dry_run = os.getenv("DRY_RUN", "true").lower() == "true"
    body = (
        f"DRY_RUN: would send emergency SMS to {TO_NUMBER}"
        if dry_run
        else "Emergency alert: EMS contacted at your location."
    )

    if dry_run:
        return body
    try:
        msg = client.messages.create(
            body=body,
            from_=FROM_NUMBER,
            to=TO_NUMBER
        )
        return f"Sent: SID={msg.sid}"
    except Exception as e:
        return f"Error: {e}"

with gr.Blocks() as demo:
    gr.Markdown("## Emergency-Contact SMS Logic Demo")
    btn = gr.Button("Send Emergency SMS")
    out = gr.Textbox(label="Status", interactive=False)
    btn.click(send_sms, outputs=out)

demo.launch(server_name="0.0.0.0", server_port=3002, share=True)
