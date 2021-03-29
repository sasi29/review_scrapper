from flask import Flask,render_template,request
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as ureq
app= Flask(__name__)
@app.route("/",methods=["GET","POST"])
def homepage():
    return render_template('index.html')

@app.route("/scrap",methods=["POST"])
def index():
    if request.method=="POST":
        searchString=request.form['content'].replace(" ","")
        try:
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString  # preparing the URL to search the product on flipkart
            uClient = ureq(flipkart_url)  # requesting the webpage from the internet
            flipkartPage = uClient.read()  # reading the webpage
            uClient.close()  # closing the connection to the web server
            flipkart_html = bs(flipkartPage, "html.parser")  # parsing the webpage as HTML
            bigboxes = flipkart_html.findAll("div", {
                    "class": "_1AtVbE col-12-12"})  # seacrhing for appropriate tag to redirect to the product link
            del bigboxes[0:3]  # the first 3 members of the list do not contain relevant information, hence deleting them.
            box = bigboxes[0]# taking the first iteration (for demo)
            productLink = "https://www.flipkart.com" + box.div.div.div.a['href']  # extracting the actual product link
            prodRes = requests.get(productLink)  # getting the product page from server
            prod_html = bs(prodRes.text, "html.parser")# parsing the product page as HTML
            commentboxes = prod_html.find_all('div', {
                    'class': "_16PBlm"})# finding the HTML section containing the customer comments
            reviews = []  # initializing an empty list for reviews
            for commentbox in commentboxes:
                try:
                    name = commentbox.div.div.find_all('p', {'class': '_2-N8zT'})[0].text

                except:
                    name = 'No Name'

                try:
                    rating = commentbox.div.div.div.div.text

                except:
                    rating = 'No Rating'

                try:
                    commentHead = commentbox.div.div.div.p.text
                except:
                    commentHead = 'No Comment Heading'
                try:
                    comtag = commentbox.div.div.find_all('div', {'class': ''})
                    custComment = comtag[0].div.text
                except:
                    custComment = 'No Customer Comment'
                mydict = {"Product": searchString, "Name": name, "Rating": rating, "CommentHead": commentHead,
                              "Comment": custComment}  # saving that detail to a dictionary
                reviews.append(mydict)  # appending the comments to the review list
            return render_template('results.html', reviews=reviews)  # showing the review to the user

        except Exception as e:
            return "something is wrong"
if __name__=="__main__":
    app.run(port=5000, debug=True)