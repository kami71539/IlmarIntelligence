#!/usr/bin/env python
# coding: utf-8

# In[7]:


import os
import shutil

def verify_and_process_files(source_dir, processed_dir, accepted_extension=".csv"):
  processed_files = set()  # Track processed files to avoid duplicates

  for filename in os.listdir(source_dir):
    filepath = source_dir + filename

    if filename not in processed_files:
      processed_files.add(filename)  # Mark as processed

      # Check if it's a non-empty file with the accepted extension
      if os.path.getsize(filepath) > 0 and filename.endswith(accepted_extension):
        os.makedirs(processed_dir, exist_ok=True) # Create directory if it does not exists.
        shutil.move(filepath, processed_dir + filename)
        print(f"File '{filename}' processed successfully.")
      else:
        invalid_dir = source_dir + 'invalid'
        os.makedirs(invalid_dir, exist_ok=True)
        shutil.move(filepath, invalid_dir)
        print(f"File '{filename}' is invalid and moved to 'invalid' directory.")

# Example usage (replace paths with your actual directories)
source_dir = r"K:\Ilmar intelligence\source\\"
processed_dir = r"K:\Ilmar intelligence\pre_processed\\"

verify_and_process_files(source_dir, processed_dir)
input('Press Enter to continue: ')

