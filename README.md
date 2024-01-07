Console bot.

The assistant bot should become a prototype of an assistant application for us. In the first approximation,
the assistant application should be able to work with the contact book and calendar.

Commands:
-"about" replise to the console all available commands and their description
-"hello", replies to the console "How can I help you?"
-"add ...". With this command, the bot saves a new contact in memory.
    Instead of ... the user enters the name and phone number, necessarily with a space.
-"change ..." With this command, the bot stores the new phone number of the existing contact in memory.
    Instead of ... the user enters the name and phone number, necessarily with a space.
    The passed argument "phonenumber" rejects all non-numeric characters.
-"phone ...." With this command, the bot outputs the phone number for the specified contact to the console.
    Instead of ... the user enters the name of the contact whose number should be displayed.
-"show all". With this command, the bot outputs all saved contacts with phone numbers to the console.
-"delete ..." With this command, the bot will delete the contact from memory.
    Instead of ... the user enters the name of the contact to be deleted.
-"good bye", "close", "exit" according to any of these commands, the bot completes its work correctly and displays "Good bye!" in the console.
    When the program is terminated correctly, the cache will be saved, and when the program is called again, the cache will be restored.
