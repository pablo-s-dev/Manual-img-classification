import os
import shutil
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox, scrolledtext

not_text_file = lambda f: not f.endswith(text_extension) and not f.endswith(".py") and not f.endswith(".md") and "." in f

args: list[str] = os.sys.argv

text_extension = ".txt"

for arg in args:
    if("--" in arg):
        args.pop(args.index(arg))
        if("--json" == arg):
            text_extension = ".json"
        if("--csv" == arg):
            text_extension = ".csv"
        if("--txt" == arg):
            text_extension = ".txt"
        break
    


if(len(args) < 2):
    print("Usage: python main.py <class1> <class2> ... <classN> [--json | --csv | --txt]")
    exit(1)

class_names = args[1: ]

 
files = os.listdir()
images = sorted([f for f in files if not_text_file(f)])

# Create the main window
root = tk.Tk()
root.title("Image classifier")
root.geometry("800x600")


content_frame = tk.Frame(root)
content_frame.pack(side=tk.TOP)

# Create frames
img_frame = tk.Frame(content_frame)
img_frame.pack(side=tk.TOP)
text_frame = tk.Frame(content_frame)
text_frame.pack(side=tk.BOTTOM)

bottom_frame = tk.Frame(root)
bottom_frame.pack(side=tk.BOTTOM, before=content_frame)

amount_left_frame = tk.Frame(bottom_frame)
amount_left_frame.pack(side=tk.BOTTOM)

amount_label = tk.Label(amount_left_frame, text=f"Amount of files left: {len(images)}", font=("Arial", 15))
amount_label.pack()

button_frame = tk.Frame(bottom_frame)
button_frame.pack(side=tk.BOTTOM)




# Function to display image and text
def display_content(image, text):

    amount_label.config(text=f"Amount of files left: {len(images)}")

    text = image.split(".")[0] + text_extension

    # Clear previous content   
    for widget in img_frame.winfo_children():
        widget.destroy()
    for widget in text_frame.winfo_children():
        widget.destroy()

    # Open an image file
    try:
        img = Image.open(image)
    except:
        messagebox.showerror("Error", f"Could not open the image file {image}! We will move to the next file.")

        if( len(images) >= 2):
            images.pop(0)
            display_content(images[0], text)

        return
    # Get the aspect ratio of the image
    aspect_ratio = img.width / img.height

    root.update_idletasks()

    # Get screen width and height
    screen_width = root.winfo_screenwidth() - button_frame.winfo_width()
    screen_height = root.winfo_screenheight() - button_frame.winfo_height()

    vmin = min(screen_width, screen_height)

    # Calculate new image dimensions
    new_width = int(vmin * 0.5)
    new_height = int(new_width / aspect_ratio)

    # Resize the image using new dimensions
    img = img.resize((new_width, new_height))

    # Convert the Image object to a PhotoImage object
    img = ImageTk.PhotoImage(img)
    panel = tk.Label(img_frame, image=img)
    panel.image = img
    panel.pack()

    # Display text
    with open(text, 'r', encoding='utf-8') as file:
        data = file.read()
    text_area = scrolledtext.ScrolledText(text_frame, wrap = tk.WORD, width = 40, height = 10, font = ("Arial",15))
    text_area.insert(tk.INSERT, data)
    text_area.pack()

def end():
    amount_label.config(text=f"Amount of files left: {len(images)}")
    messagebox.showinfo("Success", "All files have been moved!", )

    for widget in img_frame.winfo_children():
        widget.destroy()

    for widget in text_frame.winfo_children():
        widget.destroy()
    
    content_frame = tk.Frame(root, )
    content_frame.place(relx=0.5, rely=0.5, anchor="center")

    end_label = tk.Label(content_frame, text="All files have been moved!", font=("Arial", 20))
    end_label.pack()

def make_dirs(class_names):
    for class_name in class_names:
        if not os.path.exists(class_name):
            os.makedirs(class_name)

# Function to move files
def move_files(class_dir):

    print('Moving files to', class_dir)

    text = images[0].split(".")[0] + text_extension

    
    shutil.move(images[0], class_dir)

    if(os.path.exists(text)):
        shutil.move(text, class_dir)
    # Remove current image and text from list and load next
    images.pop(0)

    if(len(images) == 0):
        end()
        

        return

    text = images[0].split(".")[0] + text_extension
    display_content(images[0], text)

make_dirs(class_names)

# Create buttons
for i in range(0, len(class_names)):
    button = tk.Button(button_frame, text=class_names[i], command=lambda i=i: move_files(class_names[i]), width=10, height=2)
    button.grid(row=0, column=i, padx=5, pady=5)

if(len(images) != 0):
    # Display first image and text

    text = images[0].split(".")[0] + text_extension
    root.after_idle(display_content, images[0], text)
else:
    end()

root.mainloop()
