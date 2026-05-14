import API from "./api";

function Upload() {

  const uploadFile = async (e) => {

    const formData = new FormData();

    formData.append("file", e.target.files[0]);

    try {

      const response = await API.post(
        "/upload",
        formData
      );

      alert(response.data.message);

    } catch (error) {

      console.log(error);

      alert("Upload failed");
    }
  };

  return (
    <div>

      <h2>Upload PDF</h2>

      <input
        type="file"
        accept=".pdf"
        onChange={uploadFile}
      />

    </div>
  );
}

export default Upload;