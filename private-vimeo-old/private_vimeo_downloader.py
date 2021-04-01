import requests, webbrowser
import tkinter as tk
from tkinter import filedialog

def get_links(text):
    text = text.split('"')
    links = [x for x in text if x.find('https://vod-progressive.akamaized.net') != -1]
    return links

def download(url, save_path):
    if not validate_save_path(save_path):
        raise ValueError("The specified save path is not valid")
    try:
        print("trying to get mp4 from the url...")
        response = requests.get(url, stream=True)
        print("writing into file...")
        mp4_file = open(save_path, 'wb+')
        for chunk in response.iter_content(1024):
            print('Writing... ' + str(chunk[0]))
            mp4_file.write(chunk)

    except:
        print("Error while trying to get the mp4 file")
        exit()
        
def validate_save_path(save_path):
    if type(save_path) != str:
        return False
    
    save_path = save_path.lower()

    if not save_path.endswith("mp4"):
        return False
    if save_path.find("/") != -1:
        save_path = [x for x in save_path.split("/") if x == ""]
    else:
        save_path = [x for x in save_path.split("\\") if x == ""]

    if len(save_path) != 0:
        return False

    return True

def select_link(links):
    if type(links) != list and type(links) != tuple:
        raise TypeError("select_link parmeter is list or tuple only")
    
    download_link = ""
    content_length = 0
    for link in links:
        try:
            res = requests.head(link)
        except:
            continue
        if content_length < int(res.headers['Content-Length']):  
            content_length = int(res.headers['Content-Length'])
            download_link = link   

    return download_link

def replace_video_in_video_viewer(video_viewer_path, mp4_path):
    try:
        with open(r"c:\test", 'r', encoding="utf-8") as f:
            template = f.read()
        
        new_html = template.replace("{$!video!$}", mp4_path).replace("{$!title!$}", "Lecture Viewer")
        with open(video_viewer_path, 'w', encoding="utf-8") as f:
            f.write(new_html) 

    except:
        print("Failed opening video viewer")
        exit()

def main():
    lecture_viewer_path = "c:\test"
    dialog_on = True
    if dialog_on:
        print("Enter file path: ")
        root = tk.Tk()
        root.withdraw()
        filepath = filedialog.askopenfilename()
    else:
        filepath = input("Enter file path: ")
    try:
        if filepath.lower() == "exit":
            exit()

        with open(filepath, 'r', encoding="utf-8") as f:
            text = f.read()

    except FileNotFoundError:
        print("Can't open this file.")
        print("try another path.")
        main()
    else:

        if dialog_on:
            print("Enter saving path: ")
            root = tk.Tk()
            root.withdraw()
            save_path = filedialog.asksaveasfilename()
        else:
            save_path = input("Enter saving path: ")
        download(select_link(get_links(text)), save_path)
        print("Saved.")
        replace_video_in_video_viewer(lecture_viewer_path, save_path)
        webbrowser.open(lecture_viewer_path)
    
if __name__ == "__main__":
    main()