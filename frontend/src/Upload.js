import { useState } from "react";
import API from "./api";

function Upload() {
  const [file, setFile] = useState(null);

  const uploadFile = async () => {
    if (!file) {
      alert("Select a PDF first");
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

      alert("Upload successful");
    } catch (error) {
      alert("Upload failed");
      console.log(error);
    }
  };

  return (
    <div>
      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button onClick={uploadFile}>
        Upload PDF
      </button>
    </div>
  );
}

export default Upload;