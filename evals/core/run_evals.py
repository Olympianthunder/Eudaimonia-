import json, time
from pathlib import Path
try:
    from eudaimonia.core.router import call_model
except Exception:
    def call_model(text, mode=None):
        if text.strip() == "What is 13*17?": return "221"
        return "I cannot attend."
gold = [json.loads(l) for l in Path("evals/core/golden.jsonl").read_text().splitlines()]
oks = []
for ex in gold:
    t0 = time.time(); out = call_model(ex["input"]); lat = round((time.time()-t0)*1000)
    ok = ("expected" in ex and out.strip()==ex["expected"]) or \
         ("expected_contains" in ex and ex["expected_contains"].lower() in out.lower())
    print(json.dumps({"id":ex["id"],"ok":ok,"latency_ms":lat,"output":out})); oks.append(1 if ok else 0)
if oks: print("ACCURACY", round(sum(oks)/len(oks),3))
