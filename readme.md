# PokerProMaster HUD

PokerProMaster, Pokerfish , PPPoker , Pokerlords are movil poker clients for play with friends, 

It is possible to play on computer with android emulator, the main goal of this project is to being able to **use a tracker (HEM2 or PT4) and get realtime hud.**

Secondaries goals:

- Dataming hands without playing (easy when main goal is reached) 
- Autoseat script (as there are no waiting list, as soon as there is one player leaving , jump in, very easy too)
- Hotkeys (fold, call, sounds, betsizings etc )
- Placemint type things (tile , cascade windows etc)


One of the biggest challenge was to recognize the players, as the display nickname could be in chinese (Harder OCR) , and could changed (if the user pay for it).


The sucessfull solution ATM was to open the player info, and scrap the playerID number.
Then check if the player changed or not every frame (very quick operation)
 



### Disclamer:
- `This project is not finished, i stopped working on it as i notice a ` [comercial launch](https://hand2note.com/PokerMaster)`from good developpers.. 
Even though the hardest challenges were solved, it would have required a lot more work (Specially the license stuff (code obfuscation), some performance tweaks as well as a lot of tests/debugging.`

- All the OCR part was done, but not incluyed as i will probably open-sourced it later as an independent module.






### Working stuff:

- Find tables:
    - By image detection, 
    - By windows window findit 
- Control the table window, (move it, focus etc)
- Get players IDs numbers
- Find empty seats and detect players changes
- Find player with cards
- Recognize cards/action/bets etc

### Todo roadmap:

- Find format to save the hands locally to ...
- ... Dataming/test as same time ..
- Find the way to convert local handhistories into .txt importable into HEM/PT4
- Work on license/hide the code 
- Do the secondaries goals
