# Victoria of the Day --- AI-Assisted Content Prep

## 1. Purpose

This is a planned extension of the existing **Victoria of the Day**
Instagram automation project.

The current production publisher already works:

``` text
Notion
→ GitHub Actions
→ Python
→ Instagram Graph API
→ Notion update
→ Telegram
```

The purpose of this extension is to help prepare future content in
Notion with AI while preserving **manual editorial approval**.

AI prepares content. It does **not** publish posts and does **not** mark
posts as `ready`.

------------------------------------------------------------------------

## 2. Core Principle

Keep the existing production publisher separate and unchanged.

``` text
AI Content Preparation
        ↓
      Notion
        ↓
 Human review/editing
        ↓
 Image preparation
        ↓
 Status → ready
        ↓
 Existing publisher
        ↓
    Instagram
```

Notion remains the source of truth.

------------------------------------------------------------------------

## 3. MVP Goal

Create a separate Python script that can be launched manually through
GitHub Actions.

The MVP should:

1.  Find upcoming Notion rows where `Publish Date` is set and `Title` is
    empty.
2.  Read existing content to understand the established Victoria of the
    Day style and avoid duplicate titles.
3.  Generate structured content for a small number of upcoming posts,
    initially about **3 posts per run**.
4.  Write the generated content back into the existing Notion fields.
5.  Never change `Status`.
6.  Never publish anything to Instagram.
7.  Never overwrite existing editorial content unless explicitly enabled
    later.

------------------------------------------------------------------------

## 4. Existing Notion Fields

The current database already contains the fields required for AI content
preparation:

``` text
ID
Day
Publish Date
Title
Category
Image URL
Status
Connection Type
Main Object
Caption
Explanation
Image Prompt
Error
IG Post ID
```

### AI may write

``` text
Title
Category
Connection Type
Main Object
Caption
Explanation
Image Prompt
```

### AI must not modify

``` text
ID
Day
Publish Date
Status
Image URL
Error
IG Post ID
```

`Status` is especially important: only a human should decide when a post
becomes `ready`.

------------------------------------------------------------------------

## 5. Expected AI Output

Each generated concept should have a strict structured result similar
to:

``` json
{
  "title": "Saint Victoria of the Forgotten Umbrella",
  "category": "Goddness of small victories",
  "connection_type": "Everyday / mock-hagiographic",
  "main_object": "Forgotten umbrella",
  "caption": "She checked the weather. The weather checked her.",
  "explanation": "An ordinary inconvenience reframed as a tiny saintly trial.",
  "image_prompt": "Victoria standing at a doorway..."
}
```

The exact schema and field rules should be finalized before
implementation.

------------------------------------------------------------------------

## 6. Style Requirements

Generated content should follow the established **Victoria of the Day**
identity rather than generic social-media copy.

Current themes include:

-   Victoria / victory associations;
-   everyday micro-victories;
-   mock-hagiographic "Saint Victoria of..." concepts;
-   dry humor;
-   absurd everyday situations;
-   cultural, linguistic, historical, geographic, symbolic and meme-like
    associations;
-   Vika/Victoria wordplay where appropriate.

Before generation, the assistant should use existing Notion content as
context and check existing titles to reduce repetition.

------------------------------------------------------------------------

## 7. Safety / Editorial Rules

The AI content-prep workflow must be isolated from publishing.

Hard rules:

-   Do not call Instagram publishing functions.
-   Do not set `Status = ready`.
-   Do not set `Status = posted`.
-   Do not modify `IG Post ID`.
-   Do not modify `Image URL`.
-   Do not overwrite a non-empty `Title`.
-   Prefer filling only genuinely empty content rows.
-   Human review remains mandatory before publication.

------------------------------------------------------------------------

## 8. Proposed Repository Changes

Keep the current publisher intact and add:

``` text
Victoria-of-the-day/
│
├── .github/
│   └── workflows/
│       ├── publish.yml
│       └── generate-content.yml       # NEW
│
├── src/
│   ├── main.py                        # existing publisher; keep separate
│   ├── notion_client.py
│   ├── instagram_client.py
│   ├── telegram_client.py
│   ├── config.py
│   └── content_assistant.py           # NEW
│
└── ...
```

Likely changes:

``` text
src/content_assistant.py
    AI content-generation orchestration

src/notion_client.py
    methods for finding empty upcoming rows
    methods for writing generated content

src/config.py
    AI-related environment variables

.github/workflows/generate-content.yml
    manual content-generation workflow
```

------------------------------------------------------------------------

## 9. OpenAI API

Planned implementation may use the OpenAI API with structured output.

Potential environment variables:

``` text
OPENAI_API_KEY
AI_MODEL
```

`OPENAI_API_KEY` must be stored as a GitHub Secret and must never be
committed to the repository.

OpenAI API billing is separate from a ChatGPT subscription. Before
implementation, create/configure the API project and decide on an
appropriate model and spending limit.

------------------------------------------------------------------------

## 10. Proposed Manual Workflow

GitHub Actions:

``` text
Actions
→ Generate content
→ Run workflow
```

Initial behavior:

``` text
Find next 3 rows
where:
    Publish Date exists
    Title is empty

        ↓

Generate content

        ↓

Validate structured response

        ↓

Write allowed fields to Notion

        ↓

STOP
```

No Instagram action follows.

------------------------------------------------------------------------

## 11. Example Result in Notion

Before:

``` text
Day:             33
Publish Date:    2026-08-29
Title:
Category:
Connection Type:
Main Object:
Caption:
Explanation:
Image Prompt:
Image URL:
Status:
```

After AI generation:

``` text
Day:             33
Publish Date:    2026-08-29
Title:           Saint Victoria of the Forgotten Umbrella
Category:        Goddness of small victories
Connection Type: Everyday / mock-hagiographic
Main Object:     Forgotten umbrella
Caption:         ...
Explanation:     ...
Image Prompt:    ...
Image URL:
Status:
```

The user then reviews/edits the concept, prepares the image, adds the
image URL, and manually changes:

``` text
Status → ready
```

The existing production publisher takes over from there.

------------------------------------------------------------------------

## 12. Implementation Order

### Phase 1 --- API Setup

-   Create a dedicated OpenAI API project for Victoria of the Day.
-   Create an API key.
-   Store it as `OPENAI_API_KEY` in GitHub Secrets.
-   Set a conservative spending limit.
-   Choose the model.

### Phase 2 --- Notion Read/Write

-   Add a method to find upcoming rows with an empty `Title`.
-   Limit the initial run to 3 rows.
-   Read existing titles/content for style and duplicate checking.
-   Add a safe update method restricted to approved AI fields.

### Phase 3 --- Content Assistant

-   Create `src/content_assistant.py`.
-   Define the generation instructions.
-   Define structured output.
-   Validate generated content.
-   Prevent overwriting populated rows.

### Phase 4 --- GitHub Actions

-   Add `generate-content.yml`.
-   Start with `workflow_dispatch` only.
-   Do not add a schedule initially.
-   Test with one empty Notion row.
-   Then test with three rows.

### Phase 5 --- Review

-   Check generated concepts manually.
-   Tune style instructions using real results.
-   Only after the MVP is reliable consider further automation.

------------------------------------------------------------------------

## 13. Possible Later Improvements

After the text-only MVP is stable:

-   configurable number of posts per run;
-   regenerate a selected concept;
-   explicit AI draft/review state;
-   automatic duplicate/concept similarity checks;
-   Telegram summary of newly generated drafts;
-   generation of image prompts with a stricter house style;
-   image generation;
-   image upload to the personal server;
-   content health checks for the next 7--14 days;
-   analytics-informed idea generation.

Image generation should remain a separate later phase. Do not combine it
with the first MVP.

------------------------------------------------------------------------

## 14. Current Decision / Resume Point

The existing Instagram publishing project is working in production.

The next planned feature is:

> **AI-assisted content preparation for empty upcoming Notion rows, with
> mandatory human approval before publication.**

No implementation has been started yet.

When resuming this project, begin with:

1.  OpenAI API project/key setup.
2.  Inspect the current `notion_client.py`.
3.  Design the safe Notion query/update methods.
4.  Implement `content_assistant.py`.
5.  Add a manually triggered `generate-content.yml`.
6.  Test on one empty future Notion row before generating multiple
    posts.

Do **not** modify the working Instagram publisher unless a shared Notion
helper genuinely requires a backward-compatible change.
