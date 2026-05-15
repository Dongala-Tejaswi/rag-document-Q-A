import "./App.css";
import Upload from "./Upload";
import Chat from "./Chat";

function App() {
  return (
    <div className="container">
      <h1>AI Document Q&A System</h1>

      <Upload />

      <hr />

      <Chat />
    </div>
  );
}

export default App;