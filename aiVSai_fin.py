import os
import chess
import time
import random
from openai import OpenAI         
from dotenv import load_dotenv
from google import genai
from google.genai import types 

load_dotenv()

# --- KLIENT OPSÆTNING ---
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- PROMPTS ---
POLICY_GEMINI = "Du er en aggressiv skakmester. Svar KUN med trækket i UCI format (f.eks. e2e4)."
POLICY_CHATGPT = "Du er en strategisk skakmester. Svar KUN med trækket i UCI format (f.eks. e2e4)."

# --- FUNKTIONER ---

def get_gemini_move(board):
    legal_moves = [move.uci() for move in board.legal_moves]
    prompt = f"FEN: {board.fen()}\nLovlige træk: {', '.join(legal_moves)}"
    
    # Vi prøver alle tænkelige navne-formater, som Google accepterer
    # Nogle gange skal den have 'models/' præfiks, andre gange ikke.
    models_to_test = [
        "gemini-1.5-flash", 
        "gemini-2.0-flash",
        "gemini-1.5-flash-8b" # En lettere model der ofte er mere ledig
    ]

    for model_id in models_to_test:
        try:
            response = gemini_client.models.generate_content(
                model=model_id,
                config=types.GenerateContentConfig(
                    system_instruction=POLICY_GEMINI,
                    temperature=0.1
                ),
                contents=prompt
            )
            
            # Hvis vi når hertil, virkede det!
            move = response.text.strip().lower()
            import re
            found = re.findall(r'[a-h][1-8][a-h][1-8]', move)
            clean_move = found[0] if found else move

            if clean_move in legal_moves:
                return clean_move
                
        except Exception as e:
            error_msg = str(e)
            if "404" in error_msg:
                # Prøv næste model i listen
                continue
            elif "429" in error_msg:
                print(f"⏳ Kvote ramt for {model_id}. Venter 32 sek...")
                time.sleep(32)
                # Vi prøver ikke igen i dette træk for at undgå uendelige loops
                break
            else:
                print(f"Ukendt fejl ved {model_id}: {e}")
                break

    print("Alle Gemini-modeller fejlede (404/429), trækker tilfældigt...")
    return random.choice(legal_moves)

def get_chatgpt_move(board):
    legal_moves = [move.uci() for move in board.legal_moves]
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": POLICY_CHATGPT},
                {"role": "user", "content": f"FEN: {board.fen()}\nLovlige træk: {', '.join(legal_moves)}"}
            ],
            temperature=0
        )
        move = response.choices[0].message.content.strip().lower()
        return move if move in legal_moves else random.choice(legal_moves)
    except Exception as e:
        print(f" ChatGPT fejl: {e}")
        return random.choice(legal_moves)

# --- GAME ENGINE ---

def play_duel():
    board = chess.Board()
    print(" DUEL: Gemini (Hvid) vs. ChatGPT (Sort)\n")

    while not board.is_game_over():
        # Hvid: Gemini
        move_w = get_gemini_move(board)
        board.push_uci(move_w)
        print(f" Gemini: {move_w}")
        
        if board.is_game_over(): break
        
        # En lille pause for at undgå Rate Limit (429)
        time.sleep(1)

        # Sort: ChatGPT
        move_b = get_chatgpt_move(board)
        board.push_uci(move_b)
        print(f" ChatGPT: {move_b}")
        
        print(f"\n{board}\n")
        print("-" * 20)

    print(f"\nSLUT! Resultat: {board.result()}")

if __name__ == "__main__":
    play_duel()