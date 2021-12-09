"""
DS2500 Final Project
Tianyang Bao 
001467761
"""
'''
In this section, I will analyze personal banking statements from July 2021 to Nov 2021
I want to emulate traveling trace based on these records
-most visit stores
-potentially living circle in geographic coordinates in Boston Area
Ultimately to indicate that losing a credit card may result in larger potention data leakage 
that may become uncontrolable.
'''

import pandas as pd
import fileinput
import glob

#Feed in 5 months Bank Statements
#in this case, I'm using a BOA credit card
#Retrieved these statements from BOA online banking

#%% Segerating this section as only need to concatenate all files once
#read names of file in the glob list
def compile_stats(name):
    
    file_list = glob.glob("*.csv")
    #create a new csv file for output
    with open('bkfiles.csv', 'w') as file:
        #open each file and read lines
        input_lines = fileinput.input(file_list)
        #write lines into the output csv
        file.writelines(input_lines)
    return name     
#%%



#read the merged bank statements
bk_tr = pd.read_csv('train_bk_cat.csv')

bk_tr['sent_len'] = bk_tr.Payee.apply(len)
bk_tr.to_csv("TRAIN_bk_cat.csv", encoding='utf-8', index=False)

  
#%%Data cleaning work especiall adding categor column
import datetime 
import pandas as pd
import fileinput
import glob
import seaborn as sns

''' array(['Posted Date', 'Reference Number', 'Payee', 'Address', 'Amount'], dtype=object)
    I will focus on cleaning Payee and Amount the most to build up a classification model predicting spending categorization'''
def cleaning_stat(name,output): 
    
    #read the merged bank statements
    bk = pd.read_csv('bkfiles.csv')
    #trim the statement down from removing Address and Reference ID
    bk = bk[['Posted Date', 'Payee', 'Amount']]
    #remove all header lines from 12 statements
    bk = bk.drop(bk['Amount'].loc[bk['Amount']=='Amount'].index)
    
    #clean dollar amounts for digit delimiters
    bk['Amount'] = bk['Amount'].str.replace(',', '').astype(float)
    bk['sent_len'] = bk.Payee.apply(len)
    bk['Date'] = pd.to_datetime(bk['Posted Date'], format ='%m/%d/%Y',errors='coerce')

    bk = bk[['Date', 'Payee', 'Amount']]
    #get rid of 12 header rows where Date==null
    bk = bk.loc[bk.Date.notnull()]


    #generate a new column of weekday label
    #saved day of week in numeric format for using as a parameter of model
    bk['Weekday'] = bk.Date.dt.dayofweek
    bk = bk.drop('Date',axis=1)

    #create payee length as another feature for prediction model
    bk['sent_len'] = bk.Payee.apply(len)
    #output portion of cleaned data as train set
    bk.to_csv(output, encoding='utf-8', index=False)
    return output

def visual_report(output):
    
    bk = pd.read_csv(output)
    
    #Purchasing amount in day frequency
    sns.distplot(bk['Amount'], bins=30)
    
    #Purchasing pattern by weekdays
    sns.countplot(x='Weekday', data=bk)
    ax = ct.plot(kind='bar', stacked=True, rot=0)
    ax.legend(title='mark', bbox_to_anchor=(1, 1.02), loc='upper left')

from sklearn.feature_extraction.text import TfidfVectorizer

def tf_model(output):
    bk_cat = pd.read_csv(output)
    tfidf_vec = TfidfVectorizer()
    tfidf_dense = tfidf_vec.fit_transform(bk_cat['Payee']).todense()
    new_cols = tfidf_vec.get_feature_names()

    bk_cat = bk_cat.join(pd.DataFrame(tfidf_dense, columns=new_cols))
    bk_cat = bk_cat[pd.notnull(bk_cat.Category)]
    
    df_predictor= bk_cat.iloc[:, bk_cat.columns != 'Category']
    target= bk_cat.iloc[:, bk_cat.columns == 'Category']
    
    #Let us now split the dataset into train & test
    from sklearn.model_selection import train_test_split
    X_train,X_test, y_train, y_test = train_test_split(df_predictor, target, test_size = 0.30, random_state=0)
    print("x_train ",X_train.shape)
    print("x_test ",X_test.shape)
    print("y_train ",y_train.shape)
    print("y_test ",y_test.shape)

    # Standarize features
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    
    X_train_scaled = pd.DataFrame(scaler.fit_transform(X_train))
    X_test_scaled = pd.DataFrame(scaler.transform(X_test))
    
    X_train_scaled.columns = X_train.columns.values
    X_test_scaled.columns = X_test.columns.values
    X_train_scaled.index = X_train.index.values
    X_test_scaled.index = X_test.index.values 
    
    X_train = X_train_scaled
    X_test = X_test_scaled
    X_train_scaled.describe()

    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import LabelEncoder
    
    classifier = RandomForestClassifier(random_state = 0, n_estimators = 100,\
                                        criterion = 'entropy', max_leaf_nodes= 20,oob_score = True, n_jobs = -1, class_weight='balanced')
                                    
    # fit the model
    model_RF = classifier.fit(X_train_scaled.dropna(), y_train.dropna())
    y_pred_RF = model_RF.predict(X_test_scaled)

    # Classification report
    from sklearn.metrics import classification_report
    print(classification_report(y_test, y_pred_RF))

    return y_pred_RF

def main():
    name = 'bkfiles.csv'
    output = 'bk_cat.csv'
    compile_stats(name)
    cleaning_stat(name,output)
    visual_report(output)
    tf_model(output)

if __name__ == '__main__':
    main()

   
