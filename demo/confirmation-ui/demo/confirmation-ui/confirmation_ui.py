import os, gradio as gr, requests

PORT    = int(os.environ.get("PORT", 3000))
API_URL = os.environ.get("API_URL", "http://localhost:8000")

def confirm_action(decision: str):
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
        "I’m about to call your local emergency number and begin CPR protocol.  \n"
        "**Confirm** to proceed or **Cancel** to abort."
    )
    with gr.Row():
        gr.Button("Confirm",  variant="primary").click(lambda: confirm_action("confirm"), outputs="out")
        gr.Button("Cancel",   variant="secondary").click(lambda: confirm_action("cancel"),  outputs="out")
    gr.Textbox(label="Engine response", interactive=False, elem_id="out")

demo.launch(server_name="0.0.0.0", server_port=PORT, share=True)
