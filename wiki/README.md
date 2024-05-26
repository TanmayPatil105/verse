# How do I obtain API tokens?

## Spotify
- Go to your [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
- Create an App.
- Fill out the `name` and `description`, and set the `redirect URI` to `http://localhost:3000`. Click `create`.
- Under `Settings`, Click `Show Client Secret`.


We now have our `CLIENT_ID` and `CLIENT_SECRET`.\
We'll need them to generate the Refresh token.

### Generate Refresh token
```bash
git clone https://github.com/TanmayPatil105/verse
cd verse/wiki

# install dependencies
pip install -r requirements.txt
```

Update your `CLIENT_ID` and `CLIENT_SECRET` in `.env` file.
```bash
python3 main.py
# refresh token is saved in '.cache' file

cat .cache # Extract `refresh_token` from it.
```

Now, we have our Spotify `Client ID`, `Client SECRET` and `Refresh Token`

## Genius

- Visit [Genius.com](https://genius.com/api-clients/new) and login
- Enter App name, Website URL and then press `Save`
- Press the `Generate Access Token` to get your GENIUS Token

