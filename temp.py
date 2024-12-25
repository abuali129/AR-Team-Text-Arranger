# use Python 3.11.3

#needed Libraries
# pip install tk
# pip install --upgrade arabic-reshaper
# pip install ttkbootstrap
# pip install python-bidi

import tkinter as tk
import re
import arabic_reshaper
from arabic_reshaper import reshape
from bidi.algorithm import get_display
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class TextManipulator:

    def __init__(self, master):
        self.master = master
        master.title('AR Team مرتب نصوص الألعاب')
        style = ttk.Style('darkly')
        for i in range(2):
            master.grid_columnconfigure(i, weight=1, minsize=150)
        for i in range(30):
            master.grid_rowconfigure(i, weight=1, minsize=10)
        master.grid_rowconfigure(6, weight=1, minsize=30)
        master.grid_rowconfigure(7, weight=1, minsize=30)
        master.grid_rowconfigure(8, weight=1, minsize=30)
        self.input_label = tk.Label(master, text='النص المدخل')
        self.input_label.grid(row=0, column=1, sticky='s', padx=10, pady=10)
        self.input_text = tk.Text(master, height=5, width=50)
        self.input_text.grid(row=1, column=1, rowspan=17, columnspan=1, padx=10, pady=5, sticky='nsew')
        self.input_scrollbar = ttk.Scrollbar(master, command=self.input_text.yview)
        self.input_scrollbar.grid(row=1, column=2, rowspan=17, columnspan=1, padx=(0, 5), pady=5, sticky='nse')
        self.input_text.config(yscrollcommand=self.input_scrollbar.set)
        self.paste_button = ttk.Button(master, text='لصق', command=self.paste_input, bootstyle=PRIMARY)
        self.paste_button.grid(row=19, column=1, sticky='e', padx=10, pady=(0, 10))
        self.clear_button = ttk.Button(master, text='مسح', command=self.clear_input)
        self.clear_button.grid(row=20, column=1, sticky='e', padx=10, pady=(0, 10))
        self.output_text = tk.Text(master, height=5, width=50)
        self.ReshapeNew_text = tk.Text(master, height=5, width=50)
        self.rearranged_label = tk.Label(master, text='الجمل المعاد ترتيبها')
        self.rearranged_label.grid(row=0, column=0, sticky='s', padx=10, pady=10)
        self.rearranged_text = tk.Text(master, height=5, width=50)
        self.rearranged_text.grid(row=1, column=0, rowspan=17, columnspan=1, padx=10, pady=5, sticky='nsew')
        self.rearranged_scrollbar = ttk.Scrollbar(master, command=self.rearranged_text.yview)
        self.rearranged_scrollbar.grid(row=1, column=0, rowspan=17, padx=(0, 5), pady=5, sticky='nse')
        self.ReshapeNew_text.config(yscrollcommand=self.rearranged_scrollbar.set)
        self.the_breaker_button = ttk.Button(master, text='ترتيب النص', command=self.run_the_breaker)
        self.the_breaker_button.grid(row=19, column=0, sticky='e', padx=10, pady=(0, 10))
        self.copy_button = ttk.Button(master, text='نسخ', command=self.copy_output)
        self.copy_button.grid(row=20, column=0, sticky='e', padx=10, pady=(0, 10))
        self.linebreaker_label = tk.Label(master, text='علامة فاصل الأسطر')
        self.linebreaker_label.grid(row=23, column=0, sticky='s', padx=10, pady=(0, 40))
        #self.min_len_label = tk.Label(master, text='الحد الأدنى لطول الجمل') #Removed in this version, not needed
        #self.min_len_label.grid(row=24, column=0, sticky='s', padx=10, pady=(0, 40)) #Removed in this version, not needed
        self.max_len_label = tk.Label(master, text='الحد الأقصى لطول الجمل')
        self.max_len_label.grid(row=25, column=0, sticky='s', padx=10, pady=(0, 40))
        self.linebreaker_entry = ttk.Entry(master)
        self.linebreaker_entry.insert(tk.END, '[LineBreaker]')
        self.linebreaker_entry.grid(row=23, column=0, sticky='s', padx=10, pady=(0, 5))
        self.min_len_entry = ttk.Entry(master)
        #self.min_len_entry.insert(tk.END, '20') #Removed in this version, not needed
        #self.min_len_entry.grid(row=24, column=0, sticky='s', padx=10, pady=(0, 5)) #Removed in this version, not needed
        self.max_len_entry = ttk.Entry(master)
        self.max_len_entry.insert(tk.END, '30')
        self.max_len_entry.grid(row=25, column=0, sticky='s', padx=10, pady=(0, 5))
        self.lang_button = ttk.Button(master, text='English', command=self.switch_lang, bootstyle=(SUCCESS, OUTLINE))
        self.lang_button.grid(row=0, column=0, padx=10, pady=(10, 0), sticky='w')


    def switch_lang(self):
        current_lang = self.lang_button['text']
        if current_lang == 'English':
            self.lang_button['text'] = 'عربي'
            self.input_label['text'] = 'النص المدخل'
            self.rearranged_label['text'] = 'الجمل المعاد ترتيبها'
            self.paste_button['text'] = 'لصق'
            self.clear_button['text'] = 'مسح'
            self.the_breaker_button['text'] = 'ترتيب النص'
            self.copy_button['text'] = 'نسخ'
            self.linebreaker_label['text'] = 'علامة فاصل الأسطر'
            #self.min_len_label['text'] = 'الحد الأدنى لطول الجمل' #Removed in this version, not needed
            self.max_len_label['text'] = 'الحد الأقصى لطول الجمل'
        else:
            self.lang_button['text'] = 'English'
            self.input_label['text'] = 'Input Text'
            self.rearranged_label['text'] = 'Rearranged Sentences'
            self.paste_button['text'] = 'Paste'
            self.clear_button['text'] = 'Clear'
            self.the_breaker_button['text'] = 'Arrange Text'
            self.copy_button['text'] = 'Copy'
            self.linebreaker_label['text'] = 'LineBreaker Marker'
            #self.min_len_label['text'] = 'Minimum Sentence Length' #Removed in this version, not needed
            self.max_len_label['text'] = 'Maximum Sentence Length'

    def paste_input(self):
        self.input_text.delete('1.0', tk.END) #Delete input_text contents
        self.input_text.insert(tk.END, self.master.clipboard_get()) #Paste from Clipboard into input_text

    def clear_input(self):
        self.input_text.delete('1.0', tk.END) #Delete input_text contents

    def copy_output(self):
        self.master.clipboard_clear() #Clear Clipboard
        self.master.clipboard_append(self.rearranged_text.get('1.0', tk.END)) #Getting clipboard contents from rearranged_text

    def add_linebreaker(self):
        input_text = self.input_text.get('1.0', 'end-1c') # Get the input text from the input text box
        arabic_regex = re.compile(r'[\u0600-\u08FF\uFB50-\uFEFF]') # Compile a regular expression to match Arabic characters
        linebreaker_marker = self.linebreaker_entry.get() # Get the linebreaker marker from the linebreaker entry box
        max_len = int(self.max_len_entry.get()) # Get the maximum length for line breaking from the max length entry box
        if max_len < 10: # If the maximum length is less than 10, set minimum length to 0
            min_len = 0
        else: # Otherwise, set the minimum length to one less than the maximum length
            min_len = max_len - 10
        output_text = '' # Initialize an empty string for the output text
        for line in input_text.splitlines(): # Iterate through each line of the input text
            if re.search(arabic_regex, line): # If the current line contains Arabic characters
                regex = f'(?s).{{{min_len},{max_len}}}(?=\\s)' # Define a regular expression to match text between min_len and max_len characters from the start of the line
                replacement = f'\\g<0>{linebreaker_marker}' # Replace the matched text with the linebreaker marker and the matched text itself
                line_output = re.sub(regex, replacement, line) # Apply the regular expression to the current line
                output_text = output_text + line_output + '\n' # Add the modified line to the output text with a newline character
            else: # If the current line does not contain Arabic characters
                output_text += line + '\n' # Add the original line to the output text with a newline character
        self.output_text.delete('1.0', tk.END) # Clear the output text box
        self.output_text.insert(tk.END, output_text) # Insert the modified output text into the output text box


    def convert_text(self):
        rearranged_text = self.output_text.get('1.0', 'end-1c') # Get the rearranged text from the output text box
        arabic_regex = re.compile(r'[\u0600-\u08FF\uFB50-\uFEFF]') # Compile a regular expression to match Arabic characters
        lines = rearranged_text.splitlines() # Split the rearranged text into individual lines
        output = [] # Initialize an empty list for the output text
        for line in lines: # Iterate through each line of the rearranged text
            if arabic_regex.search(line): # If the current line contains Arabic characters
                reshaped_text = arabic_reshaper.reshape(line) # Reshape the current line using the arabic_reshaper library
                final_text = get_display(reshaped_text) # Get the display version of the reshaped text using the get_display function
                output.append(final_text) # Add the final text to the output list
            else: # If the current line does not contain Arabic characters
                output.append(line) # Add the original line to the output list
        self.ReshapeNew_text.delete('1.0', tk.END) # Clear the ReshapeNew text box
        self.ReshapeNew_text.insert('1.0', '\n'.join(output)) # Insert the modified output text into the ReshapeNew text box with newline characters between each line


    def rearrange_sentences(self):
        ReshapeNew_text = self.ReshapeNew_text.get('1.0', 'end-1c') # Get the text from the ReshapeNew_text box
        arabic_regex = re.compile(r'[\u0600-\u08FF\uFB50-\uFEFF]') # Compile a regular expression to match Arabic characters
        linebreaker_marker = self.linebreaker_entry.get() # Get the linebreaker marker from the linebreaker entry box
        sentences = [] # Initialize an empty list for the sentences
        for line in ReshapeNew_text.splitlines(): # Iterate through each line of the text
            if re.search(arabic_regex, line): # If the current line contains Arabic characters
                line = line.strip() # Remove leading and trailing whitespace from the current line
                if not line: # If the current line is empty after removing leading and trailing whitespace
                    sentences.append(line) # Add the empty line to the list of sentences
                    continue # Move on to the next iteration of the loop
                line_sentences = re.split(re.escape(linebreaker_marker), line) # Split the current line into individual sentences using the linebreaker marker as a delimiter
                line_sentences = [s.strip() for s in line_sentences if s.strip()] # Remove leading and trailing whitespace from each sentence and filter out empty strings
                line_sentences.reverse() # Reverse the order of the sentences
                line = linebreaker_marker.join(line_sentences) # Join the reversed list of sentences back into a single string using the linebreaker marker as a delimiter
                sentences.append(line) # Add the modified sentence to the list of sentences
            else: # If the current line does not contain Arabic characters
                sentences.append(line) # Add the original line to the list of sentences
        ReshapeNew_text = '\n'.join(sentences) # Join all the sentences back into a single string with newline characters between each sentence
        self.rearranged_text.delete('1.0', tk.END) # Clear the rearranged text box
        self.rearranged_text.insert(tk.END, ReshapeNew_text) # Insert the modified output text into the rearranged text box with newline characters between each sentence

    def run_the_breaker(self): #Function assgined to the button, runs 3 functions in sequence
        self.add_linebreaker()
        self.convert_text()
        self.rearrange_sentences()
        
root = tk.Tk() # Create a new Tkinter window
text_manipulator = TextManipulator(root) # Initialize an instance of the TextManipulator class with the Tkinter window as its argument
root.mainloop() # Start the event loop for the Tkinter window