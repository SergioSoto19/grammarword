class Grammar:
    def __init__(self):
        self.terminals = []
        self.non_terminals = []
        self.axiom = ""
        self.productions = {}

    def set_data(self, terminals, non_terminals, axiom, productions):
        self.terminals = terminals
        self.non_terminals = non_terminals
        self.axiom = axiom
        self.productions = productions

    def add_production(self, non_terminal, production):
        if non_terminal in self.productions:
            self.productions[non_terminal].append(production)
        else:
            self.productions[non_terminal] = [production]


    def parse_productions(self, productions_text):
        try:
            for production in productions_text.split(';'):
                left, right = production.split(',')
                non_terminal = left.strip()
                rhs_productions = [r.strip() for r in right.split('|')]
                for prod in rhs_productions:
                    self.add_production(non_terminal, prod)
        except ValueError:
            raise ValueError("Formato de producción no es el adecuado")

    def display_grammar(self):
        print("Terminales:", self.terminals)
        print("No Terminales:", self.non_terminals)
        print("Axioma:", self.axiom)
        #print("Producciones:", self.productions)
        print("Producciones:")
        for left, rights in self.productions.items():
            print(f"{left} -> {' | '.join(rights)}")

     
    def derive(self, word):
        
        def derive_step(current_string, target_word, steps, productions_used):
            if current_string == target_word:
                return True, steps, productions_used
            if len(current_string) > len(target_word):
                return False, steps, productions_used
            
            for i, symbol in enumerate(current_string):
                if symbol in self.non_terminals:
                    for production in self.productions[symbol]:
                        new_string = current_string[:i] + production + current_string[i+1:]
                        steps.append(f"{current_string} -> {new_string}")
                        productions_used.append(f"{symbol} -> {production}")
                        success, result_steps, result_productions = derive_step(new_string, target_word, steps, productions_used)
                        if success:
                            return True, result_steps, result_productions
                        steps.pop()  # Retroceder si el paso no lleva a la solución
                        productions_used.pop()  # Retroceder la producción también
            return False, steps, productions_used

        success, steps, productions_used = derive_step(self.axiom, word, [], [])
        derivations = list(zip(productions_used, steps))

        print(f"\nDerivación para la palabra '{word}':")
        print(derivations, "\n estado derivacion: ", success) 
        
        return derivations, success

      