from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

my_database = mysql.connector.connect(
    host="AykutEngur.mysql.pythonanywhere-services.com",
    user="AykutEngur",
    passwd="Aykut1323",
    database="AykutEngur$kodland_project"
)

@app.route('/', methods=['GET', 'POST'])
def home():
    current_score = None
    best_score = None

    if request.method == "POST":
        username = request.form["username"]
        answers = {
            'question1': request.form.get('question1'),
            'question2': request.form.get('question2'),
            'question3': request.form.get('question3'),
            'question4': request.form.get('question4')
        }

        if not username or not all(answers.values()):
            return render_template("index.html", error="Please fill out all fields.")

        # Calculate the current score
        current_score = 0
        correct_answers = {
            'question1': "C",
            'question2': "A",
            'question3': "C",
            'question4': "B"
        }

        for question, answer in answers.items():
            if answer == correct_answers[question]:
                current_score += 25

        my_cursor = my_database.cursor()

        # Fetch the current highest score for the username
        my_cursor.execute("""
            SELECT total_score FROM kodland_database_table WHERE username = %s ORDER BY total_score DESC LIMIT 1
        """, (username,))
        result = my_cursor.fetchone()
        best_score = result[0] if result else 0

        # Update the database if the current score is higher than the best score
        if current_score > best_score:
            if best_score == 0:  # No existing record, insert a new one
                my_cursor.execute("""
                    INSERT INTO kodland_database_table (username, question_1, question_2, question_3, question_4, total_score)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (username, answers['question1'], answers['question2'], answers['question3'], answers['question4'], current_score))
            else:  # Update the existing record with the new best score
                my_cursor.execute("""
                    UPDATE kodland_database_table
                    SET question_1 = %s, question_2 = %s, question_3 = %s, question_4 = %s, total_score = %s
                    WHERE username = %s
                """, (answers['question1'], answers['question2'], answers['question3'], answers['question4'], current_score, username))

            best_score = current_score  # Update the best score to the current score

        # Commit the changes
        my_database.commit()
        my_cursor.close()

        # Render the template with both scores
        return render_template("index.html", current_score=current_score, best_score=best_score, username=username)

    return render_template("index.html", current_score=current_score, best_score=best_score)