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
      alert("Failed to fetch answer");
    }
  };

  return (
    <div>
      <input
        type="text"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask Question"
      />

      <button onClick={askQuestion}>
        Ask
      </button>

      <h3>Answer:</h3>
      <p>{answer}</p>
    </div>
  );
}

export default App;