import React, { useState, useEffect } from "react";
import axios from "axios";
import { TextField, Button, Paper, Typography, Box, CircularProgress } from "@mui/material";
import { getCSRFToken } from "./csrf"; // Import CSRF function

const Chatbot = () => {
  const [messages, setMessages] = useState([{ sender: "bot", text: "Hello! How can I help you?" }]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    getCSRFToken(); // Fetch token on component mount
  }, []);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMessages = [...messages, { sender: "user", text: input }];
    setMessages(newMessages);
    setInput("");
    setLoading(true);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/chatbot/",
        { message: input }, // Send message in request body
        { headers: { "X-CSRFToken": axios.defaults.headers.common["X-CSRFToken"] }, withCredentials: true }
      );
      console.log("Chatbot input:", input);
      console.log("Chatbot Response:", response.data.response);
      setMessages([...newMessages, { sender: "bot", text: response.data.response }]);
    } catch (error) {
      console.error("Error fetching chatbot response:", error);
      setMessages([...newMessages, { sender: "bot", text: "Error fetching response." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ maxWidth: 500, mx: "auto", mt: 4, p: 2 }}>
      <Typography variant="h4" gutterBottom>Chatbot</Typography>
      <Paper sx={{ p: 2, minHeight: 300, maxHeight: 400, overflowY: "auto" }}>
        {messages.map((msg, index) => (
          <Typography
            key={index}
            sx={{
              textAlign: msg.sender === "user" ? "right" : "left",
              bgcolor: msg.sender === "user" ? "#e3f2fd" : "#f1f1f1",
              p: 1,
              borderRadius: 2,
              my: 1,
              maxWidth: "80%",
              ml: msg.sender === "user" ? "auto" : 0
            }}
          >
            {msg.text}
          </Typography>
        ))}
      </Paper>
      <Box sx={{ display: "flex", mt: 2 }}>
        <TextField
          fullWidth
          label="Type your message..."
          variant="outlined"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === "Enter" && sendMessage()}
        />
        <Button
          variant="contained"
          color="primary"
          onClick={sendMessage}
          sx={{ ml: 2 }}
          disabled={loading}
        >
          {loading ? <CircularProgress size={24} /> : "Send"}
        </Button>
      </Box>
    </Box>
  );
};

export default Chatbot;
