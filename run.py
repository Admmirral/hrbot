from highrise.__main__ import *
import os
import time
"""Bot Settings"""
room_id = "68b40dffbfba642d49873fdb"
bot_token = os.getenv("BOT_TOKEN")
bot_file = "bot"
bot_class = "Bot"

if __name__ == "__main__":
  definitions = [
      BotDefinition(
          getattr(import_module(bot_file), bot_class)(), room_id, bot_token)
  ]  # More BotDefinition classes can be added to the definitions list
  while True:
    try:
      arun(main(definitions))
    except Exception as e:
      # Print the full traceback for the exception
      import traceback
      print("Caught an exception:")
      traceback.print_exc()  # This will print the full traceback
      time.sleep(1)
      continue
