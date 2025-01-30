# Social Media Cross Posting Script

A Python script that allows you to post a text message (from a `.json` file) and one or more images to Mastodon, Twitter, and Bluesky with a single command. Mentions and hashtags are formatted correctly on each platform.

## Table of Contents
- [Features](#features)
- [Setup](#setup)
  - [Clone & Install Requirements](#clone--install-requirements)
  - [Environment Variables](#environment-variables)
- [Usage](#usage)
  - [Basic Command](#basic-command)
  - [Adding Images](#adding-images)
  - [Selecting Platforms](#selecting-platforms)
- [JSON Input Format](#json-input-format)
- [Examples](#examples)
- [License](#license)

## Features
- Post text and images to **Mastodon, Twitter, and Bluesky**.
- Supports **mentions and hashtags** for each platform.
- Uses **command-line arguments** to choose platforms dynamically.

## Setup

### Clone & Install Requirements
1. **Clone** the repository (or download the script file).
2. **Install dependencies**:
   ```bash
   pip install mastodon.py tweepy atproto python-dotenv
   ```

### Environment Variables

Create a `.env` file in the same directory and set the following variables:

```ini
# Mastodon
MASTODON_BASE_URL=https://mastodon.example
MASTODON_ACCESS_TOKEN=YOUR_MASTODON_ACCESS_TOKEN

# Twitter
TWITTER_API_KEY=YOUR_TWITTER_API_KEY
TWITTER_API_SECRET=YOUR_TWITTER_API_SECRET
TWITTER_ACCESS_TOKEN=YOUR_TWITTER_ACCESS_TOKEN
TWITTER_ACCESS_TOKEN_SECRET=YOUR_TWITTER_ACCESS_TOKEN_SECRET
TWITTER_BEARER_TOKEN=YOUR_TWITTER_BEARER_TOKEN

# Bluesky
BLUESKY_HANDLE=@username.bsky.social
```

> **Note**:  
> - Obtain Mastodon tokens by creating a new application in your Mastodon server’s settings.  
> - Obtain Twitter API credentials from [developer.x.com](https://developer.twitter.com/).  
> - For Bluesky, you’ll need a handle (e.g., `@username.bsky.social`) and password.

---

## Usage

From the command line, run:
```bash
python crosspost.py <json_file> [--images <image1> <image2> ...] [--all | --twitter | --mastodon | --bluesky]
```

### Basic Command
- **Positional Argument**: `<json_file>` is the path to the `.json` file containing the text of your post and mentions.
- **Optional Argument**: `--images` can be followed by one or more image paths.
- **Platform Selection**: Use flags to choose which platforms to post to.

### Adding Images
You can attach multiple images by providing them after `--images`. For example:
```bash
python crosspost.py my_post.json --images image1.jpg image2.jpg
```

### Selecting Platforms
Use one of the following flags to post to specific platforms:
- `--all`: Post to **all** platforms.
- `--twitter`: Post **only** to Twitter.
- `--mastodon`: Post **only** to Mastodon.
- `--bluesky`: Post **only** to Bluesky.

> **If no platform is specified, the script will skip posting.**

---

## JSON Input Format

Your post content should be stored in a `.json` file in the following format:

```json
{
    "post": "This is my post content! #my_hashtag_1 #my_hashtag_2",
    "mastodon_mentions": "@mastodon_mention_1 @mastodon_mention_2",
    "twitter_mentions": "@twitter_mention_1 @twitter_mention_2",
    "bluesky_mentions": "@mention_1.bsky.social @mention_2.bsky.social"
}
```

- The `post` field contains the common text for all platforms.
- The `mastodon_mentions`, `twitter_mentions`, and `bluesky_mentions` fields append platform-specific mentions and hashtags.

---

## Examples

### Post to all platforms
```bash
python crosspost.py my_post.json --all
```

### Post only to Mastodon
```bash
python crosspost.py my_post.json --mastodon
```

### Post with images to Twitter and Bluesky
```bash
python crosspost.py my_post.json --twitter --bluesky --images pic1.jpg pic2.png
```

## License

This project is released under the [MIT License](https://opensource.org/licenses/MIT). Feel free to modify and distribute as you see fit.

---

**Enjoy posting to multiple platforms with a single command!**