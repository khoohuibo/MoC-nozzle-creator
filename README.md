# MoC-nozzle-creator
A simple python code written for an assignment which outputs in excel sheet as well as a pyplot graph to visualize the minimum length nozzle

To-do list:
1. Actually write proper comments
2. Clean up some iterative loops
3. Add pictures and equations manual/documentation on what actually happens

FAQ:
Q: Why didnt you do this in Excel like your professor asked you to?
A: Because I personally feel it is easier to modify functions that involve linear interpolation and such in Python, also because I'm more comfortable with it

Q: Why did you put in so much effort into an assignment worth 10%?
A: It's that moment of "Hey I'll add more functionality and so on and so forth" and it just kept going till it consumed my whole life

Q: How many hours did this take to make?
A: Approximately 2 afternoons worth of time, give-or-take

Q: Why does the code round to the nearest value when finding the Mach number for the points?
A: Because apparently the professor's code only works on nearest value, which is a bit suspicious considering that linear interpolation is a much easier function in python compared to rounding to nearest element in a list. See : np.interp vs bisect.left, which are part of the find_nearest function and linear_interpolation function found in the code

Q:Why did you write this readme when nobody's gonna read it?
A:Because I wanted to self-validate myself that I'm writing something useful that may or may not help someone else in the future.

Q:How do I contact you to flame you about some of the bad code you've written?
A:You can contact me on github, please dont flood me.

Q:Which course was this at which university, and where is the question sheet?
A: I'm not entirely sure I can legally give away assignment answers like that, so I'll leave it as a simple MoC calculator left to the public for usage.

Q: Your equations are wrong
A: That's not even a question, but yes they certainly might be, do put an issue flag on it and I'll work on it

Q: It's been a (insert_number_of_years), why havent you fixed it?
A: Because I got the 10% i wanted and I have other stuff to do, so this is a low priority repo
