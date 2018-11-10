columns = ['user_id', 'user_created_at', 'user_verified', 'user_name', 'user_screen_name', 'user_lang', 'user_location', 'user_url', 'user_likes_count', 'user_tweets_count', 'user_followers_count', 'user_friends_count', 'user_descriptions', 'user_following', 'user_listed_count', 'user_default_profile_image', 'user_default_profile', 'user_profile_bg_color', 'user_profile_image_url', 'user_time_zone', 'user_utc_offset', 'status_id', 'status_created_at', 'status_lang', 'status_text', 'status_favorite_count', 'status_retweeted', 'status_source', 'status_favorited', 'status_retweet_count', 'status_place', 'status_coordinates', 'status_geo_enabled', 'status_geo', 'hashtags', 'mentions']

statuses = []
tweet_count = 0

for status in Cursor(api.user_timeline, id='teammovewith').items():
    hashtags = []
    mentions = []
    tweet_count += 1
    print("---------")
    if tweet_count == 5: break
    if hasattr(status, "entities"):
        entities = status.entities
        if "hashtags" in entities:
            for ent in entities["hashtags"]:
                if ent is not None and "text" in ent:
                    hashtag = ent["text"]
                    if hashtag is not None:
                        hashtags.append(hashtag)
        if "user_mentions" in entities:
            for ent in entities["user_mentions"]:
                if ent is not None:
                    if "screen_name" in ent:
                        name = ent["screen_name"]
                        if name is not None:
                            mentions.append(name)
    status = (status.user.id,
         status.user.created_at,
         status.user.verified,
         status.user.name,
         status.user.screen_name,
         status.user.lang,
         status.user.location,
         status.user.url,
         status.user.favourites_count,
         status.user.statuses_count,
        status.user.followers_count,
        status.user.friends_count,
        status.user.description,
        status.user.following,
        status.user.listed_count,
        status.user.default_profile_image,
        status.user.default_profile,
        status.user.profile_background_color,
        status.user.profile_image_url,
        status.user.time_zone,
        status.user.utc_offset,
        status.id,
        status.created_at,
        status.lang,
        status.text,
        status.favorite_count,
        status.retweeted,
        status.source,
        status.favorited,
        status.retweet_count,
        status.place,
        status.coordinates,
        status.user.geo_enabled,
        status.geo, 
        hashtags,
        mentions)
    statuses.append(status)

st = pd.DataFrame(statuses, columns=columns)
st.to_csv('status.csv', index=False)
