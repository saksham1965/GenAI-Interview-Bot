import json, os, time
from utils import generate_questions, evaluate_answer
from rich import print

def run_interview(role="Backend Engineer", skill="APIs"):
    questions = generate_questions(role, skill, n=5)
    print("[bold green]Generated questions:[/bold green]")
    for i,q in enumerate(questions,1):
        print(f"{i}. {q}")

    transcript = {"role": role, "skill": skill, "qa": []}
    for i,q in enumerate(questions,1):
        print(f"\n[bold blue]Q{i}:[/bold blue] {q}")
        ans = input("Candidate answer (paste or type):\n")
        print("Evaluating...")
        eval_res = evaluate_answer(q, ans)
        print("[bold yellow]Evaluation:[/bold yellow]")
        print(eval_res)
        transcript["qa"].append({"q": q, "a": ans, "eval": eval_res})
        time.sleep(0.5)

    os.makedirs("sample_transcripts", exist_ok=True)
    fname = f"sample_transcripts/{role.replace(' ','_')}_{skill}_{int(time.time())}.json"
    with open(fname,"w") as f:
        json.dump(transcript,f,indent=2)
    print(f"[green]Transcript saved to {fname}")

if __name__ == "__main__":
    role = input("Role (default: Backend Engineer): ") or "Backend Engineer"
    skill = input("Skill (default: APIs): ") or "APIs"
    run_interview(role, skill)
