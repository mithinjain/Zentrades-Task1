from flask import Flask, render_template
import requests
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)


@app.route("/")
def display_products():
    # Fetching the JSON data
    url = "https://s3.amazonaws.com/open-to-cors/assignment.json"
    response = requests.get(url)
    data = response.json()

    # Extracting product data from the 'products' key in the JSON
    products_data = data.get("products", {})

    # Creating a DataFrame from the product data
    df = pd.DataFrame(products_data).transpose()

    # Converting data types to appropriate types
    df["Price"] = pd.to_numeric(df["price"])
    df["Popularity"] = pd.to_numeric(df["popularity"])

    # Sorting the DataFrame based on descending popularity
    df_sorted = df.sort_values(by="Popularity", ascending=False)

    # Rendering the HTML template with the relevant data
    table_html = df_sorted[["title", "Price"]].to_html(index=False)

    # Optionally, creating a bar chart and embedding it in the HTML
    plt.bar(df_sorted["title"], df_sorted["Popularity"])
    plt.xlabel("Title")
    plt.ylabel("Popularity")
    plt.title("Popularity of Products")
    plt.xticks(rotation=90)
    chart_image = BytesIO()
    plt.savefig(chart_image, format="png")
    chart_image_base64 = base64.b64encode(chart_image.getvalue()).decode("utf-8")
    chart_html = f'<img src="data:image/png;base64,{chart_image_base64}">'

    return render_template("index.html", table_html=table_html, chart_html=chart_html)


if __name__ == "__main__":
    app.run(debug=True)
