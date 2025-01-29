# Media Cross Posting Script

A Python script that allows you to post a text message (from a `.txt` file) and one or more images to Mastodon, Twitter, and Bluesky with a single command.

## Table of Contents
- [Features](#features)
- [Setup](#setup)
  - [Clone & Install Requirements](#clone--install-requirements)
  - [Environment Variables](#environment-variables)
- [Usage](#usage)
  - [Basic Command](#basic-command)
  - [Adding Images](#adding-images)
- [Examples](#examples)
- [License](#license)


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
BLUESKY_HANDLE=username.bsky.social
```

> **Note**:  
> - Obtain Mastodon tokens by creating a new application in your Mastodon server’s settings.  
> - Obtain Twitter API credentials from [developer.twitter.com](https://developer.twitter.com/).  
> - For Bluesky, you’ll need a handle (e.g., `username.bsky.social`) and password.

---

## Usage

From the command line, run:
```bash
python crosspost.py <text_file> [--images <image1> <image2> ...]
```

### Basic Command
- **Positional Argument**: `<text_file>` is the path to the `.txt` file containing the text of your post.
- **Optional Argument**: `--images` can be followed by one or more image paths.

### Adding Images
You can attach multiple images by providing them after `--images`. For example:
```bash
python crosspost.py my_post.txt --images image1.jpg image2.jpg
```

## License

This project is released under the [MIT License](https://opensource.org/licenses/MIT). Feel free to modify and distribute as you see fit.

---

**Enjoy posting to multiple platforms with a single command!**