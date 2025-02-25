## Privacy Focused Analytics

> My blog post: [Privacy Focused Analytics From Scratch](https://healeycodes.com/privacy-focused-analytics-from-scratch/)

<br>

I wanted to learn more about web analytics so I budgeted myself a few hours and built a small analytics system.

It uses a Flask application with a SQLite database, and a HTML snippet to collect **anonymous user data** from any website.

<br>

### Features

- Uses a dynamic tracking pixel (optionally works without JavaScript)
- Collects information about:
  - What pages users visit
  - Where users are referred from
  - What browsers and screen sizes are used
  - Which country the user is from (without an API call)
- Lets you view analytics from different time slices
<br>

### Snippet

Include this on any page you want to gather analytics from.

Change `https://example.org` to wherever you host the Flask application.

```html
<script>
  const website = 'https://example.org'
  const url = new URL(website + "/pixel.gif")

  // '/'
  url.searchParams.append("path", location.pathname)

  // 'Analytics Test Page'
  url.searchParams.append("title", document.title)

  // 'https://www.google.com'
  url.searchParams.append("referrer", document.referrer)

  // '320,568'
  url.searchParams.append(
    "resolution",
    window.screen.width + "," + window.screen.height
  )

  const img = document.createElement("img")
  img.src = url
  // When the element exists in the DOM, the request is made
  document.body.appendChild(img)
</script>
<noscript>
  <!-- Without JavaScript, less information is available to be sent
  e.g. just the path and title, set via static template logic -->
  <img src="https://example.org/pixel.gif?path=%2F&title=Analytics%20Test%20Page" />
</noscript>
```
<br>

### Setup

Download a free [GeoLite2 country database](https://dev.maxmind.com/geoip/geoip2/geolite2/) to `./GeoLite2-Country.mmdb`

`pip install -r requirements.txt`

<br>

### Run

`env FLASK_APP=analytics.py flask run`

<br>

The tracking pixel is hosted from `/pixel.gif`.

Note: It's likely that most ad blockers will stop the request.

<br>

There is a test page at `/` that will serve up the snippet for test purposes.

<br>

Analytics can be viewed at `/analytics`. Search parameters can be passed to view a time slice.

- (optional) `start` - The start of the time slice in UNIX seconds (inclusive). Defaults to `0`.
- (optional) `end` - The end of the time slice in UNIX seconds. Defaults to current time.

<br>

### Possible improvements

Hopefully none? This was a self-contained experiment to learn more about something 😊

<br>

License: MIT.
