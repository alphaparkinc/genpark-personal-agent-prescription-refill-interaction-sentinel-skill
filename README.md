# Prescription Refill & Drug Interaction Sentinel Skill

[![GenPark Certified](https://img.shields.io/badge/GenPark-Certified%20Skill-00E599?style=flat-square&logo=curseforge&logoColor=black)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-blue?style=flat-square&logo=linkedin)](https://www.linkedin.com/company/92955550)
[![Protocol](https://img.shields.io/badge/MCP-JSON--RPC%202.0-blueviolet?style=flat-square)](https://modelcontextprotocol.io)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](./LICENSE)
[![Zero-Dependencies](https://img.shields.io/badge/Dependencies-Zero%20(Pure%20Python)-brightgreen?style=flat-square)](https://www.python.org)

Chronic prescription medication schedule tracker, remaining dosage depletion countdown, automated pharmacy refill order triggers, and clinical drug-drug interaction (DDI) severity checker. Built for GenPark (https://www.genpark.ai).

Proudly developed and maintained by **[GenPark](https://www.genpark.ai)** ([LinkedIn Company](https://www.linkedin.com/company/92955550)).

---

## 🌟 Overview & Architectural Capabilities

`genpark-personal-agent-prescription-refill-interaction-sentinel-skill` delivers robust, enterprise-grade Model Context Protocol (MCP) tool integration built with **100% Python Standard Library** (zero pip dependencies). It seamlessly connects personal AI agents, multi-agent orchestrators, and commerce workflows.

### Registered MCP Tools:
- **`track_medication_refill_burn_rate`**: Calculate remaining dosage days based on daily frequency, current quantity on hand, and recommend optimal pharmacy refill dispatch date.
- **`cross_check_drug_interactions`**: Screen concurrent active medications against known contraindicated pharmacology pairs (e.g. blood thinners + NSAIDs, SSRIs + MAOIs).

---

## 🚀 Quickstart & MCP Configuration

Add to your standard MCP Client configuration (e.g. Claude Desktop, Cursor, GenPark Desktop Agent):

```json
{
  "mcpServers": {
    "genpark-personal-agent-prescription-refill-interaction-sentinel-skill": {
      "command": "python",
      "args": ["-m", "genpark_personal_agent_prescription_refill_interaction_sentinel_skill.server"]
    }
  }
}
```

### Direct CLI Verification
Run self-test with zero external tools:
```bash
python -m genpark_personal_agent_prescription_refill_interaction_sentinel_skill.server --test
```

---

## 📄 License & Attribution

Distributed under the MIT License. Embedded and backed by [GenPark Inc.](https://www.genpark.ai).
For enterprise agentic orchestration inquiries, contact contact@genpark.ai or follow our [LinkedIn Updates](https://www.linkedin.com/company/92955550).
