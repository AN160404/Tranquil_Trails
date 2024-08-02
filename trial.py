import os
import pathlib
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import google.generativeai as genai
from hello import api_key
from gtts import gTTS
import IPython.display as ipd

# Step 1: Authenticate and configure the API
os.environ['api_key'] = api_key
if not api_key:
    raise ValueError("API key not found. Please set the environment variable 'GOOGLE_GENAI_API_KEY'.")

genai.configure(api_key=api_key)

# Step 2: Allow user to upload an image using a file dialog
Tk().withdraw()  # We don't want a full GUI, so keep the root window from appearing
image_path = askopenfilename(title="Select an image file", filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])

if not image_path:
    raise ValueError("No file selected. Please select an image file.")

# Load the image
image_data = pathlib.Path(image_path).read_bytes()

# Define the image object as required by the API
image1 = {
    'mime_type': 'image/jpeg',
    'data': image_data
}

# Define the prompt
prompt = "Guess this place and give 5-line description for this place"

# Choose a model that's appropriate for your use case.
model = genai.GenerativeModel('gemini-1.5-flash')

# Generate content (Assuming the model supports image input in this manner)
response = model.generate_content([prompt, image1])

# Extract the text from the response object
generated_text = response.text  # Adjust this if 'text' is not the correct attribute

# Print the response
print(generated_text)

# Convert the generated text to audio
tts = gTTS(text=generated_text, lang='en')
tts.save("response.mp3")

# Play the audio (Note: IPython display may not work outside of Jupyter/Colab environments)
ipd.display(ipd.Audio("response.mp3"))
