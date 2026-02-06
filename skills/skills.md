
### Skills 


## 8. Runtime Skills (Agent Capability Layer)

### Skill: `skill_fetch_trends`

**Purpose:** Detect trending topics.

Input:

```json
{ "platform": "twitter" }
```

Output:

```json
{ "trends": ["AI Agents", "Tech News"] }
```

---

### Skill: `skill_generate_caption`

**Purpose:** Write captions aligned to persona.

Input:

```json
{ "topic": "AI", "tone": "professional" }
```

Output:

```json
{ "caption": "AI agents are transforming software." }
```

---

### Skill: `skill_generate_media`

**Purpose:** Generate video or image content.

Input:

```json
{ "script": "text", "style": "modern" }
```

Output:

```json
{ "mediaUrl": "https://cdn/video.mp4" }
```

---

### Skill: `skill_publish_social`

**Purpose:** Publish content using Social MCP.

Input:

```json
{ "contentId": "abc123", "platform": "twitter" }
```

Output:

```json
{ "success": true }
```

---