import React, { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

  const handleFileChange = (e) => setFile(e.target.files[0]);

  const handleUpload = async () => {
    if (!file) return alert("Select a file first!");
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://localhost:8000/upload", formData);
      setMessage(response.data.message);
    } catch (error) {
      setMessage(error.response?.data?.error || "Upload failed");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>SmartProposal Upload</h1>
      <input type="file" accept=".odt" onChange={handleFileChange} />
      <button onClick={handleUpload} style={{ marginLeft: "10px" }}>Upload</button>
      <p>{message}</p>
    </div>
  );
}

export default App;
