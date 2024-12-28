import sqlite3
import os

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

def sentiment_analysis(text):
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(text)
    if (sentiment['neg'] > sentiment['pos']):
        return True
    else:
        return False

def make_database():
    # Connect to the database
    conn = sqlite3.connect('Designverse.db')
    cursor = conn.cursor()

    conn.execute('''
    CREATE TABLE IF NOT EXISTS assets (
        asset_path VARCHAR(255) PRIMARY KEY,
        asset_name VARCHAR(100),
        artist_name VARCHAR(100),
        artist_rollno INT,
        course_related VARCHAR(255),
        file_type VARCHAR(50),
        prof_of_course VARCHAR(100),
        asset_year INT,
        asset_description TEXT
    );
    ''')
    
    conn.execute('''
    CREATE TABLE IF NOT EXISTS comments (
        asset_path VARCHAR(255),
        comment TEXT,
        comment_by VARCHAR(100),
        comment_by_rollno INT,
        comment_date DATE,
        FOREIGN KEY (asset_path) REFERENCES assets(asset_path)
    );
    ''')
    
    conn.execute('''
    INSERT INTO assets (asset_path, asset_name, artist_name, artist_rollno, course_related, file_type, prof_of_course, asset_year, asset_description) VALUES
    ('assets/1.jpg', 'Project1', 'Artist1', 123, 'Design Drawing & Visualization', 'image', 'Professor1', 2022, 'Description1'),
    ('assets/2.jpg', 'Project2', 'Artist2', 234, 'Introduction to HCI', 'image', 'Professor2', 2023, 'Description2'),
    ('assets/3.jpg', 'Project3', 'Artist3', 345, 'Prototyping Interactive Systems', 'image', 'Professor3', 2021, 'Description3'),
    ('assets/4.jpg', 'Project4', 'Artist4', 456, 'Design Processes and Perspectives', 'image', 'Professor1', 2024, 'Description4'),
    ('assets/5.jpg', 'Project5', 'Artist5', 567, 'Visual Design & Communication', 'image', 'Professor4', 2023, 'Description5'),
    ('assets/6.jpg', 'Project6', 'Artist6', 678, 'Design Drawing & Visualization', 'image', 'Professor2', 2022, 'Description6');
    ''')
    
    conn.execute('''
    INSERT INTO comments(asset_path, comment, comment_by, comment_by_rollno, comment_date) VALUES
    ('assets/1.jpg', 'Wow', 'User1', 123, '2022-01-01'),
    ('assets/1.jpg', 'Not good', 'User2', 234, '2022-01-02'),
    ('assets/1.jpg', 'Very beautiful', 'User3', 345, '2022-01-03'),
    ('assets/1.jpg', 'Nice', 'User4', 456, '2022-01-04'),
    ('assets/1.jpg', 'Mid art', 'User5', 567, '2022-01-05'),
    ('assets/1.jpg', 'Scope of improvement', 'User6', 678, '2022-01-06'),
    ('assets/2.jpg', 'Comment7', 'User7', 789, '2022-01-07'),
    ('assets/2.jpg', 'Comment8', 'User8', 890, '2022-01-08'),
    ('assets/2.jpg', 'Comment9', 'User9', 901, '2022-01-09'),
    ('assets/2.jpg', 'Comment10', 'User10', 101, '2022-01-10'),
    ('assets/2.jpg', 'Comment11', 'User11', 111, '2022-01-11'),
    ('assets/2.jpg', 'Comment12', 'User12', 222, '2022-01-12'),
    ('assets/3.jpg', 'Comment13', 'User13', 333, '2022-01-13'),
    ('assets/3.jpg', 'Comment14', 'User14', 444, '2022-01-14'),
    ('assets/3.jpg', 'Comment15', 'User15', 555, '2022-01-15'),
    ('assets/3.jpg', 'Comment16', 'User16', 666, '2022-01-16'),
    ('assets/3.jpg', 'Comment17', 'User17', 777, '2022-01-17'),
    ('assets/3.jpg', 'Comment18', 'User18', 888, '2022-01-18'),
    ('assets/4.jpg', 'Comment19', 'User19', 999, '2022-01-19'),
    ('assets/4.jpg', 'Comment20', 'User20', 121, '2022-01-20'),
    ('assets/4.jpg', 'Comment21', 'User21', 122, '2022-01-21'),
    ('assets/4.jpg', 'Comment22', 'User22', 223, '2022-01-22'),
    ('assets/4.jpg', 'Comment23', 'User23', 334, '2022-01-23'),
    ('assets/4.jpg', 'Comment24', 'User24', 445, '2022-01-24'),
    ('assets/5.jpg', 'Comment25', 'User25', 556, '2022-01-25'),
    ('assets/5.jpg', 'Comment26', 'User26', 667, '2022-01-26'),
    ('assets/5.jpg', 'Comment27', 'User27', 778, '2022-01-27'),
    ('assets/5.jpg', 'Comment28', 'User28', 889, '2022-01-28');
    ''')

    # Commit and close the connection
    conn.commit()
    conn.close()

    print("Database created successfully")

def fetch_project_details(asset_path):
    # Connect to the database
    conn = sqlite3.connect('Designverse.db')
    cursor = conn.cursor()

    # Fetch project details using asset path
    cursor.execute("SELECT * FROM assets WHERE asset_path = ?", (asset_path,))
    project_details = cursor.fetchone()

    # Close the connection
    conn.close()

    return project_details

def fetch_comments(asset_path):
    # Connect to the database
    conn = sqlite3.connect('Designverse.db')
    cursor = conn.cursor()

    # Fetch comments using asset path
    cursor.execute("SELECT * FROM comments WHERE asset_path = ?", (asset_path,))
    comments = cursor.fetchall()

    # Close the connection
    conn.close()
    # add sentiment analysis
    for i, comment in enumerate(comments):
        if sentiment_analysis(comment[1]):
            comments[i] = list(comments[i])
            comments[i].append("red")
            comments[i] = tuple(comments[i])
        else:
            comments[i] = list(comments[i])
            comments[i].append("green")
            comments[i] = tuple(comments[i])
    return comments
        
def make_html(file_path, asset_path):
    # Fetch project details from the database
    project_details = fetch_project_details(asset_path)
    comment_details = fetch_comments(asset_path)

    # Check if asset_path[0:len(asset_path)-4] + ".mp4" exists
    if os.path.exists(asset_path[0:len(asset_path)-4] + ".mp4"):
        print("Video file found for asset:", asset_path)
        # Define HTML content for video
        html_content = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>DIS Project</title>
        <style>
            /* Font */
            body {{
                font-family: 'Roboto', sans-serif;
                color: #333;
                background-color: #f0f0f0;
            }}

            /* Colors */
            header {{
                background-color: #333;
                color: #fff;
                position: fixed; /* keep header fixed */
                top: 0;
                left: 0;
                width: 100%;
                z-index: 1; /* ensure header is on top */
                display: flex;
                justify-content: center;
                align-items: center;
                height: 80px;
            }}

            .logo {{
                font-size: 36px;
                font-weight: bold;
                text-transform: uppercase;
                color: #ff69b4; /* vibrant font color */
                cursor: pointer;
                position: relative;
            }}

            .logo:hover .dropdown {{
                display: block;
            }}

            .dropdown {{
                display: none;
                position: absolute;
                background-color: #fff;
                min-width: 160px;
                box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
                z-index: 1;
            }}

            .dropdown a {{
                color: #333;
                padding: 12px 16px;
                text-decoration: none;
                font-size: 20px;
                display: block;
            }}

            .dropdown a:hover {{background-color: #f1f1f1}}

            /* Layout */
            main {{
                max-width: 1600px;
                margin: 0 auto;
                padding: 1rem;
                padding-top: 100px; /* adjust for fixed header */
            }}

            section {{
                margin-bottom: 2rem;
                background-color: #fff;
                padding: 1rem;
                border-radius: 5px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }}

            .horizontal-boxes {{
                display: flex;
                justify-content: space-between;
                margin-top: 1rem;
            }}

            .placeholder-video {{
                width: 100%;
                border-radius: 5px;
            }}

            .comments {{
                margin-top: 2rem;
            }}

            .comment {{
                margin-bottom: 1rem;
                padding: 1rem;
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: #f9f9f9;
            }}

            .comment-text {{
                margin: 0;
                font-weight: bold;
            }}

            .comment-by {{
                margin-top: 0.5rem;
                font-size: 0.9rem;
            }}

            .comment-date {{
                margin-top: 0.5rem;
                font-size: 0.9rem;
                color: #666;
            }}
        </style>
        </head>
        <body>
        <header>
            <div class="logo">
            DesignVerse
            <div class="dropdown">
                <a href="home_page.html">Home</a>
                <a href="projects_page.html">Projects</a>
                <a href="ranking_page.html">Most Popular Designs</a>
                <a href="upload_page.html">Upload Design</a>
            </div>
            </div>
        </header>

        <main>
            <section>
                <video controls class="placeholder-video">
                    <source src="{asset_path[0:len(asset_path)-4]}.mp4" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            </section>
            <section>
                <h2>{str(project_details[1])}</h2>
                <p>Artist: <strong>{str(project_details[2])}</strong></p>
                <p>Roll No: <strong>{str(project_details[3])}</strong></p>
                <p>Course <strong>{str(project_details[4])}</strong> <strong>{str(project_details[7])}</strong> by Prof. <strong>{str(project_details[6])}</strong></p>
                <p>Description: <strong>{str(project_details[8])}</strong></p>
            </section>
        '''
    else:
        # Define HTML content for image
        html_content = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>DIS Project</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
        <style>
            /* Font */
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
            * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Poppins', sans-serif;
            }}
            body {{
                font-family: 'Roboto', sans-serif;
                color: #333;
                background-color: #f0f0f0;
            }}

            header {{
            background-color: #333;
            color: #fff;
            padding: 20px;
            text-align: center;
            }}

            nav {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            max-width: 1200px;
            margin: 0 auto;
            }}

            nav .logo {{
            font-size: 24px;
            font-weight: 700;
            color: #ff69b4;
            cursor: pointer;
            position: relative;
            align-self: center;
            align-items: center;
            align-content: center;
            align-tracks: center;
            }}

            .dropdown {{
            display: none;
            position: absolute;
            background-color: #fff;
            min-width: 160px;
            box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
            z-index: 1;
            }}

            .dropdown a {{
            color: #333;
            padding: 12px 16px;
            text-decoration: none;
            font-size: 16px;
            display: block;
            }}

            .dropdown a:hover {{
            background-color: #f1f1f1;
            }}

            nav .logo:hover .dropdown {{
            display: block;
            }}

            /* Layout */
            main {{
                max-width: 1600px;
                margin: 0 auto;
                padding: 1rem;
                padding-top: 100px; /* adjust for fixed header */
            }}

            section {{
                margin-bottom: 2rem;
                background-color: #fff;
                padding: 1rem;
                border-radius: 5px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }}

            .horizontal-boxes {{
                display: flex;
                justify-content: space-between;
                margin-top: 1rem;
            }}

            .placeholder-image {{
                width: 100%;
                height: 200px;
                background-color: #ddd;
                border-radius: 5px;
                display: flex;
                justify-content: center;
                align-items: center;
                text-align: center;
                font-size: 24px;
                font-weight: bold;
                color: #333;
            }}

            .placeholder-image:hover {{
                background-color: #f5f5f5;
            }}

            .placeholder-image a {{
                color: #333;
                text-decoration: none;
            }}

            .placeholder-image a:hover {{
                color: #ff69b4;
            }}

            .comments {{
                margin-top: 2rem;
            }}

            .comment {{
                margin-bottom: 1rem;
                padding: 1rem;
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: #f9f9f9;
            }}

            .comment-text {{
                margin: 0;
                font-weight: bold;
            }}

            .comment-by {{
                margin-top: 0.5rem;
                font-size: 0.9rem;
            }}

            .comment-date {{
                margin-top: 0.5rem;
                font-size: 0.9rem;
                color: #666;
            }}
        </style>
        </head>
        <body>
        <header>
            <nav>
                <div class="logo">
                DesignVerse
                <div class="dropdown">
                    <a href="home_page.html">Home</a>
                    <a href="projects_page.html">Projects</a>
                    <a href="ranking_page.html">Most Popular Designs</a>
                    <a href="upload_page.html">Upload Design</a>
                </div>
                </div>
            </nav>
        </header>

        <main>
            <section>
                <img src="{asset_path}" alt="Project Image" style="width: 100%; border-radius: 5px;">
            </section>
            <section>
                <h2>{str(project_details[1])}</h2>
                <p>Artist: <strong>{str(project_details[2])}</strong></p>
                <p>Roll No: <strong>{str(project_details[3])}</strong></p>
                <p>Course <strong>{str(project_details[4])}</strong> <strong>{str(project_details[7])}</strong> by Prof. <strong>{str(project_details[6])}</strong></p>
                <p>Description: <strong>{str(project_details[8])}</strong></p>
            </section>
        '''

    # Append comments section to HTML content
    for comment in comment_details:
        if comment[5] == "green":
            html_content += f'''
            <section class="comments">
                <div class="comment" style="border-color: green;">
                    <p class="comment-text">{str(comment[1])}</p>
                    <p class="comment-by
                    ">By: {str(comment[2])} ({str(comment[3])})</p>
                    <p class="comment-date">Date: {str(comment[4])}</p>
                </div>
            </section>
            '''
        else:
            html_content += f'''
            <section class="comments">
                <div class="comment" style="border-color: red;">
                    <p class="comment-text">{str(comment[1])}</p>
                    <p class="comment-by
                    ">By: {str(comment[2])} ({str(comment[3])})</p>
                    <p class="comment-date">Date: {str(comment[4])}</p>
                </div>
            </section>
            '''

    # Close HTML content
    html_content += '''
        </main>
        </body>
        </html>
    '''

    # Write HTML content to file
    with open(file_path, "w") as file:
        file.write(html_content)

    print("Static webpage created successfully at:", file_path)

if __name__ == "__main__":
    make_database()
    asset_files = os.listdir("assets/")
    print("Assets:", asset_files)

    # Define the file path for each HTML file
    for f in range(6):
        i = asset_files[f]
        file_path = "templates/" + str(i)[0:len(str(i))-4] + ".html"
        make_html(file_path, "assets/" + i)
