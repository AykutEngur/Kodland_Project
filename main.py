from flask import Flask, render_template, request, redirect
import mysql.connector

app =  Flask(__name__)

my_database = mysql.connector.connect(
    host = "AykutEngur.mysql.pythonanywhere-services.com",
    user = "AykutEngur",
    passwd= "Aykut1323",
    database = "AykutEngur$kodland_project"
)

@app.route('/',methods=['GET', 'POST'])
def home():
    best_score = None
    if request.method == "POST":


        username = request.form["username"]
        answers = {
            'question1' : request.form.get('question1'),
            'question2' : request.form.get('question2'),
            'question3' : request.form.get('question3'),
            'question4' : request.form.get('question4')
        }
    
        if not username or not all(answers.values()):
            return render_template("index.html", error="Please fill out all fields.")
        
        total_score = 0
        
        correct_answers = {
            'question1' : "C",
            'question2' : "A",
            'question3' : "C",
            'question4' : "B"
        }
        
        for question, answer in answers.items():
            if answer == correct_answers[question]:
                total_score += 25
        
        my_cursor = my_database.cursor()
        my_cursor.execute("""
                        SELECT MAX(total_score) FROM kodland_database_table WHERE username = %s
        """, (username,))
        max_score = my_cursor.fetchone()[0]

        if max_score is None or total_score > max_score:
            my_cursor.execute("""
                            INSERT INTO kodland_database_table (username, question_1 , question_2, question_3, question_4, total_score)
                            VALUES (%s, %s, %s, %s, %s, %s)
                            
                            """, (username, answers['question1'], answers['question2'], answers['question3'], answers['question4'], total_score))
        else:
            my_cursor.execute("""
                            UPDATE kodland_database_table
                            SET question_1 = %s,  question_2 = %s, question_3 = %s, question_4 = %s, total_score = %s
                    WHERE username = %s """, (answers['question1'], answers['question2'], answers['question3'], answers['question4'], total_score, username))
        my_database.commit()
        
        my_cursor.execute("""SELECT MAX(total_score) FROM kodland_database_table WHERE username = %s
            """, (username,))
        best_score = my_cursor.fetchone()[0]
        
        return render_template("index.html",best_score= f" ({best_score}%)", username=username)

    return render_template("index.html", best_score=best_score )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")