# TDGA Global Leaderboard setup

This folder contains the Google Apps Script backend for the Tiny Disc Golf global leaderboard.

## What it does

- New player submissions are written to a private `Submissions` sheet with status `PENDING`.
- The public leaderboard endpoint returns **only** rows whose status is `APPROVED`.
- You control approval by changing the Status cell in Google Sheets to `APPROVED` or `REJECTED`.
- Approved rankings are sorted highest to lowest.

## One-time setup you must do in your Google account

1. Create a blank Google Sheet named **TDGA Global Leaderboard**.
2. In the sheet, choose **Extensions → Apps Script**.
3. Open `Code.gs` in this folder on GitHub and copy its full contents into the Apps Script editor, replacing the starter code.
4. Save. In the function dropdown, select `setupLeaderboard` and press **Run**. Follow Google's authorization prompts. This creates the `Submissions` tab and its columns.
5. Choose **Deploy → New deployment → Web app**.
6. Set **Execute as** to **Me** and **Who has access** to **Anyone**, then deploy and approve the authorization prompt.
7. Copy the deployed web app URL ending in `/exec`. Keep the Google Sheet itself private; do not share editor access publicly.
8. Send that `/exec` URL to the app maintainer so the Tiny Disc Golf front end can be connected.

## Approving a player

Open the private `Submissions` tab. Review the name and ranking, then change Status from `PENDING` to `APPROVED`. Only then will the player appear on the public leaderboard. Change it to `REJECTED` to keep it off the leaderboard.

## Important notes

- This backend does not create a Google Sheet inside your account automatically; you must create the sheet and deploy the script because only you can authorize it in your Google account.
- Treat the `/exec` URL as the app's public endpoint. Anyone can submit a proposed entry, but pending entries are not public until you approve them.
- The leaderboard's numeric ranking is currently sorted **highest number first**. Confirm that matches your intended TDGA Ranking rules before launch.
- This is a lightweight community leaderboard. Approval moderates public entries but does not verify a player's identity or independently validate their ranking.
