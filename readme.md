1. Install required packages by entering the following into a terminal pointed at this directory:
`pip install -r requirements.txt`
2. Run the server by running the following command in a python environment with the previously installed packages:
`python app.py`
3. As the CLI starts up your application, it will output two addresses. One which is accesssible only on your own computer, and another which can be reached from other devices on your LAN (this is the address you'll have to enter into your phone's browser if that is the way you want to do it).

Now you can either quiz yourself from your desk, or any couch in your house from your phone! If you'd like to add other quizes to answer, simply add the JSON file into the same directory as ExampleQuestions.json is kept. Be sure that the questions all follow the same structure as the given demo file. 
I have found that it's extremely easy to make study materials this way by tossing a study-guide's worth of example questions from anywhere to ChatGPT, and having it format the question into the JSON we're looking for; in case you do this, you don't need Ids for each question right off the bat you can instead just run addIdsToQuestions.py with the right .json filename edited into the script on line 4.

Happy studying!