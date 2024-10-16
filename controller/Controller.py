from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QFileDialog, QMessageBox


class Controller:
    def __init__(self, ui, model):
        self.ui = ui
        self.model = model
        self.grammar_saved = False 
        self.connect_signals()

    def connect_signals(self):
        self.ui.pushButton_generate_gra.clicked.connect(self.generate_grammar)
        self.ui.pushButton_validate_W.clicked.connect(self.validate_word)
        self.ui.pushButton_deriva_2.clicked.connect(self.reset_interface)
        self.ui.pushButton_load_gra.clicked.connect(self.load_grammar_file)

    def generate_grammar(self):
        terminals = self.ui.lineEdit_Terminal.text().split(',')
        non_terminals = self.ui.lineEdit_nterminal_.text().split(',')
        axiom = self.ui.lineEdit_noterminal_2.text()
        productions = self.ui.lineEdit_produ.text()

        self.model.set_data(terminals, non_terminals, axiom, {})
        try:
            self.model.parse_productions(productions)
            self.model.display_grammar()
            self.update_grammar_display()
            self.grammar_saved = True 
        except ValueError as e:
            self.show_error_message(str(e))


    def update_grammar_display(self):
        grammar_text = "Terminales: {}\nNo Terminales: {}\nAxioma: {}\nProducciones:\n".format(
            self.model.terminals, self.model.non_terminals, self.model.axiom)
        for left, rights in self.model.productions.items():
            grammar_text += "{} -> {}\n".format(left, " | ".join(rights))
        self.ui.label_home.setText(grammar_text)

    
    def validate_word(self):
        if not self.grammar_saved:
            self.show_error_message("Primero debe ingresar una gramática para validar la palabra.")
            return

        word = self.ui.lineEdit_Terminal_3.text()
        derivations, is_valid = self.model.derive(word)

        if is_valid:
            self.ui.labe_Terminal_4.setText("VALIDA")
        else:
            self.ui.labe_Terminal_4.setText("NO VALIDA")

        self.update_table_widget(derivations)


    def show_error_message(self, message):
        error_dialog = QtWidgets.QMessageBox()
        error_dialog.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        error_dialog.setWindowTitle("Error")
        error_dialog.setText(message)
        error_dialog.exec()

    def reset_interface(self):
        self.ui.lineEdit_Terminal.clear()
        self.ui.lineEdit_nterminal_.clear()
        self.ui.lineEdit_noterminal_2.clear()
        self.ui.lineEdit_produ.clear()
        self.ui.lineEdit_Terminal_3.clear()
        self.ui.label_home.setText("")
        self.ui.labe_Terminal_4.setText("")
        self.ui.tableWidget.setRowCount(0)
        
        self.model.set_data([], [], "", {})
        self.grammar_saved = False

    def load_grammar_file(self):
        # Abrir cuadro de diálogo para seleccionar el archivo
        file_name, _ = QFileDialog.getOpenFileName(None, "Seleccionar archivo de gramática", "", "Text Files (*.txt);;All Files (*)")

        if file_name:
            try:
                # Leer el archivo seleccionado
                with open(file_name, 'r', encoding='utf-8') as file:
                    grammar_text = file.read()

                    # Parsear las producciones desde el archivo de texto
                    self.parse_grammar(grammar_text)

                    # Actualizar la interfaz con la nueva gramática cargada
                    self.update_grammar_display()

            except Exception as e:
                # Mostrar un mensaje de error si ocurre una excepción
                QMessageBox.critical(None, "Error", f"No se pudo leer el archivo: {e}")

    def parse_grammar(self, grammar_text):
        lines = grammar_text.splitlines()

        terminals = set()
        non_terminals = set()
        productions = {}

        for line in lines:
            if '->' in line:
                left, right = line.split('->')
                left = left.strip()
                non_terminals.add(left)  # Agregar no terminal
                rhs_productions = [r.strip() for r in right.split('|')]

                for production in rhs_productions:
                    # Identificar terminales en la producción
                    for symbol in production:
                        if symbol.islower() or symbol.isdigit():
                            terminals.add(symbol)
                    # Agregar la producción al modelo
                    self.model.add_production(left, production)

        # Establecer datos en el modelo
        self.model.set_data(list(terminals), list(non_terminals), 'S', self.model.productions)  # 'S' como axioma predeterminado
        print(self.model.productions)
        self.grammar_saved = True 


    
        
    def update_table_widget(self, derivations):
        self.ui.tableWidget.setRowCount(len(derivations))
        for row, (production, derivation) in enumerate(derivations):
            self.ui.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(production))
            self.ui.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(derivation))