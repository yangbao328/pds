# jojobot alpha
### an attempt at shortform text generation using OpenAI's GPT-2

## Directory Contents
- `textcleaning.py`: Contains the transformations performed to convert text message data from XML to a standardized Dataframe
- `keepnotecleaning.py`: Contains the transformations performed to convert a folder of seperate .json files containing note information into a standardized Dataframe
- `tweetcleaning.py`: Contains the transformations performed to convert a text representation of tweets into a standardized Dataframe
- `text-analysis.ipynb`: Visualizations and large-transformations on entire corpus
- `Run_2_training_and_generation.ipynb`: Creation of Model 2 with gpt-2-simple
- `model1-sample-output`: A collection of a few samplings from the first model
- `model2-sample-output`: A collection of a few samplings from the second model
## Overview
In this part of the project, I extracted a bunch of personal text data and used that as a finetuning corpus to train
the 124M model of the [GPT-2 language model](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf).
My goal for this project was to create an implementation that could create shortform bodies of texts, e.g.
tweets or little witty quips / jokes, in a style similar to that of my own use of language.

## Data Sources & Cleaning Processes
Final corpus (590kb) was composed of the following:
- 9394 sent texts, from 2020-12-30 to 2021-11-16
    - Obtained in .xml format from SMS Backup and Restore App
- 1203 notes stored in Google Keep, from 2018-03-16 to 2021-11-07
    - Obtained in individual .json files requesting data from Google Takeout
- 878 tweets, from 2018-09-29 to 2021-11-27
    - Originally obtained in .json format from requesting data from twitter
    - After realizing there was no extra metadata I found important, resulted to using third party app (AllMyTweets)

Data transformation and cleaning performed on sources included:
- Removing all unnecessary metadata columns, and only preserving message body, date created / sent, 
  and time created / sent
- Removing all items in data that weren't created by myself - for example, my downloaded texts included text messages 
  received, and my tweets included retweets
- After first training session, performed regex matching to remove urls
- Various trimming of whitespace

Once data was cleaned and stored in a Pandas Dataframe, I wrote all of it to a text file, with each
individual message separated by carriage returns; this was the text file I used to finetune the GPT-2 model.

Out of interest of my own personal privacy, I will not be uploading the final corpus or any of the files
containing the contents that ended up forming it; I have however uploaded the .py files that the data transformation
was performed via.
## Model Training
I used Max Woolf's Google Colab page, ["Train a GPT-2 Text Generating Model w/ GPU For Free"](https://colab.research.google.com/github/sarthakmalik/GPT2.Training.Google.Colaboratory/blob/master/Train_a_GPT_2_Text_Generating_Model_w_GPU.ipynb),
as the basis for the training of the model. This included details about packet managemet, syntax, and performance
considerations for training the model.  

So far I've made two models, both trained using the 124M GPT-2 model; I am computationally limited by the restrictions
of Google Colab Free as well as the capabilities of my personal computer, which prevented me from training
with a larger model.  

Model 1 was trained on my original corpus (not as cleaned, included URLs, 169,248 tokens), and was finetuned over 1000 steps;
This took approximately 75 minutes on a Tesla K80 GPU, with the following loss metrics (sampled every 200 steps for brevity).  
**Loss Metrics:** 
```
[200 | 865.37] loss=2.13 avg=2.90  
[400 | 1744.48] loss=0.78 avg=2.05  
[600 | 2628.43] loss=0.15 avg=1.38  
[800 | 3510.70] loss=0.07 avg=0.96
[1000 | 4392.96] loss=0.07 avg=0.71
```
At this point, I noticed a couple of problems with Model 1; I had overfitted my training data, resulting in
a bunch of repeated, largely nonsensical phrases by the end of training; I remedied this in the next step by
greatly reducing the number of training steps. Additionally, I noticed this model would often create nonsense urls
(usually to twitter images or spotify playlists that didn't exist); this was remedied through regex matching urls
and replacing them with empty space, and then removing any entries in the dataframe that were empty / entirely whitespace.

Model 2 used this updated corpus (163,163 tokens), and training consisted of only 400 steps (30 minutes on a Tesla K80 GPU). 
I had better results with this; I may have underfitted the finetuning data (shown by loss metrics), but I found that this was a compromise that I was happy with,
as it allowed the original model's "understanding" of the English language to subsidize what was lacking in the small finetuning corpus.  
**Loss Metrics:**
```
[80 | 341.77] loss=3.39 avg=3.56
[160 | 700.17] loss=2.61 avg=3.18
[240 | 1060.18] loss=1.71 avg=2.78
[320 | 1416.63] loss=0.95 avg=2.39
[400 | 1753.50] loss=0.92 avg=2.03
```
In this model, I found the URL problem was better, but there were still a few performance problems; namely, long stretches
where the model would just repeat text, and directly copying phrases from the corpus. There was also some
maintaining of context between lines, which isn't something that I was interested in; I believe this just comes down to the way that the source
text was organized, as I finetuned the model on chronologically ordered texts, in which multiple entries can be used
to compose an entire thought, or refer to context previously in the conversation. Easy changes I could make to potentially change
this include randomly shuffling the order of the corpus around.

Once again, in the interests of my personal privacy, I won't be uploading either of the models or their weights;
I will, however, include raw sampled texts from both models, with any hugely identifying information (phone numbers,
addresses) visibly redacted.

## Future Steps
I believe the best things I could do for improved performance from jojobot would be to increase the corpus size,
train using a larger model, and try different formats for the training data; GPT-2 was trained on WebText, which is a dataset
largely consisting of longer-form texts such as articles, and as such is more successful producing longer texts.
In the paper about GPT-2 linked above, the language models are used to solve problems over a variety of domains,
just by transforming the input that it is supposed to append to; I believe this is worth taking some time to test with
and see how finetuned models would perform differently in these scenarios as opposed to the original pre-trained model.