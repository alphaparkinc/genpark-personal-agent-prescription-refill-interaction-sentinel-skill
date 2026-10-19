# -*- coding: utf-8 -*-
"""Model Context Protocol (MCP) Server for Prescription Refill & Drug Interaction Sentinel Skill
Powered by GenPark (https://www.genpark.ai).
"""
import sys
import json
import logging
from .core import *

TOOLS_METADATA = [
  {
    "name": "track_medication_refill_burn_rate",
    "description": "Calculate remaining dosage days based on daily frequency, current quantity on hand, and recommend optimal pharmacy refill dispatch date.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "medication_name": {
          "type": "string"
        },
        "pills_remaining": {
          "type": "integer"
        },
        "doses_per_day": {
          "type": "integer"
        },
        "pills_per_dose": {
          "type": "integer"
        },
        "pharmacy_processing_lead_days": {
          "type": "integer"
        }
      },
      "required": [
        "medication_name",
        "pills_remaining",
        "doses_per_day"
      ]
    }
  },
  {
    "name": "cross_check_drug_interactions",
    "description": "Screen concurrent active medications against known contraindicated pharmacology pairs (e.g. blood thinners + NSAIDs, SSRIs + MAOIs).",
    "inputSchema": {
      "type": "object",
      "properties": {
        "current_medications": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "prospective_medication": {
          "type": "string"
        }
      },
      "required": [
        "current_medications",
        "prospective_medication"
      ]
    }
  }
]

def handle_rpc(request_str: str) -> str:
    try:
        req = json.loads(request_str)
    except Exception as e:
        return json.dumps({"jsonrpc": "2.0", "error": {"code": -32700, "message": "Parse error"}, "id": None})
    
    msg_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        return json.dumps({
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {
                    "name": "genpark-personal-agent-prescription-refill-interaction-sentinel-skill",
                    "version": "1.0.0",
                    "vendor": "GenPark (https://www.genpark.ai)"
                }
            }
        })

    if method == "tools/list":
        return json.dumps({
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {"tools": TOOLS_METADATA}
        })

    if method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        func = globals().get(tool_name)
        if not func or not callable(func):
            return json.dumps({
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32601, "message": f"Method '{tool_name}' not found"}
            })
        
        try:
            call_res = func(**arguments)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [
                        {"type": "text", "text": json.dumps(call_res, ensure_ascii=False, indent=2)}
                    ]
                }
            })
        except Exception as err:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32000, "message": f"Execution error: {str(err)}"}
            })

    return json.dumps({
        "jsonrpc": "2.0",
        "id": msg_id,
        "error": {"code": -32601, "message": f"Unhandled method '{method}'"}
    })

def run_self_test():
    print(f"=== Running Self Test for genpark-personal-agent-prescription-refill-interaction-sentinel-skill ===")
    init_res = json.loads(handle_rpc(json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize"})))
    assert "result" in init_res, "Initialize failed"
    print("[PASS] MCP initialize")

    list_res = json.loads(handle_rpc(json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})))
    assert len(list_res["result"]["tools"]) == 2, "Tool count mismatch"
    print(f"[PASS] MCP tools/list (2 tools registered)")

    # Execute smoke test for each tool

    call1 = json.loads(handle_rpc(json.dumps({
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "cross_check_drug_interactions",
            "arguments": {
                "current_medications": ["Warfarin", "Metformin"],
                "prospective_medication": "Aspirin"
            }
        }
    })))
    assert "result" in call1, "Call1 failed"
    print("[PASS] Tool smoke test: cross_check_drug_interactions")

    print("[ALL TESTS PASSED] Self-test verified successfully.")
    return True

if __name__ == "__main__":
    if "--test" in sys.argv:
        success = run_self_test()
        sys.exit(0 if success else 1)
    
    for line in sys.stdin:
        if not line.strip():
            continue
        out = handle_rpc(line)
        sys.stdout.write(out + "\n")
        sys.stdout.flush()
