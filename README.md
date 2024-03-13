# GPT Advice

## CS50x Final Hobby Project

#### Using ChatGPT API for working with data

#### Description

It is a Python-Django web-based application designed to ask questions and receive answers using the OpenAI GPT API, working with provided text files or an entire directory.

#### Functions

First, I had to be familiar with Python and especially Django, which is significantly more complex than Flask. Django features its own unique logic and numerous built-in functionalities, such as database management and an administrative view. I created 'adviser' application to manage all functionalities related to seeking advice and ask questions from the GPT API.

- __File upload:__
A document model was created to store text file data within the database. It was all implemented with Django features, and I made the media/documents folder to store the text files. A confirmation message is displayed upon successful text file upload.

- __File select:__
Used JavaScript to enable active selection and submission of the appropriate text file via the form.

- __File delete:__
The document model and its corresponding file were removed from their specific location. Following a deletion, the page immediately refreshes.

- __Use the OpenAI GPT API with a single text file__:
An API key must be specified within 'constants.py', you can get one after registration and subscription on the OpenAI website. When you click 'Submit', it loads the text file, and after that you can query your questions to the GPT API for that single text file.

- __Use the OpenAI GPT API with an entire directory and load all text files__:
By selecting 'Load All', users can load text files from an entire directory to ask questions from the GPT API regarding all text files.

Ask questions, get answers, have fun with it! :)