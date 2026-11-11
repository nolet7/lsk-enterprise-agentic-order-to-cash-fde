"""Executed-model eval. Measures results without claiming success for proxy checks."""
import json,time,statistics,os
import httpx
URL=os.getenv("EVAL_API_URL","http://localhost:18474")
cases=[json.loads(line) for line in open("evals/golden.jsonl") if line.strip()]
out=[]
for c in cases:
    start=time.perf_counter()
    try:
        resp=httpx.post(URL+"/api/chat",headers={"Authorization":"Bearer "+c["actor"]},json={"message":c["question"]},timeout=60)
        body=resp.json()
        ok=resp.status_code==200 and c.get("must_use_tool") in body.get("tool_calls",[]) if c.get("must_use_tool") else resp.status_code==200
        if "must_not_claim" in c:ok=ok and c["must_not_claim"] not in body.get("answer","").lower()
        out.append({"id":c["id"],"http_status":resp.status_code,"proxy_tool_gate_pass":ok,"elapsed_ms":round(1000*(time.perf_counter()-start),2),"answer":body.get("answer",""),"tool_calls":body.get("tool_calls",[])})
    except Exception as ex:
        out.append({"id":c["id"],"error":type(ex).__name__,"proxy_tool_gate_pass":False})
times=sorted(row["elapsed_ms"] for row in out if "elapsed_ms" in row)
p95=times[min(len(times)-1,int(.95*len(times)))] if times else None
summary={"cases":len(out),"proxy_tool_gate_pass":sum(r["proxy_tool_gate_pass"] for r in out),"p95_ms":p95,"limitations":"Tool-selection proxy only; does not establish factual correctness, RAG faithfulness, full end-to-end task success or cost. Human groundedness review required.","results":out}
os.makedirs("evals/results",exist_ok=True)
with open("evals/results/last_run.json","w") as f:json.dump(summary,f,indent=2)
print(json.dumps(summary,indent=2))
