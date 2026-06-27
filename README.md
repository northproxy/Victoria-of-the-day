## Victoria-of-the-day

The main idea is to show a new image, symbol, object, place, character, word, or meme-like association connected to the name Victoria / Vika every day.

Automated Instagram publisher for the **Victoria-of-the-day** project.

Stack:

- Notion as content database
- Public image URLs hosted on personal server
- Python publishing script
- GitHub Actions scheduler
- Instagram Graph API
- Optional Telegram notifications

## MVP Goal

Publish one daily Instagram image post from Notion and update the Notion status after publishing.

UPDATE 27 Juni 2026

What's Built

A fully automated Instagram publishing pipeline that runs daily without any manual intervention.

Stack

Notion → GitHub Actions → Python → Instagram Graph API → Notion update

What's Done

Infrastructure
- GitHub repository set up and connected to local VSCode
- GitHub Actions workflow running on a daily schedule (09:00 Vienna time)
- All secrets stored securely in GitHub Secrets
Notion
- Database created with all required columns including Status, Error, IG Post ID
- First 10 posts created with images, captions, and dates
- Notion Integration connected
Python Scripts
- config.py — loads all environment variables and validates them
- notion_client.py — reads today's ready post, writes back status, post ID, and errors
- instagram_client.py — creates media container, waits for processing, publishes
- main.py — orchestrates the full pipeline
Features working
- Finds today's post by date and status
- Validates image URL before publishing
- Builds caption from title, text, and hashtags
- Publishes image to Instagram
- Saves IG Post ID back to Notion
- Marks post as posted or error in Notion
- Prevents duplicate publishing
- Dry-run mode for safe testing
---

What's Been Tested

Test
Result
Notion read
✅
Image URL validation
✅
Caption builder
✅
mark_as_error() write to Notion
✅
mark_as_posted() write to Notion
✅
Real Instagram publish
✅
Duplicate publish guard
✅
GitHub Actions manual trigger
✅
GitHub Actions daily schedule
✅

---

What's Next

- Telegram notifications — optional but useful for monitoring
- Token refresh — Instagram access token expires in ~60 days
- Content preparation — fill Notion with posts for the next 30+ days
- Image hosting check — verify all image URLs are reachable
