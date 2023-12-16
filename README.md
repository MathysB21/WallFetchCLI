# WallFetchCLI
This tool searches and downloads wallpapers from WallHaven by searching for tags and then downloading them.

## Requirements
Please note that you will need to add the following packages through pip:
- selenium
- requests

Please note that you will need to install the following from the original websites:
- geckodriver (This is for Firefox. Remember to have the geckodriver.exe in the same file as the main python file.)
- python (If you have not installed this yet)

This application will download all the images into a folder with the tag as the name. Each of the images will be named by the date and image number. 

## Things to note:
The WHavenIDs JSON file is used to store the tags of the images you have already downloaded as to not download doubles should you have multiple tags you want to download. Thus, if you ever delete these images or want to redownload some for some reason, you need to manually clear all the tags within the square brackets of the data object.

## Running the application
- There have been some bugs when people try to run the python file. It will simply close without doing anything. A simple workaround is to open the project inside an IDE like VS Code and then opening the python file and then running it from there. (Somewhere in the future I am going to make an executable which will replace the source code, but for now this will have to do)