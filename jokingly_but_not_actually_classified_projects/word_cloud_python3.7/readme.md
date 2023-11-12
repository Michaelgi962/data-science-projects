# Module Dependencies ( This project will use the python vers 3.7)
  
pandas 
numpy 
regex 
PIL 
opencv 
plotly 
mpl_toolkits (should come with matplotlib)
matplotlib 
wordcloud 
time 
psutil
ploty plotly-orca

## Install Module Dependencies with Command Line
  
conda install -c anaconda pandas psutil
conda install -c conda-forge numpy regex pillow opencv plotly matplotlib wordcloud
conda install -c plotly plotly-orca
  
# Intro 
 
The goal of this project is to make a word cloud using text related to each state state that is in the shape of the state. Then for each state, we insert its word cloud into the US map.

# Process

## 1. initialize an instance of the class:
  
  
  - set scale_factor -> int -> the size of the final image (1:small, 2:medium, or 3:large)
  
  
- set filename -> str -> the name of the final image (eg. mikes_word_cloud, ...)
  
  
- run instance = USWordCloud(scale_factor,filename)
    
## 2. create word cloud image in a state 
  
    
- set state -> str -> the capital 2-letter abbreviation of a state (eg. 'NY', ...)
  
  
- set text -> list of str -> the words to be included in the word cloud
  
  
- run instance.execute(state,text)
     
## 3. repeat step 2 for other states and other text data
    
## 4. check us_word_clouds folder for final image!
 



