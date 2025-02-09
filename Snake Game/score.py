import os
from config import scores_file, top_score_font, screen, width

def load_top_scores():
    try:
        with open(scores_file, "r") as file:
            scores = [line.strip().split(":") for line in file.readlines()]
            return [(name, int(score)) for name, score in scores]
    except FileNotFoundError:
        return []

def save_top_scores_to_file(scores):
    with open(scores_file, "w") as file:
        for name, score in scores:
            file.write(f"{name}:{score}\n")

def update_top_scores(name, score, top_scores):
    existing_entry = next((entry for entry in top_scores if entry[0] == name), None)
    if existing_entry:
        if score > existing_entry[1]:
            top_scores = [(n, s) if n != name else (name, score) for n, s in top_scores]
    else:
        top_scores.append((name, score))
    top_scores = sorted(top_scores, key=lambda x: x[1], reverse=True)[:3]
    save_top_scores_to_file(top_scores)

def display_top_scores(top_scores):
    screen.blit(top_score_font.render("Top Scores:", True, (50, 153, 213)), [width - 150, 10])
    for i, (name, score) in enumerate(top_scores[:3]):
        score_text = f"{name}: {score}"
        screen.blit(top_score_font.render(score_text, True, (50, 153, 213)), [width - 150, 30 + i * 20])
