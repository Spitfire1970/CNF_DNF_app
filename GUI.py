from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QSlider, QGroupBox, QLineEdit, QHBoxLayout, QSizePolicy, QCheckBox, QTextEdit, QButtonGroup, QGridLayout
from PyQt5.QtCore import Qt
from solveFormula import generate_formula, check
from leaderboard import read_leaderboard, update_user_record
import sys

global question
global answers
global difficulty
global dnf
global username
global user_input
global question_left
global lives
global score

window_width = 800
window_height = 600

## Main Page
class MainPage(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window properties
        self.setWindowTitle("Main Page")
        self.setGeometry(100, 100, window_width, window_height)

        # Add the main title
        self.main_title = QLabel("Propositional Logic Practice: DNF & CNF", self)
        self.main_title.setStyleSheet("font-family: 'Comic Sans MS'; font-size: 32px;")
        self.main_title.adjustSize()
        self.main_title.move((self.width() - self.main_title.width()) // 2, 50)


        # Set the font for the buttons
        font = QFont("roboto", 20)

        # Set Button Height and Button Width and x-coordinte
        button_width = 200
        button_height = 80
        button_x = (self.width() - button_width) // 2
        button_y = (self.height() - button_height) // 2

        # Button stylesheet
        button_style = """
        QPushButton {
            border: 5px solid black;
        }
        QPushButton:hover {
            background-color: lightgray;
        }
        QPushButton:pressed {
            background-color: grey;
        }
        """

        # Create the Start button
        self.start_button = QPushButton("Start", self)
        self.start_button.setFont(font)
        self.start_button.setGeometry(button_x, button_y - 100, button_width, button_height)
        self.start_button.setStyleSheet(button_style)
        self.start_button.clicked.connect(self.go_to_start)

        # Create the Leaderboard button
        self.leaderboard_button = QPushButton("Leaderboard", self)
        self.leaderboard_button.setFont(font)
        self.leaderboard_button.setGeometry(button_x, button_y, button_width, button_height)
        self.leaderboard_button.setStyleSheet(button_style)
        self.leaderboard_button.clicked.connect(self.go_to_leaderboard)

        # Create the Exit button
        self.exit_button = QPushButton("Exit", self)
        self.exit_button.setFont(font)
        self.exit_button.setGeometry(button_x, button_y + 100, button_width, button_height)
        self.exit_button.setStyleSheet(button_style)
        self.exit_button.clicked.connect(self.exit_application)

        # Footer
        self.footer = QLabel("Crafted with 💡 by 4 UCL Students in Group 2", self)
        self.footer.setStyleSheet("font-family: 'Comic Sans MS'; font-size: 14px;")
        self.footer.adjustSize()
        self.footer.move((self.width() - self.footer.width()) // 2, self.height() - self.footer.height() - 30)

    def go_to_start(self):
        self.start_page = StartPage()
        self.start_page.show()
        self.close()

    def go_to_leaderboard(self):
        scores = read_leaderboard()
        self.leaderboard_page = LeaderboardPage(scores)
        self.leaderboard_page.show()
        self.close()

    def exit_application(self):
        sys.exit()
    
## Leaderboard Page
class LeaderboardPage(QMainWindow):
    def __init__(self, scores):
        super().__init__()

        self.setWindowTitle("Leaderboard Page")
        self.setGeometry(100, 100, window_width, window_height)

        button_style = """
        QPushButton {
            border: 5px solid black;
        }
        QPushButton:hover {
            background-color: lightgray;
        }
        QPushButton:pressed {
            background-color: grey;
        }
        """

        # Set up central widget and layout
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 10, 50, 10)  # Larger side margins
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.label = QLabel()
        self.label.setText("Leaderboard")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-family: 'Comic Sans MS'; font-size: 32px; font-weight: bold;")  # Larger font size
        layout.addWidget(self.label)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Username", "Score"])
        self.table.setStyleSheet("font-family: 'Comic Sans MS'; font-size: 16px;")
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers) # Disable editing
        layout.addWidget(self.table)

        self.button = QPushButton()
        self.button.setText("Back")
        self.button.clicked.connect(self.go_to_main)
        self.button.setStyleSheet(button_style)
        self.button.setFixedWidth(150)
        self.button.setFixedHeight(80)
        layout.addWidget(self.button)
        layout.setAlignment(self.button, Qt.AlignmentFlag.AlignCenter)

        self.populate_table(scores)

        self.current_page = None

    def go_to_main(self):
        self.main_page = MainPage()
        self.main_page.show()
        self.close()

    def populate_table(self, scores):
        scores = {k: v for k, v in sorted(scores.items(), key=lambda item: item[1], reverse=True)}
        for i, user in enumerate(scores.keys()):
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(user))
            self.table.setItem(i, 1, QTableWidgetItem(str(scores[user])))

## Start Page
class StartPage(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Start")
        self.setGeometry(100, 100, window_width, window_height)
        button_style = """
        QPushButton {
            font-family: 'Comic Sans MS';
            font-size: 16px;
            padding: 10px;
            border: 2px solid black;
        }
        QPushButton:hover {
            background-color: lightgray;
        }
        QPushButton:pressed {
            font-family: 'Comic Sans MS';
            font-size: 16px;
            padding: 10px;
            background-color: grey;
        }
        """

        # Set up central widget and layout
        central_widget = QWidget()
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.label = QLabel("Choose Difficulty Level:")
        self.label.setStyleSheet("font-family: 'Comic Sans MS'; font-size: 24px;")
        layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(1, 3)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(1)
        self.slider.setFixedWidth(window_width // 2)
        self.slider.setStyleSheet("""
            QSlider::handle:horizontal {
                background-color: red;
                width: 20px;
                height: 20px;
                margin: -10px 0;
                border-radius: 10px;
            }
            QSlider::tick-label {
                font-family: 'Comic Sans MS';
                font-size: 14px;
            }
            QSlider::groove:horizontal {
                height: 10px;
            }
            QSlider::sub-page:horizontal {
                background: none;
            }
            QSlider::add-page:horizontal {
                background: none;
            }
            QSlider::tick:horizontal {
                background-color: black;
                width: 20px;
                height: 20px;
                border-radius: 10px;
                margin: -10px 0;
            }
        """)

        layout.addWidget(self.slider, alignment=Qt.AlignmentFlag.AlignCenter)

        hbox = QHBoxLayout()

        example_box = QGroupBox()
        example_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        example_box.setStyleSheet("""
            QGroupBox {
                font-family: 'Comic Sans MS';
                font-size: 18px;
                border: 2px solid black;
                margin-top: 1.2em;
            }
        """)
        example_layout = QVBoxLayout()
        example_box.setLayout(example_layout)

        example_title = QLabel("Example")
        example_title.setStyleSheet("font-family: 'Comic Sans MS'; font-size: 24px;")
        example_layout.addWidget(example_title, alignment=Qt.AlignmentFlag.AlignCenter)

        self.example_text = QLabel(f"{generate_formula(1)[0]}")
        self.example_text.setStyleSheet("font-family: 'Comic Sans MS'; font-size: 18px;")
        example_layout.addWidget(self.example_text, alignment=Qt.AlignmentFlag.AlignCenter)

        hbox.addWidget(example_box)

        layout.addWidget(self.slider, alignment=Qt.AlignmentFlag.AlignCenter)

        slider_labels_layout = QHBoxLayout()
        slider_labels_layout.setSpacing(window_width // 6 - 10)
        slider_labels_layout.setContentsMargins(window_width // 4, 0, window_width // 4, 0)
        for i in range(1, 4):
            label = QLabel(str(i))
            label.setStyleSheet("font-family: 'Comic Sans MS'; font-size: 14px;")
            slider_labels_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(slider_labels_layout)

        username_box = QGroupBox("Username")
        username_box.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        username_box.setStyleSheet("""
            QGroupBox {
                font-family:'Comic Sans MS';
                font-size: 18px;
                border: 2px solid black;
                margin-top: 1.2em;
                }
                QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                }
            """)
        username_layout = QVBoxLayout()
        username_box.setLayout(username_layout)
        self.username_input = QLineEdit()
        self.username_input.setStyleSheet("font-family: 'Comic Sans MS'; font-size: 14px;")
        username_layout.addWidget(self.username_input)
        hbox.addWidget(username_box)

        layout.addLayout(hbox)

        self.button = QPushButton("Go")
        self.button.setStyleSheet(button_style)

        self.button.setFixedSize(100, 50)
        self.button.clicked.connect(self.go_to_go)
        layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignRight)

        self.close_button = QPushButton("X", self)
        self.close_button.setStyleSheet("font-family: 'Comic Sans MS'; font-size: 12px;")
        self.close_button.setFixedSize(30, 30)
        self.close_button.clicked.connect(self.go_to_main)
        self.close_button.move(10, 10)
        self.current_page = None

        self.slider.valueChanged.connect(self.update_example)
        
    def update_example(self):
        new_difficulty = self.slider.value()
        new_example_text = generate_formula(new_difficulty)[0]
        self.example_text.setText(new_example_text)

    def go_to_main(self):
        self.main_page = MainPage()
        self.main_page.show()
        self.close()

    def go_to_go(self):
        global difficulty, question_left, lives, score, username
        username = "anonymous" if self.username_input.text() == "" else self.username_input.text().replace(" ", "-")
        difficulty = self.slider.value()
        question_left = 10
        lives = 3
        score = 0
        self.go_page = GoPage()
        self.go_page.show()
        self.close()

## Go Page
class GoPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Go Page")
        self.init_ui()

    def init_ui(self):
        button_style = """
        QPushButton {
            border: none;
            border-radius: 5px;
            padding: 5px;
            font-size: 14px;
            font-family: "Comic Sans MS";
            color: black;
            background-color: white;
        }
        QPushButton:hover {
            background-color: lightgray;
        }
        QPushButton:pressed {
            background-color: gray;
        }
        """

        symbol_style = """
        QPushButton {
            border: 1px solid black;
            border-radius: 5px;
            padding: 5px;
            font-size: 14px;
            font-family: "Comic Sans MS";
            color: black;
            background-color: white;
        }
        QPushButton:hover {
            background-color: lightgray;
        }
        QPushButton:pressed {
            background-color: gray;
        }
        """

        # Create the top box with text centered
        top_box = QGroupBox(self)
        top_box.setStyleSheet("QGroupBox {border: 2px solid black; margin-top: 1.2em;}")
        top_box_layout = QVBoxLayout(top_box)
        top_box_layout.setContentsMargins(20, 20, 20, 0)
        top_box_layout.setSpacing(10)
        global question, answers
        question, answers = generate_formula(difficulty)
        top_label = QLabel(question, top_box)
        top_label.setAlignment(Qt.AlignCenter)
        top_label.setFont(QFont("Comic Sans MS", 20))
        top_box_layout.addWidget(top_label)

        # Create the labels for lives, score, and checkboxes
        lives_label = QLabel("Lives: " + "X"*lives, self)
        score_label = QLabel(f"Score: {score}", self)
        cnf_checkbox = QCheckBox("CNF", self)
        self.dnf_checkbox = QCheckBox("DNF", self)
        lives_label.setFont(QFont("Comic Sans MS", 18))
        score_label.setFont(QFont("Comic Sans MS", 18))
        cnf_checkbox.setFont(QFont("Comic Sans MS", 18))
        self.dnf_checkbox.setFont(QFont("Comic Sans MS", 18))

        # Create a button group for the checkboxes and make them mutually exclusive
        checkbox_group = QButtonGroup(self)
        checkbox_group.addButton(cnf_checkbox)
        checkbox_group.addButton(self.dnf_checkbox)
        checkbox_group.setExclusive(True)
        checkbox_group.buttonToggled.connect(self.handle_checkbox)
        self.dnf_checkbox.setChecked(True)  # set CNF as the default choice
        checkbox_layout = QHBoxLayout()
        checkbox_layout.addWidget(lives_label)
        checkbox_layout.addWidget(score_label)
        checkbox_layout.addWidget(self.dnf_checkbox)
        checkbox_layout.addWidget(cnf_checkbox)
        checkbox_layout.setSpacing(10)
        checkbox_layout.setContentsMargins(20, 20, 20, 0)

        # Create the input box and button to go to SolutionPage
        self.input_box = QLineEdit(self)  # Add 'self.' before input_box
        input_button = QPushButton("Solve", self)
        input_button.clicked.connect(self.go_to_solution)
        input_button.setStyleSheet(button_style)
        self.input_box.setFont(QFont("Comic Sans MS", 14))  # Add 'self.' before input_box
        input_button.setFont(QFont("Comic Sans MS", 14))
        input_layout = QVBoxLayout()  # Change this to QVBoxLayout
        input_layout.addWidget(self.input_box)  # Add
        # the input box to input_layout
        input_layout.addWidget(input_button)
        input_layout.setSpacing(20)
        input_layout.setContentsMargins(20, 20, 20, 0)

        keyboard_widget = QWidget(self)
        keyboard_layout = self.create_keyboard(symbol_style)
        keyboard_widget.setLayout(keyboard_layout)
        keyboard_widget.setFocusProxy(self.input_box)  # Add this line to set the focus proxy

        # Add all the widgets to the main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(top_box)
        main_layout.addLayout(checkbox_layout)
        main_layout.addLayout(input_layout)
        main_layout.addWidget(keyboard_widget)  # This line has been changed
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Set the main layout and size of the window
        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        self.setGeometry(100, 100, 800, 600)

        # Add back button to the toolbar
        self.close_button = QPushButton("X", self)
        self.close_button.setStyleSheet("font-family: 'Comic Sans MS'; font-size: 12px;")
        self.close_button.setFixedSize(30, 30)
        self.close_button.clicked.connect(self.back_button_clicked)
        self.close_button.move(10, 10)
        self.current_page = None

    def create_keyboard(self, symbol_style):
        symbols = ['¬', '∧', '∨', '→', '↔', '(', ')']
        keyboard_layout = QGridLayout()

        for i, symbol in enumerate(symbols):
            button = QPushButton(symbol, self)
            button.setFont(QFont("Comic Sans MS", 14))
            button.setStyleSheet(symbol_style)
            button.clicked.connect(lambda checked, s=symbol: self.add_symbol(s))
            keyboard_layout.addWidget(button, i // 4, i % 4)

        return keyboard_layout
    
    def add_symbol(self, symbol):
        current_text = self.input_box.text()
        self.input_box.setText(current_text + symbol)


    def handle_checkbox(self, button, checked):
        if checked:
            print(f"{button.text()} checkbox checked")
        else:
            print(f"{button.text()} checkbox unchecked")

    def go_to_solution(self):
        global user_input, dnf, question_left
        user_input = self.input_box.text()
        dnf = 0 if self.dnf_checkbox.isChecked() else 1
        question_left -= 1
        self.go_page = SolutionPage()
        self.go_page.show()
        self.close()

    def back_button_clicked(self):
        self.start_page = StartPage()
        self.start_page.show()
        self.close()

## Solution Page
class SolutionPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Solution Page")
        self.init_ui()

    def init_ui(self):
        button_style = """
        QPushButton {
            border: 2px solid black;
        }
        QPushButton:hover {
            background-color: lightgray;
        }
        QPushButton:pressed {
            background-color: grey;
        }
        """
        check_answer = check(user_input, answers, dnf)
        if check_answer != "Answer Correct":
            global lives
            lives -= 1
        else:
            global score
            score += 2**difficulty
        
        # Create the top box with text centered
        top_box = QGroupBox(self)
        top_box.setStyleSheet("QGroupBox {border: 2px solid black; margin-top: 1.2em;}")
        top_box_layout = QVBoxLayout(top_box)
        top_box_layout.setContentsMargins(20, 20, 20, 0)
        top_box_layout.setSpacing(10)
        top_label = QLabel("Solution and Explanation", top_box)
        top_label.setAlignment(Qt.AlignCenter)
        top_label.setFont(QFont("Comic Sans MS", 20))
        top_box_layout.addWidget(top_label)

        # Create the labels for lives and score
        lives_label = QLabel("Lives: " + "X"*lives, self)
        score_label = QLabel(f"Score: {score}", self)
        lives_label.setFont(QFont("Comic Sans MS", 18))
        score_label.setFont(QFont("Comic Sans MS", 18))
        lives_score_layout = QHBoxLayout()
        lives_score_layout.addWidget(lives_label)
        lives_score_layout.addWidget(score_label)
        lives_score_layout.setSpacing(10)
        lives_score_layout.setContentsMargins(20, 20, 20, 0)

        # Create the Answer and Explanation box
        answer_explanation_box = QTextEdit(self)
        answer_explanation_box.setFixedHeight(300)
        answer_explanation_box.setStyleSheet("QTextEdit {border: 2px solid black;}")
        answer_explanation_box.setReadOnly(True)
        answer_explanation_box.setFont(QFont("Comic Sans MS", 14))
        answer_explanation_box.setHtml(
            "<p style='font-size: 18px; font-weight: bold; text-align: center;'>Your Answer:</p>"
            f"<p style='text-align: center;'>{user_input}</p>"
            "<p style='font-size: 18px; font-weight: bold; text-align: center;'>Correct Answer:</p>"
            f"<p style='text-align: center;'>{answers[dnf]}</p>"
            f"<p style='text-align: center;'>{check(user_input, answers, dnf)}</p>"
        )
        answer_explanation_layout = QHBoxLayout()
        answer_explanation_layout.addWidget(answer_explanation_box)
        answer_explanation_layout.setContentsMargins(20, 20, 0, 20)

        # Create the Next button to go to ScorePage
        next_button = QPushButton("Next", self)
        next_button.setFont(QFont("Comic Sans MS", 14))
        next_button.setStyleSheet(button_style)
        next_button.clicked.connect(self.go_to_next)
        next_button_layout = QHBoxLayout()
        next_button_layout.addWidget(next_button)
        next_button_layout.setContentsMargins(0, 0, 20, 20)
        next_button_layout.setAlignment(Qt.AlignRight | Qt.AlignBottom)

        # Add all the widgets to the main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(top_box)
        main_layout.addLayout(lives_score_layout)
        main_layout.addLayout(answer_explanation_layout)
        main_layout.addLayout(next_button_layout)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Set the main layout and size of the window
        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        self.setGeometry(100, 100, 800, 600)

        # Add back button to the toolbar
        self.close_button = QPushButton("X", self)
        self.close_button.setStyleSheet("font-family: 'Comic Sans MS'; font-size: 12px;")
        self.close_button.setFixedSize(30, 30)
        self.close_button.clicked.connect(self.back_button_clicked)
        self.close_button.move(10, 10)
        self.current_page = None

    def go_to_next(self):
        if question_left and lives:
            self.go_to_next = GoPage()
        else:
            self.go_to_next = ScorePage()
        self.go_to_next.show()
        self.close()

    def go_to_go_page(self):
        self.go_page = GoPage()
        self.go_page.show()
        self.close()

    def back_button_clicked(self):
        self.go_to_go_page()


## Score Page
class ScorePage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.update_score()
        self.setWindowTitle("Score Page")
        self.init_ui()

    def init_ui(self):
        button_style = """
        QPushButton {
            border: 5px solid black;
        }
        QPushButton:hover {
            background-color: lightgray;
        }
        QPushButton:pressed {
            background-color: grey;
        }
        """

        # Create the top box with text centered
        top_box = QGroupBox(self)
        top_box.setStyleSheet("QGroupBox {border: 2px solid black; margin-top: 0.2em;}")
        top_box_layout = QVBoxLayout(top_box)
        top_box_layout.setContentsMargins(20, 5, 20, 0)
        top_box_layout.setSpacing(5)
        top_label = QLabel(f"     Your Final Score: {score}     ", top_box)
        top_label.setAlignment(Qt.AlignCenter)
        top_label.setFont(QFont("Comic Sans MS", 24))
        top_box_layout.addWidget(top_label)

        # Create the box with high score
        high_score_box = QGroupBox(self)
        high_score_box.setStyleSheet("QGroupBox {border: 2px solid black; margin-top: 0.2em;}")
        high_score_layout = QVBoxLayout(high_score_box)
        high_score_layout.setContentsMargins(20, 5, 20, 0)
        high_score_layout.setSpacing(5)
        high_score_label = QLabel(f"       Your Highest Score: {self.highest_history}      ", high_score_box)
        high_score_label.setAlignment(Qt.AlignCenter)
        high_score_label.setFont(QFont("Comic Sans MS", 24))
        high_score_layout.addWidget(high_score_label)

        # Create the "Try Again" button
        try_again_button = QPushButton("Try Again", self)
        try_again_button.setFont(QFont("Comic Sans MS", 18))
        try_again_button.setStyleSheet(button_style)
        try_again_button.setFixedSize(130, 50)
        try_again_button.clicked.connect(self.go_to_start_page)
        try_again_layout = QHBoxLayout()
        try_again_layout.addWidget(try_again_button, alignment=Qt.AlignCenter)
        try_again_layout.setContentsMargins(0, 5, 0, 5)
        try_again_layout.setSpacing(5)

        # Create the "Back" button
        back_button = QPushButton("Back", self)
        back_button.setFont(QFont("Comic Sans MS", 18))
        back_button.setStyleSheet(button_style)
        back_button.setFixedSize(100, 50)
        back_button.clicked.connect(self.go_to_home_page)
        back_layout = QHBoxLayout()
        back_layout.addWidget(back_button, alignment=Qt.AlignCenter)
        back_layout.setContentsMargins(0, 5, 0, 5)
        back_layout.setSpacing(5)

        # Add all the widgets to the main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(top_box, alignment=Qt.AlignCenter)
        main_layout.addWidget(high_score_box, alignment=Qt.AlignCenter)
        main_layout.addLayout(try_again_layout)
        main_layout.addLayout(back_layout)
        main_layout.setSpacing(5)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Set the main layout and size of the window
        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        self.setGeometry(100, 100, 800, 600)

    def update_score(self):
        global username, score
        self.highest_history = update_user_record(username, score)

    def go_to_start_page(self):
        self.start_page = StartPage()
        self.start_page.show()
        self.close()

    def go_to_home_page(self):
        self.home_page = MainPage()
        self.home_page.show()
        self.close()

def run_app():
    app = QApplication(sys.argv)
    main_page = MainPage()
    main_page.show()
    sys.exit(app.exec())

## Main
if __name__ == '__main__':
    run_app()