# utils/logging.py
import time, json

def log_tool_call(tool_name, args, fn):
    start = time.time()
    try:
        res = fn(**args)
        latency = round((time.time()-start)*1000)
        print(json.dumps({"tool": tool_name, "latency_ms": latency, "status": "ok"}))
        return res
    except Exception as e:
        latency = round((time.time()-start)*1000)
        print(json.dumps({"tool": tool_name, "latency_ms": latency, "status": "error", "error": str(e)}))
        raise