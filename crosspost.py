import argparse
import os
import getpass

from dotenv import load_dotenv

from mastodon import Mastodon
import tweepy
from atproto import Client as BlueskyClient


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
    """
    Post to Mastodon with multiple images.
    Args:
        content (str): The text content of the post.
        images (list[str]): A list of image file paths.
    """
    mastodon = Mastodon(
        access_token=MASTODON_ACCESS_TOKEN,
        api_base_url=MASTODON_BASE_URL
    )

    media_ids = []
    if images:
        for img_path in images:
            # Upload each image and collect its media ID
            media_resp = mastodon.media_post(img_path)
            media_ids.append(media_resp['id'])

    # Post with or without media
    mastodon.status_post(content, media_ids=media_ids if media_ids else None)





def post_to_twitter(content, images=None):
    """
    Post to Twitter with multiple images.
    Args:
        content (str): The text content of the post.
        images (list[str]): A list of image file paths.
    """
    auth = tweepy.OAuth1UserHandler(
        consumer_key=TWITTER_API_KEY,
        consumer_secret=TWITTER_API_SECRET,
        access_token=TWITTER_ACCESS_TOKEN,
        access_token_secret=TWITTER_ACCESS_TOKEN_SECRET
    )
    api = tweepy.API(auth)  # For media uploads

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
        response = client.create_tweet(text=content, media_ids=media_ids, user_auth=True)
    else:
        response = client.create_tweet(text=content)





def post_to_bluesky(content, images=None):
    """
    Post to Bluesky with multiple images.
    Args:
        content (str): The text content of the post.
        images (list[str]): A list of image file paths.
    """
    # Initialize the client
    client = BlueskyClient()
    
    # Prompt for the password
    bluesky_password = getpass.getpass(prompt=f"Bluesky {BLUESKY_HANDLE} password: ")
    client.login(BLUESKY_HANDLE, bluesky_password)

    if images:
        # Build the embed with each image
        images_list = []
        for img_path in images:
            with open(img_path, "rb") as img_file:
                img_data = img_file.read()
            blob = client.upload_blob(img_data)
            images_list.append({
                "image": blob.blob,
                "alt": ""  # Optional alt text
            })

        embed = {
            "$type": "app.bsky.embed.images",
            "images": images_list
        }
        client.post(content, embed=embed)
    else:
        # Post text-only
        client.post(content)





def main():
    parser = argparse.ArgumentParser(description="Post content and optional images to multiple platforms.")

    parser.add_argument(
        "text_file",
        type=str,
        help="Path to the .txt file containing the post content."
    )
    parser.add_argument(
        "--images",
        type=str,
        nargs="*",
        help="Paths to the image files. You can provide multiple image paths.",
        default=[]
    )

    args = parser.parse_args()

    # Read content from .txt file
    if not os.path.exists(args.text_file):
        print("The specified text file does not exist.")
        return

    with open(args.text_file, "r") as file:
        content = file.read().strip()

    # Validate image paths
    invalid_images = [image for image in args.images if not os.path.exists(image)]
    if invalid_images:
        print(f"The following image files do not exist: {', '.join(invalid_images)}")
        return

    # Post to all platforms
    print("Posting to Mastodon...")
    post_to_mastodon(content, args.images)

    print("Posting to Twitter...")
    post_to_twitter(content, args.images)

    print("Posting to Bluesky...")
    post_to_bluesky(content, args.images)

    print("Post successfully published to all platforms!")


if __name__ == "__main__":
    main()
