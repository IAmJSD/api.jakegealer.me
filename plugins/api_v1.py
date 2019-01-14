from flask import Blueprint, request
from models import U15EmailKeys, U15HitCounter
import boto3
from botocore.exceptions import ClientError
# Imports go here.

api_v1 = Blueprint("api_v1", __name__)
# Defines the API V1 blueprint.


@api_v1.route("/college/u15/form_email_handler", methods=["GET"])
def form_email_handler_get_not_allowed():
    """Lets user know that GET requests are not allowed."""
    return "Please do a POST request.", 400


@api_v1.route("/college/u15/form_email_handler", methods=["POST"])
def form_email_handler():
    """This parses the data from a HTTP POST form into something email-able."""
    try:
        key = request.args['key']
    except KeyError:
        return "Key not found as argument.", 400

    try:
        key_db = U15EmailKeys.get(key)
    except U15EmailKeys.DoesNotExist:
        return "Key invalid.", 400

    parsed_text = ""
    for i in request.form:
        parsed_text += f"{i}: {request.form[i]}\n"

    parsed_text = f"The following POST form arguments were present:\n\n{parsed_text}"

    ses_client = boto3.client("ses", region_name="eu-west-1")

    try:
        ses_client.send_email(
            Destination={
                "ToAddresses": [
                    key_db.email
                ]
            },
            Message={
                "Body": {
                    "Text": {
                        "Charset": "UTF-8",
                        "Data": parsed_text
                    }
                },
                "Subject": {
                    "Charset": "UTF-8",
                    "Data": "New HTTP POST form response"
                }
            },
            Source="HTTP POST Form Response <noreply@ses.jakegealer.me>"
        )
    except ClientError as e:
        return e.response['Error']['Message'], 500

    return '', 204


@api_v1.route("/college/u15/counter/<counter_id>")
def hit_counter(counter_id):
    """This function handles my webpage hit counter."""
    try:
        counter = U15HitCounter.get(counter_id)
    except U15HitCounter.DoesNotExist:
        counter = U15HitCounter(counter_id=counter_id, count=0)

    counter.count += 1
    counter.save()

    return str(counter.count), 200


def setup(server):
    server.register_blueprint(api_v1, url_prefix="/v1")
