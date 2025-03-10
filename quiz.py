import json
import random
import os

PROGRESS_FILE = "progress.json"


def load_questions(filename="questions.json"):
    """Load questions from a JSON file."""
    with open(filename, "r") as file:
        return json.load(file)


def save_progress(progress):
    """Save progress to a file."""
    with open(PROGRESS_FILE, "w") as file:
        json.dump(progress, file, indent=4)


def load_progress():
    """Load progress from a file if it exists."""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as file:
            return json.load(file)
    return {"attempted": 0, "correct": 0, "incorrect": 0, "missed_questions": []}


def ask_question(question_data, question_num, total_questions):
    """Ask a question with numbered question and answer choices."""
    print(f"\n🔹 {question_num}. {question_data['question']}")

    options = question_data["options"]
    random.shuffle(options)  # Randomize answer choices

    correct_answer = question_data["answer"]
    answer_map = {chr(97 + i): option for i, option in enumerate(options)}  # a, b, c, d

    for key, value in answer_map.items():
        print(f"  {key}) {value}")

    while True:
        user_answer = input("\nYour answer (a/b/c/d): ").strip().lower()
        if user_answer in answer_map:
            return answer_map[user_answer] == correct_answer, correct_answer
        print("❌ Invalid choice. Please enter a/b/c/d.")


def run_quiz():
    """Run the interactive CLI quiz."""
    questions = load_questions()
    random.shuffle(questions)  # Shuffle question order
    progress = load_progress()

    total_questions = len(questions)

    for index, question in enumerate(questions, start=1):
        progress["attempted"] += 1
        is_correct, correct_answer = ask_question(question, index, total_questions)

        if is_correct:
            print("✅ Correct!\n")
            progress["correct"] += 1
        else:
            print(f"❌ Wrong! The correct answer is: {correct_answer}\n")
            progress["incorrect"] += 1
            progress["missed_questions"].append(question)

    save_progress(progress)
    print(f"\n🎯 Quiz Finished! Score: {progress['correct']}/{progress['attempted']}")
    print("🔄 Use 'python quiz.py --review' to review missed questions.\n")


def review_missed_questions():
    """Review incorrectly answered questions."""
    progress = load_progress()
    missed_questions = progress["missed_questions"]

    if not missed_questions:
        print("🎉 No missed questions to review! Well done!")
        return

    print("\n📌 Review Mode: Re-attempting previously missed questions.")

    total_questions = len(missed_questions)

    for index, question in enumerate(missed_questions, start=1):
        _, correct_answer = ask_question(question, index, total_questions)
        print(f"✅ Correct Answer: {correct_answer}\n")

    # Reset missed questions after review
    progress["missed_questions"] = []
    save_progress(progress)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--review":
        review_missed_questions()
    else:
        run_quiz()
