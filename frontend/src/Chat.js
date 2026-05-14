import { useState } from "react";
import API from "./api";

function Chat() {

  const [query, setQuery] = useState("");

  const [answer, setAnswer] = useState("");

  const askQuestion = async () => {

    try {

      const response = await API.get(
        `/ask?query=${query}`
      );

      setAnswer(response.data.answer);

    } catch (error) {

      console.log(error);

      alert("Question failed");
    }
  };

  return (
    <div>

      <h2>Ask Question</h2>

      <input
        type="text"
        placeholder="Ask question"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
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