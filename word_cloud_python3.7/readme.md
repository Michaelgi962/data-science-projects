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
 
The goal of this project is to make a wordcloud using the job titles from all of the US job descriptions related to the search 'data-scientist' for each or all of the different states.

# Process
  
First a mask for a state needs to be created if trying to plot data for other states besides california. 
  
Store this state png image in the sample_images folder or use the file for california that currently exists.
  
## Open create_mask.ipynb
  
If using a new state png image rename the input to the state png image in the sample_images folder that will be converted to a mask.
  
If using a new state png image also rename the output to the name of the state mask image that will be stored in the masks folder.
  
Run the file when finished.

## Open word_cloud.ipynb
  
Run this file from top to bottom.
 
Read and run each of the cells, they are well documented.
  
The figures that are generated are saved in the figs folder.
  




