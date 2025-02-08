import random
import tkinter as tk
from customtkinter import CTk, CTkButton

class SimpleApp:

    def __init__(self):
        self.counter = 0
        self.app = CTk()
        self.app.title("X")

        # Start the application in fullscreen mode
        self.app.attributes("-fullscreen", True)

        # Display counter text
        self.text = tk.Text(self.app, height=2, width=20, font=("Impact", 16), bg="#2E2E2E", fg="white", bd=0, state=tk.DISABLED)
        self.text.place(relx=0.01, rely=0.01, anchor="nw")
        self.text.config(state=tk.NORMAL)
        self.text.insert("1.0", f"Current count: {self.counter}")
        self.text.config(state=tk.DISABLED)

        self.buttons = []  # Store buttons separately
        self.first_click = False  # Flag to track if the first button has been clicked

        # Spawn the first button
        self.spawn_first_button()

    def spawn_first_button(self):
        """Spawn the first X button on the screen."""
        padding = 50
        screenWidth = self.app.winfo_width()
        screenHeight = self.app.winfo_height()

        # Initial spawn location for the first button
        newX = random.uniform(padding / screenWidth, 1 - padding / screenWidth)
        newY = random.uniform(padding / screenHeight, 1 - padding / screenHeight)

        # Create a new button instance
        firstButton = CTkButton(
            master=self.app, text="❌", text_color="white",
            width=120, height=120,
            fg_color="#1A1A1A", hover_color="#373662",
            font=("Impact", 40)  # Set font
        )

        firstButton.configure(command=lambda btn=firstButton: self.first_button_clicked(btn))

        firstButton.place(relx=newX, rely=newY, anchor="center")
        self.buttons.append(firstButton)  # Store reference

    def first_button_clicked(self, button):
        """Called when the first X button is clicked."""
        self.counter += 1
        self.text.config(state=tk.NORMAL)
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", f"Current count: {self.counter}")
        self.text.config(state=tk.DISABLED)

        button.destroy()  # Destroy the first button
        self.buttons.remove(button)  # Remove from the list

        if not self.first_click:
            self.first_click = True  # Set the flag to True after the first click
            self.spawn_button()  # Start spawning more buttons after the first click

    def spawn_button(self):
        """Start spawning new X buttons after the first click."""
        if len(self.buttons) >= 10:
            self.end_game()  # End game if more than 10 buttons
            return
        
        if self.counter >= 100:
            self.win_game()  # Win game if counter reaches 100
            return

        padding = 50
        screenWidth = self.app.winfo_width()
        screenHeight = self.app.winfo_height()

        if self.buttons:
            last_button = self.buttons[-1]
            last_x = last_button.winfo_x() + last_button.winfo_width() / 2
            last_y = last_button.winfo_y() + last_button.winfo_height() / 2

            while True:
                newX = random.uniform(padding / screenWidth, 1 - padding / screenWidth)
                newY = random.uniform(padding / screenHeight, 1 - padding / screenHeight)

                new_x_pixels = newX * screenWidth
                new_y_pixels = newY * screenHeight

                distance = ((new_x_pixels - last_x) ** 2 + (new_y_pixels - last_y) ** 2) ** 0.5

                if 200 <= distance <= 500:  # Ensure new button is within a certain distance
                    break
        else:
            newX = random.uniform(padding / screenWidth, 1 - padding / screenWidth)
            newY = random.uniform(padding / screenHeight, 1 - padding / screenHeight)

        # Create a new button instance
        closeButton = CTkButton(
            master=self.app, text="❌", text_color="white",
            width=120, height=120,
            fg_color="#1A1A1A", hover_color="#373662",
            font=("Impact", 40)  # Set font
        )

        closeButton.configure(command=lambda btn=closeButton: self.button_clicked(btn))

        closeButton.place(relx=newX, rely=newY, anchor="center")
        self.buttons.append(closeButton)  # Store reference
        self.fade_in(closeButton, 0)  # Start fade-in

        # Schedule the next button spawn
        self.app.after(250, self.spawn_button)  # spawns an X every .25 seconds

    def fade_in(self, button, step):
        if step <= 10:
            intensity = int(42 + (26 * (step / 10)))  # Start from a darker shade and go lighter
            color = f"#{intensity:02x}{intensity:02x}{intensity:02x}" 
            button.configure(fg_color=color)
            self.app.after(50, self.fade_in, button, step + 1)  # Next step in 50ms

    def button_clicked(self, button):
        """Destroy only the button that was clicked."""
        self.counter += 1
        self.text.config(state=tk.NORMAL)
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", f"Current count: {self.counter}")
        self.text.config(state=tk.DISABLED)

        button.destroy()  # Destroy button
        self.buttons.remove(button)  # Remove from list

    def destroy_all_buttons(self):
        for button in self.buttons:
            button.destroy()
        self.buttons.clear()

    def end_game(self):
        self.destroy_all_buttons()  # Remove all buttons
        self.text.config(state=tk.NORMAL)
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", "Game Over! \nMore than 10 Xs!")
        self.text.config(font=("Impact", 64), fg="lightgray")  # Increase font size and change text color
        self.text.place(relx=0.5, rely=0.5, anchor="center")  # Center the text
        self.text.config(state=tk.DISABLED)
        self.app.after(5000, self.app.destroy)  # Close the app after 5 seconds

    def win_game(self):
        self.destroy_all_buttons()  # Remove all buttons
        self.text.config(state=tk.NORMAL)
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", "Congratulations! \nYou Win!")
        self.text.config(font=("Impact", 64), fg="lightgray")  # Increase font size and change text color
        self.text.place(relx=0.5, rely=0.5, anchor="center")  # Center the text
        self.text.config(state=tk.DISABLED)
        self.app.after(5000, self.app.destroy)  # Close the app after 5 seconds

    def get_button_count(self):
        return len(self.buttons)  # Return the number of buttons

    def run(self):
        self.app.mainloop()  # Run the application

myApp = SimpleApp()  # Create an instance
myApp.run()  # Run that instance
