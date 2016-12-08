import os
import time
import rauth
from slackclient import SlackClient

#BOT_ID = os.environ.get("BOT_ID")

BOT_ID="U3A35V4TZ"


# constants
AT_BOT = "<@" + BOT_ID + ">"
SLACK_BOT_TOKEN = "xoxb-112107990951-opwJsVkKVaTCyGMaYtRIJ0RH"

slack_client = SlackClient(SLACK_BOT_TOKEN)


def handle_command(command, channel):
    response = "Not sure what you mean. Use the \"help\" command for more information regarding the format for YelpBot commands."
    if command.startswith("find ") and command.find(" near ") != -1:
        term = command.split("find ")[1].split()[0]
        while True:
                if command.endswith(term) == False and command.split(term)[1].split()[0] != "near" and command.split(term)[1].split()[0] != "phone" and command.split(term)[1].split()[0] != "address" and command.split(term)[1].split()[0] != "url" and command.split(term)[1].split()[0] != "rating" and command.split(term)[1].split()[0] != "display":
                        term = term + " " + command.split(term)[1].split()[0]
                else:
                        break
        location = command.split("near ")[1].split()[0]
        while True:
                if command.endswith(location) == False and command.split(location)[1].split()[0] != "near" and command.split(location)[1].split()[0] != "phone" and command.split(location)[1].split()[0] != "address" and command.split(location)[1].split()[0] != "url" and command.split(location)[1].split()[0] != "rating" and command.split(location)[1].split()[0] != "display":
                        location = location + " " + command.split(location)[1].split()[0]
                else:
                        break

        params = {
                'term': term,
                'location': location
        }
        queryResults = get_results(params)
        response = ""
        if 'error' in queryResults:
                response = "There were no results to return."
        else:
                for item in queryResults['businesses']:
                        response += item['name'] + "\n"
                        if "phone" in command:
                                if item.get('phone'):
                                        response += "Phone: " + item['phone'] + "\n"
                        if "address" in command:
                                if item.get('address'):
                                        response += "Address: " + item['display_address'] + "\n"
                        if "url" in command:
                                if item.get('url'):
                                        response += "Yelp URL: " + item['url'] + "\n"
                        if "rating" in command:
                                if item.get('rating'):
                                        response += "Rating: " + str(item['rating']) + "/5.0 \n"
                        response += "\n"
                if queryResults['total'] == 0:
                        response = "There were no results to return."
    elif command.startswith("help"):
        response = "Use the format: \"find <item/business> near <location> You can additionally add \"display (phone)(address)(url)(rating)\" on the end of your command for the corresponding information to be added if available."
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None

def get_results(params):
        consumer_key = "daeoNp6cLVDr2U3Hqkp2hQ"
        consumer_secret = "GO4KMlI9fappdqMWkpUdIr3X3wg"
        token =  "rYzrdQGYsA_tuRyC8g92u9bKhKeVDRuV"
        token_secret = "FUbqr2SOGz-tKQd5c6QUQdg4ZhI"

        session = rauth.OAuth1Session(
                consumer_key = consumer_key,
                consumer_secret = consumer_secret,
                access_token = token,
                access_token_secret = token_secret)

        request = session.get("http://api.yelp.com/v2/search",params=params)

        data = request.json()
        session.close()

        return data


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
