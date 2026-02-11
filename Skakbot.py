from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

CHESS_PLAYER_POLICY_CHATGPT = """
du er en skak stormester. Din opgave er at vinde spillet.
- du modtager brættets tilstand i FEN-format.
- du får en liste over lovlige træk i UCI-format.
- du skal kun svare med et ord: det træk du vælger fra listen.
- analyserer stillingen og vælg det strategisk bedste træk.
"""

model = "gpt-5.2"

def chatgpt_bot(fen, legal_moves):
    messages = [
        {"role": "system", "content": CHESS_PLAYER_POLICY_CHATGPT},
        {"role": "user", "content": f"FEN: {fen}\nLovlige træk: {', '.join(legal_moves)}"}


    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0

    )

    move = response.choices[0].message.content.strip()
    if move in legal_moves:
        return move
    
    return None

if __name__ == "__main__":
    import chess

    board = chess.Board()

    fen = board.fen()
    legal_moves = [move.uci() for move in board.legal_moves]

    move = chatgpt_bot(fen, legal_moves)
    print(f"GPTskakbot vælger træk: {move}")
    