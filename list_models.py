from google import genai

client = genai.Client(api_key="AIzaSyCjaxakn-46O3QSwuwNDg7AWBZpGvw6Ka4")

for model in client.models.list():
    print(model.name)