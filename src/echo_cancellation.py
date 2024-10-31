#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

'''Echo cancellation (template).'''

import logging

import minimal
import buffer
import numpy as np
        
# class Echo_Cancellation(buffer.Buffering):
#     def __init__(self):
#         super().__init__()
#         logging.info(__doc__)

class Echo_Cancellation(buffer.Buffering):
    def __init__(self, echo_delay=11):  # echo_delay en número de chunks (ajustar según sea necesario)
        super().__init__()
        logging.info(__doc__)
        self.echo_delay = echo_delay
        self.buffer = []  # Buffer para almacenar chunks anteriores

    def remove_echo(self, current_chunk):
        """Restar el eco de la señal actual usando el buffer de señales anteriores."""
        if len(self.buffer) < self.echo_delay:
            # Si el buffer no está lleno, solo agrega el fragmento actual
            self.buffer.append(current_chunk)
            return current_chunk

        for i in self.buffer:
            print(np.max(buffer[i]))
        # Si el buffer está lleno, retira el fragmento más antiguo y añade el actual
        delayed_chunk = self.buffer.pop(0)  # Fragmento con retardo
        self.buffer.append(current_chunk)   # Añade el fragmento actual


        for i in self.buffer:
            print(np.max(buffer[i]))

        # Resta el eco (delayed_chunk) a la señal actual (current_chunk)
        return current_chunk - 2*delayed_chunk

    def process_chunk(self, chunk):
        """Procesa el chunk antes de enviarlo o reproducirlo."""
        chunk = self.remove_echo(chunk)
        return chunk


        
class Echo_Cancellation__verbose(Echo_Cancellation, buffer.Buffering__verbose):
    def __init__(self):
        super().__init__()

try:
    import argcomplete  # <tab> completion for argparse.
except ImportError:
    logging.warning("Unable to import argcomplete (optional)")

if __name__ == "__main__":
    minimal.parser.description = __doc__
    try:
        argcomplete.autocomplete(minimal.parser)
    except Exception:
        logging.warning("argcomplete not working :-/")
    minimal.args = minimal.parser.parse_known_args()[0]

    if minimal.args.show_stats or minimal.args.show_samples or minimal.args.show_spectrum:
        intercom = Echo_Cancellation__verbose()
    else:
        intercom = Echo_Cancellation()
    try:
        intercom.run()
    except KeyboardInterrupt:
        minimal.parser.exit("\nSIGINT received")
    finally:
       intercom.print_final_averages()

