import time
import gradio as gr
import requests
import os

PORT    = int(os.environ.get("PORT", 3001))
API_URL = os.environ.get("API_URL", "http://localhost:8000")

BPM = 110
INTERVAL = 60.0 / BPM  # seconds per beat

def start_metronome(duration: int):
    try:
        requests.post(
            f"{API_URL}/sop/metronome/start",
            json={"sop_id":"bls_emergency_v2","bpm":BPM,"duration":duration},
            timeout=5
        )
    except Exception:
        pass

    ticks = []
    end = time.time() + duration
    while time.time() < end:
        ticks.append(f"Tick at {time.strftime('%H:%M:%S')}")
        time.sleep(INTERVAL)
    return "\n".join(ticks)

with gr.Blocks() as demo:
    gr.Markdown("## Metronome Stub (110 bpm)")
    dura = gr.Slider(label="Duration (seconds)", minimum=5, maximum=60, step=5, value=30)
    out = gr.Textbox(label="Tick Log", interactive=False)
    btn = gr.Button("Start Metronome")
    btn.click(start_metronome, inputs=dura, outputs=out)

demo.launch(server_name="0.0.0.0", server_port=PORT, share=True)
