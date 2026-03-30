import express from "express";
import fetch from "node-fetch";

const app = express();
app.use(express.json());

const EC2_URL = "http://13.235.19.87:8000";

app.get("/", (req, res) => {
  res.send("Proxy running");
});

app.all("/api/*", async (req, res) => {
  try {
    const url = EC2_URL + req.originalUrl.replace("/api", "");

    const response = await fetch(url, {
      method: req.method,
      headers: { "Content-Type": "application/json" },
      body: ["GET", "HEAD"].includes(req.method)
        ? undefined
        : JSON.stringify(req.body),
    });

    const data = await response.text();
    res.status(response.status).send(data);
  } catch (err) {
    res.status(500).send("Proxy error");
  }
});

app.listen(3000, () => console.log("Proxy running"));