import plotly
import plotly.graph_objs as go 
import time

# some more libraries to plot graphs
from plotly.offline import download_plotlyjs, init_notebook_mode, iplot, plot 
import matplotlib.pyplot as plt

# some libraries to process images
import numpy as np
import cv2

# some more libraries that we will use
import pandas as pd # For storing and manipulating data
from wordcloud import WordCloud # For cleaning text of stopwords and creating word cloud
import re # For cleaning text of symbols and numbers

# some libraries to color the graphs
from matplotlib.cm import ScalarMappable # For color mapping 
from matplotlib.colors import Normalize # For transforming freq values between 0 and 1
from mpl_toolkits.axes_grid1 import make_axes_locatable # For formatting colorbar

# some data for referencing
from list_us_states import states

class USWordCloud():
    '''
    get the word_cloud for text data for a US state and insert it into the us map with this class.

    Methods:
    - __init__: initialize
    - execute:
    - __checkStateAndTextData:
    - __makeUSMapFigure:
    - __saveUSMapFigure:
    - __getLongString(self):
    - __getMask(self,mask_scale):
    - __buildStateWC(self):        
    - __insertStateWC(self):
    
    Process:
    1. initialize an instance of the class:
    - set scale_factor -> int -> the size of the final image (1:small, 2:medium, or 3:large)
    - set filename -> str -> the name of the final image (eg. mikes_word_cloud, ...)
    - run instance = USWordCloud(scale_factor,filename)
    
    2. create word cloud image in a state 
    - set _state -> str -> the capital 2-letter abbreviation of a state (eg. 'NY', ...)
    - set text -> list of str -> the words to be included in the word cloud
    - run instance.execute(state,text)
     
    3. repeat step 2 for other states and other text data
    
    4. check us_word_clouds folder for final image!
  
    '''
    
    # initialize instance variables
    def __init__(self,scale_factor,filename):
        
        # Initialize instance attributes
        assert type(scale_factor) == int, "scale_factor input must be an integer"
        assert (scale_factor == 1)|(scale_factor == 2)|(scale_factor == 3), "scale_factor input must have values 1, 2, or 3!"
        self._scale_factor = scale_factor # store the integer scale factor as 1,2, or 3 for a small, medium, or large final image
        
        assert type(filename) == str, "filename input must be a string"
        self._filename = filename # store the string filename for the final image
        
        # Initialize other data
        self._text_data = []
        self._fig = []
        self._state = 'NY'
        self._scale = 5
        self._large_scale = self._scale*self._scale_factor
        self._US_wc_path = 'us_word_clouds/'+self._filename+'.png'
        self._US_map_path = 'us_map/us_map.png'
        self._state_wc_path = 'word_cloud/state_word_cloud.png'
        self._mask_path = ''
        
        # make the US map
        self.__makeUSMapFigure()
        
        # Create a blank US Map for the final word cloud
        self.__saveUSMapFigure(image_scale=self._large_scale, path=self._US_wc_path)
        
        # Save the blank US Map for referencing in __insertStateWC(self)
        self.__saveUSMapFigure(image_scale=self._large_scale, path=self._US_map_path)

    
    def execute(self,state,text):
        '''
        run the sequence of commands that will build the word cloud
        input: 
        - _state: str -> capital,2-letter state name like ('NY','CA',...) 
        - text: str -> a list of text gathered for the state
        '''
        # we need to initialize the state and text data for each word cloud
        self._state = state
        self._text_data = text
        
        # check the state and text data for correct formatting
        self.__checkStateAndTextData()
        
        # filter the text data
        self.__getLongString()
        self.__filterSymbols()
        
        # get the small mask
        self.__getMask(mask_scale = self._scale)
        
        # build the word cloud for the state
        self.__buildStateWC()
                
        # build the large mask
        self.__getMask(mask_scale = self._large_scale)
        
        # insert the word cloud into the US map
        self.__insertStateWC()
        
    def __checkStateAndTextData(self):
        '''
        verify the state and the list of text is in the right form
        '''
        assert self._state in states, "the input for s_tate has to be a capital 2-letter US state acryonym"
        
        assert type(self._text_data) == list, "The input for text needs to be a list of strings"
        for text in self._text_data:
            assert type(text)==str, "the input for _text_data needs to be list containing only strings"
        
    def __makeUSMapFigure(self):
        '''
        make a figure of the US Map using plotly 
        '''
        # To establish connection 
        init_notebook_mode(connected = True) 

        # type defined is choropleth to 
        # plot geographical plots 
        data = dict(type = 'choropleth', 
                    # location: Arizoana, California, Newyork 
                    locations = [self._state], 
                    # States of USA 
                    locationmode = 'USA-states', 
                    # Hide Colorbar
                    showscale=False,
                    # colorscale can be added as per requirement 
                    colorscale = 'greys',                 
                    # choose the color to fill the state
                    z = [0])

        # Adjust layout of image
        layout = go.Layout(geo={'scope': 'usa'},
                            margin=go.layout.Margin(
                                l=0,
                                r=0,
                                b=0,
                                t=0,
                                pad=0))

        # pass data dictionary as a list  
        choromap = go.Figure(data = [data], layout = layout) 

        self._fig =choromap
        
    def __saveUSMapFigure(self,image_scale,path):
        '''
        save the US map figure
        
        input: 
        - image_scale: int -> the multiple that will increase the size of the base figure
        - path: str -> the path to the file
        
        '''
        # Save figures to file
        plotly.io.write_image(self._fig, 
                              path, 
                              format='png',
                              # Adjust the image dimensions
                              scale=image_scale, 
                              validate=False)
        
    def __getLongString(self):
        '''
        transform a list of text into a long string of space-separated,
        lowercase words.
        '''
        # we need an empty string to store all of the words
        long_string = ' '

        # iterate through each row of the job title column 
        for value in self._text_data: 

            # change each value to string 
            value = str(value) 

            # split the job titles into a list separated by spaces  
            sub_words = value.split() 

            # i. converts each sub-word from the job title into lowercase 
            sub_words = [value.lower() for value in sub_words]

            for word in sub_words: 

                # ii. append each sub-word to the long string
                long_string = long_string + word

                # iii. separate each word by a space
                long_string = long_string + ' ' 
        
        self._text_data = long_string

    def __filterSymbols(self):
        '''
        filter out symbols and numbers from a long string
        '''
        # filter out the symbols from the long string with the re.sub method
        long_string_no_sym_num = re.sub('[^a-zA-Z+#0234]', # keep a-z, A-Z, #, +, 2-4, for c#, c++, d3, h20, neo4 
                                        ' ', # replace anything else with a space
                                        self._text_data) # filter long_string 
        
        self._text_data = long_string_no_sym_num
        
    def __getMask(self,mask_scale):
        '''
        get a certain size mask for a state

        input: 
        - mask_scale: int -> the scale of the mask being made
        - path_to_file: str -> the path to the filename (path/to/file)
        '''
        
        # store US figure in fig variable
        self.__makeUSMapFigure()
        
        # assign mask path
        self._mask_path='masks/'+str(mask_scale)+'x_mask.png'
        
        # save the US fig for mask
        self.__saveUSMapFigure(image_scale=mask_scale,
                               path=self._mask_path)
    
        # import image as greyscale
        img = cv2.imread(self._mask_path,  0)

        # use THRESH_TOZERO_INV to set values greater than 190 to zero
        val = 190
        val, thresh_img = cv2.threshold(img,val,255,cv2.THRESH_TOZERO_INV)

        # use THRESH_TOZERO to set values less than or equal to 189 to zero
        val = 189
        val, thresh_thresh_img = cv2.threshold(thresh_img,val,255,cv2.THRESH_TOZERO)

        # use THRESH_BINARY to set values greater than 189 to 255
        val = 189
        val, thresh_thresh_thresh_img = cv2.threshold(thresh_thresh_img,val,255,cv2.THRESH_BINARY)
        
        # Store the 1-channel mask
        mask_1chan = thresh_thresh_thresh_img

        # Import 3-channel version of image
        img_3chan = cv2.imread(self._mask_path,1)

        # Make empty array with dimensions of 3-channel image
        full_img = np.full(img_3chan.shape,255,dtype='uint8')

        # This bitwise_or function combines the two white images in all 3 channals only in
        # the area where the mask is 255
        mask_3chan = cv2.bitwise_or(full_img,full_img,mask=mask_1chan)

        # Save state mask to file
        cv2.imwrite(self._mask_path,mask_3chan)
    
    def __buildStateWC(self):
        '''
        get the word cloud for the text data from a state in the shape of the state
        '''
        
        # filter out the stopwords from the long string and get the word/word-freq dictionary
        words_and_freqs_dict = WordCloud().process_text(self._text_data)

        # store the mask image as greyscale
        img = cv2.imread('masks/'+str(self._scale)+'x_mask.png',0)

        # invert the mask image for wc input
        img = cv2.bitwise_not(img)

        ## WC takes mask as 2D numpy array
        state_mask = np.array(img)

        # create the word cloud
        wc = WordCloud(background_color="black",
                       mask=state_mask,
                       contour_width=5,
                       colormap='gist_rainbow',
                       relative_scaling = .5,
                       scale=self._scale_factor,
                       min_font_size=2,
                       contour_color='steelblue')

        # generate word cloud
        wc.fit_words(words_and_freqs_dict)

        # Save Wordcloud as image 
        wc.to_file(self._state_wc_path)
        # Print a success statement when wc is made successfully
        print('Word cloud was made successfully for: '+str(self._state))
            
    def __insertStateWC(self):
        '''
        get the word cloud from a state into the map of the whole US
        '''

        # import full scale US image
        US_img = cv2.imread(self._US_wc_path,1)

        # import the full scale state mask
        state_mask = cv2.imread('masks/'+str(self._large_scale)+'x_mask.png',0)

        # Get the inv
        state_mask_inv = cv2.bitwise_not(state_mask)

        # Use bitwise_OR
        cut_US_img = cv2.bitwise_or(US_img,US_img,mask = state_mask_inv) 

        # import the large scale state word cloud 
        state_wc = cv2.imread(self._state_wc_path,-1)

        # use bitwise OR on state_wc with state_mask_inv
        cut_state_wc = cv2.bitwise_or(state_wc,state_wc,mask = state_mask)

        # use bitwise AND on cut_CA_wc with cut_US_img
        US_wc = cv2.bitwise_or(cut_state_wc,cut_US_img)

        # write the modified full scale us map image
        cv2.imwrite(self._US_wc_path,US_wc)

        print('the word cloud was successfully added for the state: '+str(self._state))