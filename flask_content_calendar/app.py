from flask import Flask, render_template, request, send_file
import pandas as pd
import random
import io
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


app = Flask(__name__)

# --- Data ---
post_types = [
    "Behind the Scenes", "Customer Testimonial", "Product Feature", "How-to Tip",
    "Offer/Discount", "Motivational Quote", "Fun Fact", "Before/After",
    "Poll/Question", "User Generated Content"
]

ctas = [
    "Save this post!", "Tag a friend who needs this!", "Follow us for more tips!",
    "Share your thoughts below!", "DM us to know more!"
]

hashtags = {
    "Fashion": ["#ootd", "#styleinspo", "#fashiondaily"],
    "Food": ["#foodie", "#tastytuesday", "#homecooking"],
    "Fitness": ["#fitlife", "#workoutmotivation", "#healthgoals"],
    "Travel": ["#wanderlust", "#travelgram", "#exploremore"],
    "Marketing": ["#digitalstrategy", "#contentcreator", "#marketingtips"]
}

# --- Routes ---
@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        biz_type = request.form["biz_type"]
        audience = request.form["audience"]
        goal = request.form["goal"]
        num_posts = int(request.form["num_posts"])

        data = []
        for i in range(num_posts):
            post = random.choice(post_types)
            tag = random.choice(hashtags[biz_type])
            call_to_action = random.choice(ctas)
            caption = f"{post} for {audience}. Goal: {goal}. {call_to_action} {tag}"
            data.append([f"Day {i+1}", post, caption])

        df = pd.DataFrame(data, columns=["Day", "Post Type", "Suggested Caption"])
        csv = df.to_csv(index=False)

        # Save CSV to memory
        csv_file = io.StringIO(csv)
        csv_file.seek(0)
        return send_file(
            io.BytesIO(csv.encode()),
            mimetype='text/csv',
            as_attachment=True,
            download_name='content_calendar.csv'
        )

    return render_template("index.html", hashtags=hashtags)

if __name__ == "__main__":
    app.run(debug=True)