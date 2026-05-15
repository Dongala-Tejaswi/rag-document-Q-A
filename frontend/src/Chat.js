import React, { useState } from "react";
import API from "./api";

function Chat() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const askQuestion = async () => {
    if (!question) {
      alert("Enter question");
      return;
    }

    try {
      const response = await API.get(
        `/ask?query=${encodeURIComponent(question)}`
      );

      setAnswer(response.data.answer);
    } catch (error) {
      console.error(error);
      alert("Failed to fetch answer");
    }
  };

  return (
    <div>
      <h2>Ask Question</h2>

      <input
        type="text"
        placeholder="Ask question"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />

      <button onClick={askQuestion}>
        Ask
      </button>

      <div className="answer-box">
        <h3>Answer:</h3>
        <p>{answer}</p>
      </div>
    </div>
  );
}

export default Chat;