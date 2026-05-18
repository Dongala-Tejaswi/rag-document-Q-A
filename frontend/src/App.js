import React, { useState } from "react";
import API from "./api";

function App() {

  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  // Upload PDF
  const uploadPDF = async () => {

    const formData = new FormData();

    formData.append("file", file);

    try {

      const response = await API.post(
        "/upload",
        formData
      );

      alert(response.data.message);

    } catch (error) {

      console.error(error);

      alert("PDF upload failed");
    }
  };

  // Ask question
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

    <div style={{
      backgroundColor: "#0b1120",
      minHeight: "100vh",
      color: "white",
      padding: "40px",
      fontFamily: "Arial"
    }}>

      <h1>AI Document Q&A System</h1>

      {/* Upload PDF */}
      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button
        onClick={uploadPDF}
        style={{
          marginLeft: "10px",
          padding: "8px"
        }}
      >
        Upload PDF
      </button>

      <hr />

      {/* Ask Question */}
      <h2>Ask Question</h2>

      <input
        type="text"
        placeholder="Ask question"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        style={{
          padding: "10px",
          width: "400px"
        }}
      />

      <br /><br />

      <button
        onClick={askQuestion}
        style={{
          padding: "10px 20px"
        }}
      >
        Ask
      </button>

      <h2>Answer:</h2>

      <div style={{
        backgroundColor: "#1e293b",
        padding: "20px",
        borderRadius: "8px"
      }}>
        {answer}
      </div>

    </div>
  );
}

export default App;