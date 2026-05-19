import React, { useState } from "react";
import API from "./api";

function App() {

  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);

  // Upload PDF
  const uploadPDF = async () => {

    if (!file) {
      alert("Please select a PDF");
      return;
    }

    const formData = new FormData();

    formData.append("file", file);

    try {

      setUploading(true);

      const response = await API.post(
        "/upload",
        formData
      );

      alert(response.data.message);

    } catch (error) {

      console.error(error);

      alert("PDF upload failed");

    } finally {

      setUploading(false);
    }
  };

  // Ask Question
  const askQuestion = async () => {

    if (!question) {
      alert("Please enter question");
      return;
    }

    try {

      setLoading(true);

      const response = await API.get(
        `/ask?query=${encodeURIComponent(question)}`
      );

      setAnswer(response.data.answer);

    } catch (error) {

      console.error(error);

      alert("Failed to fetch answer");

    } finally {

      setLoading(false);
    }
  };

  return (

    <div
      style={{
        background: "#0f172a",
        minHeight: "100vh",
        color: "white",
        fontFamily: "Arial, sans-serif",
        padding: "30px"
      }}
    >

      {/* HEADER */}
      <div
        style={{
          textAlign: "center",
          marginBottom: "40px"
        }}
      >
        <h1
          style={{
            fontSize: "42px",
            marginBottom: "10px",
            color: "#38bdf8"
          }}
        >
          AI RAG Document Q&A
        </h1>

        <p
          style={{
            color: "#cbd5e1",
            fontSize: "18px"
          }}
        >
          Upload PDF and Ask Questions using AI
        </p>
      </div>

      {/* MAIN CARD */}
      <div
        style={{
          maxWidth: "900px",
          margin: "auto",
          background: "#1e293b",
          padding: "30px",
          borderRadius: "20px",
          boxShadow: "0px 0px 20px rgba(0,0,0,0.4)"
        }}
      >

        {/* Upload Section */}
        <div
          style={{
            marginBottom: "40px"
          }}
        >

          <h2
            style={{
              color: "#38bdf8"
            }}
          >
            Upload PDF
          </h2>

          <input
            type="file"
            onChange={(e) => setFile(e.target.files[0])}
            style={{
              marginTop: "15px",
              marginBottom: "20px",
              color: "white"
            }}
          />

          <br />

          <button
            onClick={uploadPDF}
            style={{
              background: "#38bdf8",
              color: "black",
              border: "none",
              padding: "12px 25px",
              borderRadius: "10px",
              cursor: "pointer",
              fontWeight: "bold",
              fontSize: "16px"
            }}
          >
            {uploading ? "Uploading..." : "Upload PDF"}
          </button>

        </div>

        {/* Ask Section */}
        <div>

          <h2
            style={{
              color: "#38bdf8"
            }}
          >
            Ask Question
          </h2>

          <textarea
            placeholder="Ask anything from the document..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            rows={4}
            style={{
              width: "100%",
              padding: "15px",
              borderRadius: "12px",
              border: "none",
              outline: "none",
              marginTop: "15px",
              background: "#334155",
              color: "white",
              fontSize: "16px"
            }}
          />

          <button
            onClick={askQuestion}
            style={{
              marginTop: "20px",
              background: "#22c55e",
              color: "white",
              border: "none",
              padding: "12px 25px",
              borderRadius: "10px",
              cursor: "pointer",
              fontWeight: "bold",
              fontSize: "16px"
            }}
          >
            {loading ? "Thinking..." : "Ask AI"}
          </button>

        </div>

        {/* Answer Section */}
        <div
          style={{
            marginTop: "40px"
          }}
        >

          <h2
            style={{
              color: "#38bdf8"
            }}
          >
            AI Answer
          </h2>

          <div
            style={{
              background: "#0f172a",
              padding: "25px",
              borderRadius: "15px",
              marginTop: "15px",
              lineHeight: "1.8",
              color: "#e2e8f0",
              minHeight: "120px",
              whiteSpace: "pre-wrap",
              border: "1px solid #334155"
            }}
          >
            {answer || "Your AI answer will appear here..."}
          </div>

        </div>

      </div>

    </div>
  );
}

export default App;