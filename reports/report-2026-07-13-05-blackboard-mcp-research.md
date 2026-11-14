# Report: Research - is there an official MCP or Claude skill for Blackboard Ultra
**Date**: 2026-07-13
**Sequence**: #05 for the day

## Summary
Researched whether an official or community MCP server / Claude skill exists for Blackboard Ultra. Ran a 6-angle parallel web sweep and verified every concrete candidate by fetching its page (25 agents, 0 errors). Finding: no official MCP or skill exists from either Anthropic or Anthology/Blackboard; several community/third-party MCP servers do exist, but none automate exam-question upload.

## What Changed
- No project files changed (research only).
- Scratch only: `bb_mcp_research.js` (sweep + verify workflow).
- This report.

## Technical Details
- Angles swept: Anthropic official registry/connectors, Anthology/Blackboard official, community MCP registries (GitHub/npm/PyPI/mcp.so/glama/smithery), Claude Agent Skills, Blackboard REST API substrate, and broader LMS MCP ecosystem (Canvas/Moodle).
- Verification: each MCP/skill candidate fetched to confirm reachable + is_real + author + last update.

## Results
- OFFICIAL: none. Blackboard is absent from github.com/modelcontextprotocol/servers and the official Claude Connectors Directory (Education category = Coursera/Udemy/etc., no LMS). Anthology's developer portal documents only REST/LTI/Building Blocks - no MCP. Their in-product AI Design Assistant is Azure OpenAI-powered; AI Alt Text uses Claude via AWS Bedrock (model consumption, not an MCP connector).
- COMMUNITY (verified real): Composio Blackboard toolkit (hosted MCP, ~300+ tools over the Blackboard REST API, managed OAuth, works with Claude Code) is the most usable; nitsuah/bb-mcp (TypeScript, REST + FERPA middleware); plus ~6 institution-specific browser-scraper MCPs (campus-cli/UPC, aula-virtual-mcp/Navarra, pku-blackboard-mcp, uoh-blackboard-mcp, blackboard-mcp, bbwatch) - student-side reading only, low adoption.
- Traps ruled out: peekwez/mcp-blackboard is the unrelated "blackboard pattern" agent-memory server; mcpmarket blackboard-learn listing is not a real installable server; karkarkins/BlackboardAssistantMCP claims MCP but implements none.
- Context: Canvas (3 mature MCPs) and Moodle (official-plugin MCP) are well ahead of Blackboard.

## Issues / Notes
- Practical takeaway for this project: even the best community MCPs wrap courses/grades/announcements/enrollments - the Blackboard REST API has no public test/question-import endpoint (that path is the UI tab-delimited upload or a QTI/Common Cartridge package). So an MCP would not automate the exam upload; the CLO835_Final_Exam_Blackboard.txt remains the correct path.
- Findings are dated as of July 2026 (verified via fetched pages).
