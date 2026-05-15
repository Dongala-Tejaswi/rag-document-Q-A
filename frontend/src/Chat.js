import { useState } from "react";
import API from "./api";

function Chat() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const askQuestion = async () => {
    try {
      const response = await API.get(`/ask?question=${question}`);

      setAnswer(response.data.answer);
    } catch (error) {
      alert("Failed to fetch answer");
      console.log(error);
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

      <h3>Answer:</h3>

      <p>{answer}</p>
    </div>
  );
}

export default Chat;