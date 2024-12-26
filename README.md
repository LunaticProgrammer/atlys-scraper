# SUBMISSION

<h3>1. Create a vertual env using -- T1</h3>
<code>$ python3 -m venv venv <br> $ source venv/bin/activate</code>


<h3>2. Have the redis installed and run -- T2 </h3>
<code>$redis-server</code>

<h3>3. on T1 run</h3>
<code>$  uvicorn main:app --reload</code>

<h4> 4. hit the post request on <a href="http://localhost:8000/scrape/?page_limit=10">http://localhost:8000/scrape/?page_limit=10</a>
it accepts the token as bearer token and accepts the params page_limit and proxy </h4>

> you will then have a products.json in the project directory