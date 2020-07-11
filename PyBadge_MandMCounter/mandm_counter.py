"""To make predictions using Azure Custom Vision, you will need to create a Custom Vision project
and train it using different images.

You will need to have an Azure subscription to use Custom Vision, and you can use a free tier of
this service.

If you don't have an Azure subscription:

If you are a student, head to https://aka.ms/FreeStudentAzure and sign up, validating with your
 student email address. This will give you $100 of Azure credit and free tiers of a load of
 service, renewable each year you are a student

If you are not a student, head to https://aka.ms/FreeAz and sign up to get $200 of credit for 30
 days, as well as free tiers of a load of services

Once you have an Azure subscription, head to https://customvision.ai and create a project.
You can train two types of models - an image classifier that will give a prediction if an image is an object,
or an object detector that can find multiple objects in an image.

To train an image classifier, follow these instructions: https://aka.ms/AA88qph
To train an object detector, follow these instructions: https://aka.ms/AA88llc

Once you have your model trained, publish an iteration of it
you will need your Prediction key, endpoint, project id and published iteration name
Add these to your secrets.py file as prediction_key, endpoint, project_id, published_name
"""
from azurecustomvision_prediction import CustomVisionPredictionClient
from secrets import secrets

class MAndMCounter:
    def __init__(self):
        # Create a custom vision predition client using the key and endpoint from the secrets file
        self._client = CustomVisionPredictionClient(secrets["prediction_key"], secrets["endpoint"])
    
    def count_mandms(self, buffer: bytearray) -> int:
        print("Counting M&Ms")
        image_prediction = None

        # Add a retry loop in case of network issues
        while image_prediction is None:
            retry = 0
            try:
                # Detect objects in the image
                image_prediction = self._client.detect_image(secrets["project_id"], secrets["published_name"], buffer)
            except Exception as err:
                print(err)
                retry += 1
                if retry > 10:
                    print("Failed after 10 attempts, dropping out")
                    return -1

        # All possible objects are found, including ones with a very low possibility of being M&Ms
        # So filter out everything with a probability of less than 75%
        probable_mandms = list(filter(lambda x: x.probability > 0.75, image_prediction.predictions))

        # Count the M&Ms found with a probability > 75%
        found_count = len(probable_mandms)

        # Print the M&Ms
        print("Found", found_count, "M&Ms")

        for prediction in probable_mandms:
            print(
                "Prediction",
                prediction.tag_name,
                "with probability",
                str(int(prediction.probability * 100)),
                "%",
                "at box",
                str(prediction.bounding_box),
            )

        # Return the number of M&Ms found
        return found_count