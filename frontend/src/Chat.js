import { useState } from "react";
import API from "./api";

function Chat() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const askQuestion = async () => {
    try {

      const response = await API.get(
        `/ask?question=${encodeURIComponent(question)}`
      );

      console.log(response.data);

      setAnswer(response.data.answer);

    } catch (error) {
      console.log(error);

      if (error.response) {
        console.log(error.response.data);
      }

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
        style={{
          width: "100%",
          padding: "12px",
          marginBottom: "10px"
        }}
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