#!/usr/bin/env python
# coding: utf-8

# # App survey
#     Guided Project: Profitable App Profiles for the App Store and Google Play Markets

# In[1]:


def file_to_list(path,has_header=True):
    opened_file = open(path)
    from csv import reader
    read_file = reader(opened_file)
    result_list = list(read_file)
    if has_header:
        return result_list[0],result_list[1:]
    return result_list

def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]
    for row in dataset_slice:
        print(row)
        print("\n")        
    if rows_and_columns:
        print("Number of rows: "+str(len(dataset)))
        print("Number of columns: "+str(len(dataset[0])))


# In[2]:


header_apple,data_apple = file_to_list('AppleStore.csv')
header_google,data_google = file_to_list('googleplaystore.csv')


# In[3]:


#data exploration
print(header_apple)
print()
explore_data(data_apple,0,4,True)
print("\n\n")
print(header_google)
print()
# explore_data(data_google,0,2,True)


# In[4]:


#data cleaning
index = 0
for row in data_google:
    if row[0]=='Life Made WI-Fi Touchscreen Photo Frame':
        print(index)
        print(row)
        break
    index += 1


# In[5]:


del data_google[index]
print(data_google[index])


# In[6]:


unique_app = []
duplicate_app = []
for row in data_google:
    name = row[0]
    if name in unique_app:
        duplicate_app.append(name)
    else:
        unique_app.append(name)
print(duplicate_app[:5])
print("Number of duplicate records: ", len(duplicate_app))
for row in data_google:
    name = row[0]
    if name=='Quick PDF Scanner + OCR FREE':
        print(row)


# --The higher the number of reviews, the more recent the data should be. Rather than removing duplicates randomly, we'll only keep the row with the highest number of reviews and remove the other entries for any given app.

# In[7]:


original_length = len(data_google)
print("Original Length: ", original_length)
print("Expected length: ", original_length-len(duplicate_app))


# In[8]:


reviews_max={}
for row in data_google:
    name = row[0]
    n_reviews = int(row[3])
    if name in reviews_max:
        reviews_max[name] = max(reviews_max[name],n_reviews)
    else:
        reviews_max[name] = n_reviews
print(len(reviews_max))


# --clean the data, pick the right record: specific name relevant to max reviews and have not been added into cleaned data(avoid completely same records have max reviews)

# In[9]:


android_clean=[]
already_added=[]
for row in data_google:
    name = row[0]
    n_reviews = int(row[3])
    if reviews_max[name]==n_reviews and name not in already_added:
        android_clean.append(row)
        already_added.append(name)
print(len(android_clean))


# In[10]:


#delete non-English apps
# def isEnglish(input):
#     for char in input:
#         if ord(char) > 127:
#             return False
#     return True
# print(isEnglish("dfksk723bd"))
# print(isEnglish("多少度"))
# print(isEnglish("dsdbadksa😁"))


# In[11]:


#delete too many apps, some English apps with emojis may be deleted wrongly
def isEnglish(input):
    counter = 0
    for char in input:
        if ord(char) > 127:
            counter += 1
    if counter>3:
        return False
    else:
        return True
print(isEnglish("dfksk723bd"))
print(isEnglish("多少度就"))
print(isEnglish("dsdbadksa😁"))


# In[12]:


print("android")
print(len(android_clean))
android_english=[]
for row in android_clean:
    if isEnglish(row[0]):
        android_english.append(row)
print(len(android_english))

print("ios")
print(len(data_apple))
ios_english=[]
for row in data_apple:
    if isEnglish(row[1]):
        ios_english.append(row)
print(len(ios_english))


# In[13]:


## select free apps


# In[14]:


print("android")
android_free = []
for row in android_english:
    price = row[7]
    if price == "0":
        android_free.append(row)
print(len(android_free))

print("ios")
ios_free = []
for row in ios_english:
    price = row[4]
    if price == '0.0':
        ios_free.append(row)
print(len(ios_free))


# # Clean finished

# In[24]:


def freq_dictionary(dataset,index):
    a_dictionary={}
    for row in dataset:
        value = row[index]
        if value in a_dictionary:
            a_dictionary[value] += 1
        else:
            a_dictionary[value] = 1
    return a_dictionary

def display_freq(dataset,index):
    #convert to a list of tuples
    length_of_dataset = len(dataset)
    a_dictionary = freq_dictionary(dataset,index)
    list_of_tuples=[]
    for key in a_dictionary:
        percentage = (a_dictionary[key]/length_of_dataset)*100
        list_of_tuples.append((percentage,key))
    list_sorted = sorted(list_of_tuples,reverse=True)
    for a_tuple in list_sorted:
        print(a_tuple[1]," : ",a_tuple[0])
        
def display_popular(dataset,type_index,popular_index):
    frequent_dictionary = freq_dictionary(dataset,type_index)
    popular_dictionary = {}
    
    for type_key in frequent_dictionary:
        popular_dictionary[type_key] = 0   
    for row in dataset:
        type_key = row[type_index]
        
        raw_value = row[popular_index]
        raw_value = raw_value.replace("+","")
        raw_value = raw_value.replace(",","")
        
        popular_value = int(raw_value)
        
        popular_dictionary[type_key] += popular_value 
        
        
    list_of_tuples=[]
    for key in popular_dictionary:
        value = popular_dictionary[key]/frequent_dictionary[key]
        list_of_tuples.append((value,key))
    list_sorted = sorted(list_of_tuples,reverse=True)
    for a_tuple in list_sorted:
        print(a_tuple[1]," : ",a_tuple[0])
        


# In[16]:


print(header_google[1],"\n")
display_freq(android_free,1)


# In[17]:


print(header_google[9],"\n")
display_freq(android_free, 9)


# In[18]:


print(header_apple[11],"\n")
display_freq(ios_free, 11)


# In[26]:


print("android_category");
display_popular(android_free,1,5)


# In[29]:


print("android_genres");
display_popular(android_free,9,5)


# In[32]:


print("ios_primegenres");
display_popular(ios_free,11,5)


# In[ ]:




