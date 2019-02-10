# Walking Notifications

This is a simple script that's meant to be setup to run via cron or something similar to send walking notifications to your team's slack channel.

Example Slack message: @channel It's freezing, maybe we should all skip the walk this time. It's currently 37°F (feels like 32°F) and cloudy.

## Setup

1. Setup your API keys.
    * Go to the [Yahoo Developer Network](https://developer.yahoo.com/apps/) and click the "Create an App" button.
    * Go to the [Slack API](https://api.slack.com/apps) website.
        - Create a new app
        - Click bots under "Add features and functionality" and then click "Add Bot User"
        - On the left navigation click "Install App" and then click "Install App to Workspace"
        - The token you'll use is the "Bot User OAuth Access Token"
        - Make sure you invite your bot to the channel you'll be using.
        
2. Install [direnv](https://direnv.net/).
3. Put the following in your .envrc file.

        export YAHOO_CLIENT_KEY=********************
        export YAHOO_CLIENT_SECRET=********************
        export SLACK_API_TOKEN=xoxb-********************
        export PYTHON_CMD_PREFIX='docker run -it -v `pwd`:/code walking_notification:latest'

4. Run direnv allow
5. Run `make build`

## Running the script

    $ make run_bash
    # For a dry run with out sending the notification to Slack
    $ ./walking-notification.py -n --location=66502
    # To send the notification to Slack
    $ ./walking-notification.py --location=66502
    
## To run tests

    $ make run_bash
    $ py.test
