import argparse
import os
import json
import getpass
import re

from dotenv import load_dotenv

from mastodon import Mastodon
import tweepy
from atproto import Client as BlueskyClient
from atproto_client.exceptions import UnauthorizedError
from atproto_client.utils.text_builder import TextBuilder


load_dotenv()


# Setup credentials for each platform
# These should be stored securely, e.g., in environment variables or a secrets manager

# A générer sur Mastodon -> Préférences -> Développement -> Nouvelle application
MASTODON_BASE_URL = os.getenv("MASTODON_BASE_URL")
MASTODON_ACCESS_TOKEN = os.getenv("MASTODON_ACCESS_TOKEN")

# A générer sur https://developer.x.com
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

# le tag du compte sur bluesky : @username.bsky.social
BLUESKY_HANDLE = os.getenv("BLUESKY_HANDLE")





def post_to_mastodon(content, images=None):
    mastodon = Mastodon(
        access_token=MASTODON_ACCESS_TOKEN,
        api_base_url=MASTODON_BASE_URL
    )

    try:
        media_ids = []
        if images:
            for img_path in images:
                media_resp = mastodon.media_post(img_path)
                media_ids.append(media_resp['id'])

        mastodon.status_post(content, media_ids=media_ids if media_ids else None)
        print(" > Mastodon post done")
        return True

    except Exception as e:
        print(f" > An error occurred while posting to Mastodon: {e}")
        print(" > Skipping Mastodon post...")
        return False





def post_to_twitter(content, images=None):
    auth = tweepy.OAuth1UserHandler(
        consumer_key=TWITTER_API_KEY,
        consumer_secret=TWITTER_API_SECRET,
        access_token=TWITTER_ACCESS_TOKEN,
        access_token_secret=TWITTER_ACCESS_TOKEN_SECRET
    )
    api = tweepy.API(auth)

    client = tweepy.Client(
        bearer_token=TWITTER_BEARER_TOKEN,
        consumer_key=TWITTER_API_KEY,
        consumer_secret=TWITTER_API_SECRET,
        access_token=TWITTER_ACCESS_TOKEN,
        access_token_secret=TWITTER_ACCESS_TOKEN_SECRET
    )

    media_ids = []
    if images:
        for img_path in images:
            media = api.media_upload(img_path)
            media_ids.append(media.media_id)

    try:
        if media_ids:
            client.create_tweet(text=content, media_ids=media_ids, user_auth=True)
        else:
            client.create_tweet(text=content)
        print(" > Twitter post done")
        return True

    except Exception as e:
        print(f" > An error occurred while posting to Twitter: {e}")
        print(" > Twitter post skipped")
        return False







def resolve_did(client, handle):
    """ Resolve a Bluesky handle (e.g., lucas-schott.bsky.social) to its DID """
    clean_handle = handle.lstrip('@').strip().lower()  # Remove '@' and ensure lowercase

    try:
        response = client.com.atproto.identity.resolve_handle({"handle": clean_handle})
        did = getattr(response, "did", None)  # Safely get the 'did' attribute

        if did:
            return did
        else:
            print(f" > DID lookup returned empty for {handle}")
            return None  # Skip mention if DID not found

    except Exception as e:  # Catch all errors
        print(f" > Could not resolve DID for {handle}: {e}")
        return None  # Skip the mention if resolution fails


def create_text_builder(client, text):
    """ Build rich text with mentions and hashtags using TextBuilder """
    text_builder = TextBuilder()
    
    # Track last processed position in text
    last_pos = 0  

    # Process mentions (@username.bsky.social) and hashtags (#hashtag)
    for match in re.finditer(r'(@[a-zA-Z0-9_.-]+\.bsky\.social|#[a-zA-Z0-9_]+)', text):
        start, end = match.span()
        matched_text = match.group(0)

        # Add any text before the match
        text_builder.text(text[last_pos:start])

        if matched_text.startswith("@"):  # Handle mentions
            handle = matched_text
            did = resolve_did(client, handle)
            if did:
                text_builder.mention(handle, did)  # Add clickable mention
            else:
                text_builder.text(handle)  # Add as plain text if DID lookup fails
        elif matched_text.startswith("#"):  # Handle hashtags
            tag_text = matched_text
            text_builder.tag(tag_text, tag_text.lstrip("#"))  # Add clickable hashtag

        last_pos = end  # Update last processed position

    # Add any remaining text after the last mention/hashtag
    text_builder.text(text[last_pos:])

    return text_builder


def post_to_bluesky(content, images=None):
    """
    Post to Bluesky with multiple images.
    """
    client = BlueskyClient()
    
    max_attempts = 3
    attempt = 0
    success = False

    while attempt < max_attempts and not success:
        bluesky_password = getpass.getpass(prompt=f"Bluesky {BLUESKY_HANDLE} password: ")

        try:
            client.login(BLUESKY_HANDLE, bluesky_password)
            success = True  # Login successful

        except UnauthorizedError:
            print(" > Invalid credentials. Please try again.")
            attempt += 1

    if not success:
        print(" > Too many failed attempts. Skipping Bluesky post...")
        return False  # Exit function if login fails after retries

    # Proceed with posting
    try:

        if images:
            images_list = []
            for img_path in images:
                with open(img_path, "rb") as img_file:
                    img_data = img_file.read()
                blob = client.upload_blob(img_data)
                images_list.append({
                    "image": blob.blob,
                    "alt": ""
                })

            embed = {
                "$type": "app.bsky.embed.images",
                "images": images_list
            }

        text_builder = create_text_builder(client, content)
        client.post(text_builder, embed=embed if images else None)

        print(" > BlueSky post done")
        return True

    except Exception as e:
        print(f" > An error occurred while posting to BlueSky: {e}")
        print(" > Skipping BlueSky post...")
        return False








def main():
    parser = argparse.ArgumentParser(description="Post content and optional images to multiple platforms.")

    parser.add_argument("json_file", type=str, help="Path to the .json file containing the post content and mentions.")
    parser.add_argument("--images", type=str, nargs="*", help="Paths to the image files.", default=[])
    parser.add_argument("--all", action="store_true", help="Post to all platforms.")
    parser.add_argument("--twitter", action="store_true", help="Post to Twitter.")
    parser.add_argument("--mastodon", action="store_true", help="Post to Mastodon.")
    parser.add_argument("--bluesky", action="store_true", help="Post to Bluesky.")

    args = parser.parse_args()

    if not (args.all or args.twitter or args.mastodon or args.bluesky):
        print("No platforms specified. Skipping post.")
        return

    with open(args.json_file, "r") as file:
        data = json.load(file)

    base_post = data.get("post", "").strip()
    mastodon_post = f"{base_post}\n{data.get('mastodon_mentions', '').strip()}".strip()
    twitter_post = f"{base_post}\n{data.get('twitter_mentions', '').strip()}".strip()
    bluesky_post = f"{base_post}\n{data.get('bluesky_mentions', '').strip()}".strip()

    if args.all or args.mastodon:
        print(" > Posting to Mastodon...")
        post_to_mastodon(mastodon_post, args.images)

    if args.all or args.twitter:
        print(" > Posting to Twitter...")
        post_to_twitter(twitter_post, args.images)

    if args.all or args.bluesky:
        print(" > Posting to Bluesky...")
        post_to_bluesky(bluesky_post, args.images)



if __name__ == "__main__":
    main()
