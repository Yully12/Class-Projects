import vlc
import time

# Define a list of songs (replace with actual file paths)
songs = [
    "song1.mp3",
    "song2.mp3",
    "song3.mp3",
    "song4.mp3",
    "song5.mp3"
]

# Function to play a song
def play_song(song_index):
    global player
    if player:
        player.stop()
    player = vlc.MediaPlayer(songs[song_index])
    player.play()

# Initialize VLC player
player = None

# Initial song index
current_song_index = 0

# User instructions
print("Welcome to the Python Music Player!")
print("Type the number (1-5) to play a song, 'forward' to go to the next song, 'backward' to go to the previous song, or 'exit' to quit.")

# Main loop
while True:
    command = input("Enter your command: ").lower()
    
    if command == "exit":
        if player:
            player.stop()
        break
    elif command.isdigit():
        song_choice = int(command) - 1
        if 0 <= song_choice < len(songs):
            current_song_index = song_choice
            play_song(current_song_index)
        else:
            print("Invalid song number. Please choose between 1-5.")
    elif command == "forward":
        if current_song_index < len(songs) - 1:
            current_song_index += 1
            play_song(current_song_index)
        else:
            print("You are at the last song.")
    elif command == "backward":
        if current_song_index > 0:
            current_song_index -= 1
            play_song(current_song_index)
        else:
            print("You are at the first song.")
    else:
        print("Unknown command. Please try again.")

print("Thank you for using the Python Music Player. Goodbye!")
