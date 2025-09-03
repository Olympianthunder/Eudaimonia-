import { useState } from "react";

function App() {
  const [prompt, setPrompt] = useState("");
  const [response, setResponse] = useState<any>(null);

  async function sendPrompt() {
    const res = await fetch("http://127.0.0.1:8123/v1/ask", {
      method: "POST",
      headers: {
        "Authorization": "Bearer dev-secret-123",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ prompt }),
    });
    const data = await res.json();
    setResponse(data);
  }

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Eudaimonia UI Demo</h1>

      <textarea
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Type your prompt here..."
        style={{ width: "100%", height: "100px" }}
      />
      <br />

      <button onClick={sendPrompt} style={{ marginTop: "1rem" }}>
        Send
      </button>

      {response && (
        <div style={{ marginTop: "2rem" }}>
          <h2>Response</h2>
          <pre>{JSON.stringify(response, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
