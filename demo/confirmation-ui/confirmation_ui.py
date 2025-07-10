import os
import gradio as gr
import requests

# Use Replit’s PORT (defaults to 3000) or override with your own
PORT    = int(os.environ.get("PORT", 3000))
API_URL = os.environ.get("API_URL", "http://localhost:8000")

def confirm_action(decision: str):
    """
    Send the user’s decision back to Eudaimonia’s SOP engine.
    Expects a FastAPI endpoint at POST /sop/confirm that returns JSON 
{"status": ...}.
    """
    try:
        r = requests.post(
            f"{API_URL}/sop/confirm",
            json={"sop_id": "bls_emergency_v2", "decision": decision},
            timeout=5
        )
        return r.json().get("status", f"HTTP {r.status_code}")
    except Exception as e:
        return f"Error: {e}"

with gr.Blocks() as demo:
    gr.Markdown("## BLS Emergency — Confirmation Required")
    gr.Markdown(
        """I’m about to call your local emergency number and begin CPR 
protocol.  
**Confirm** to proceed or **Cancel** to abort."""
    )

    with gr.Row():
        confirm_btn = gr.Button("Confirm", variant="primary")
        cancel_btn  = gr.Button("Cancel",  variant="secondary")

    output = gr.Textbox(label="Engine response", interactive=False)

    confirm_btn.click(lambda: confirm_action("confirm"), outputs=output)
    cancel_btn.click(lambda: confirm_action("cancel"),  outputs=output)

# Launch on 0.0.0.0 so Replit’s proxy can reach it; share=True gives a public link
demo.launch(server_name="0.0.0.0", server_port=PORT, share=True)


