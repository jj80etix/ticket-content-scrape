---
title: "vivenu Opens Ticketing Operations to ChatGPT, Claude With New MCP Server"
author: "Dave Clark"
source: "https://www.ticketnews.com/feed/"
url: "https://www.ticketnews.com/2026/10/vivenu-mcp-server-chatgpt-claude/"
type: article
date: 2026-10-30
tags: [q12, q14, build, improve, ai-context, vivenu]
---

# vivenu Opens Ticketing Operations to ChatGPT, Claude With New MCP Server

## Summary

Ticketing platform vivenu launched an MCP (Model Context Protocol) Server giving organizers over 100 ticketing functions — sales reporting, pricing, inventory holds, event creation — directly through ChatGPT, Claude, and Codex, extending its in-platform AI Assistant (launched July) to external AI tools. The company frames it as meeting a demand for ticketing data to appear inside tools organizers already use (CRM, marketing, board reporting) rather than a separate dashboard.

### Key Points
- MCP Server announced October 29; exposes 100+ ticketing functions via conversational commands
- Builds on vivenu's AI Assistant (introduced July) which brought conversational AI into its own platform
- Example use cases: checking sales performance, generating branded reports, creating discount codes, finding/holding seats across multiple events, all without the native dashboard
- Uses Model Context Protocol, the open standard for connecting AI applications to external software/actions

### Highlights
- First ticketing vendor (in our coverage) to expose core ticketing operations as an MCP server for third-party AI assistants, not just an in-house chatbot
- CEO framing: customers want data "where the rest of their work already happens" rather than another dashboard

### Industry Problem
Ticketing operators juggle multiple disconnected tools (ticketing dashboard, CRM, marketing, reporting); conversational/agentic access to operational data addresses the fragmentation and manual-reporting burden organizers face, and sets a new competitive bar for what "AI-native" ticketing operations look like.

### Proposed Solution
vivenu's answer is an open MCP interface rather than a closed assistant. For Etix Assistant, this is a direct benchmark: evaluate exposing an MCP server (or equivalent tool-use API) over core ticketing operations (reporting, pricing, inventory, discounting) so organizers can act through ChatGPT/Claude rather than only Etix's own AI surface — a concrete #build candidate.

#q12 #q14 #build #improve #ai-context #vivenu

## Transcript

![](https://www.ticketnews.com/wp-content/uploads/2026/10/vivenu-mcp-1200.webp)

Ticketing technology company vivenu has launched a new integration that allows event organizers to manage ticket sales, inventory, pricing and other operations directly through artificial intelligence tools including ChatGPT, Claude and Codex, extending its AI capabilities beyond the company’s own platform.

The [vivenu MCP Server, announced October 29](https://www.vivenu.com/vivenu-launches-mcp-server?utm_source=TicketNews&utm_medium=content), gives customers access to more than 100 ticketing functions through compatible AI assistants. Users can ask questions about sales performance, create events, adjust pricing, issue tickets, hold seats and generate reports through conversational commands, without navigating the company’s traditional ticketing dashboard for each task.

The launch represents the next step in vivenu’s effort to make ticketing data more accessible and actionable for organizers, building on the AI Assistant it introduced in July. That product brought conversational AI capabilities into vivenu’s existing platform, while the new MCP Server allows organizers to access their ticketing systems from external AI applications they already use.

“Our customers didn’t ask for another dashboard. They asked for their ticketing data to show up where the rest of their work already happens, with their CRM, their marketing numbers and their board report,” said Simon Hennes, co-founder and CEO of vivenu. “The MCP Server does exactly that. A marketing director can ask about last weekend’s sales, get a branded report back, and create the discount code the answer points to, without leaving their AI tool.”

Advertisement

  [<video width="728" height="90"><source src="https://www.ticketnews.com/wp-content/uploads/2026/08/broker-copilot-ticketnews-banner-728x90-1.webm" type="video/webm"> <source src="https://www.ticketnews.com/wp-content/uploads/2026/08/broker-copilot-ticketnews-banner-728x90-1.mp4" type="video/mp4"> <img src="https://www.ticketnews.com/wp-content/uploads/2026/08/broker-copilot-ticketnews-banner-728x90-poster.webp" width="728" height="90" alt="Broker Copilot - The AI Assistant for Tickets"></video>](https://brokercopilot.io/?utm_source=ticketnews&utm_medium=banner)

The technology uses Model Context Protocol, or MCP, an open standard that enables AI applications to connect with external software, retrieve information and execute supported actions. For ticketing operators, it creates a way to manage transactions and operational workflows through conversational requests rather than performing each step manually within separate software interfaces.

For example, vivenu says an organizer could ask an AI assistant to locate five seats together across three upcoming home games. The assistant could check availability, release inventory from an existing hold when necessary and place seats on hold for the prospective buyer.

Another scenario involves analyzing sales performance and responding immediately. A ticketing or marketing manager could request a report covering revenue, order volume, average order value and top-selling events, then instruct the assistant to create a promotional discount for an upcoming event based on the results.

The platform also supports recurring tasks, including daily sales reports and notifications about events performing below sales targets.

Advertisement

  [<video width="728" height="90"><source src="https://www.ticketnews.com/wp-content/uploads/2026/10/tickets-dev_02-stop-maintaining-scrapers_desktop-728x90_animated.webm" type="video/webm"> <source src="https://www.ticketnews.com/wp-content/uploads/2026/10/tickets-dev_02-stop-maintaining-scrapers_desktop-728x90_animated.mp4" type="video/mp4"> <img src="https://www.ticketnews.com/wp-content/uploads/2026/10/tickets-dev_02-stop-maintaining-scrapers_desktop-728x90_static.png" width="728" height="90" alt="Tickets.dev ticket pricing API"></video>](https://tickets.dev/?utm_source=ticketnews&utm_medium=banner&utm_campaign=tickets-dev&utm_content=internal_p8_v02_desktop)

Importantly, the AI tools are not operating independently of vivenu’s existing permission structure. According to the company, each user connects through an individual vivenu account, and the actions available through the MCP Server are limited to those already authorized for that person.

Actions that modify data, including changes to ticket prices, are flagged to the connected AI application for human confirmation before execution, vivenu says.

“We built the MCP Server on the same principles as the vivenu AI Assistant: it reads the live data the platform runs on, and it respects every existing role and permission,” said Jens Teichert, co-founder and CTO of vivenu. “The difference is where it lives. Organizers choose the AI tool, we make sure vivenu is a first-class citizen inside it.”

## Moving Ticketing Beyond the Dashboard

The announcement also reflects a broader change in how ticketing software companies are approaching the relationship between their platforms and the organizations using them.

Traditional ticketing administration generally requires operators to access specific dashboards to handle inventory, pricing, reports and other functions. MCP integrations introduce another option, allowing outside applications to serve as the interface while the ticketing platform continues managing the underlying data and transactions.

vivenu is not alone in pursuing that approach. Ticket Tailor previously introduced an [MCP-based AI Assist integration](https://www.tickettailor.com/blog/introducing-ai-assist?utm_source=TicketNews&utm_medium=content) that enables organizers to perform tasks such as creating events, changing ticket prices and retrieving sales reports through Claude.

For vivenu, the distinction is the breadth of functions being made available across multiple AI tools and the integration of those capabilities with its existing enterprise ticketing infrastructure.

The new offering also fits into the company’s larger emphasis on giving organizers control over their customer information and enabling that data to be used across business functions.

In June, vivenu [introduced vivenu Engage](https://www.ticketnews.com/2026/06/vivenu-launches-engage-ticketing-data-fan-marketing-fuel/?utm_source=TicketNews&utm_medium=content), connecting ticketing transactions with audience segmentation, marketing campaigns and customer relationship management capabilities.

More recently, discussions at the company’s September AI Summit highlighted the problems created when [fan and customer data is fragmented across multiple business systems](https://www.ticketnews.com/2026/09/vivenu-ai-summit-ticketing-fan-data/?utm_source=TicketNews&utm_medium=content). Participants identified disconnected ticketing, marketing, sponsorship and other platforms as barriers to using AI effectively.

The MCP Server addresses another part of that challenge by making ticketing information available within compatible AI environments, where organizers may also be working with CRM records, financial documents and marketing information.

The ability to connect those systems does not necessarily mean they are automatically integrated, however. The usefulness of a combined workflow will depend on which external applications and data sources the organizer has connected, along with the permissions and capabilities available in each.

The arrangement also leaves vivenu responsible for the underlying ticketing infrastructure. AI assistants provide an additional way to interact with that infrastructure rather than replacing the platform that maintains inventory, customer records and transaction data.

For organizations managing frequent events, multiple ticket types and large volumes of inventory, the potential advantage is reducing the number of manual steps required to move from identifying an operational issue to taking action.

Whether those efficiencies materialize across complex real-world ticketing environments will depend on implementation, the reliability of AI-generated instructions and the safeguards governing changes to live operational data.

vivenu says its MCP Server is now available to customers using ChatGPT, Claude, Codex and other MCP-compatible AI tools. The company has not publicly detailed separate pricing for the integration or identified specific customer deployments in its launch announcement.
