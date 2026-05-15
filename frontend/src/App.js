import React, { useState } from "react";
import API from "./api";

function App() {

  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const askQuestion = async () => {

    try {

      const response = await API.get(
        `/ask?query=${encodeURIComponent(question)}`
      );

      setAnswer(response.data.answer);

    } catch (error) {

      console.error(error);
      setAnswer("Failed to fetch answer");
    }
  };

  return (

    <div style={{
      backgroundColor: "#0b1120",
      minHeight: "100vh",
      color: "white",
      padding: "40px",
      fontFamily: "Arial"
    }}>

      <h1>AI Document Q&A System</h1>

      <h2>Ask Question</h2>

      <input
        type="text"
        placeholder="Enter your question"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        style={{
          padding: "12px",
          width: "400px",
          borderRadius: "5px",
          border: "none"
        }}
      />

      <br /><br />

      <button
        onClick={askQuestion}
        style={{
          padding: "10px 20px",
          backgroundColor: "#00bfff",
          color: "white",
          border: "none",
          borderRadius: "5px",
          cursor: "pointer"
        }}
      >
        Ask
      </button>

      <h2 style={{ marginTop: "30px" }}>Answer:</h2>

      <div style={{
        backgroundColor: "#1e293b",
        padding: "20px",
        borderRadius: "8px",
        width: "600px"
      }}>
        {answer}
      </div>

    </div>
  );
}

export default App;