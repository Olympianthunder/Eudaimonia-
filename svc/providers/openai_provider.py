import os

def _estimate_usd_from_env(prompt_tokens: int, completion_tokens: int) -> float:
    """Estimate cost using env-configured per-1k token prices to avoid hardcoding rates."""
    in_rate = float(os.getenv("MODEL_IN_PRICE_PER_1K", "0") or 0)
    out_rate = float(os.getenv("MODEL_OUT_PRICE_PER_1K", "0") or 0)
    usd = (prompt_tokens/1000.0)*in_rate + (completion_tokens/1000.0)*out_rate
    return round(usd, 6)

def chat_complete(prompt: str, model: str | None = None, temperature: float = 0.2):
    model = model or os.getenv("MODEL", "gpt-4o-mini")
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")

    # Try modern SDK first
    try:
        from openai import OpenAI  # >=1.x
        client = OpenAI(api_key=api_key)
        r = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
        )
        text = (r.choices[0].message.content or "").strip()
        usage = getattr(r, "usage", None)
        if usage is None:
            pt = ct = tt = 0
        else:
            # usage may be a pydantic-like object or dict-ish
            pt = getattr(usage, "prompt_tokens", None) or getattr(usage, "input_tokens", None) or usage.get("prompt_tokens", 0)
            ct = getattr(usage, "completion_tokens", None) or getattr(usage, "output_tokens", None) or usage.get("completion_tokens", 0)
            tt = getattr(usage, "total_tokens", None) or usage.get("total_tokens", (pt or 0) + (ct or 0))
        usd = _estimate_usd_from_env(pt or 0, ct or 0)
        return {"text": text, "usage": {"model": model, "prompt_tokens": pt or 0, "completion_tokens": ct or 0, "total_tokens": tt or 0, "usd": usd}}
    except ImportError:
        pass  # fall back to legacy

    # Legacy SDK (openai<1.0)
    import openai  # type: ignore
    openai.api_key = api_key
    r = openai.ChatCompletion.create(  # type: ignore
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
    )
    text = r["choices"][0]["message"]["content"].strip()
    u = r.get("usage", {}) or {}
    pt = int(u.get("prompt_tokens", 0))
    ct = int(u.get("completion_tokens", 0))
    tt = int(u.get("total_tokens", pt + ct))
    usd = _estimate_usd_from_env(pt, ct)
    return {"text": text, "usage": {"model": model, "prompt_tokens": pt, "completion_tokens": ct, "total_tokens": tt, "usd": usd}}
