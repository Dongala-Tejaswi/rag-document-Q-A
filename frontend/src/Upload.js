import React, { useState } from "react";
import API from "./api";

function Upload() {
  const [file, setFile] = useState(null);

  const uploadFile = async () => {
    if (!file) {
      alert("Please select PDF");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      await API.post("/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      alert("PDF uploaded successfully");
    } catch (error) {
      console.error(error);
      alert("Upload failed");
    }
  };

  return (
    <div className="upload-box">
      <input
        type="file"
        accept=".pdf"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button onClick={uploadFile}>
        Upload PDF
      </button>
    </div>
  );
}

export default Upload;