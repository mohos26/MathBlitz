"""
banners.py - Text resources, banners, and help instructions for the MAthBlitz.
"""

# Welcome banner template
WELCOME_BANNER = """--------------------------------------------------------------------------------
                     🧠 WORKING MEMORY TRAINER 🧠
               Focus • Calculate • Retain • Type 'help'
--------------------------------------------------------------------------------"""

# Help instructions text
HELP_INSTRUCTIONS = """
================================================================================
 GAME INSTRUCTIONS 
================================================================================
 Welcome to the Mental Math Training Game!
 Your goal is to solve math equations to train your brain and working memory.
 Periodically, your answers will be saved as memory variables (A and B).
 These variables may appear in future equations to test your focus.
--------------------------------------------------------------------------------
 AVAILABLE COMMANDS:
   • help  - Show this help message and game rules.
   • vars  - View your currently stored memory variables.
   • count - Check how many equations you have solved correctly.
   • exit  - Quit the game and see your final score.
================================================================================
"""

# Milestone message
MILESTONE_MESSAGE = """
================================================================================
🎉 Milestone Reached! You have solved 40 equations! Incredible focus! 🎉
================================================================================
"""


def get_goodbye_banner(correct_count: int) -> str:
    """Return the formatted goodbye summary banner."""
    return f"""--------------------------------------------------------------------------------
  Session Finished!
  Score: {correct_count} equations solved correctly.
  
  Great workout for your brain today. See you next session!
--------------------------------------------------------------------------------"""