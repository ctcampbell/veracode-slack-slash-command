# veracode-slack-slash-command

Two AWS Lambda functions, that enable something like:

    /veracode list apps
    /veracode list builds <app_id>
    /veracode get build <build_id>

in Slack.

# Install

    git clone https://github.com/ctcampbell/veracode-slack-slash-command.git
    cd veracode-slack-slash-command/veracodeslackslashcommand
    pip install -r requirements.txt -t ./
    
The folders each contain an AWS lambda function that requires a `SLACK_TOKEN` env variable configured. The dispatcher lambda must have permission to invoke other lambda functions. The main lambda must also have `VID` and `VKEY` env variables configured.

Lambda timeout for the dispatcher should be 1 min, and for the main lambda 5 min.

The dispatcher should be configured as open accessible via the AWS API gateway. The main lambda is only called from the dispatcher so does not need a trigger.

The AWS API gateway URL should be added to Slack under a custom app in the slash command config.
