import tkinter as tk
from PIL import ImageTk, Image

class PhotoFrameApp:
    def __init__(self, root):
        self.root = root
        self.photos = []
        self.current_photo_index = 0

        # Load photos
        self.load_photos()

        # Display current photo
        self.display_current_photo()

        # Auto slideshow
        self.root.after(3000, self.next_photo)

        # Button to skip
        self.skip_button = tk.Button(self.root, text="Skip", command=self.next_photo)
        self.skip_button.pack()

    def load_photos(self):
        for i in range(1, 6):
            photo = Image.open(f"ft{i}.jpg")  # Change file extension if necessary
            self.photos.append(photo)

    def display_current_photo(self):
        current_photo = self.photos[self.current_photo_index]
        current_photo = current_photo.resize((400, 300), Image.ANTIALIAS)
        photo_img = ImageTk.PhotoImage(current_photo)
        self.photo_label = tk.Label(self.root, image=photo_img)
        self.photo_label.image = photo_img
        self.photo_label.pack()

    def next_photo(self):
        self.current_photo_index = (self.current_photo_index + 1) % len(self.photos)
        self.photo_label.pack_forget()
        self.display_current_photo()
        self.root.after(3000, self.next_photo)

if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoFrameApp(root)
    root.mainloop()
