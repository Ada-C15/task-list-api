## **Wave 4 Notes**

bot token = xoxb-2063763926209-2036400917623-Dz3FJZHzFb55Vf16PkGpm01W

1. **What is the responsibility of this endpoint?**

This method posts a message to a public channel, private channel, or direct message/IM channel.

2. **What is the URL and HTTP method for this endpoint?**

https://slack.com/api/chat.postMessage

POST

3. **What are the two required arguments for this endpoint?**

token
channel

4. **How does this endpoint relate to the Slackbot API key (token) we just created?**

Tokens should be passed as an HTTP Authorization header or alternatively, as a POST parameter. But Slask prefers API keys to be sent in the "Authorization" request header.
