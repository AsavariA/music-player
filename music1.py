from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root = Tk()
root.title('Music Player')
root.iconbitmap('musicicon.ico')
root.geometry("800x500")

# initialise pygame mixer
pygame.mixer.init()

# song length
def play_time():
    # check for double timing
    if stopped:
        return

    current_time = pygame.mixer.music.get_pos()/1000
    converted_time = time.strftime('%M:%S', time.gmtime(current_time))

    # current_song = song_box.curselection()
    song = song_box.get(ACTIVE)
    song = f'D:/Asa/projects/tkinter/music/{song}.mp3'

    # load song using mutagen
    song_load = MP3(song)

    # get song length
    global song_length
    song_length = song_load.info.length
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))
    status_bar.config(text=f'Time Elapsed: {converted_time} of {converted_song_length}')

    # increase current time by one sec
    current_time += 1

    if int(my_slider.get()) == int(song_length):
        status_bar.config(text=f'Time Elapsed: {converted_song_length} of {converted_song_length}')

    elif paused:
        pass

    elif int(my_slider.get())==int(current_time):
        # slider hasnt been moved
        # update slider
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(current_time))

    else:
        # slider has been moved
        # update slider
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(my_slider.get()))

        # convert slider position time to time format
        converted_time = time.strftime('%M:%S', time.gmtime(int(my_slider.get())))

        # output time to staus bar
        status_bar.config(text=f'Time Elapsed: {converted_time} of {converted_song_length}')

        # move this thing along
        next_time = int(my_slider.get()) + 1
        my_slider.config(value=next_time)

    # output time to staus bar
    # status_bar.config(text=f'Time Elapsed: {converted_time} of {converted_song_length}')

    # update slider position value to current song position
    # my_slider.config(value=int(current_time))

    # update time
    status_bar.after(1000, play_time)

# add song func
def add_song():
    song = filedialog.askopenfilename(initialdir='music/', title="choose a song", filetypes=(("mp3 Files", "*.mp3"), ))
    song = song.replace("D:/Asa/projects/tkinter/music/","")
    song = song.replace(".mp3", "")
    song_box.insert(END, song)

def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir='music/', title="choose a song", filetypes=(("mp3 Files", "*.mp3"),))
    # loop through list
    for song in songs:
        song = song.replace("D:/Asa/projects/tkinter/music/", "")
        song = song.replace(".mp3", "")
        song_box.insert(END, song)

def play():
    # set stopped variable to false
    global stopped
    stopped = False
    song = song_box.get(ACTIVE)
    song = f'D:/Asa/projects/tkinter/music/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # call play time func
    play_time()

    # update slider
    # slider_position = int(song_length)
    # my_slider.config(to=slider_position, value=0)

    # current_volume = pygame.mixer.music.get_volume()
    # slider_label.config(text=current_volume*100)
global stopped
stopped = False
def stop():
    # reset status and slider
    status_bar.config(text='')
    my_slider.config(value=0)

    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)

    # clear the status bar
    status_bar.config(text='')

    # set stop variable
    global stopped
    stopped = True

# create global pause
global paused
paused = False

def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True

def next_song():
    # reset status and slider
    status_bar.config(text='')
    my_slider.config(value=0)

    # get current song tuple number
    next_one = song_box.curselection()
    # add one to current song number
    next_one = next_one[0]+1
    song = song_box.get(next_one)
    song = f'D:/Asa/projects/tkinter/music/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    song_box.selection_clear(ACTIVE)
    song_box.activate(next_one)

    song_box.selection_set(next_one, last=None)

def prev_song():
    # reset status and slider
    status_bar.config(text='')
    my_slider.config(value=0)

    # get current song tuple number
    prev_one = song_box.curselection()
    # add one to current song number
    prev_one = prev_one[0]-1
    song = song_box.get(prev_one)

    song = f'D:/Asa/projects/tkinter/music/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    song_box.selection_clear(ACTIVE)
    song_box.activate(prev_one)

    song_box.selection_set(prev_one, last=None)

def delete_song():
    stop()
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()

def delete_all_songs():
    stop()
    song_box.delete(0, END)
    pygame.mixer.music.stop()

def slide(x):
    # slider_label.config(text=f'{int(my_slider.get())} of {int(song_length)}')
    song = song_box.get(ACTIVE)
    song = f'D:/Asa/projects/tkinter/music/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(my_slider.get()))

def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())

    # get current volume
    # current_volume = pygame.mixer.music.get_volume()
    # slider_label.config(text=current_volume * 100)

# create master fram
master_frame = Frame(root)
master_frame.pack(pady=20)

# create playlist box
song_box = Listbox(master_frame, bg="black", fg="white", width=100, selectbackground="grey")
song_box.grid(row=0, column=0)

# create player controls
back_btnimg = PhotoImage(file="back.png")
play_btnimg = PhotoImage(file="play.png")
pause_btnimg = PhotoImage(file="pause.png")
stop_btnimg = PhotoImage(file="stop.png")
forward_btnimg = PhotoImage(file="forward.png")

# create player control frames
controls_frame = Frame(root)
controls_frame.pack(pady=20)

# create volume label frame
volume_frame = LabelFrame(master_frame,text="volume")
volume_frame.grid(row=0,column=1,padx=30)


# create control buttons
back_btn = Button(controls_frame,image=back_btnimg ,borderwidth=0, command=prev_song)
play_btn = Button(controls_frame,image=play_btnimg ,borderwidth=0, command=play)
pause_btn = Button(controls_frame,image=pause_btnimg ,borderwidth=0, command=lambda: pause(paused))
stop_btn = Button(controls_frame,image=stop_btnimg ,borderwidth=0, command=stop)
forward_btn = Button(controls_frame,image=forward_btnimg ,borderwidth=0, command=next_song)

back_btn.grid(row=0, column=0, padx=10)
play_btn.grid(row=0, column=1, padx=10)
pause_btn.grid(row=0, column=3, padx=10)
stop_btn.grid(row=0, column=2, padx=10)
forward_btn.grid(row=0, column=4, padx=10)

# menu
my_menu = Menu(root)
root.config(menu=my_menu)

# add songmneu
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs",menu=add_song_menu)
add_song_menu.add_command(label="add one song to playlist", command=add_song)
add_song_menu.add_command(label="add many songs to playlist", command=add_many_songs)

# delete song menu
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove songs",menu=remove_song_menu)
remove_song_menu.add_command(label="Delete a song from playlist", command=delete_song)
remove_song_menu.add_command(label="Delete all songs from playlist", command=delete_all_songs)

# create status bar
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

#music position slider
my_slider = ttk.Scale(root, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length = 680)
my_slider.pack(pady=20)

# volume silder
volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient=VERTICAL, value=1, command=volume, length = 125)
volume_slider.pack(pady=10)


# temp slider label
# slider_label = Label(root, text="0" )
# slider_label.pack(pady=10)

root.mainloop()
