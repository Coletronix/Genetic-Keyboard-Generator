from dataclasses import dataclass
import keyboard
import threading
import time


@dataclass
class charTime:
    char: str
    time: float

user_typed_keystrokes = []

def keyboard_input():
    global user_typed_keystrokes
    user_typed_keystrokes = keyboard.record(until='enter')

input_thread = threading.Thread(target=keyboard_input)
input_thread.start()

timeString = []

string_to_type = "Since again the simulation completed with no errors, there were no issues with the simulated memory stage implementation. Finally, the a post-implementation simulation was performed to gauge how the memory stage might perform in the real world. This simulation is presented in. In conclusion, the memory and writeback stages of the MIPS processor were successfully implemented using reference Verilog files and various simulation techniques. These stages offer memory to the system and redirect signals back into previous stages of the system, tying the results computed by previous units together. /par For this exercise, Verilog code for the data memory and writeback stage was provided to be translated into VHDL code. "
timeout = 1.5
save_filename = "userTestBenches/user_bigram_time_qwerty.txt"

print("Type the following string: ")
print(">" + string_to_type)
input(">")

input_thread.join()

start_time = user_typed_keystrokes[0].time

for keyEvent in user_typed_keystrokes:
    absolute_time = keyEvent.time - start_time
    if keyEvent.event_type == 'up':
        continue
    if keyEvent.name == 'backspace':
        timeString.pop()
    elif keyEvent.name == 'space':
        timeString.append(charTime(' ', absolute_time))
    elif keyEvent.name.isalnum() and len(keyEvent.name) == 1: # check if it is alphanumeric and a single key
        timeString.append(charTime(keyEvent.name, absolute_time))
    
bigram_average_time_dict = dict()

# create bigram_average_time_dict
for i in range(len(timeString) - 1):
    bigram = timeString[i].char.lower() + timeString[i+1].char.lower()
    time_diff = timeString[i+1].time - timeString[i].time
    
    # timeout
    if time_diff > timeout:
        continue
    # ignore spaces and repeated characters
    if bigram[0] == ' ' or bigram[1] == ' ' or bigram[0] == bigram[1]:
        continue
    
    if bigram in bigram_average_time_dict:
        bigram_average_time_dict[bigram].append(time_diff)
    else:
        bigram_average_time_dict[bigram] = [time_diff]
        
# calculate average time for each bigram
for bigram in bigram_average_time_dict:
    bigram_average_time_dict[bigram] = sum(bigram_average_time_dict[bigram]) / len(bigram_average_time_dict[bigram])
    
# print out the bigram and average time in descending order
for bigram in sorted(bigram_average_time_dict, key=bigram_average_time_dict.get, reverse=False):
    print(bigram, bigram_average_time_dict[bigram])
    
# write to file
with open(save_filename, 'w') as f:
    for bigram in sorted(bigram_average_time_dict, key=bigram_average_time_dict.get, reverse=False):
        f.write(bigram + ' ' + str(bigram_average_time_dict[bigram]) + '\n')
