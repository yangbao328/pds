# import necessary packages
import json 
import numpy as np
import pandas as pd
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
 
# Opening JSON file
f = open('search-history.json')
 
# returns JSON object as
# a dictionary
data = json.load(f)
# open text file in write mode
file1 = open("search_history.txt","w") 
print(len(data))
#extracting title from the data
for idx in range(len(data)-1):
    data_val = data[1-idx+1]
    print(data_val['title'])
    title = data_val['title']
    # write the title into the file search_history.txt
    file1.writelines(title)
# close file 1 object
file1.close()
# close f object
f.close()
# open text file in read mode
text = open("search_history.txt").read()
# generate watchcloud
wordcloud = WordCloud().generate(text)

# Display the generated image:
plt.imshow(wordcloud)
plt.axis("off")
plt.show()
