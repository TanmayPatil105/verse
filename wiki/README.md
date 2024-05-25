# How do I obtain API tokens?

## Spotify
- Go to your [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
- Create an App.
- Fill out the name and description and click create.
- Click `Show Client Secret`.


We have our Client ID and Client Secret.\
We'll need them to generate the Refresh token.


1. Authorize with [scopes](https://developer.spotify.com/documentation/web-api/concepts/authorization#list-of-scopes) and retrieve code parameter

After running the following bash script in your terminal, you'll be redirected to a url `http://localhost:3000/callback?code=O3rnwd...9Ajd` \
Extract the code parameter from it, we'll need it!

```bash
#!/bin/bash
CLIENT_ID=<client_id>

xdg-open "https://accounts.spotify.com/authorize?client_id=${CLIENT_ID}&response_type=code&redirect_uri=http%3A%2F%2Flocalhost:3000&scope=user-read-currently-playing"
```


2. Encode <client_id:client_secret> using base64 encoding

```bash
#!/bin/bash

CLIENT_ID=<client_id>
CLIENT_SECRET=<client_secret>
printf "${CLIENT_ID}:${CLIENT_SECRET}" | base64
```
3. Retrieve refresh token

```bash
#!/bin/bash

CODE=<code parameter>
BASE64=<base64 encoded client_id:client_secret> 

curl -H "Authorization: Basic ${BASE64}" -d grant_type=authorization_code -d code=${CODE} -d redirect_uri=http%3A%2F%2Flocalhost:3000 https://accounts.spotify.com/api/token

```
We will recieve a `JSON` object. Extract `refresh_token` from it.

Now, we have our Spotify `Client ID`, `Client SECRET` and `Refresh Token`

## Genius

- Visit [Genius.com](https://genius.com/api-clients/new) and login
- Enter App name, Website URL and then press `Save`
- Press the `Generate Access Token` to get your GENIUS Token

