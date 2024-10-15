class Grammar:
    def __init__(self):
        self.terminals = []
        self.non_terminals = []
        self.axiom = ""
        self.productions = {}

    def set_data(self, terminals, non_terminals, axiom, productions):
        # """Establecer los datos de la gramática."""
        self.terminals = terminals
        self.non_terminals = non_terminals
        self.axiom = axiom
        self.productions = productions

    def add_production(self, non_terminal, production):
        #  """Añadir una producción a un no terminal."""
        if non_terminal in self.productions:
            self.productions[non_terminal].append(production)
        else:
            self.productions[non_terminal] = [production]


    def parse_productions(self, productions_text):
        # Analizar y agregar producciones desde el texto dado
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
            print(f"Derivando: {current_string} | Objetivo: {target_word}")  # Mostrar estado actual
            # Si la cadena actual es igual a la palabra objetivo, hemos tenido éxito
            if current_string == target_word:
                return True, steps, productions_used
            
            # Si la longitud de la cadena actual es mayor que la de la palabra objetivo, falla
            if len(current_string) > len(target_word):
                return False, steps, productions_used

            for i, symbol in enumerate(current_string):
                print("paaaaaa", current_string)
                if symbol in self.non_terminals:
                    for production in self.productions[symbol]:
                        print("la produccion es:" , production)
                       
                        # Si la producción es λ, eliminamos el símbolo no terminal
                        if production == 'λ' or production == 'ϵ':
                            print("terminal simbolo", symbol)
                            print("esssAntenewna", new_string)
                            new_string = new_string.replace(symbol, '')
                            #print("esss actual ", current_string)
                            #print("coje el valor antes de la cadena ", current_string[:i])
                            #print("coje el valor despues de la cadena ", current_string[i + 1:])
                            #print("es", i )
                            #print("esdddd", new_string[:i+1 ] +new_string[i +2:])
                            #new_string = new_string[:i] + current_string[i + 1:]
                           # new_string = new_string[:i+1 ] +new_string[i +2:]
                           # print("esss", new_string)
                        else:
                            new_string = current_string[:i] + production + current_string[i + 1:]

                        steps.append(f"{current_string} -> {new_string}")
                        productions_used.append(f"{symbol} -> {production}")

                        # Intentamos derivar desde la nueva cadena
                        success, result_steps, result_productions = derive_step(new_string, target_word, steps, productions_used)

                        if success:
                            return True, result_steps, result_productions
                        # Retrocedemos si la derivación no fue exitosa
                        steps.pop()
                        productions_used.pop()

            return False, steps, productions_used

        success, steps, productions_used = derive_step(self.axiom, word, [], [])
        derivations = list(zip(productions_used, steps))

        print(f"\nDerivación para la palabra '{word}':")
        for production, step in derivations:
            print(f"{production}: {step}")
        print("\nEstado de derivación:", success)
        
        return derivations, success


"""
# Ejemplo de uso
grammar = Grammar()
grammar.set_data(
    terminals=['a', 'b'],
    non_terminals=['S'],
    axiom='S',
    productions={'S': ['aSb', 'λ']}
)

grammar.display_grammar()

# Derivar la palabra 'ab'
print("\nDerivando 'ab':")
grammar.derive('ab')



# Ejemplo dos
grammar_2 = Grammar()
grammar_2.set_data(
    terminals=['a', 'b'],
    non_terminals=['S', 'A'],
    axiom='S',
    productions={
        'S': ['aA', 'bA'],  # Producciones de S
        'A': ['λ']          # Producción de A
    }
)

grammar_2.display_grammar()

# Derivar la palabra 'a'
print("\nDerivando 'a':")
grammar_2.derive('a')

# Derivar la palabra vacía
#print("\nDerivando la cadena vacía:")
#grammar_2.derive('')


#ejemplo 3

grammar_3  = Grammar()
grammar_3.set_data(
    terminals=['a', 'b'],
    non_terminals=['S,A,B'],
    axiom='S',
    productions={'S': ['aAB','aA','λ'],
                 'B':['bB','λ']}
)

grammar_3.display_grammar()

# Derivar la palabra 'a'
print("\nDerivando 'a':")
grammar_3.derive('ab')
"""