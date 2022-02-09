import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QTextCursor, QColor
from PyQt5.QtWidgets import QApplication, QTextEdit, QAction, QMainWindow, QFileDialog, \
    QMessageBox, QInputDialog, QFontDialog, QColorDialog


class MyFirstNotepad(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initialize_ui()

    def initialize_ui(self):
        self.setGeometry(150, 150, 450, 550)
        self.setWindowTitle("My Notepad")
        self.create_my_notepad()
        self.my_notepad_menu()
        self.show()

    def create_my_notepad(self):
        self.text_field = QTextEdit()
        self.setCentralWidget(self.text_field)

    def my_notepad_menu(self):
        # File menu
        new_file = QAction(QIcon("images/new.png"), "New File", self)
        new_file.setShortcut("Ctrl + N")
        new_file.triggered.connect(self.clear_text)

        open_file = QAction(QIcon("images/open.jpeg"), "Open File", self)
        open_file.setShortcut("Ctrl + O")
        open_file.triggered.connect(self.open_file)

        save_file = QAction(QIcon("images/save.jpeg"), "Save File", self)
        save_file.setShortcut("Ctrl + S")
        save_file.triggered.connect(self.save_to_file)

        exit_file = QAction(QIcon("images/exit.jpeg"), "Exit File", self)
        exit_file.setShortcut("Ctrl + Q")
        exit_file.triggered.connect(self.close)

        # Edit menu
        undo_text = QAction(QIcon("images/undo.jpg"), "Undo Text", self)
        undo_text.setShortcut("Ctrl + Z")
        undo_text.triggered.connect(self.text_field.undo)

        redo_text = QAction(QIcon("images/redo.png"), "Redo Text", self)
        redo_text.setShortcut("Ctrl + Shift + Z")
        redo_text.triggered.connect(self.text_field.redo)

        copy_text = QAction(QIcon("images/copy.jpeg"), "Copy Text", self)
        copy_text.setShortcut("Ctrl + C")
        copy_text.triggered.connect(self.text_field.copy)

        paste_text = QAction(QIcon("images/paste.jpeg"), "Paste Text", self)
        paste_text.setShortcut("Ctrl + V")
        paste_text.triggered.connect(self.text_field.paste)

        # Tools Menu
        font_tool = QAction(QIcon("images/font_image.png"), "Font", self)
        font_tool.setShortcut("Ctrl + T")
        font_tool.triggered.connect(self.choose_font)

        color_tool = QAction(QIcon("images/color.jpeg"), "Color", self)
        color_tool.setShortcut("Ctrl + D")
        color_tool.triggered.connect(self.choose_color)

        highlight_tool = QAction(QIcon("images/highlight.jpeg"), "Highlight", self)
        highlight_tool.setShortcut("Ctrl + H")
        highlight_tool.triggered.connect(self.choose_background)

        # Help & Find menu
        help_tool = QAction("Help About", self)
        help_tool.triggered.connect(self.help_dialog)

        find_text = QAction(QIcon("images/find.jpeg"), "Find Text", self)
        find_text.setShortcut("Ctrl + F")
        find_text.triggered.connect(self.finding_text)

        # Menubar
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)

        # Creating file menu & Actions
        file_menu = menu_bar.addMenu("Files")
        file_menu.addAction(new_file)
        file_menu.addSeparator()
        file_menu.addAction(open_file)
        file_menu.addAction(save_file)
        file_menu.addSeparator()
        file_menu.addAction(exit_file)

        # Creating edit menu & Actions
        edit_menu = menu_bar.addMenu("Edit")
        edit_menu.addAction(undo_text)
        edit_menu.addAction(redo_text)
        edit_menu.addSeparator()
        edit_menu.addAction(copy_text)
        edit_menu.addAction(paste_text)

        # Creating Tools menu & Actions
        tool_menu = menu_bar.addMenu("Tools")
        tool_menu.addAction(font_tool)
        tool_menu.addSeparator()
        tool_menu.addAction(color_tool)
        tool_menu.addSeparator()
        tool_menu.addAction(highlight_tool)

        # Creating Help & Find menu & Actions
        help_menu = menu_bar.addMenu("Help / Find")
        help_menu.addAction(help_tool)
        help_menu.addSeparator()

        # Find and Replace Menu
        find_menu = help_menu.addMenu("Find And Replace")
        find_menu.addAction(find_text)

    def clear_text(self):
        questions = QMessageBox.question(self, "Clear Text", "Are you sure you want to clear the text?",
                                         QMessageBox.No | QMessageBox.Yes, QMessageBox.No)

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "HTML Files (*.html);;"
                                                                          "Text Files (*.txt);;CSV Files (*.csv)")
        if file_name:
            with open(file_name, "r") as file:
                self.text_field.setText(file.read())
        else:
            QMessageBox.information(self, "Error", "Unable to open the file.", QMessageBox.Ok)

    def save_to_file(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "HTML Files (*.html);;"
                                                                          "Text Files (*.txt);;CSV Files (*.csv)")
        if file_name.endswith(".txt"):
            with open(file_name, "w") as file:
                file.write(self.text_field.toPlainText())
        elif file_name.endswith(".html"):
            with open(file_name, "w") as file:
                file.write(self.text_field.toHtml())
        elif file_name.endswith(".csv"):
            with open(file_name, "w") as file:
                file.write(self.text_field.toCsv())
        else:
            QMessageBox.information(self, "Error", "Unable to save file.", QMessageBox.Ok)

    def choose_font(self):
        now_font = self.text_field.currentFont()
        font, ok = QFontDialog.getFont(now_font, self, options=QFontDialog.DontUseNativeDialog)
        if ok:
            self.text_field.setCurrentFont(font)
        self.text_field.setCurrentFont(font)

    def choose_color(self):
        colors = QColorDialog.getColor()
        if colors.isValid():
            self.text_field.setTextColor(colors)

    def choose_background(self):
        colors = QColorDialog.getColor()
        if colors.isValid():
            self.text_field.setTextColor(colors)

    def help_dialog(self):
        QMessageBox.help(self, "Help to Notepad", "Rich Notepad")

    def finding_text(self):
        find_text, ok = QInputDialog.getText(self, "Search For Text", "Find:")
        all_selections = []

        if ok and not self.text_field.isReadOnly():
            self.text_field.moveCursor(QTextCursor.Start)
            colors = QColor(Qt.purple)

            while self.text_field.find(find_text):
                selection = QTextEdit.ExtraSelection()
                selection.format.setBackground(colors)

                selection.cursor = self.text_field.textCursor()

                all_selections.append(selection)

            for _ in all_selections:
                self.text_field.setExtraSelections(all_selections)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyFirstNotepad()
    sys.exit(app.exec_())
