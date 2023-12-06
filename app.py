# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template
import csv

app = Flask(__name__)

@app.route('/', methods=["GET"])
def default_response():
    # Return the components to the HTML template
    return render_template(template_name_or_list='index.html')


@app.route('/temps', methods=["GET"])
def temps_function():
    temperature_data = []
    labels = []

    with open('temperature_data.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            labels.append(str(row[0]))
            temperature_data.append(float(row[1]))

    # Return the components to the HTML template
    return render_template(
        template_name_or_list='filter.html',
        data=temperature_data,
        labels=labels,
        header="Simple line graph", description="Graph shows sales per month."
        )

@app.route('/about', methods=["GET"])
def about_function():
    return render_template(template_name_or_list='about.html')

@app.route('/register', methods=["GET"])
def register_function():
    return render_template(template_name_or_list='register.html')

@app.route('/login', methods=["GET"])
def login_function():
    return render_template(template_name_or_list='login.html')

@app.route('/sales', methods=["GET"])
def sales_function():
    # Define Plot Data
    labels = [
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
    ]
    data = [0, 10, 15, 8, 22, 18, 25]

    # Return the components to the HTML template
    return render_template(
        template_name_or_list='temp_graph.html',
        data=data,
        labels=labels,
        header="Simple line graph", description="Graph shows sales per month."
        )


if __name__ == '__main__':
    app.run(debug=True, port=5000)
