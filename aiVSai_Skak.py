import os
from wsgiref import types
import chess
from openai import OpenAI       
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

CHESS_PLAYER_POLICY_GEMINI = """
Du er 'The Gemini Attacker'. Du er skakmester. Din spillestil er ekstremt aggressiv og taktisk. Din opgave er at vinde spillet.
- Du modtager brættets tilstand i FEN-format.
- Du får en liste over LOVLIGE TRÆK i UCI-format (f.eks. e2e4, g1f3).
- Du skal KUN svare med ét ord: det træk du vælger fra listen.
- Analyser stillingen og vælg det strategisk bedste træk.
"""

# --- FUNKTIONER ---

def get_gemini_move(bord):
    legal_moves = [move.uci() for move in bord.legal_moves]
    prompt = f"FEN: {bord.fen()}\nLovlige træk: {', '.join(legal_moves)}"

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction=CHESS_PLAYER_POLICY_GEMINI,
            temperature=0.2
        ),
        contents=prompt
    )
    move = response.text.strip().lower()
    return move if move in legal_moves else legal_moves[0]




# efter vi har fået den ti at virke kan vi måske få den til at give en kort ground til at den valgte dette træk