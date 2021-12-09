# import necessary packages
import json
import numpy as np
import pandas as pd
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
import re
 
# Opening JSON file
f = open('watch-history.json',encoding="utf8")
 
# returns JSON object as
# a dictionary
data = json.load(f)
# open text file in write mode
file1 = open("watch_history.txt","w")
print(len(data))
for idx in range(1500):
    print(idx)
    data_val = data[1-idx+1]
    print(data_val['title'])
    title = data_val['title']
    pattern = re.compile('\W+')
    new_title = re.sub(pattern, '', title)
    new_title = [idx for idx in new_title if not re.findall("[^\u0000-\u05C0\u2100-\u214F]+", idx)]
    # write the title into the file search_history.txt
    file1.writelines(new_title)
    file1.writelines("\n")
# close file 1 object
file1.close()
# close f object
f.close()

# open text file in read mode
text = open("watch_history.txt").read()

# generate watchcloud
wordcloud = WordCloud().generate(text)

# Display the generated image:
plt.imshow(wordcloud)
plt.axis("off")
plt.show()
