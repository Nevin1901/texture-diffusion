import { useState } from "react";
import { invoke } from "@tauri-apps/api/tauri";
// import "./App.css";

function App() {
  const [greetMsg, setGreetMsg] = useState("");
  const [name, setName] = useState("");

  async function greet() {
    setGreetMsg(await invoke("get_python_dir", { name }));
  }

  return (
    <div>
      <h1>hello</h1>
      <button onClick={greet}>click me</button>
      <h1>{greetMsg}</h1>
    </div>
  );
}

export default App;
