import time
import tkinter as tk
from random import randint
from PIL import Image, ImageTk
import time

MOVE_INCREMENT = 20
starttime=time.time()



class Snake(tk.Canvas):
    def __init__(self):
        super().__init__(width=900, height=625, background="black", highlightthickness=0)

        self.snake_positions = [(100, 100), (80, 100), (60, 100)]
        self.food_position = self.set_new_food_position()
        self.direction = "Right"

        self.score = 0
        self.time=0
        self.hour=0
        self.seconds=0
        self.minu=0

        self.loadAssets()
        self.createObjects()

        self.bind_all("<Key>", self.on_key_press)

        self.pack()

        self.after(100, self.perform_actions)
        
    def loadAssets(self):
        try:
            self.snake_head_image = Image.open("snake_head2.png")
            self.snake_head = ImageTk.PhotoImage(self.snake_head_image)

            self.snake_body_image = Image.open("snake_body3.png")
            self.snake_body = ImageTk.PhotoImage(self.snake_body_image)

            self.food_image = Image.open("food.png")
            self.food = ImageTk.PhotoImage(self.food_image)

            self.arrow_image = Image.open("arrows.png")
            self.arrow=ImageTk.PhotoImage(self.arrow_image)

            self.snake_logo_image = Image.open("snake_game_logo.png")
            self.snake_logo=ImageTk.PhotoImage(self.snake_logo_image)

            self.game_signature_image = Image.open("snake_game_signature.png")
            self.game_signature=ImageTk.PhotoImage(self.game_signature_image)

        except IOError as error:
            print(error)
            root.destroy()

    def createObjects(self):
        self.create_text(90, 10, text=f"Score: {self.score} Time elapsed: {self.hour} : {self.minu} : {self.seconds} ", tag="score", fill="#fff")
        self.create_image(750, 200, image=self.arrow)
        self.create_image(750, 450, image=self.snake_logo)
        self.create_image(750, 585, image=self.game_signature)
        for x_position, y_position in self.snake_positions:
            if x_position==100 and y_position==100:
                self.create_image(x_position, y_position, image=self.snake_head, tag="snake")
            else:
                self.create_image(x_position, y_position, image=self.snake_body, tag="snake")

        self.create_image(*self.food_position, image=self.food, tag="food")
        self.create_rectangle(1,20,600,620,width=5,outline="#525d69")
        

    def check_collisions(self):
        head_x_position, head_y_position = self.snake_positions[0]

        if head_x_position in (0, 600) or head_y_position in (20, 620):
            return True
        elif (head_x_position, head_y_position) in self.snake_positions[1:]:
            return True

    def check_food_collision(self):
        if self.snake_positions[0] == self.food_position:
            self.score += 1
            self.snake_positions.append(self.snake_positions[-1])

            self.create_image(*self.snake_positions[-1], image=self.snake_body, tag="snake")
            self.food_position = self.set_new_food_position()
            self.coords(self.find_withtag("food"), *self.food_position)

            

    def end_game(self):
        self.delete(tk.ALL)
        self.create_text(
            self.winfo_width() / 2,
            self.winfo_height() / 2,
            text=f"Game over! You scored {self.score}!",
            fill="#fff"
        )
        self.after(1500,root.destroy)#Close the window automatically after 1000 ms once the game is over

    def move_snake(self):
        head_x_position, head_y_position = self.snake_positions[0]

        if self.direction == "Left":
            new_head_position = (head_x_position - MOVE_INCREMENT, head_y_position)
        elif self.direction == "Right":
            new_head_position = (head_x_position + MOVE_INCREMENT, head_y_position)
        elif self.direction == "Down":
            new_head_position = (head_x_position, head_y_position + MOVE_INCREMENT)
        elif self.direction == "Up":
            new_head_position = (head_x_position, head_y_position - MOVE_INCREMENT)


        self.snake_positions = [new_head_position] + self.snake_positions[:-1]

        for segment, position in zip(self.find_withtag("snake"), self.snake_positions):
            self.coords(segment, position)

    def on_key_press(self, e):
        if e.keysym in ("Up", "Down", "Left", "Right"):
            self.direction = e.keysym

    def perform_actions(self):
        self.time=round(time.time()-starttime,0)
        self.time=self.time%(24*3600)
        self.hour=round(self.time//3600)
        self.time%=3600
        self.minu=round(self.time//60)
        self.time%=60
        self.seconds=round(self.time)
        
        score = self.find_withtag("score")
        self.itemconfigure(score, text=f"Score: {self.score}  Time elapsed: {self.hour} : {self.minu} : {self.seconds} ", tag="score")
        if self.check_collisions():
            self.end_game()

        self.check_food_collision()
        self.move_snake()

        self.after(100, self.perform_actions)

    def set_new_food_position(self):
        while True:
            x_position = randint(1, 29) * MOVE_INCREMENT
            y_position = randint(3, 30) * MOVE_INCREMENT
            food_position = (x_position, y_position)

            if food_position not in self.snake_positions:
                return food_position


root = tk.Tk()
root.title("Snakes And Apples")
root.iconbitmap(r'hnet.com-image.ico')
board = Snake()
#root.attributes("-fullscreen", True)#If you want to open your screen in full window mode!! 
root.mainloop()
