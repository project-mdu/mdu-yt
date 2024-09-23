from PySide6.QtWidgets import QApplication, QListWidget, QListWidgetItem, QWidget, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class NoteListApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Notes")
        
        # Create the main layout
        layout = QVBoxLayout()
        
        # Create the QListWidget
        self.list_widget = QListWidget()
        
        # Create the items for the list
        note1 = QListWidgetItem("Note 1\n"
                                "evolution and some for goaffd fkqfgk to hmm let's go and kick the ball to\n"
                                "the swim hall of the school court hmm let's go and kick the ball to the swim\n"
                                "hmm let's go and kick the ball to the swim hmm let's go and kick the ball to the swim\n"
                                "let's go and kick the ball to the swim hmm let's go and kick the ball to the swim\n"
                                "let's go and kick the ball to the swim")
        note2 = QListWidgetItem("Note 2\nGet back to exercise, you hear me?")
        
        # Add notes to the list widget
        self.list_widget.addItem(note1)
        self.list_widget.addItem(note2)

        # Optional: Set a larger font for better visibility
        font = QFont()
        font.setPointSize(12)
        self.list_widget.setFont(font)
        
        # Select the second note to simulate the blue highlight
        self.list_widget.setCurrentItem(note2)
        self.list_widget.setSelectionMode(QListWidget.SingleSelection)
        self.list_widget.setFocus()

        # Add the list widget to the layout
        layout.addWidget(self.list_widget)

        # Set the layout for the main window
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication([])
    app.setStyle("fusion")
    window = NoteListApp()
    window.show()
    app.exec()
