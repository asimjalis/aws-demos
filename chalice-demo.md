# Chalice

## Create Chalice Project

```bash
chalice new-project demo1
cd demo1
gvim app.py 
chalice local
```

## App

Paste this code into `app.py`.

```python
from chalice import Chalice, Response

app = Chalice(app_name='demo1')

import boto3
import urllib

def image_url_to_labels(image_url):
    # Get image
    f = urllib.urlopen(image_url)
    image_bytes = f.read()
    f.close()

    # Convert to labels
    rekognition = boto3.client('rekognition')
    image_object = {'Bytes':image_bytes}
    response = rekognition.detect_labels(Image=image_object)
    return response

@app.route('/introspect')
def introspect():
    return app.current_request.to_dict()

def query_params_to_body(query_params):
    if 'image_url' in query_params:
        image_url = query_params['image_url']
        return image_url_to_labels(image_url)
    else:
        return {}
 
@app.route('/',cors=True)
def index():
    query_params = app.current_request.query_params
    body = query_params_to_body(query_params)
    return body

```

## Front-End

Paste this code into `index.html`.

```html
<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/mustache.js/2.3.0/mustache.min.js"></script>

<script id="image_template" type="text/template">
<table class="table table-striped">
<tr><th>Label</th><th>Confidence</th></tr>
{{#Labels}}
<tr>
<td>{{Name}}</td>
<td>{{Confidence}}</td>
</tr>
{{/Labels}}
</table>
</script>

<script id="error_template" type="text/template">
<div class="alert alert-danger">{{message}}</div>
</script>

<script id="progress_template" type="text/template">
<div class="alert alert-info">{{message}}</div>
</script>

<script>
function clear_all() {
  $("#output").html("");
  $("#labels").html("");
}
function progress() {
  clear_all();
  var template = $('#progress_template').html();
  var html = Mustache.render(template, {message: "Working..."})
  $("#output").html(html);
}
$(document).ready(function(){
  $("button").click(function(){
    progress();
    var demo_url = "https://i.pinimg.com/originals/81/6d/a5/816da533638aee63cfbd315ea24cccbd.jpg"
    var image_url = $("#image_url").val()
    if (image_url == "") { image_url = demo_url; }
    var local_endpoint = "http://localhost:8000/"
    // Paste from output of chalice deploy and use in service_url.
    var cloud_endpoint = "https://abc1234.execute-api.us-west-2.amazonaws.com/api/";
    var service_endpoint = local_endpoint;
    var service_url = service_endpoint + "?image_url=" + image_url
    $.ajax({
      url: service_url,
      dataType: 'json',
      success: function(data) {
        console.log(data);
        clear_all();
        var template = $('#image_template').html();
        var html = Mustache.render(template, data);
        $("#labels").html(html);
        $("#output").prepend($("<img>",{src:image_url,height:200}));
        $("#labels").prepend("<hr>");
      },
      error: function(data) {
        clear_all();
        var template = $('#error_template').html();
        var html = Mustache.render(template, {message: "Error: No image was found."})
        $("#output").html(html);
      }
    });
  });
});
</script>
</head>
<body>

<div class="container-fluid">
  <h1 class="display-3">Image Recognizer</h1>
  <br>
  <input class="form-control" id="image_url" placeholder="Paste image URL" type="text"> 
  <hr>
  <button class="btn btn-primary">Recognize</button>
  <button class="btn btn-primary" onclick='$("#image_url").val("")'>Demo</button>
  <hr>
  <div id="output"></div>
  <div id="labels"></div>
</div>

</body>
</html>
```

## Demo Local

To run the service locally run `chalice local`. In `index.html` set
`service_endpoint` to `local_endpoint`. Open `index.html` and it
should recognize images.

## Demo Cloud

To run the service on API Gateway, run `chalice deploy`. In
`index.html`, paste the API Gateway endpoint for your service into the
value of `cloud_endpoint`. Set `service_endpoint` to `cloud_endpoint`.
Open `index.html` and it should recognize images.

## Demo All-In-Cloud

To push the application completely into the cloud deploy `index.html`
as a static HTML page on S3. 
