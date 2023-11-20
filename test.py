import inquirer

questions = [
    inquirer.List(
        "size",
        message="What size do you need?",
        choices=["Jumbo", "Large", "Standard", "Medium", "Small", "Micro"],
    ),
    inquirer.Checkbox(
        "interests",
        message="What are you interested in? (Press <space> to select, <return> to submit))",
        choices=["Computers", "Books", "Science", "Nature", "Fantasy", "History"],
    ),
]
answers = inquirer.prompt(questions)
print(answers)
