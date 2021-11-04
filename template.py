""" Template for Project 1: Morse code """

from GPIOSimulator_v1 import *
GPIO = GPIOSimulator()

# Variables for time T and the signal/pause-types
T = 1
dot = '.'
dash = '-'
symbol_pause = 2
word_pause = 3
message_end = 4


class MorseDecoder():
    """ Morse code class """

    # Define class variable morse_codes; a python dictionary
    morse_codes = {'.-': 'a', '-...': 'b', '-.-.': 'c', '-..': 'd', '.': 'e', '..-.': 'f', '--.': 'g',
                  '....': 'h', '..': 'i', '.---': 'j', '-.-': 'k', '.-..': 'l', '--': 'm', '-.': 'n',
                  '---': 'o', '.--.': 'p', '--.-': 'q', '.-.': 'r', '...': 's', '-': 't', '..-': 'u',
                  '...-': 'v', '.--': 'w', '-..-': 'x', '-.--': 'y', '--..': 'z', '.----': '1',
                  '..---': '2', '...--': '3', '....-': '4', '.....': '5', '-....': '6', '--...': '7',
                  '---..': '8', '----.': '9', '-----': '0'}

    def __init__(self, current_symbol, current_word, message):
        """ initialize your class """

        # Define instance variables
        self.current_symbol = current_symbol    # Symbol currently under construction (signal+signal+..)
        self.current_word = current_word        # Word currently under construction (symbol+symbol+..)
        self.message = message                  # Final message to be printed to screen (word+word+..)
        self.done = False                       # Main loop variable

    def reset(self):
        """ reset the variable for a new run """

        self.current_symbol = ''
        self.current_word = ''

    def main_loop(self):
        """ read a signal from Raspberry Pi """
        # Read signal as from 'button' and classify as button-pressed (dot/dash) or not pressed(pause-types)

        """
            Trenger følgende variabler for å beregne press/pause tider:
            - time_start_press
            - time_end_press
            - total_press_time = (time_end_press - time_start_press)
            - time_start_pause
            - time_end_pause
            - total_pause_time = (time_end_pause - time_start_pause)
        """
        prev_state = 0
        time_start_pause = 0
        time_end_pause = 0
        total_pause_time = 0

        # Main loop for running program: Takes in a morse-code -> decodes it -> prints result to screen -> quits
        while not self.done:

            current_state = GPIO.input(PIN_BTN)     # Continuously reads state of the button

            if current_state != prev_state:         # Looks for changes in the button-state

                # Endring: går fra pause til trykk 0->1
                # Change: going from PAUSE to PRESS (0 -> 1)
                if prev_state == 0:                 # Means we come from a pause and are going to a press

                    if time_start_pause != 0:       #
                        time_end_pause = time.time()
                        total_pause_time = (time_end_pause - time_start_pause)
                        # print('pause time: ', total_pause_time)

                        # Dekoder pausen!
                        # Decoding PAUSES
                        if (2.0*T) <= total_pause_time <= (4.0*T):
                            # prev_state = 1
                            self.process_signal(symbol_pause)
                        elif (4.0*T) < total_pause_time <= (6.0*T):
                            self.process_signal(word_pause)
                            # prev_state = 1
                        # elif total_pause_time > (7.0*T):
                            # self.process_signal(message_end)

                    # Ferdig med pause!
                    # Finished PAUSING
                    time_start_press = time.time()
                    prev_state = 1
                    if total_pause_time > (6.0*T):
                        self.process_signal(message_end)


                # Endring: går fra trykk til pause 1->0
                # Change: going from PRESS to PAUSE (1 -> 0)
                else:
                    time_end_press = time.time()
                    total_press_time = (time_end_press - time_start_press)
                    # print('Press time: ', total_press_time)

                    # Dekoder trykkene våre!!!
                    # Decoding PRESSES
                    if total_press_time < 2*T:
                        self.process_signal(dot)
                    else:
                        self.process_signal(dash)

                    # Ferdig med å trykke! (press)
                    # Finished PRESSING
                    time_start_pause = time.time()
                    prev_state = 0                  # Resetting prev to 0 because we are done pressing
        return

    def process_signal(self, signal):
        """ handle the signals using corresponding functions """

        # Process signals (dot/dash)
        if signal == dot or signal == dash:
            # Printing LED-states to screen
            if signal == dot:
                GPIO.output(PIN_RED_LED_0, GPIO.HIGH)
            else:
                GPIO.output(PIN_BLUE_LED, GPIO.HIGH)

            self.update_current_symbol(signal)
            print(signal)

        # Process signals (symbol/word/message pause)
        elif signal == symbol_pause:
            self.handle_symbol_end()

        elif signal == word_pause:
            self.handle_word_end()

        elif signal == message_end:
            self.handle_message_end()

    def update_current_symbol(self, signal):
        """ append the signal to current symbol code """

        # If the signal is a dot/ dash it gets added to the current symbol
        self.current_symbol += signal

    # def handle_signal_end(self):
        # may not need this
    def update_current_word(self, symbol):
        self.current_word += symbol

    def update_message(self, word):
        self.message += (word + ' ')

    def handle_symbol_end(self):
        """ process when a symbol ending appears """

        # When symbol is done, use it as key for the morse_codes dictionary to find the right symbol,
        # which is then given as an argument to update_curr_word
        if self.current_symbol in self.morse_codes:
            symbol = self.morse_codes[self.current_symbol]      # We find correct symbol in dictionary
            self.update_current_word(symbol)
            self.current_symbol = ''
        else:
            self.update_current_word('?')   # Could not find symbol in morse-dictionary
            self.current_symbol = ''

    def handle_word_end(self):
        """ process when a word ending appears """

        # print(self.current_symbol)
        self.handle_symbol_end()  # Ordet avsluttes mde et symbol så dette gir mening
        # print(self.current_word)
        self.update_message(self.current_word)
        self.reset()


    def handle_message_end(self):
        print('message is: ')
        self.handle_word_end()
        print(self.message)
        self.done = True


def main():
    """ the main function """

    test1 = MorseDecoder('','','')
    test1.main_loop()
    """
    TIME REMINDER, T=1sek:
    dot < 2
    2 < dash < 4
    2 < symbol_break <4
    4 < word_break < 6
    message_end > 6 
    """



if __name__ == "__main__":
    main()




