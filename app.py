"""TopperMind: Teach-Back Arena — Gradio entry point."""
import os, uuid, logging
import gradio as gr
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
import pandas as pd
from config import MODEL_NAME, EMBEDDING_MODEL
from knowledge import NOTES, MODEL, seed_database
from tools import retrieve, add_note, web_search
from agents import choose_topic, followup, score_explanation, examiner, answer_from_notes, llm

logging.basicConfig(level=logging.INFO)
embedding = SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)
client = chromadb.Client()
collections = seed_database(client, embedding)
print(f"TopperMind self-test | GROQ_API_KEY present: {bool(os.environ.get('GROQ_API_KEY'))} | model: {MODEL_NAME} | " + " | ".join(f"{n}: {c.count()} notes" for n, c in collections.items()))

def language_hint(language): return f"Reply in {language}, using simple words."

def start(topic, mode, language):
    chosen = choose_topic(mode, topic or "", MODEL)
    if not chosen: return {"topic":"", "mode":mode, "round":0, "explanations":[], "done":False}, "Choose a listed topic first. You can do this!", ""
    docs = retrieve(collections[mode], chosen, 4) or [MODEL[mode][chosen]]
    return {"topic":chosen, "mode":mode, "round":1, "explanations":[], "done":False}, f"🧒 Curious Student — Round 1/3\n\nTeach me **{chosen}** as if I'm 10.\n\n{followup(chosen, docs, language_hint(language))}", ""

def submit(explanation, mode, language, state, weak_scores):
    try:
        state = dict(state or {"topic":"", "mode":mode, "round":0, "explanations":[], "done":False})
        state["explanations"] = list(state.get("explanations", []))
        weak_scores = dict(weak_scores or {})
        if not state.get("topic") or state.get("done"): return state, weak_scores, "Start a topic first. One step at a time!", ""
        if state.get("mode", mode) != mode: return state, weak_scores, "You changed the knowledge base. Start this topic again in the selected mode. Keep going!", ""
        explanation = (explanation or "").strip()
        if not explanation: return state, weak_scores, "Please explain the idea first. Give it a try!", ""
        state["explanations"].append(explanation)
        if state["round"] < 3:
            state["round"] += 1
            docs = retrieve(collections[mode], state["topic"], 4) or [MODEL[mode][state["topic"]]]
            return state, weak_scores, f"🧒 Curious Student — Round {state['round']}/3\n\nThanks! One more thought: {followup(state['topic'], docs, language_hint(language))}", ""
        answer = MODEL[mode][state["topic"]]
        score, explained, missed = score_explanation(" ".join(state["explanations"]), answer, embedding)
        feedback = examiner(state["topic"], score, explained, missed, language_hint(language))
        weak_scores[f"{mode} — {state['topic']}"] = score; state["done"] = True
        result = f"📝 Examiner\n\n**Score: {score}/100**\n\n**Explained well:** {', '.join(explained) or 'Keep building the core idea'}\n\n**Missed key terms:** {', '.join(missed) or 'None spotted'}\n\n**Feedback:** {feedback}\n\nKeep practicing—you are getting stronger!"
        return state, weak_scores, result, ""
    except Exception:
        logging.exception("Teach-back failed")
        return state or {}, weak_scores or {}, "That round hit a snag. Please start again. You've got this!", ""

def save_notes(text, mode):
    if not (text or "").strip(): return "Paste a few lines of notes first. Every note helps!"
    return add_note(collections[mode], text.strip(), f"user_{uuid.uuid4().hex}")[1]

def ask(query, mode, language, latest):
    try:
        if not (query or "").strip(): return "Type a question to get started. Stay curious!"
        response = answer_from_notes(query, collections[mode], language_hint(language))
        if latest: response += f"\n\n**Latest news search:**\n{web_search(query)}\n\nKeep learning every day!"
        return response
    except Exception:
        logging.exception("Ask failed"); return "I couldn't complete that request. Please try again. Keep going!"

def make_quiz(topic, mode, language):
    try:
        chosen = choose_topic(mode, topic or "", MODEL)
        if not chosen: return "Choose a topic from this mode. You can do it!", ""
        docs = retrieve(collections[mode], chosen, 5)
        if not docs: return "I couldn't find notes for that topic. Add notes and try again!", ""
        result = llm(f"Create exactly 3 MCQs about {chosen} using ONLY these notes. Give each A-D options, then put the answer key after a heading ANSWERS. {language_hint(language)}\nNotes:\n" + "\n".join(docs), "You are a careful quiz writer. Do not invent facts.")
        if "ANSWERS" not in result.upper():
            return "I couldn't safely separate the quiz answer key. Please generate it again. Keep practicing!", ""
        split_at = result.upper().index("ANSWERS")
        questions, key = result[:split_at], result[split_at + len("ANSWERS"):]
        return questions + "\n\nTry before you peek! Keep it up!", key
    except Exception:
        logging.exception("Quiz failed"); return "Quiz generation failed temporarily. Try again soon!", ""

def make_plan(days, hours, scores):
    try:
        weak = [(t,int(s)) for t,s in (scores or {}).items() if int(s) < 80]
        if not weak: return pd.DataFrame(columns=["topic","score","hours","hours per day"]), "No weak topics yet. Use the time for revision and mock tests. Keep your momentum!"
        days=max(1,float(days)); total=days*max(0,float(hours)); weights=[max(1,100-s) for _,s in weak]; denom=sum(weights)
        rows=[{"topic":t,"score":s,"hours":round(total*w/denom,2),"hours per day":round(total*w/denom/days,2)} for (t,s),w in zip(weak,weights)]
        return pd.DataFrame(rows), "Study hours are weighted by each topic's score gap. Small daily sessions add up!"
    except Exception:
        logging.exception("Plan failed"); return pd.DataFrame(columns=["topic","score","hours","hours per day"]), "Enter valid day and hour values, then try again. You've got this!"

def show_progress(scores):
    data=scores or {}; df=pd.DataFrame([{"topic":k,"score":v} for k,v in data.items()]) if data else pd.DataFrame(columns=["topic","score"])
    summary=f"You've completed {len(data)} topic attempt(s); average score {round(sum(data.values())/len(data))}/100." if data else "Your scores will appear after your first Teach-Back. Start whenever you're ready!"
    return df, summary

def demo_values():
    return "Stack", "A stack stores items and removes the first one put in.", "How does photosynthesis work?", "Stack", 7, 2, "Explaining a stack helps me remember it."

with gr.Blocks(theme=gr.themes.Soft(), title="TopperMind — Teach-Back Arena") as app:
    gr.Markdown("# TopperMind: Teach-Back Arena\n### Don't just ask AI. Teach it.\nA friendly practice coach for school, college, UPSC and UGC NET topics.")
    gr.Markdown("**🤖 Router / CEO:** coordinates three agents: 🧒 Curious Student retrieves notes and asks a follow-up → 📝 Examiner scores your explanation → 📅 Strategist turns weak scores into a plan.")
    with gr.Accordion("How it works", open=False): gr.Markdown("Student teaches → 🧒 Curious Student (RAG notes + follow-up) → up to 3 Python-controlled rounds → 📝 Examiner (cosine score + feedback) → 📅 Strategist (weighted plan).\n\nAsk: question → ChromaDB notes → grounded reply. The model cannot control Teach-Back flow.")
    state=gr.State({"topic":"","round":0,"explanations":[],"done":False}); scores=gr.State({})
    with gr.Row():
        mode=gr.Dropdown(list(NOTES),value="College CS (DSA + DBMS)",label="Mode / knowledge base")
        language=gr.Dropdown(["English","Hindi","Telugu","Tamil"],value="English",label="Language")
    demo_btn=gr.Button("🎬 Demo Mode: prefill inputs")
    with gr.Tabs():
        with gr.Tab("🧒 Teach-Back Arena"):
            topic=gr.Dropdown(list(MODEL["College CS (DSA + DBMS)"]),value="Stack",label="Topic",allow_custom_value=True)
            start_btn=gr.Button("Start Teach-Back",variant="primary"); prompt=gr.Markdown(); explanation=gr.Textbox(label="Teach the Curious Student",lines=4)
            send_btn=gr.Button("Submit explanation"); result=gr.Markdown()
            mode.change(lambda m: gr.update(choices=list(MODEL[m]),value=list(MODEL[m])[0]),mode,topic)
            start_btn.click(start,[topic,mode,language],[state,prompt,result])
            send_btn.click(submit,[explanation,mode,language,state,scores],[state,scores,result,explanation])
        with gr.Tab("💬 Ask"):
            question=gr.Textbox(label="Ask from your notes",lines=2); latest=gr.Checkbox(label="Latest news (adds web search)",value=False)
            ask_btn=gr.Button("Ask",variant="primary"); answer=gr.Markdown(); ask_btn.click(ask,[question,mode,language,latest],answer)
            add_text=gr.Textbox(label="Add my notes",lines=4); add_btn=gr.Button("Add notes"); add_status=gr.Markdown(); add_btn.click(save_notes,[add_text,mode],add_status)
        with gr.Tab("📝 Quiz"):
            quiz_topic=gr.Dropdown(list(MODEL["College CS (DSA + DBMS)"]),value="Stack",label="Quiz topic",allow_custom_value=True)
            mode.change(lambda m: gr.update(choices=list(MODEL[m]),value=list(MODEL[m])[0]),mode,quiz_topic)
            quiz_btn=gr.Button("Generate 3 MCQs"); quiz_questions=gr.Markdown()
            with gr.Accordion("🔒 Reveal answer key",open=False): quiz_key=gr.Markdown()
            quiz_btn.click(make_quiz,[quiz_topic,mode,language],[quiz_questions,quiz_key])
        with gr.Tab("📅 Strategist"):
            days=gr.Number(label="Days left",value=7,minimum=1,precision=0); hours=gr.Number(label="Study hours per day",value=2,minimum=0.5)
            plan_btn=gr.Button("Build study plan"); plan_table=gr.Dataframe(headers=["topic","score","hours","hours per day"],interactive=False); plan_text=gr.Markdown()
            plan_btn.click(make_plan,[days,hours,scores],[plan_table,plan_text])
        with gr.Tab("📊 Progress"):
            refresh=gr.Button("Refresh progress"); plot=gr.BarPlot(x="topic",y="score",title="Teach-Back scores",y_lim=[0,100]); summary=gr.Markdown()
            refresh.click(show_progress,scores,[plot,summary]); send_btn.click(show_progress,scores,[plot,summary])
    gr.Markdown("For learning practice. Check current official exam sources for updates. Keep showing up!")
    demo_btn.click(demo_values,outputs=[topic,explanation,question,quiz_topic,days,hours,add_text])

if __name__ == "__main__": app.launch(server_name="0.0.0.0")

